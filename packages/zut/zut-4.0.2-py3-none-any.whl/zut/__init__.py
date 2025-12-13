"""
Reusable Python utilities to avoid reinventing the wheel.
"""
from __future__ import annotations

__prog__ = 'zut'

__version__: str
__version_tuple__: tuple[int|str, ...]
try:
    from zut._version import __version__, __version_tuple__  # type: ignore
except ModuleNotFoundError:
    __version__ = '?'
    __version_tuple__ = (0, 0, 0, '?')
