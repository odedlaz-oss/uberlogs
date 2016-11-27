import six
from ..private import (rewrite_record,
                       extract_keywords)

from .simple_jsonf import SimpleJsonFormatter


class JsonFormatter(SimpleJsonFormatter):

    def _get_message_obj(self, record):
        msg_obj = super(JsonFormatter, self)._get_message_obj(record)
        if not self.uber_record(record):
            return msg_obj

        arguments = dict(rewrite_record(record))

        message = record.getMessage()

        if self.parse_text:
            message = message.format(**arguments)

        msg_obj["message"] = message

        include_keywords = self.include_format_keywords
        if not self.parse_text:
            include_keywords = True

        return dict(msg_obj,
                    **{k: v for k, v in six.iteritems(arguments)
                       if include_keywords or k not in keywords})
