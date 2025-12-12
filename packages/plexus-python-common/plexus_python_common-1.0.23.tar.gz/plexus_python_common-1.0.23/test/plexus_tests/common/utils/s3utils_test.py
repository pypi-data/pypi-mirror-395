import tempfile
import unittest

import ddt
import moto
from iker.common.utils.randutils import randomizer
from iker.common.utils.shutils import listfile
from iker.common.utils.testutils import norm_path

from plexus.common.utils.s3utils import *
from plexus_tests import resources_directory


@ddt.ddt
class S3UtilsTest(unittest.TestCase):

    def test_s3_list_object__random_text_files(self):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 2000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%04d" % i
                data.append((key, text))

            for key, text in data:
                s3_push_text(client, text, "dummy-bucket", key)

            result = list(s3_list_objects(client, "dummy-bucket", "dummy_prefix/"))

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(s3_pull_text(client, "dummy-bucket", key), text)

        with moto.mock_aws(), s3_make_progressed_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 2000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%04d" % i
                data.append((key, text))

            for key, text in data:
                client.CloudPath("s3://dummy-bucket/", key).write_text(text)

            result = list(s3_list_objects(client, "dummy-bucket", "dummy_prefix/"))

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(client.CloudPath("s3://dummy-bucket", key).read_text(), text)

    def test_s3_listfile__random_text_files(self):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 2000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%04d" % i
                data.append((key, text))

            for key, text in data:
                s3_push_text(client, text, "dummy-bucket", key)

            result = list(s3_listfile(client, "dummy-bucket", "dummy_prefix/"))

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(s3_pull_text(client, "dummy-bucket", key), text)

        with moto.mock_aws(), s3_make_progressed_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 2000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%04d" % i
                data.append((key, text))

            for key, text in data:
                client.CloudPath("s3://dummy-bucket/", key).write_text(text)

            result = list(s3_listfile(client, "dummy-bucket", "dummy_prefix/"))

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(client.CloudPath("s3://dummy-bucket", key).read_text(), text)

    data_s3_listfile = [
        (
            "{res_dir}/unittest/s3utils/",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            [],
            0,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.baz/file.foo.baz",
                "unittest/s3utils/dir.baz/file.bar.baz",
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.baz",
                "unittest/s3utils/dir.foo/file.foo",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            [],
            0,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.baz/file.foo.baz",
                "unittest/s3utils/dir.baz/file.bar.baz",
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.baz",
                "unittest/s3utils/dir.foo/file.foo",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils/dir.foo",
            "dummy-bucket",
            "unittest/s3utils/dir.foo",
            [],
            [],
            0,
            [
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.baz",
                "unittest/s3utils/dir.foo/file.foo",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils/dir.baz",
            "dummy-bucket",
            "unittest/s3utils/dir.baz",
            [],
            [],
            0,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.baz/file.foo.baz",
                "unittest/s3utils/dir.baz/file.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            ["*.foo", "*.bar"],
            ["*.foo.bar"],
            0,
            [
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.foo",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            ["*.foo", "*.bar"],
            [],
            0,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.foo",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            ["*.baz"],
            0,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.foo",
                "unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils",
            [],
            [],
            2,
            [
                "unittest/s3utils/dir.baz/file.foo.bar",
                "unittest/s3utils/dir.baz/file.foo.baz",
                "unittest/s3utils/dir.baz/file.bar.baz",
                "unittest/s3utils/dir.foo/file.bar",
                "unittest/s3utils/dir.foo/file.baz",
                "unittest/s3utils/dir.foo/file.foo",
            ],
        ),
    ]

    @ddt.idata(data_s3_listfile)
    @ddt.unpack
    def test_s3_listfile(self, src, bucket, prefix, include_patterns, exclude_patterns, depth, expect):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix)

            object_metas = s3_listfile(client,
                                       bucket,
                                       prefix,
                                       include_patterns=include_patterns,
                                       exclude_patterns=exclude_patterns,
                                       depth=depth)

            self.assertSetEqual(set(map(lambda x: norm_path(x.key), object_metas)),
                                set(map(lambda x: norm_path(x), expect)))

    data_s3_sync = [
        (
            "{res_dir}/unittest/s3utils/",
            "{tmp_dir}/unittest/s3utils/",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "{tmp_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils/dir.foo",
            "{tmp_dir}/unittest/s3utils/dir.foo",
            "dummy-bucket",
            "unittest/s3utils/dir.foo",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils/dir.baz",
            "{tmp_dir}/unittest/s3utils/dir.baz",
            "dummy-bucket",
            "unittest/s3utils/dir.baz",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "{tmp_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            ["*.foo", "*.bar"],
            ["*.foo.bar"],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "{tmp_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            ["*.foo", "*.bar"],
            [],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "{tmp_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils/",
            [],
            ["*.baz"],
            0,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
                "{tmp_dir}/unittest/s3utils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/s3utils",
            "{tmp_dir}/unittest/s3utils",
            "dummy-bucket",
            "unittest/s3utils",
            [],
            [],
            2,
            [
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/s3utils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.bar",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.baz",
                "{tmp_dir}/unittest/s3utils/dir.foo/file.foo",
            ],
        ),
    ]

    @ddt.idata(data_s3_sync)
    @ddt.unpack
    def test_s3_sync(self, src, dst, bucket, prefix, include_patterns, exclude_patterns, depth, expect):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix,
                           include_patterns=include_patterns,
                           exclude_patterns=exclude_patterns,
                           depth=depth)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory))

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory),
                                 include_patterns=include_patterns,
                                 exclude_patterns=exclude_patterns,
                                 depth=depth)

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix,
                           include_patterns=include_patterns,
                           depth=depth)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory),
                                 exclude_patterns=exclude_patterns,
                                 depth=depth)

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

    data_s3_text = [
        ("dummy-bucket", "dummy/key", "dummy content", None),
        ("dummy-bucket", "dummy/key.alpha", "Old MacDonald had a farm", None),
        ("dummy-bucket", "dummy/key.beta", "Ee-i-ee-i-o", None),
        ("dummy-bucket", "dummy/key", "dummy content", "ascii"),
        ("dummy-bucket", "dummy/key.alpha", "Old MacDonald had a farm", "ascii"),
        ("dummy-bucket", "dummy/key.beta", "Ee-i-ee-i-o", "ascii"),
    ]

    @ddt.idata(data_s3_text)
    @ddt.unpack
    def test_s3_text(self, bucket, key, text, encoding):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.client.create_bucket(Bucket=bucket)

            s3_push_text(client, text, bucket, key, encoding=encoding)
            self.assertEqual(s3_pull_text(client, bucket, key, encoding=encoding), text)
