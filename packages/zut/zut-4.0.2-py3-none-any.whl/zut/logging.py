"""
Configuration of logging and helpers for specific use cases.

Nominal use case is through standard library's `logging.getLogger`.
"""
from __future__ import annotations

import atexit
import logging
import logging.config
import os
import re
import sys
from contextlib import contextmanager
from traceback import format_exception
from types import TracebackType
from typing import TYPE_CHECKING, Callable, Mapping
from warnings import catch_warnings

from zut.console import Color

if TYPE_CHECKING:
    from typing import Literal


#region Configure

_configured_logging: dict|None = None

def configure_logging(level: str|int|None = None, *, colors = True, names: bool|None = None, file: str|os.PathLike|None = None, file_level: int|str|None = None, count = True, count_on_exit = True, loggers: Mapping[str,str|int|dict|None]|None = None, reconfigure: bool|Literal['warn'] = 'warn') -> None:
    global _configured_logging

    config = get_logging_config(level, colors=colors, names=names, file=file, file_level=file_level, count=count, count_on_exit=count_on_exit, loggers=loggers)
    
    if _configured_logging is None:
        pass

    elif config == _configured_logging:
        log_preinit(logging.DEBUG, "Ignore reconfiguration of logging: same config dict")
        return

    elif not reconfigure:
        log_preinit(logging.DEBUG, "Ignore reconfiguration of logging: reconfiguration disabled")
        return

    else:
        log_preinit(logging.DEBUG if reconfigure is True else logging.WARNING, "Reconfiguration of logging")
        pass

    logging.config.dictConfig(config)
    _configured_logging = config


def get_logging_config(level: int|str|None = None, *, colors = True, names: bool|None = None, file: str|os.PathLike|None = None, file_level: int|str|None = None, count = True, count_on_exit = True, loggers: Mapping[str,str|int|dict|None]|None = None) -> dict:
    """
    Get logging configuration dictionnary.

    :param colors: Indicate whether the console handler should be colorized (this has no effect if `Colors.NO_COLORS` is set).
    :param names:  Indicate whether the console handler should include logger names.
    """
    
    # ---------- Define base config ----------

    if not isinstance(level, str):
        if isinstance(level, int):
            level = logging.getLevelName(level)
        else:
            level = os.environ.get('LOG_LEVEL', '').upper() or 'INFO'

    if names is None:
        names = os.environ.get('LOG_NAMES', '').lower() in {'1', 'yes', 'true', 'on'}
    
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'without_names': {
                'format': '%(levelname)-8s %(message)s'
            },
            'with_names': {
                'format': '%(levelname)-8s [%(name)s] %(message)s'
            },
            'colored_without_names': {                
                '()': ColoredFormatter.__module__ + '.' + ColoredFormatter.__qualname__,
                'format': '%(log_color)s%(levelname)-8s%(reset)s %(message)s'
            },
            'colored_with_names': {
                '()': ColoredFormatter.__module__ + '.' + ColoredFormatter.__qualname__,
                'format': '%(log_color)s%(levelname)-8s%(reset)s %(light_black)s[%(name)s]%(reset)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': ('colored_' if colors else '') + ('with_names' if names else 'without_names'),
                'level': level,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': level,
        },
        'loggers': {
            'django': { 'level': 'INFO', 'propagate': False },
            'daphne': { 'level': 'INFO', 'propagate': False },
            'asyncio': { 'level': 'INFO', 'propagate': False },
            'urllib3': { 'level': 'INFO', 'propagate': False },
            'botocore': { 'level': 'INFO', 'propagate': False },
            'boto3': { 'level': 'INFO', 'propagate': False },
            's3transfer': { 'level': 'INFO', 'propagate': False },
            'PIL': { 'level': 'INFO', 'propagate': False },
            'celery.utils.functional': { 'level': 'INFO', 'propagate': False },
            'smbprotocol': { 'level': 'WARNING', 'propagate': False },
        },
    }
    
    # ---------- Add file handler ----------
    
    if file is None:
        file = os.environ.get('LOG_FILE', '')
        if file.upper() in {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}:
            if file_level:
                raise ValueError("file and file_level are both defined as logging levels")
            file_level = file
    
    if file_level and file is None:
        file = '~log'

    if file:
        if not isinstance(file_level, str):
            if isinstance(file_level, int):
                file_level = logging.getLevelName(file_level)
            else:
                file_level = os.environ.get('LOG_FILE_LEVEL', '').upper() or level

        log_dir = os.path.dirname(file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        config['formatters']['file'] = {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        }

        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'level': file_level,
            'formatter': 'file',
            'filename': file,
            'encoding': 'utf-8',
        }

        config['root']['handlers'].append('file')
    
        file_intlevel = logging.getLevelName(file_level)
        intlevel = logging.getLevelName(level)
        if file_intlevel < intlevel:
            config['root']['level'] = file_level

    # ---------- Add log counter ----------

    if count or count_on_exit:
        config['handlers']['counter'] = {
            'class': LogCounter.__module__ + '.' + LogCounter.__qualname__,
            'level': 'WARNING',
            'count_on_exit': count_on_exit,
        }

        config['root']['handlers'].append('counter')
    
    # ---------- Add specific logger configurations ----------

    if loggers:
        for logger_name, logger_config in loggers.items():
            if logger_config is None:
                config['loggers'].pop(logger_name, None)
                continue
            
            if isinstance(logger_config, str):
                logger_config = { 'level': logger_config, 'propagate': False }
            elif isinstance(logger_config, int):
                logger_config = { 'level': logging.getLevelName(logger_config), 'propagate': False }
            config['loggers'][logger_name] = logger_config

    return config


