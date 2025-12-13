from __future__ import annotations
import functools as functools
import logging as logging
from logging.Logger import setLevel as _setLevel
from logging.Logger import setLevel as set_level_wrapper
from nuri._log_interface import set_log_level
__all__: list[str] = ['functools', 'logger', 'logging', 'set_level_wrapper', 'set_log_level']
logger: logging.Logger  # value = <Logger nuri (INFO)>
