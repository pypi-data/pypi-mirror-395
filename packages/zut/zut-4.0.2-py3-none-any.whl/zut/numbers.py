"""
Parse and convert numbers.
"""
from __future__ import annotations

import re
import sys
from decimal import Decimal
from typing import TYPE_CHECKING, Sequence, overload

if TYPE_CHECKING:
    from typing import Literal


#region Protocols

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    Protocol = object

class GoogleMoney(Protocol):
    """
    Represents an amount of money with its currency type, as defined by Google.
    
    See https://developers.google.com/actions-center/verticals/things-to-do/reference/feed-spec/google-types?hl=fr#googletypemoney_definition
    """

    currency_code: str
    """ 3-letter currency code defined in ISO 4217. """

    units: int|float
    """ Number of units of the amount (should be integers but float are accepted). """

    nanos: int
    """ Number of nano (10^-9) units of the amount. """

#endregion


#region Parse from strings

def parse_float(value: str|GoogleMoney, *, decimal_separator: Literal['.',',','detect'] = '.') -> float:
    if isinstance(value, str):
        return float(_handle_decimal_str(value, decimal_separator))
    elif hasattr(value, 'units') and hasattr(value, 'nanos'): # GoogleMoney
        return float(getattr(value, 'units') + getattr(value, 'nanos') / 1E9)
    else:
        raise TypeError(f"value: {type(value).__name__}")


def parse_decimal(value: Decimal|str|float|GoogleMoney, *, max_decimals: int|None = None, reduce_decimals:int|Sequence[int]|bool = False, decimal_separator: Literal['.',',','detect'] = '.') -> Decimal:
    """
    Parse a Decimal value.

    :param value:               The value to convert.
    :param max_decimals:        Maximal number of decimal digits to use (the value will be rounded if necessary).
    :param reduce_decimals:     If set, reduce the number of decimal digits to the given number if this can be done without rounding (if set to True, try to reduce to 2 digits, otherwise to 5).
    :param decimal_separator:   Indicate if `.` or `,` is used as decimal separator, or `detect` to detect it (use with caution: might introduce errors if the values can have thousands separators).
    """
    decimal_value: Decimal
    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, (float,int)):
        decimal_value = Decimal(value)
    elif isinstance(value, str):
        decimal_value = Decimal(_handle_decimal_str(value, decimal_separator))
    elif hasattr(value, 'units') and hasattr(value, 'nanos'): # GoogleMoney
        decimal_value = Decimal(getattr(value, 'units') + getattr(value, 'nanos') / 1E9)
        if max_decimals is None:
            max_decimals = 9
    else:
        raise TypeError(f"value: {type(value).__name__}")

    if max_decimals is not None:
        decimal_value = round(decimal_value, max_decimals)

    if reduce_decimals is False or reduce_decimals is None:
        lower_boundaries = []
    elif reduce_decimals is True:
        lower_boundaries = [2, 5]
    elif isinstance(reduce_decimals, int):
        lower_boundaries = [reduce_decimals]
    elif isinstance(reduce_decimals, Sequence):
        lower_boundaries = sorted(reduce_decimals)
    else:
        raise TypeError(f"reduce_decimals: {type(reduce_decimals).__name__}")
    
    for boundary in lower_boundaries:
        expo = decimal_value * 10 ** boundary
        remaining = expo - int(expo)
        if remaining == 0:
            return round(decimal_value, boundary)
    
    return decimal_value


def _handle_decimal_str(value: str, decimal_separator: Literal['.',',','detect']):
    # Remove spaces and non-break spaces that may be used as thousands separators
    value = re.sub(r'[ \u00A0\u202F]', '', value)

    if decimal_separator == 'detect':
        comma_rfind = value.rfind(',')
        dot_rfind = value.rfind('.')

        if dot_rfind >= 0 and comma_rfind > dot_rfind: # comma after dot
            return _remove_thousand_separator(value, '.').replace(',', '.')

        elif comma_rfind >= 0 and dot_rfind > comma_rfind: # dot after comma
            return _remove_thousand_separator(value, ',')

        elif comma_rfind >= 0: # comma only
            if not _check_thousand_separator(value, ','):
                return value.replace(',', '.')

        elif dot_rfind >= 0: # dot only
            if not _check_thousand_separator(value, '.'):
                return value

        else: # no comma or dot (no need to make a conversion)
            return value
        
        # Here, there is only one comma or one dot, and it may be a thousand separator (or a decimal separator)
        # => we rely on the locale configuration to determine what is the decimal separator
        from zut.locale import get_locale_decimal_separator
        if get_locale_decimal_separator() == ',':
            return value.replace(',', '.')
        else:
            return value
    
    elif decimal_separator == '.':
        return _remove_thousand_separator(value, ',')
    else:
        return _remove_thousand_separator(value, '.').replace(decimal_separator, '.')


