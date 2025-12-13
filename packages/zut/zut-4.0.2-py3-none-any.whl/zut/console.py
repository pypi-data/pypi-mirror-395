"""
Console colors and other terminal utilities (live/transient output that can be erased).
"""
from __future__ import annotations

import os
import sys

#region Colors

class Color:
    RESET = '\033[0m'

    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    GRAY = LIGHT_BLACK = '\033[0;90m'
    BG_RED = '\033[0;41m'

    # Disable coloring if environment variable NO_COLORS is set to 1 or if stderr is piped/redirected
    NO_COLORS = False
    if os.environ.get('NO_COLORS', '').lower() in {'1', 'yes', 'true', 'on'} or not sys.stderr.isatty():
        NO_COLORS = True
        for _ in dir():
            if isinstance(_, str) and _[0] != '_' and _ not in ['NO_COLORS']:
                locals()[_] = ''

    # Set Windows console in VT mode
    if not NO_COLORS and sys.platform == 'win32':
        import ctypes
        _kernel32 = ctypes.windll.kernel32
        _kernel32.SetConsoleMode(_kernel32.GetStdHandle(-11), 7)
        del _kernel32

#endregion


#region Live/transient output

_transient_to_erase: dict[bool, list[int]] = {False: [], True: []}
_last_transient:  dict[bool, float|None] = {False: None, True: None}

def write_transient(text: str, *, stdout = False, newline=False, delay: float|int|None = None):
    """
    Write text to the terminal, keeping track of what was written, so that it can be erased later.

    Text lines are stripped to terminal column length.
    """    
    from time import time_ns

    t = time_ns()
    if delay is not None:
        t0 = _last_transient[stdout]
        if t0 is not None and (t - t0) / 1E9 < delay:
            return

    file = sys.stdout if stdout else sys.stderr
    if not sys.stderr.isatty(): # Ignore if we're not on a terminal
        return
    
    erase_transient(stdout=stdout)
    columns, _ = os.get_terminal_size()

    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.rstrip()
        
        nb_chars = len(line)
        if nb_chars > columns:
            line = line[:columns-1] + '…'
            nb_chars = columns

        _transient_to_erase[stdout].insert(0, nb_chars)

        file.write(line)
        if newline or i < len(lines) - 1:
            file.write('\n')

    if newline:
        _transient_to_erase[stdout].insert(0, 0)
    
    file.flush()
    _last_transient[stdout] = t


def erase_transient(*, stdout = False):
    """
    Erase text written using :func:`write_transient`.

    Text lines are stripped to terminal column length.
    """
    if not _transient_to_erase[stdout]:
        return
    
    file = sys.stdout if stdout else sys.stderr
    for i, nb_chars in enumerate(_transient_to_erase[stdout]):
        if i == 0:
            file.write('\r') # move to beginning of line
        else:
            file.write('\033[F') # move to beginning of previous line
        file.write(' ' * nb_chars)
    file.write('\r')

    _transient_to_erase[stdout].clear()
    _last_transient[stdout] = None

#endregion
