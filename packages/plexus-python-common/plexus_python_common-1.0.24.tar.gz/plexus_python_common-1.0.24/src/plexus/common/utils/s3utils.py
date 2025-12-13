import concurrent.futures
import contextlib
import dataclasses
import datetime
import functools
import mimetypes
import os
import os.path
import tempfile
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Literal

import boto3
from cloudpathlib import CloudPath, S3Client, S3Path
from iker.common.utils.shutils import glob_match, listfile, path_depth
from iker.common.utils.strutils import is_empty, trim_to_none
from rich.progress import BarColumn, DownloadColumn, Progress, TaskID, TextColumn, TransferSpeedColumn

__all__ = [
    "S3ObjectMeta",
    "s3_make_client",
    "s3_list_objects",
    "s3_listfile",
    "s3_cp_download",
    "s3_cp_upload",
    "s3_sync_download",
    "s3_sync_upload",
    "s3_pull_text",
    "s3_push_text",
    "S3TransferCallbackClient",
    "s3_make_progress_callback",
    "s3_make_progressed_client",
]


@dataclasses.dataclass
class S3ObjectMeta(object):
    key: str
    last_modified: datetime.datetime
    size: int


@contextlib.contextmanager
def s3_make_client(
    access_key_id: str = None,
    secret_access_key: str = None,
    region_name: str = None,
    endpoint_url: str = None,
) -> Generator[S3Client]:
    """
    Creates an S3 client as a context manager for safe resource handling.

    :param access_key_id: AWS access key ID.
    :param secret_access_key: AWS secret access key.
    :param region_name: AWS service region name.
    :param endpoint_url: AWS service endpoint URL.
    :return: An instance of ``S3Client``.
    """
    session = boto3.Session(aws_access_key_id=trim_to_none(access_key_id),
                            aws_secret_access_key=trim_to_none(secret_access_key),
                            region_name=trim_to_none(region_name))
    yield S3Client(boto3_session=session, endpoint_url=trim_to_none(endpoint_url))


def s3_list_objects(client: S3Client, bucket: str, prefix: str, limit: int = None) -> Generator[S3ObjectMeta]:
    """
    Lists all objects from the given S3 ``bucket`` and ``prefix``.

    :param client: An instance of ``S3Client``.
    :param bucket: Bucket name.
    :param prefix: Object keys prefix.
    :param limit: Maximum number of objects to return (``None`` for all).
    :return: An iterable of ``S3ObjectMeta`` objects representing the S3 objects.
    """
    continuation_token = None
    count = 0
    while True:
        if is_empty(continuation_token):
            response = client.client.list_objects_v2(MaxKeys=1000, Bucket=bucket, Prefix=prefix)
        else:
            response = client.client.list_objects_v2(MaxKeys=1000,
                                                     Bucket=bucket,
                                                     Prefix=prefix,
                                                     ContinuationToken=continuation_token)

        contents = response.get("Contents", [])
        count += len(contents)
        if limit is not None and count > limit:
            contents = contents[:limit - count]

        yield from (S3ObjectMeta(key=e["Key"], last_modified=e["LastModified"], size=e["Size"]) for e in contents)

        if not response.get("IsTruncated") or (limit is not None and count >= limit):
            break

        continuation_token = response.get("NextContinuationToken")


