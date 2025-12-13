"""
Flexible conversion functions.
"""
from __future__ import annotations

import inspect
import re
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Iterable, Mapping, Sequence, Set, TypeVar

from zut.time import parse_date, parse_datetime
from zut.errors import NotImplementedBy, NotSupportedBy
from zut.json import decode_json, encode_json
from zut.numbers import get_number_str, parse_decimal, parse_float
from zut.types import get_single_generic_argument

if TYPE_CHECKING:
    from typing import Literal


#region Parse from strings

def parse_bool(value: bool|str) -> bool:
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")

    lower = value.lower()
    # same rules as RawConfigParser.BOOLEAN_STATES
    if lower in {'1', 'yes', 'true', 'on'}:
        return True
    elif lower in {'0', 'no', 'false', 'off'}:
        return False
    else:
        raise ValueError('Not a boolean: %s' % lower)


def parse_list(value: str|list, *, separator='|') -> list[str]:
    if isinstance(value, list):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value).__name__}")
    
    value = value.strip()
    if value == '':
        return []

    # Assume format depending on first character
    if value.startswith('{'):
        return parse_pg_array(value)
    elif value.startswith('['):
        return decode_json(value)
    else:
        return [element.strip() for element in value.split(separator)]


def parse_dict(value: str, *, separator='|') -> dict[str,str|Literal[True]]:
    if value is None:
        return None
    elif isinstance(value, dict):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")
    
    value = value.strip()
    if value == '':
        raise ValueError("Invalid dict value: empty string")

    # Assume format depending on first character
    if value.startswith('{'):
        return decode_json(value)
    else:
        result: dict[str,str|Literal[True]] = {}
        for element in value.split(separator):
            element = element.strip()
            try:
                pos = element.index('=')
                key = element[:pos].strip()
                result[key] = element[pos+1:].strip()
            except ValueError:
                key = element
                result[key] = True
        return result


def parse_func_parameters(func: Callable, *args: str):
    """
    Convert `args` (list of strings typically comming from the command line) into typed args and kwargs for `func`.
    """
    if not args:
        return tuple(), dict()
    
    # Determine argument types
    signature = inspect.signature(func)
    var_positional_type = None
    var_keyword_type = None
    parameter_types = {}
    positional_types = []
    for parameter in signature.parameters.values():
        parameter_type = None if parameter.annotation is inspect.Parameter.empty else parameter.annotation
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            var_positional_type = parameter_type
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            var_keyword_type = parameter_type
        else:
            parameter_types[parameter.name] = parameter_type
            if parameter.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]:
                positional_types.append(parameter_type)
    
    # Distinguish args and kwargs
    positionnal_args = []
    keyword_args = {}
    for arg in args:
        m = re.match(r'^([a-z0-9_]+)=(.+)$', arg)
        if m:
            keyword_args[m[1]] = m[2]
        else:
            positionnal_args.append(arg)

    # Convert kwargs
    for parameter, value in keyword_args.items():
        if parameter in parameter_types:
            target_type = parameter_types[parameter]
            if target_type:
                value = convert(value, target_type)
                keyword_args[parameter] = value

        elif var_keyword_type:
            keyword_args[parameter] = convert(value, var_keyword_type)

    # Convert args
    for i, value in enumerate(positionnal_args):
        if i < len(positional_types):
            target_type = positional_types[i]
            if target_type:
                positionnal_args[i] = convert(value, target_type)

        elif var_positional_type:
            positionnal_args[i] = convert(value, var_positional_type)

    return tuple(positionnal_args), keyword_args


def parse_pg_array(value: str) -> list[str]:
    """ Parse an array literal (using PostgreSQL syntax) into a list. """
    # See: https://www.postgresql.org/docs/current/arrays.html#ARRAYS-INPUT
    if not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")

    if len(value) == 0:
        raise ValueError(f"Invalid postgresql array literal: empty string")
    elif value[0] != '{' or value[-1] != '}':
        raise ValueError(f"Invalid postgresql array literal '{value}': does not start with '{{' and end with '}}'")
        
    def split(text: str):
        pos = 0

        def get_quoted_part(start_pos: int):
            nonlocal pos
            pos = start_pos
            while True:
                try:
                    next_pos = text.index('"', pos + 1)
                except ValueError:
                    raise ValueError(f"Unclosed quote from position {pos}: {text[pos:]}")
                
                pos = next_pos
                if text[pos - 1] == '\\' and (pos <= 2 or text[pos - 2] != '\\'): # escaped quote
                    pos += 1 # will search next quote
                else:
                    value = text[start_pos+1:pos]
                    pos += 1
                    if pos == len(text): # end
                        pass
                    else:
                        if text[pos] != ',':
                            raise ValueError(f"Quoted part \"{value}\" is followed by \"{text[pos]}\", expected a comma")
                        pos += 1
                    return value

        def get_unquoted_part(start_pos: int):
            nonlocal pos
            try:
                pos = text.index(',', start_pos)
                value = text[start_pos:pos]
                pos += 1
            except ValueError:
                pos = len(text) # end
                value = text[start_pos:]

            if value.lower() == 'null':
                return None
            return value

        def unescape(part: str|None):
            if part is None:
                return part
            return part.replace('\\"', '"').replace('\\\\', '\\')
        
        parts: list[str] = []
        while pos < len(text):
            char = text[pos]
            if char == ',':
                part = ''
                pos += 1
            elif char == '"':
                part = get_quoted_part(pos)
            elif char == '{':
                raise NotImplementedBy("zut librabry", "parse sub arrays") #ROADMAP: see issue #15
            else:
                part = get_unquoted_part(pos)
            parts.append(unescape(part)) # type: ignore (part not None so unescape cannot be None)

        return parts

    return split(value[1:-1])

