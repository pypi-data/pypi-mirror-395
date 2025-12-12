"""Technical logger for QCI Connect application."""

import logging
from json import dumps

# default stdout logging format
DEFAULT_LOG_MESSAGE_FORMAT_JSON = dumps({
    "time": "%(asctime)s",
    "processName": "%(processName)s",
    "PID": "%(process)d",
    "threadName": "%(threadName)s",
    "TID": "%(thread)d",
    "module": "%(module)s",
    "funcName": "%(funcName)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "log": "%(message)s"
})

DEFAULT_LOG_MESSAGE_FORMAT = (
    "%(asctime)s - %(processName)s (PID %(process)d): %(threadName)s "
    "(TID %(thread)d) - %(module)s - %(funcName)s - %(name)s - %(levelname)s "
    "- %(message)s"
)


# name of the default technical logger
DEFAULT_LOGGER_NAME = "qciconnect.default"


class QCIConnectLogging:
    """Default technical logger."""

    @classmethod
    def get_logger(cls):
        """Get default logger of the application."""
        return logging.getLogger(DEFAULT_LOGGER_NAME)