def s3_listfile(
    client: S3Client,
    bucket: str,
    prefix: str,
    *,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    depth: int = 0,
) -> Generator[S3ObjectMeta]:
    """
    Lists all objects from the given S3 ``bucket`` and ``prefix``, filtered by patterns and directory depth.

    :param client: An instance of ``S3Client``.
    :param bucket: Bucket name.
    :param prefix: Object keys prefix.
    :param include_patterns: Inclusive glob patterns applied to filenames.
    :param exclude_patterns: Exclusive glob patterns applied to filenames.
    :param depth: Maximum depth of subdirectories to include in the scan (``0`` for unlimited depth).
    :return: An iterable of ``S3ObjectMeta`` objects representing the filtered S3 objects.
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    def filter_object_meta(object_meta: S3ObjectMeta) -> bool:
        if 0 < depth <= path_depth(prefix, os.path.dirname(object_meta.key)):
            return False
        if len(glob_match([os.path.basename(object_meta.key)], include_patterns, exclude_patterns)) == 0:
            return False
        return True

    yield from filter(filter_object_meta, s3_list_objects(client, bucket, prefix))


def s3_cp_download(client: S3Client, bucket: str, key: str, file_path: str | os.PathLike[str]):
    """
    Downloads an object from the given S3 ``bucket`` and ``key`` to a local file path.

    :param client: An instance of ``S3Client``.
    :param bucket: Bucket name.
    :param key: Object key.
    :param file_path: Local file path to save the object.
    """
    client.client.download_file(bucket, key, file_path)


def s3_cp_upload(client: S3Client, file_path: str | os.PathLike[str], bucket: str, key: str):
    """
    Uploads a local file to the given S3 ``bucket`` and ``key``.

    :param client: An instance of ``S3Client``.
    :param file_path: Local file path to upload.
    :param bucket: Bucket name.
    :param key: Object key for the uploaded file.
    """
    t, _ = mimetypes.MimeTypes().guess_type(file_path)
    client.client.upload_file(file_path,
                              bucket,
                              key,
                              ExtraArgs={"ContentType": "binary/octet-stream" if t is None else t})


def s3_sync_download(
    client: S3Client,
    bucket: str,
    prefix: str,
    dir_path: str | os.PathLike[str],
    *,
    max_workers: int = None,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
):
    """
    Recursively downloads all objects from the given S3 ``bucket`` and ``prefix`` to a local directory path, using a thread pool.

    :param client: An instance of ``S3Client``.
    :param bucket: Bucket name.
    :param prefix: Object keys prefix.
    :param dir_path: Local directory path to save objects.
    :param max_workers: Maximum number of worker threads.
    :param include_patterns: Inclusive glob patterns applied to filenames.
    :param exclude_patterns: Exclusive glob patterns applied to filenames.
    :param depth: Maximum depth of subdirectories to include in the scan (``0`` for unlimited depth).
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    objects = s3_listfile(client,
                          bucket,
                          prefix,
                          include_patterns=include_patterns,
                          exclude_patterns=exclude_patterns,
                          depth=depth)

    def download_file(key: str):
        file_path = os.path.join(dir_path, key[len(prefix):])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        s3_cp_download(client, bucket, key, file_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, obj.key) for obj in objects]
        done_futures, not_done_futures = concurrent.futures.wait(futures,
                                                                 return_when=concurrent.futures.FIRST_EXCEPTION)
        if len(not_done_futures) > 0:
            for future in not_done_futures:
                future.cancel()
        for future in done_futures:
            exc = future.exception()
            if exc is not None:
                raise exc
        if len(not_done_futures) > 0:
            raise RuntimeError("download did not complete due to errors in some threads")


