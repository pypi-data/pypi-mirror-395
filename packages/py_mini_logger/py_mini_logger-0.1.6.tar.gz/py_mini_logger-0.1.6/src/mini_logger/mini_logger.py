#!/usr/bin/env python3

# Copyright 2025 (author: lamnt45)


# common
import os
from io import StringIO


# technical
import logging
import typing as tp
from booleanify import booleanify


### CLASSES
class MultiArgLogger(logging.Logger):


    def _log_with_args(self, level, *args, **kwargs):
        if not self.isEnabledFor(level):
            return

        # Capture output like print() would format it
        sio = StringIO()
        print(*args, file=sio, **kwargs)
        msg = sio.getvalue().rstrip()

        # Call the original _log method
        self._log(level, msg, ())



    def debug(self, *args, **kwargs):
        self._log_with_args(logging.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._log_with_args(logging.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._log_with_args(logging.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._log_with_args(logging.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._log_with_args(logging.CRITICAL, *args, **kwargs)

    def exception(self, *args, **kwargs):
        kwargs.setdefault('exc_info', True)
        self._log_with_args(logging.ERROR, *args, **kwargs)



### FUNCTIONS
def getMiniLogger(
    name      : str,
    log_level : tp.Optional[tp.Union[int, str]] = None,
    log_time  : tp.Optional[bool] = None,
) -> MultiArgLogger:
    return getLogger(
        name      = name,
        log_level = log_level,
        log_time  = log_time,
    )



def getLogger(
    name      : str,
    log_level : tp.Optional[tp.Union[int, str]] = None,
    log_time  : tp.Optional[bool] = None,
) -> MultiArgLogger:

    # Register our custom logger class
    logging.setLoggerClass(MultiArgLogger)

    logger = logging.getLogger(name)
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers = []

    logger_sole_handler = logging.StreamHandler()

    log_level = log_level or os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(log_level)

    if log_time is None:
        log_time = booleanify(os.environ.get('HU_LOG_TIME', True))

    if log_time:
        log_time_str_fmt = r'%(asctime)s '
    else:
        log_time_str_fmt = ''

    process_level = int(os.environ.get('PROCESS_LEVEL', 0))
    format_str = r'{0}{1}<%(name)s> {2}{3}%(message)s'.format(
        '\033' + '[38;5;243m',
        log_time_str_fmt,
        '└───' * process_level,
        '\033' + '[0m',
    )

    logger_sole_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(logger_sole_handler)

    return logger
