#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

Logging functions.

Copyright 2020-2023 Light Conversion
Contact: support@lightcon.com
"""

import logging


def init_logger(logger_name, file_name) -> logging.Logger:
    """Init a logger that simultaneously writes to stderr and a log file.
    
    Args:
        logger_name (str): name of the logger
        file_name (str): local file name

    Returns:
        logger instance (logging.Logger)
    """
    logger = logging.getLogger(logger_name)

    file_log_handler = logging.FileHandler(file_name)
    logger.addHandler(file_log_handler)

    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)

    formatter = logging.Formatter(
        fmt = '[%(asctime)s.%(msecs)03d %(levelname).3s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S')
    
    file_log_handler.setFormatter(formatter)
    stderr_log_handler.setFormatter(formatter)

    logger.setLevel('DEBUG')

    return logger
