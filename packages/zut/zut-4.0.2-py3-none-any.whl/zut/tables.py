"""
General-purpose utilities for tabular data: Column class, tabulate functions (including a polyfill if necessary).
"""
from __future__ import annotations

import builtins
import os
import re
import sys
from contextlib import nullcontext
from typing import IO, TYPE_CHECKING, Any, Callable, Mapping

if TYPE_CHECKING:
    from typing import Iterable, Literal, Sequence


#region Column and column types

_re_type_fullspec = re.compile(r'^(?P<type_spec>.+)\(\s*(?P<precision>\d+)\s*(?:,\s*(?P<scale>\d+)\s*)?\)\s*$')


class Column:
    """
    Column name with details, used in databases and CSV files.
    """
    name: str
    """ Name of the column. """

    type: type|None
    """ Python type of the column. """

    type_spec: str|None # pyright: ignore[reportRedeclaration]
    """ Type specification in the source or destination system (typically a database engine), without precision and scale (see property `type_fullspec` to include precision and scale). """

    type_fullspec: str|None # pyright: ignore[reportRedeclaration]
    """ Type specification in the source or destination system (typically a database engine), including precision and scale (see property `type_spec` to not include precision and scale). """

    precision: int|None
    """ Max length for character types, max number of digits for decimal type. """

    scale: int|None
    """ Number of decimal digits for decimal type. """

    not_null: bool|None
    """ Indicate whether the column has a NOT NULL contraint. """

    primary_key: bool|None
    """ Indicate whether the column is part of the primary key. """

    identity: bool|None
    """ Indicate whether the column is an identity column. """

    default: Any|None
    """ Default value. Use `now` or `now()` for the current timestamp in the default timezone. Use `sql:...` to use direct sql. """

    converter: Callable[[Any],Any]|Any|None
    """ A converter callable, or a constant value. """

    def __init__(self, name: str, type: type|str|None = None, precision: int|None = None, scale: int|None = None, *, type_spec: str|None = None, not_null: bool|None = None, primary_key: bool|None = None, identity: bool|None = None, default: Any|None = None, converter: Callable[[Any],Any]|Any|None = None):
        self.name = name

        self.type = None
        self._type_spec = None
        self.precision = precision
        self.scale = scale
        self.not_null = not_null
        self.primary_key = primary_key
        self.identity = identity
        self.default = default
        self.converter = converter

        if type is not None:
            if isinstance(type, builtins.type):
                self.type = type
            elif isinstance(type, str):
                if type_spec is not None:
                    raise ValueError("Cannot use 'type' argument as a string: argument 'type_spec' also given")
                type_spec = type
            else:
                raise TypeError("Invalid type for 'type': %s" % type)
            
        if type_spec is not None:
            if '(' in type_spec:
                self.type_fullspec = type_spec
            else:
                self.type_spec = type_spec

        if precision is not None: # otherwise might override self.precision assigned in type_fullspec setter
            if self.precision is not None:
                if self.precision != precision:
                    raise ValueError("Inconsistent precision '%s' with type specification '%s'" % (precision, type_spec))
            self.precision = precision
        
        if scale is not None: # otherwise might override self.scale assigned in type_fullspec setter
            if self.scale is not None:
                if self.scale != scale:
                    raise ValueError("Inconsistent scale '%s' with type specification '%s'" % (scale, type_spec))
            self.scale = scale
    
    @property
    def type_spec(self) -> str|None:
        return self._type_spec
    
    @type_spec.setter
    def type_spec(self, value: str|None):
        if value is not None and '(' in value:
            raise ValueError("Property 'type_spec' cannot contain precision and scale")
        self._type_spec = value

    @property
    def type_fullspec(self) -> str|None:
        result = self._type_spec
        if result is not None and self.precision is not None:
            result += f'({self.precision}'
            if self.scale is not None:
                result += f',{self.scale}'
            result += ')'
        return result
    
    @type_fullspec.setter
    def type_fullspec(self, value: str|None):
        self._type_spec, self.precision, self.scale = parse_type_spec(value)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        result = f'Column({self.name}'
        if self.type is not None:
            result += f',type={self.type}'
        if self.type_spec is not None:
            result += f',type_spec={self.type_spec}'
        if self.precision is not None:
            result += f',precision={self.precision}'
        if self.scale is not None:
            result += f',scale={self.scale}'
        if self.not_null is not None:
            result += f',not_null={self.not_null}'
        if self.primary_key is not None:
            result += f',primary_key={self.primary_key}'
        if self.identity is not None:
            result += f',identity={self.identity}'
        if self.default is not None:
            result += f',default={self.default}'
        if self.converter is not None:
            result += f',converter={self.converter}'
        result += ')'
        return result

    def replace(self, *,
            name: str|None = None,
            type: str|type|None = None,
            type_spec: str|None = None,
            precision: int|None = None,
            scale: int|None = None,
            not_null: bool|None = None,
            primary_key: bool|None = None,
            identity: bool|None = None,
            default: Any|None = None,
            converter: Callable[[Any],Any]|Any|None = None) -> Column:
        
        return Column(
            name = name if name is not None else self.name,
            type = type if type is not None else self.type,
            type_spec = type_spec if type_spec is not None else self.type_spec,
            precision = precision if precision is not None else self.precision,
            scale = scale if scale is not None else self.scale,
            not_null = not_null if not_null is not None else self.not_null,
            primary_key = primary_key if primary_key is not None else self.primary_key,
            identity = identity if identity is not None else self.identity,
            default = default if default is not None else self.default,
            converter = converter if converter is not None else self.converter,
        )