#endregion


#region Convert to strings

def get_pg_array_str(values: Iterable) -> str:
    """ Parse an Iterable into an array literal (using PostgreSQL syntax). """
    # See: https://www.postgresql.org/docs/current/arrays.html#ARRAYS-INPUT

    if values is None:
        return None
    
    escaped: list[str] = []
    for value in values:
        if value is None:
            value = "null"
        elif isinstance(value, (list,tuple)):
            value = get_pg_array_str(value)
        else:
            if not isinstance(value, str):
                value = str(value)
            if value.lower() == "null":
                value = f'"{value}"'
            elif ',' in value or '"' in value or '\\' in value or '{' in value or '}' in value:
                value = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
        escaped.append(value)

    return '{' + ','.join(escaped) + '}'


def get_visual_list_str(values: Iterable, *, separator = '|') -> str:
    target_str = ''

    for value in values:
        value = get_str(value)
        
        if separator in value:
            return encode_json(values)
        
        if not target_str:
            if value.startswith(('{', '[')):
                return encode_json(values) # avoid ambiguity with postgresql literal or with JSON dump
            target_str = value
        else:        
            target_str += f'{separator}{value}'
    
    return target_str


def get_visual_dict_str(values: Mapping, *, separator = '|'):    
    target_str = ''
    
    for key, value in values.items():
        key = get_str(key)
        value = get_str(value)
        
        if '=' in key or separator in key or '=' in value or separator in value:
            return encode_json(values)
        elif not target_str and key.startswith(('{', '[')):
            return encode_json(values) # avoid ambiguity with postgresql literal or with JSON dump
        
        target_str += (separator if target_str else '') + (f'{key}={value}' if value else key)

    return target_str


def get_str(value: Any, default: Callable[[Any],str] = str) -> str:
    if value is None:
        return ''
    elif isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (float,Decimal,int)):
        return get_number_str(value)
    elif isinstance(value, Mapping):
        return get_visual_dict_str(value)
    elif isinstance(value, (Sequence,Set)):
        return get_visual_list_str(value)
    else:
        return default(value)

#endregion


#region Flexible convert

T = TypeVar('T')

def convert(value: Any, to: type[T]|Callable[[Any],T], *, use_locale = True, max_decimals: int|None = None, reduce_decimals: int|Sequence[int]|bool = False, decimal_separator: Literal['.',',','detect'] = 'detect', list_separator = '|') -> T|None:
    if value is None:
        return None
    
    if isinstance(to, type):
        if isinstance(value, to):
            return value
        
        if issubclass(to, str):
            converted_value = get_str(value)
        
        elif issubclass(to, bool):
            converted_value = parse_bool(value)

        elif issubclass(to, float):
            converted_value = parse_float(value, decimal_separator=decimal_separator)

        elif issubclass(to, Decimal):
            converted_value = parse_decimal(value, max_decimals=max_decimals, reduce_decimals=reduce_decimals, decimal_separator=decimal_separator)
        
        elif issubclass(to, (datetime,time)):
            converted_value = parse_datetime(value, use_locale=use_locale)
        
        elif issubclass(to, date):
            converted_value = parse_date(value, use_locale=use_locale)

        elif issubclass(to, Mapping):
            converted_value = parse_dict(value, separator=list_separator)
        
        elif issubclass(to, (Sequence,Set)):
            converted_value = parse_list(value, separator=list_separator)
            if converted_value is not None:
                element_to = get_single_generic_argument(to)
                if element_to: # type: ignore
                    converted_value = [convert(element, element_to, max_decimals=max_decimals, reduce_decimals=reduce_decimals, use_locale=use_locale, list_separator=list_separator) for element in converted_value]
                
                if to != list:
                    converted_value = to(converted_value)  # type: ignore
    
    elif callable(to):
        converted_value = to(value) # type: ignore

    else:
        raise NotSupportedBy("zut library", f"convert type {type(value).__name__} to {to}")

    return converted_value # type: ignore

#endregion