def _remove_thousand_separator(text: str, thousand_separator: str):
    """
    Return `text` with `thousand_separator` removed if it actually is compatible with a thousands separator. Otherwise a `ValueError` is raised.
    """
    if _check_thousand_separator(text, thousand_separator):
        return text.replace(thousand_separator, '')
    else:
        raise ValueError(f"Invalid thousands separator `{thousand_separator}` in `{text}`")


def _check_thousand_separator(text: str, thousand_separator: str):
    """
    Determine if the given separator may be a thousands separator of the text.
    """
    decimal_separator = '.' if thousand_separator == ',' else ','
    decimal_separator_pos = text.rfind(decimal_separator)

    group_i = 0
    at_least_one_separator = False
    for char in reversed(text[0:decimal_separator_pos] if decimal_separator_pos >= 0 else text):
        if group_i < 3:
            if not char.isdigit():
                return False
            group_i += 1
        else: # group_i == 3
            if char != thousand_separator:
                return False
            at_least_one_separator = True
            group_i = 0 # next group will start

    return at_least_one_separator

#endregion


#region Convert to strings

def get_number_str(value: float|Decimal|int, *, max_decimals = 15, decimal_separator = '.', no_scientific_notation = False):
    """
    Display the number as a digits string without using scientifical notation, with integer part, decimal separator and decimal part (if any).
    
    This is less accurate for small decimals but more readable and portable when approximations are OK.
    """
    if isinstance(value, int):
        return str(value)
    else:
        text = format(value, f".{max_decimals}{'f' if no_scientific_notation else 'g'}")
        if not 'e' in text:
            pos = text.rfind('.')
            if pos > 0:
                last = len(text) - 1
                while last > pos:
                    if text.endswith('0'):
                        text = text[:-1]
                    else:
                        break
                if text.endswith('.'):
                    text = text[:-1]
        if decimal_separator != '.':
            return text.replace('.', decimal_separator)
        return text


@overload
def human_bytes(value: int, *, unit: str = 'iB', divider: int = 1024, decimals: int = 1, max_multiple: str|None = None) -> str:
    ...

@overload
def human_bytes(value: None, *, unit: str = 'iB', divider: int = 1024, decimals: int = 1, max_multiple: str|None = None) -> None:
    ...

def human_bytes(value: int|None, *, unit: str = 'iB', divider: int = 1024, decimals: int = 1, max_multiple: str|None = None) -> str|None:
    """
    Get a human-readable representation of a number of bytes.
    
    :param max_multiple: may be `K`, `M`, `G` or `T`.
    """
    return human_number(value, unit=unit, divider=divider, decimals=decimals, max_multiple=max_multiple)


@overload
def human_number(value: int, *, unit: str = '', divider: int = 1000, decimals: int = 1, max_multiple: str|None = None) -> str:
    ...

@overload
def human_number(value: None, *, unit: str = '', divider: int = 1000, decimals: int = 1, max_multiple: str|None = None) -> None:
    ...

def human_number(value: int|None, *, unit: str = '', divider: int = 1000, decimals: int = 1, max_multiple: str|None = None) -> str|None:
    """
    Get a human-readable representation of a number.

    :param max_multiple: may be `K`, `M`, `G` or `T`.
    """
    if value is None:
        return None

    suffixes = []

    # Append non-multiple suffix (bytes)
    # (if unit is 'iB' we dont display the 'i' as it makes more sens to display "123 B" than "123 iB")
    if unit:
        suffixes.append(' ' + (unit[1:] if len(unit) >= 2 and unit[0] == 'i' else unit))
    else:
        suffixes.append('')

    # Append multiple suffixes
    for multiple in ['K', 'M', 'G', 'T']:
        suffixes.append(f' {multiple}{unit}')
        if max_multiple and max_multiple.upper() == multiple:
            break

    i = 0
    suffix = suffixes[i]
    divided_value = value

    while divided_value > 1000 and i < len(suffixes) - 1:
        divided_value /= divider
        i += 1
        suffix = suffixes[i]

    # Format value
    formatted_value = ('{0:,.'+('0' if i == 0 else str(decimals))+'f}').format(divided_value)
    
    # Display formatted value with suffix
    return f'{formatted_value}{suffix}'

#endregion
