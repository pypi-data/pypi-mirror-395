# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
"""
Personal knowledge Library
--------------------------
This library provides a set of tools to manage Wacom private knowledge graph API.
All services are wrapped in a pythonic way to make it easy to use.
Additionally, the library provides a set of tools to utilise Wikidata.
"""
import sys
from datetime import datetime

__author__ = "Markus Weber"
__copyright__ = "Copyright 2021-present Wacom. All rights reserved."
__credits__ = ["Markus Weber"]
__license__ = "Wacom"
__maintainer__ = ["Markus Weber"]
__email__ = "markus.weber@wacom.com"
__status__ = "beta"
__version__ = "4.0.3"

import loguru

# Create the Logger
logger = None

if logger is None:
    import logging
    import inspect
    from typing import Union

    class InterceptHandler(logging.Handler):
        """
        Custom logging handler to redirect logs from the standard logging module to Loguru.
        This handler intercepts log messages and forwards them to the Loguru logger.
        """

        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists.
            try:
                level: Union[str, int] = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = inspect.currentframe(), 0
            while frame:
                filename = frame.f_code.co_filename
                is_logging = filename == logging.__file__
                is_frozen = "importlib" in filename and "_bootstrap" in filename
                if depth > 0 and not (is_logging or is_frozen):
                    break
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logger = loguru.logger
    logger.remove()
    logger.info("Logger initialized in for pks tools.")
    today = datetime.now()
    logger.add(
        sys.stderr,
        colorize=True,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        level="INFO",
        enqueue=True,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

__all__ = [
    "__copyright__",
    "__credits__",
    "__license__",
    "__maintainer__",
    "__email__",
    "__status__",
    "__version__",
    "logger",
    "base",
    "nel",
    "public",
    "services",
    "utils",
]

from knowledge import base
from knowledge import nel
from knowledge import public
from knowledge import services
from knowledge import utils