def s3_sync_upload(
    client: S3Client,
    dir_path: str | os.PathLike[str],
    bucket: str,
    prefix: str,
    *,
    max_workers: int = None,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
):
    """
    Recursively uploads all files from a local directory to the given S3 ``bucket`` and ``prefix``, using a thread pool.

    :param client: An instance of ``S3Client``.
    :param dir_path: Local directory path to upload from.
    :param bucket: Bucket name.
    :param prefix: Object keys prefix for uploaded files.
    :param max_workers: Maximum number of worker threads.
    :param include_patterns: Inclusive glob patterns applied to filenames.
    :param exclude_patterns: Exclusive glob patterns applied to filenames.
    :param depth: Maximum depth of subdirectories to include in the scan (``0`` for unlimited depth).
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    file_paths = listfile(dir_path,
                          include_patterns=include_patterns,
                          exclude_patterns=exclude_patterns,
                          depth=depth)

    def upload_file(file_path: str):
        s3_cp_upload(client, file_path, bucket, prefix + os.path.relpath(file_path, dir_path))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(upload_file, file_path) for file_path in file_paths]
        done_futures, not_done_futures = concurrent.futures.wait(futures,
                                                                 return_when=concurrent.futures.FIRST_EXCEPTION)
        if len(not_done_futures) > 0:
            for future in not_done_futures:
                future.cancel()
        for future in done_futures:
            exc = future.exception()
            if exc is not None:
                raise exc
        if len(not_done_futures) > 0:
            raise RuntimeError("upload did not complete due to errors in some threads")


def s3_pull_text(client: S3Client, bucket: str, key: str, encoding: str = None) -> str:
    """
    Downloads and decodes text content stored as an object in the given S3 ``bucket`` and ``key``.

    :param client: An instance of ``S3Client``.
    :param bucket: Bucket name.
    :param key: Object key storing the text.
    :param encoding: String encoding to use (defaults to UTF-8).
    :return: The decoded text content.
    """
    with tempfile.TemporaryFile() as fp:
        client.client.download_fileobj(bucket, key, fp)
        fp.seek(0)
        return fp.read().decode(encoding or "utf-8")


def s3_push_text(client: S3Client, text: str, bucket: str, key: str, encoding: str = None):
    """
    Uploads the given text as an object to the specified S3 ``bucket`` and ``key``.

    :param client: An instance of ``S3Client``.
    :param text: Text content to upload.
    :param bucket: Bucket name.
    :param key: Object key to store the text.
    :param encoding: String encoding to use (defaults to UTF-8).
    """
    with tempfile.TemporaryFile() as fp:
        fp.write(text.encode(encoding or "utf-8"))
        fp.seek(0)
        client.client.upload_fileobj(fp, bucket, key)


TransferDirection = Literal["download", "upload"]
TransferState = Literal["start", "update", "stop"]


@contextlib.contextmanager
def make_transfer_callback(
    callback: Callable[[CloudPath, TransferDirection, TransferState, int], None],
    path: Path | CloudPath,
    direction: TransferDirection,
):
    if callback is None:
        yield None
        return

    callback(path, direction, "start", 0)
    try:
        yield functools.partial(callback, path, direction, "update")
    finally:
        callback(path, direction, "stop", 0)


class S3TransferCallbackClient(S3Client):
    def __init__(
        self,
        *args,
        transfer_callback: Callable[[Path | CloudPath, TransferDirection, TransferState, int], None],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.transfer_callback = transfer_callback

    def _download_file(self, cloud_path: S3Path, local_path: str | os.PathLike[str]) -> Path:
        local_path = Path(local_path)

        obj = self.s3.Object(cloud_path.bucket, cloud_path.key)

        with make_transfer_callback(self.transfer_callback, cloud_path, "download") as callback:
            obj.download_file(
                str(local_path),
                Config=self.boto3_transfer_config,
                ExtraArgs=self.boto3_dl_extra_args,
                Callback=callback,
            )
        return local_path

    def _upload_file(self, local_path: str | os.PathLike[str], cloud_path: S3Path) -> S3Path:
        local_path = Path(local_path)

        obj = self.s3.Object(cloud_path.bucket, cloud_path.key)

        extra_args = self.boto3_ul_extra_args.copy()

        if self.content_type_method is not None:
            content_type, content_encoding = self.content_type_method(str(local_path))
            if content_type is not None:
                extra_args["ContentType"] = content_type
            if content_encoding is not None:
                extra_args["ContentEncoding"] = content_encoding

        with make_transfer_callback(self.transfer_callback, local_path, "upload") as callback:
            obj.upload_file(
                str(local_path),
                Config=self.boto3_transfer_config,
                ExtraArgs=extra_args,
                Callback=callback,
            )
        return cloud_path


def s3_make_progress_callback(
    progress: Progress,
) -> Callable[[Path | CloudPath, TransferDirection, TransferState, int], None]:
    task_ids: dict[Path | CloudPath, TaskID] = {}

    def progress_callback(path: Path | CloudPath, direction: TransferDirection, state: TransferState, bytes_sent: int):
        if state == "start":
            size = path.stat().st_size
            task_ids[path] = progress.add_task(direction, total=size, filename=path.name)
        elif state == "stop":
            if path in task_ids:
                progress.remove_task(task_ids[path])
                del task_ids[path]
        else:
            progress.update(task_ids[path], advance=bytes_sent)

    return progress_callback


@contextlib.contextmanager
def s3_make_progressed_client(
    access_key_id: str = None,
    secret_access_key: str = None,
    region_name: str = None,
    endpoint_url: str = None,
) -> Generator[S3Client]:
    """
    Creates an S3 client with progress callback as a context manager for safe resource handling.

    :param access_key_id: AWS access key ID.
    :param secret_access_key: AWS secret access key.
    :param region_name: AWS service region name.
    :param endpoint_url: AWS service endpoint URL.
    :return: An instance of ``S3TransferCallbackClient``.
    """
    with Progress(
        TextColumn("[blue]{task.fields[filename]}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
    ) as progress:
        session = boto3.Session(aws_access_key_id=trim_to_none(access_key_id),
                                aws_secret_access_key=trim_to_none(secret_access_key),
                                region_name=trim_to_none(region_name))
        yield S3TransferCallbackClient(boto3_session=session,
                                       endpoint_url=trim_to_none(endpoint_url),
                                       transfer_callback=s3_make_progress_callback(progress))
