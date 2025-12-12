"""QCI Connect Logging configuration."""

import logging
import os
from logging import config

from qciconnect_logging.logger import (
    DEFAULT_LOG_MESSAGE_FORMAT,
    DEFAULT_LOG_MESSAGE_FORMAT_JSON,
    DEFAULT_LOGGER_NAME,
)

STREAM_HANDLER_CLASS = "logging.StreamHandler"
FILE_HANDLER_CLASS = "logging.FileHandler"
STDOUT_STREAM = "ext://sys.stdout"
LOG_FILENAME = os.getenv("LOG_FILENAME", "logs.log")
LOG_PATH = f"/app/logs/{LOG_FILENAME}"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
DEV_ENV = os.getenv("DEV_ENV", "true").lower() == "true"

class SingleLineFormatter(logging.Formatter):
    """Custom formatter to replace newline characters with spaces in log messages."""

    def format(self, record) -> str:
        """Format log record."""
        if isinstance(record.msg, str):
            record.msg = record.msg.replace('\n', ' ')
            record.msg = record.msg.replace('\r', ' ')
            record.msg = record.msg.replace('\t', ' ')
            record.msg = record.msg.replace('"', '\\"')
        return super().format(record)

if DEV_ENV:
    message_format = DEFAULT_LOG_MESSAGE_FORMAT
    handlers = {
        "stdout_default": {
            "formatter": "formatter_default",
            "class": STREAM_HANDLER_CLASS,
            "stream": STDOUT_STREAM,
            "level": LOG_LEVEL,
        },
    }
    celery_log_level = "INFO"
    sqlalchemy_log_level = "INFO"
else:
    message_format = DEFAULT_LOG_MESSAGE_FORMAT_JSON
    handlers = {
        "stdout_default": {
            "formatter": "formatter_default",
            "class": STREAM_HANDLER_CLASS,
            "stream": STDOUT_STREAM,
            "level": LOG_LEVEL,
        },
    } 
    celery_log_level = "WARNING"
    sqlalchemy_log_level = "WARNING"

log_config = {
    "version": 1,
    "formatters": {
        "formatter_default": {"()": SingleLineFormatter,"format":message_format},
    },
    "handlers": handlers,
    "loggers": {
        # root logger to stdout
        "": {"handlers": ["stdout_default"], "level": LOG_LEVEL},
        # QCI Connect  default technical logger
        DEFAULT_LOGGER_NAME: {
            "handlers": ["stdout_default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # 3 uvicorn loggers
        "uvicorn.access": {
            "handlers": ["stdout_default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["stdout_default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["stdout_default"],
            "level": "INFO",
            "propagate": False,
        },
        # python warnings propagated to stdout
        "py.warnings": {
            "handlers": ["stdout_default"],
            "level": "INFO",
            "propagate": False,
        },
        # SQL queries to stdout
        "sqlalchemy.engine": {
            "handlers": ["stdout_default"],
            "level": sqlalchemy_log_level,
            "propagate": False,
        },
        # celery logging to stdout
        "celery": {"handlers": ["stdout_default"], "level": celery_log_level, "propagate": False},
    },
}


def initialize_logging():
    """Initialize logging configuration based on dict config."""
    # capture warnings with logger
    logging.captureWarnings(True)
    # configure logging from dict configuration
    config.dictConfig(log_config)
