"""Utils Library"""

import tomllib

from os import environ

from loguru import logger

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


def load_toml_file(file: str) -> dict:
    """Load TOML file"""

    info: str = "load toml file"

    try:

        logger.info(f"{info} [ start ]")

        with open(file, "rb", encoding="utf-8") as _file:
            config = tomllib.load(_file)

        logger.success(f"{info} [ success ]")

        return config

    except Exception as e:

        logger.error(f"{info} [ error ]")

        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)

        return {}


# --------------------------------------------------------------------------------------------------
