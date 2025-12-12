"""Logger."""

import logging
import sys


def decorate_emit(fn):
    """Add color to logging levels."""

    # add methods we need to the class
    def new(*args):
        levelno = args[0].levelno
        if levelno >= logging.CRITICAL:
            color = "\x1b[31;1m"
        elif levelno >= logging.ERROR:
            color = "\x1b[31;1m"
        elif levelno >= logging.WARNING:
            color = "\x1b[33;1m"
        elif levelno >= logging.INFO:
            color = "\x1b[32;1m"
        elif levelno >= logging.DEBUG:
            color = "\x1b[35;1m"
        else:
            color = "\x1b[0m"
        # add colored *** in the beginning of the message
        args[0].msg = "{0}***\x1b[0m {1}".format(color, args[0].msg)

        # new feature i like: bolder each args of message
        args[0].args = tuple("\x1b[1m" + arg + "\x1b[0m" for arg in args[0].args)
        return fn(*args)

    return new


log_level = logging.INFO
logger = logging.getLogger("ta-captcha-solver")
if logger.hasHandlers():
    logger.handlers = []
logger.propagate = False

log_format = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s")
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(log_level)
handler.setFormatter(log_format)
logger.addHandler(handler)
handler.emit = decorate_emit(handler.emit)
logger.addHandler(handler)
