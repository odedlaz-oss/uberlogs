import sys
import os
from logging import Handler as LoggingHandler


class KillProcessHandler(LoggingHandler):

    def emit(self, record):
        if record.levelno != self.level:
            return

        try:
            # flush text before exiting
            for fd in [sys.stdout, sys.stderr]:
                fd.flush()
        finally:
            # Twisted writes unhandled errors in different calls
            # If we exit on the first call, we'd lose the actual error
            for log_to_ignore in ["Unhandled error in Deferred"]:
                if log_to_ignore.lower() in record.getMessage().lower():
                    return
            os._exit(1)