def parse_type_spec(fullspec: str|None) -> tuple[str|None, int|None, int|None]:
    """
    Split a type full specification (with potential precision and scale) into a type spec, precision and scale.
    """
    type_spec = None
    precision = None
    scale = None

    if fullspec is not None:
        m = _re_type_fullspec.match(fullspec)
        if m:
            type_spec = m['type_spec'].strip().lower()
            precision = int(m['precision'])
            if m['scale']:
                scale = int(m['scale'])
        else:
            type_spec = fullspec.strip().lower()
        if type_spec == '':
            type_spec = None

    return type_spec, precision, scale

#endregion


#region Tabulate (including a polyfill if necessary)

try:
    from tabulate import tabulate  # type: ignore

except ModuleNotFoundError:
    def tabulate(tabular_data: Iterable[Iterable|Mapping], headers: Sequence[str]|Literal['keys']|None = None):
        """
        Emulate a basic _tabulate_ function in case the original _tabulate_ package (developped by Sergey Astanin) is not available as a dependency.

        Original package: https://pypi.org/project/tabulate/.
        """
        # Compute headers and header widths
        if headers:
            if headers == 'keys':
                first_row = next(iter(tabular_data), None)
                if not isinstance(first_row, Mapping):
                    raise ValueError(f"First row must be a dict, got {type(first_row).__name__}")
                headers = [key for key in first_row]
            
            header_widths = [len(header) for header in headers]
            for row in tabular_data:                
                if isinstance(row, Mapping):
                    row = [row.get(header) for header in headers]
                for i, value in enumerate(row):
                    if i < len(header_widths):
                        header_widths[i] = max(header_widths[i], len(str(value) if value is not None else ''))
        else:
            header_widths = []
            for row in tabular_data:                
                if isinstance(row, Mapping):
                    raise ValueError("Cannot use dict rows without headers. Specify headers='keys' to use keys of the first dict as headers.")
                for i, value in enumerate(row):
                    if i >= len(header_widths):
                        header_widths += [0] * (len(header_widths) - i + 1)
                    header_widths[i] = max(header_widths[i], len(str(value) if value is not None else ''))

        # Prepare format string
        fmt = '  '.join(f'{{:{w}}}' for w in header_widths)
        
        # Prepare output
        output = []
        if headers:
            output.append(fmt.format(*headers))
            output.append(fmt.format(*['-' * w for w in header_widths]))

        for row in tabular_data:           
            if isinstance(row, Mapping):
                if not headers:
                    raise ValueError("Cannot use dict rows without headers. Specify headers='keys' to use keys of the first dict as headers.")
                row = [row.get(header) for header in headers]
            output.append(fmt.format(*(str(v) if v is not None else '' for v in row)))

        return '\n'.join(output)


def dump_tabulate(data: Any, headers: Sequence[str|Column]|dict[str,Any]|None = None, *, file: str|os.PathLike|IO[str] = sys.stdout):
    if headers is None or headers == 'keys':
        _headers = 'keys'
    else:
        _headers = [str(header) if not isinstance(header, str) else header for header in headers]

    if _headers != 'keys':
        data = [[elem.get(key, None) for key in _headers] if isinstance(elem, dict) else elem for elem in data]
    
    text = tabulate(data, _headers)
    with open(file, 'w', encoding='utf-8') if isinstance(file, (str,os.PathLike)) else nullcontext(file) as file:
        file.write(text) # type: ignore
        file.write('\n') # type: ignore

#endregion
