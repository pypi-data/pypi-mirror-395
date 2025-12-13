"""
Registration of locales and retrieval of information about locales.
"""
from __future__ import annotations

import locale
import sys
import threading
from contextlib import contextmanager

#region Configure

def register_locale(name: str = ''):
    """
    Register a locale for the entire application.

    :param name: The locale to register (if none, register the system default locale).
    """
    locale.setlocale(locale.LC_ALL, _prepare_locale_name(name))


_locale_lock = threading.Lock()

@contextmanager
def use_locale(name: str = ''):
    """
    Use a locale temporary (in the following thread-local block/context).

    See: https://stackoverflow.com/a/24070673

    :param name: The locale to register (if none, use the system default locale).
    """
    with _locale_lock:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, _prepare_locale_name(name))
        finally:
            locale.setlocale(locale.LC_ALL, saved)


def _prepare_locale_name(name: str):
    if not name:
        return ''
    if not '.' in name:
        if sys.platform == 'win32':
            name += '.1252'
        else:
            name += '.UTF-8'
    return name

#endregion


#region Get information

_locale_name = None
_locale_decimal_separator = None
_locale_date_format = None


def get_locale_name():
    """
    Return the current locale name, for example: `fr_FR.UTF-8` on Linux or `French_France.1252` on Windows.
    """
    global _locale_name

    if _locale_name is None:
        with use_locale():
            region, encoding = locale.getlocale()
            _locale_name = f"{region or ''}.{encoding or ''}"

    return _locale_name


def get_locale_decimal_separator(name: str = ''):
    """
    Return locale decimal separator (use current locale if name is empty).
    """
    global _locale_decimal_separator
    if not name and _locale_decimal_separator is not None:
        return _locale_decimal_separator
    
    with use_locale(name):
        value = locale.localeconv()["decimal_point"]
    
    if not name:
        _locale_decimal_separator = value
    return value


def get_locale_date_format(name: str = '') -> str|None:
    """
    Return locale date format, if known (e.g. "%d/%m/%Y") (use current locale if name is empty).
    """
    global _locale_date_format
    if not name and _locale_date_format is not None:
        return _locale_date_format
    
    with use_locale(name):
        try:
            value = locale.nl_langinfo(locale.D_FMT) # type: ignore
        except AttributeError:
            name = get_locale_name()
            if name.startswith(('fr_FR.', 'French_France.')):
                value = '%d/%m/%Y'
            else:
                value = None

    if not name:
        _locale_date_format = value
    return value

#endregion
