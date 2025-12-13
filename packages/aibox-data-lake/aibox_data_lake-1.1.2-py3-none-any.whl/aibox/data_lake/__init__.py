import logging.config

from .client import Client

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich_fmt": {"format": "[%(name)s][%(funcName)s]: %(message)s"},
    },
    "handlers": {
        "rich": {
            "level": "DEBUG",
            "formatter": "rich_fmt",
            "omit_repeated_times": False,
            "show_path": False,
            "class": "rich.logging.RichHandler",
        },
    },
    "loggers": {
        "aibox.data_lake": {
            "handlers": ["rich"],
            "level": "DEBUG",
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
del logging, LOGGING_CONFIG
