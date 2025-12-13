import hashlib

from iker.common.utils import logger
from iker.common.utils.config import Config
from iker.common.utils.funcutils import singleton
from iker.common.utils.shutils import expanded_path


@singleton
def config() -> Config:
    default_items: list[tuple[str, str, str]] = [
        ("pulse.commons", "logging.level", "INFO"),
        ("pulse.commons", "logging.format", "%(asctime)s [%(levelname)s] %(name)s: %(message)s"),
    ]

    config = Config(expanded_path("~/.iker.pulse.cfg"))
    config.restore()
    config.update(default_items, overwrite=False)

    return config


def validate_pulse_super_token(token: str) -> bool:
    """
    Validate the pulse super token.
    :param token: The token to validate.
    :return: True if the token is valid, False otherwise.
    """
    return hashlib.sha256(token.encode()).hexdigest() == pulse_super_token_sha256()


def ask_pulse_super_token():
    import getpass
    super_token = getpass.getpass("Pulse super token required: ")
    if not validate_pulse_super_token(super_token):
        raise ValueError("wrong Pulse super token")


@singleton
def pulse_super_token_sha256() -> str:
    return "d7f97abe12bb00a7d19cb5957350509c14b3b085cf84524b80d389c6c2086f1b"


def config_print_or_set(config: Config, section: str, key: str, value: str):
    if value is not None:
        if section is None or key is None:
            raise ValueError("cannot specify value without section and key")

        old_value = config.get(section, key)
        config.set(section, key, value)
        config.persist()

        print(f"Configuration file '{config.config_path}'", )
        print(f"Section <{section}>")
        print(f"  {key} = {old_value} -> {value}")

    else:
        if section is None and key is None:
            print(f"Configuration file '{config.config_path}'", )
            for section in config.config_parser.sections():
                print(f"Section <{section}>")
                for key, value in config.config_parser.items(section):
                    print(f"  {key} = {value}")

        elif section is not None and key is None:
            if not config.has_section(section):
                logger.warning("Configuration section <%s> not found", section)
                return
            print(f"Configuration file '{config.config_path}'", )
            print(f"Section <{section}>")
            for key, value in config.config_parser.items(section):
                print(f"  {key} = {value}")

        elif section is not None and key is not None:
            value = config.get(section, key)
            if value is None:
                logger.warning("Configuration section <%s> key <%s> not found", section, key)
                return
            print(f"Configuration file '{config.config_path}'", )
            print(f"Section <{section}>")
            print(f"  {key} = {value}")

        else:
            raise ValueError("cannot specify key without section")
