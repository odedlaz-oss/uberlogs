import ujson as json
from math import floor
from .base import UberFormatter
from logging import Formatter as LoggingFormatter


MESSAGE = "message"
LOGGER = "logger"
LEVEL = "level"
FILE = "file"
FUNC = "func"
EPOCH = "epoch"


class SimpleJsonFormatter(UberFormatter):

    def __init__(self, indent=None, fmt=None, datefmt=None, **kwargs):
        """
        Initialize the handler.
        If stream is not specified, sys.stderr is used.
        """
        if fmt is not None or datefmt is not None:
            msg = "JsonFormatter doesn't allow to set 'format' and 'datefmt'!"
            raise ValueError(msg)

        super(SimpleJsonFormatter, self).__init__(fmt="%(uber_json)s",
                                                  **kwargs)
        self.indent = indent or 0

    def formatException(self, exc_info):
        """
        does nothing, because the default formatException
        dumps the formatted exception in a non json format
        """
        return ""

    @profile
    def _get_message_obj(self, record):
        msg_obj = {
            MESSAGE: record.getMessage(),
            LOGGER: record.name,
            LEVEL: record.levelname,
            FILE: record.pathname,
            FUNC: record.funcName,
            EPOCH: floor(record.created)
        }

        if record.exc_info:
            fn = LoggingFormatter.formatException
            msg_obj["exc_info"] = fn(self, record.exc_info)

        return msg_obj

    @profile
    def format(self, record):
        # create a clone of the record,
        # to make sure we don't change the original

        # get the message and format it
        msg_obj = self._get_message_obj(record)
        record.uber_json = json.dumps(msg_obj,
                                      sort_keys=True,
                                      indent=self.indent)

        return super(SimpleJsonFormatter, self).format(record)
