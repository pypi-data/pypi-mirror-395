from __future__ import annotations

import io
import logging
import os
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import MutableMapping

MSG_PREFIX = " - "


class PrefixLoggerAdapter(logging.LoggerAdapter):
    """A logger adapter that adds a prefix to every message"""

    def process(self, msg: str, kwargs: MutableMapping[str, str]) -> Any:
        msg = MSG_PREFIX + msg
        if self.extra is not None:
            prefix = self.extra["prefix"]
            msg = f"[{prefix}]" + msg
        return msg, kwargs


YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

BQ_FORMAT = (
    "{color0}[BQ-PYTHON-SDK]{reset}[{color}%(levelname)s{reset}]%(message)s{reset}"
)


class BlueQubitLoggerFormatter(logging.Formatter):
    class Default(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    BQ_COLORED_FORMAT = BQ_FORMAT.format_map(
        Default(
            color0=CYAN,
            reset=RESET,
        )
    )

    FORMATS = {  # noqa: RUF012
        logging.DEBUG: BQ_COLORED_FORMAT.format(color=BLUE),
        logging.INFO: BQ_COLORED_FORMAT.format(color=GREEN),
        logging.WARNING: BQ_COLORED_FORMAT.format(color=YELLOW),
        logging.ERROR: BQ_COLORED_FORMAT.format(color=RED),
        logging.CRITICAL: BQ_COLORED_FORMAT.format(color=RED),
    }

    def __init__(self, *, colored):
        super().__init__()
        self.colored = colored
        self.formatters = {}
        for levelno, log_fmt in self.FORMATS.items():
            if self.colored:
                self.formatters[levelno] = logging.Formatter(log_fmt)
            else:
                self.formatters[levelno] = logging.Formatter(
                    fmt=BQ_FORMAT.format(color0="", reset="", color="")
                )

    def format(self, record):
        return self.formatters[record.levelno].format(record)


# modified from https://github.com/termcolor/termcolor/blob/main/src/termcolor/termcolor.py
def _can_do_colour() -> bool:
    """Check env vars and for tty/dumb terminal"""
    # Then check env vars:
    if "ANSI_COLORS_DISABLED" in os.environ:
        return False
    if "NO_COLOR" in os.environ:
        return False
    if "FORCE_COLOR" in os.environ:
        return True

    # Then check system:
    if os.environ.get("TERM") == "dumb":
        return False
    if not hasattr(sys.stdout, "fileno"):
        return False
    if not hasattr(sys.stderr, "fileno"):
        return False

    try:
        return os.isatty(sys.stdout.fileno()) and os.isatty(sys.stderr.fileno())
    except io.UnsupportedOperation:
        return sys.stdout.isatty() and sys.stderr.isatty()


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)


class PrefixWithSpaceFilter(logging.Filter):
    def filter(self, record):
        if record.msg[0] != "[":
            record.msg = MSG_PREFIX + record.msg
        return True


def init_logger():
    handler1 = logging.StreamHandler(sys.stdout)
    handler2 = logging.StreamHandler(sys.stderr)
    if _can_do_colour():
        handler1.setFormatter(BlueQubitLoggerFormatter(colored=True))
        handler2.setFormatter(BlueQubitLoggerFormatter(colored=True))
    else:
        handler1.setFormatter(BlueQubitLoggerFormatter(colored=False))
        handler2.setFormatter(BlueQubitLoggerFormatter(colored=False))

    handler1.setLevel(logging.DEBUG)
    handler1.addFilter(InfoFilter())

    handler2.setLevel(logging.WARNING)

    handler1.addFilter(PrefixWithSpaceFilter())
    handler2.addFilter(PrefixWithSpaceFilter())

    logger = logging.getLogger("bluequbit-python-sdk")
    log_level = os.environ.get("BLUEQUBIT_LOG_LEVEL", "INFO")
    log_level = log_level.upper()
    logger.setLevel(log_level)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger
