# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def create_json_logger(logger_name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create logger which write output to console and log file.
    Logging levels: https://docs.python.org/3/library/logging.html#logging-levels
    Format options: https://docs.python.org/3/library/logging.html#logrecord-attributes

    Args:
        logger_name (str): Name to identify logger and used as log file's name.
        level (int, optional): Level of log message will be included. Defaults to logging.INFO.

    Returns:
        Logger: Logger class for manipulate message
    """
    logger = logging.getLogger(logger_name)
    logger.level = level
    logger.propagate = False

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    return logger