class ColoredRecord:
    LOG_COLORS = {
        logging.DEBUG:     Color.GRAY,
        logging.INFO:      Color.CYAN,
        logging.WARNING:   Color.YELLOW,
        logging.ERROR:     Color.RED,
        logging.CRITICAL:  Color.BG_RED,
    }

    def __init__(self, record: logging.LogRecord):
        # The internal dict is used by Python logging library when formatting the message.
        # (inspired from library "colorlog").
        self.__dict__.update(record.__dict__)
        
        self.log_color = self.LOG_COLORS.get(record.levelno, '')

        for attname, value in Color.__dict__.items():
            if attname == 'NO_COLORS' or attname.startswith('_'):
                continue
            setattr(self, attname.lower(), value)


class ColoredFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        wrapper = ColoredRecord(record)
        message = super().formatMessage(wrapper) # type: ignore
        return message


class LogCounter(logging.Handler):
    """
    A logging handler that counts warnings and errors.
    
    If warnings and errors occured during the program execution, display counts at exit
    and set exit code (if it was not explicitely set with `sys.exit` function).
    """
    counts: dict[int, int] = {}

    error_exit_code = 199
    warning_exit_code = 198
    
    _detected_exception: tuple[type[BaseException], BaseException, TracebackType|None]|None = None
    _detected_exit_code = 0
    _original_exit: Callable[[int],None] = sys.exit
    _original_excepthook = sys.excepthook

    _exit_handler_registered = False
    _logger: logging.Logger

    def __init__(self, *, level = logging.WARNING, count_on_exit = True):        
        if count_on_exit and not self.__class__._exit_handler_registered:
            sys.exit = self.__class__._exit
            sys.excepthook = self.__class__._excepthook
            atexit.register(self.__class__._exit_handler)
            self.__class__._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__qualname__}")
            self.__class__._exit_handler_registered = True
        
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord):        
        if not record.levelno in self.__class__.counts:
            self.__class__.counts[record.levelno] = 1
        else:
            self.__class__.counts[record.levelno] += 1
    
    @classmethod
    def _exit(cls, code: int = 0):
        cls._detected_exit_code = code
        cls._original_exit(code)
    
    @classmethod
    def _excepthook(cls, exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType|None):
        cls._detected_exception = exc_type, exc_value, exc_traceback
        cls._original_exit(1)

    @classmethod
    def _exit_handler(cls):
        if cls._detected_exception:
            exc_type, exc_value, exc_traceback = cls._detected_exception

            msg = 'An unhandled exception occured\n'
            msg += ''.join(format_exception(exc_type, exc_value, exc_traceback)).strip()
            cls._logger.critical(msg)

        else:
            error_count = 0
            warning_count = 0
            for level, count in cls.counts.items():
                if level >= logging.ERROR:
                    error_count += count
                elif level >= logging.WARNING:
                    warning_count += count
            
            msg = ''
            if error_count > 0:
                msg += (', ' if msg else 'Logged ') + f"{error_count:,} error{'s' if error_count > 1 else ''}"
            if warning_count > 0:
                msg += (', ' if msg else 'Logged ') + f"{warning_count:,} warning{'s' if warning_count > 1 else ''}"
            
            if msg:
                cls._logger.log(logging.ERROR if error_count > 0 else logging.WARNING, msg)                             
                # Change exit code if it was not originally set explicitely to another value using `sys.exit()`
                if cls._detected_exit_code == 0:
                    r = cls.error_exit_code if error_count > 0 else cls.warning_exit_code
                    cls._logger.debug("Change exit code to %d", r)
                    os._exit(r)

#endregion


#region Specific use cases

_is_log_preinit_enabled_for_debug: bool|None = None

def is_log_preinit_enabled_for(level: int):
    global _is_log_preinit_enabled_for_debug

    if level <= logging.DEBUG:
        if _is_log_preinit_enabled_for_debug is None:
            _is_log_preinit_enabled_for_debug = os.environ.get('LOG_LEVEL', '').upper() == 'DEBUG'
        return _is_log_preinit_enabled_for_debug
    
    else:
        return True


def log_preinit(level: int, message: str, *args, logger_name: str|None = None):
    """
    Log a message, possibly before initialization of the application (i.e. before logging is configured).
    """
    if _configured_logging is not None:
        logging.getLogger(logger_name or __name__).log(level, message, *args)
        return

    if not is_log_preinit_enabled_for(level):
        return

    if args:
        message = message % args
    
    color = ''
    if level <= logging.DEBUG:
        color = Color.GRAY

    sys.stderr.write(f"%s%s{Color.RESET} {Color.GRAY}[preinit]{Color.RESET} %s\n" % (color, logging.getLevelName(level).ljust(8), message))


@contextmanager
def log_caught_warnings(*, ignore: str|re.Pattern|list[str|re.Pattern]|None = None, logger: logging.Logger|None = None):
    catch = catch_warnings(record=True)
    ctx = None
    try:
        ctx = catch.__enter__()
        yield None
    
    finally:
        if isinstance(ignore, (str,re.Pattern)):
            ignore = [ignore]

        if ctx is not None:
            for warning in ctx:
                ignored = False
                if ignore:
                    message = str(warning.message)
                    for spec in ignore:
                        if isinstance(spec, re.Pattern):
                            if spec.match(message):
                                ignored = True
                                break
                        elif spec == message:
                            ignored = True
                            break
                
                if not ignored:                                
                    if not logger:
                        logger = logging.getLogger(__name__)
                    logger.warning("%s: %s", warning.category.__name__, warning.message)
        
        catch.__exit__(None, None, None)

#endregion
