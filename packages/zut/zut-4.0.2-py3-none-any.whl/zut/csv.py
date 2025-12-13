"""
Write and read CSV tables.
"""
from __future__ import annotations

import csv
import json
import logging
import os
import sys
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field
from datetime import datetime, time, tzinfo
from decimal import Decimal
from enum import Enum, Flag
from io import SEEK_END, StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO, TYPE_CHECKING, Any, Callable, ClassVar, Iterable, Mapping, Sequence, Set, overload

from zut.time import is_iso_datetime, make_aware, make_naive, parse_tz
from zut.errors import InternalError
from zut.tables import Column, dump_tabulate

if TYPE_CHECKING:
    from typing import Literal

    Converter = Callable[[Any],Any]|Any


#region High-level wrapper functions

def dump_csv(data: Any, file: str|os.PathLike|IO[str], headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, append = False, delay = False, check_newline_on_append: bool|None = None, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|str|None = None, archivate: bool|str|os.PathLike|None = None):
    """
    :param tz: If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone.
    """
    with CsvWriter(file, headers, append=append, delay=delay, check_newline_on_append=check_newline_on_append, fmt=fmt, tz=tz, archivate=archivate) as writer:
        for row in data:
            writer.writerow(row)
        return writer.rowcount


def dump_csv_or_tabulate(data: Any, file: str|os.PathLike|IO[str]|None, headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, tabulate_headers: Sequence[str]|None = None, append = False, delay = False, check_newline_on_append: bool|None = None, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|str|None = None):
    """
    Dump to CSV if `file` is a path or tabulate to stdout or stderr if `file` is stdout or stderr.

    Usefull for flexible `--out` arguments of command-line applications.
    """
    if file is None:
        pass # Do nothing
    elif file in {sys.stdout, sys.stderr}:
        dump_tabulate(data, file=file, headers=tabulate_headers if tabulate_headers is not None else headers)
    else:
        return dump_csv(data, file, headers, append=append, delay=delay, check_newline_on_append=check_newline_on_append, fmt=fmt, tz=tz)


@contextmanager
def dump_csv_temp(data: Any, headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, append = False, delay = False, check_newline_on_append: bool|None = None, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|str|None = None):
    """
    :param tz: If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone.
    """    
    temp_writer = None
    try:
        with CsvWriter(headers=headers, append=append, delay=delay, check_newline_on_append=check_newline_on_append, fmt=fmt, tz=tz) as temp_writer:
            for row in data:
                temp_writer.writerow(row)
 
        yield temp_writer.path
    finally:
        if temp_writer is not None:
            temp_writer.path.unlink()


def load_csv(file: str|os.PathLike|IO[str], headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, no_headers = False, tz: tzinfo|Literal['local','utc']|None = None, delimiter: str|None = None, encoding = 'utf-8-sig') -> list[dict[str,Any]]:
    """
    :param tz: If set, naive datetimes read from the CSV file are considered as aware datetimes in the given timezone.
    """
    with CsvReader(file, headers, no_headers=no_headers, tz=tz, delimiter=delimiter, encoding=encoding) as reader:
        return [data for data in reader.iter_dicts()]

#endregion


#region Write CSV

class CsvFormat:
    """
    Determine how CSV values are formatted.
    - `PG`, `VISUAL` and `JSON` are invariant of the locale. They all use `,` as the comma separator. They differ on the way they handle lists and dicts.
    - `EXCEL` tries to make the CSV file directly openable on Excel. It depends on the locale.
    """
    def __init__(self, *, delimiter: str|Literal['locale'] = ',', decimal_separator: str|None = None, lists: Literal['pg','visual','json'] = 'pg', dicts: Literal['visual','json'] = 'json', enums: Literal['name','value'] = 'value', no_microsecond = False, no_scientific_notation = False, encoding: str = 'utf-8', use_local_tz_by_default = False):
        if delimiter == 'locale':
            from zut.locale import get_locale_decimal_separator
            delimiter = ';' if get_locale_decimal_separator() == ',' else ','        
        self.delimiter = delimiter

        if not decimal_separator:
            decimal_separator = ',' if delimiter == ';' else '.'
        self.decimal_separator = decimal_separator

        self.lists = lists
        self.dicts = dicts
        self.enums = enums
        self.no_microsecond = no_microsecond
        self.no_scientific_notation = no_scientific_notation
        self.encoding = encoding
        self.use_local_tz_by_default = use_local_tz_by_default

    @classmethod
    def parse(cls, value: CsvFormat|str|None) -> CsvFormat:
        if not value:
            # Get default
            fmt = os.environ.get('CSV_FORMAT')
            if fmt:
                return cls.parse(fmt)
            
            fmt = CsvWriter.default_format
            if fmt:
                return cls.parse(fmt)
            
            return CsvWriter.PG
        
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise TypeError(f"value: {type(value).__name__}")
                
        # Try by name
        attr_value = getattr(CsvWriter, value.upper(), None)
        if attr_value is not None and isinstance(attr_value, cls):
            return attr_value

        # Aliases        
        lower = value.lower()
        if lower in {'xls', 'xlsx'}:
            return CsvWriter.EXCEL
        elif lower in {'postgres', 'postgresql'}:
            return CsvWriter.PG

        raise ValueError(f"Unknown CSV format: {value}")


class CsvWriter:
    default_format: ClassVar[CsvFormat|str|None] = None
    default_check_newline_on_append: ClassVar[bool] = False

    PG = CsvFormat()
    """ Export lists as PostgreSQL array literals and dicts as JSON. """

    VISUAL = CsvFormat(lists='visual', dicts='visual', enums='name')
    """ Export lists and dicts as easily visuable strings when possible, otherwise as JSON. """

    JSON = CsvFormat(lists='json', dicts='json')
    """ Export lists and dicts as JSON. """

    EXCEL = CsvFormat(delimiter='locale', lists='visual', dicts='visual', enums='name', no_microsecond=True, no_scientific_notation=True, encoding='utf-8-sig', use_local_tz_by_default=True)
    """ Datetimes in local timezone, no microseconds, no scientific notation, visual lists and dicts. CSV delimiter and decimal separator depend on the locale. """

    def __init__(self, file: str|os.PathLike|IO[str]|None = None, headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, append = False, delay = False, check_newline_on_append: bool|None = None, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|str|None = None, archivate: bool|str|os.PathLike|None = None, delete_temp = True):
        """        
        :param tz: If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone.
        """
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__qualname__}")

        self.append = append
        self.check_newline_on_append = check_newline_on_append if check_newline_on_append is not None else self.__class__.default_check_newline_on_append

        self.delay = delay

        # Determine final CSV configuration settings
        self.fmt = CsvFormat.parse(fmt)

        self.is_temp = False
        self.delete_temp = delete_temp
        
        # Prepare file and name depending on the passed file
        self._archivate = archivate
        self._file_or_path: Path|Literal['<temp>']|IO[str]
        self._name: str
        if file is None or file == '<temp>':
            self._file_or_path = '<temp>'
            self._name = '<temp>'
            self.is_temp = True
        elif isinstance(file, (str, os.PathLike)):
            self._file_or_path = Path(file) if not isinstance(file, Path) else file
            self._name = self._file_or_path.name
        else:
            self._file_or_path = file
            self._name = getattr(file, 'name', f'<{type(file).__name__}>')

        self._file_manager: AbstractContextManager[IO[str]]|None = None
        self._file: IO[str]|None = None
        
        # Initialize usefull variables
        self._manager = CsvReadWriteManager(headers, is_reading=False, tz=tz)
        self._rowcount = 0
        self._actually_written_rowcount = 0
        self._missing_keys: list[str] = []
        self._additional_keys: list[str] = []
        self._delayed_rows: list[Mapping[str,Any]|Sequence[Any]] = []

    def close(self):
        self.flush()
        if self._file_manager:
            self._file_manager.__exit__(None, None, None)
            if self.is_temp and self.delete_temp:
                os.unlink(self.path)

    def __enter__(self):
        if self._file is not None:
            raise ValueError(f"Context manager {type(self).__name__} already entered")

        examined: ExaminedCsvFile|None = None
        if self._file_or_path == '<temp>':
            self._file_manager = NamedTemporaryFile('w', encoding=self.fmt.encoding, newline='', suffix='.csv', delete=False).__enter__()
            self._file = self._file_manager.file
            self._file_or_path = Path(self._file_manager.name)
        elif isinstance(self._file_or_path, Path):
            if self.append:
                if self.path.exists():
                    examined = examine_csv_file(self.path, encoding=self.fmt.encoding, need_ends_with_newline=self.check_newline_on_append)
            else:
                if self._archivate:
                    from zut.paths import archivate_file
                    archivate_file(self.path, self._archivate, missing_ok=True)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._file_manager = open(self.path, 'a' if self.append else 'w', encoding=self.fmt.encoding, newline='')
            self._file = self._file_manager.__enter__()
        else:
            self._file_manager = None # managed externally
            self._file = self._file_or_path
            if self.append:
                examined = examine_csv_file(self._file, need_ends_with_newline=self.check_newline_on_append)
                self._file.seek(0, SEEK_END)

        if self.append and examined is not None:
            self._manager.set_existing_file_headers(examined.headers, self.name)
            if len(examined.headers) >= 2:
                self.delimiter = examined.delimiter
            if self.check_newline_on_append and not examined.ends_with_newline:
                self._file.write('\n')

        if self._manager.headers:
            self._prepare_headers()

        return self
    
    def __exit__(self, *exc_info):
        self.close()

    @property
    def file(self) -> IO[str]:
        if self._file is None:
            raise ValueError(f"Context manager {type(self).__name__} not entered")        
        return self._file

    @property
    def path(self) -> Path:
        if not isinstance(self._file_or_path, Path):
            raise ValueError("Not writing to a path")
        return self._file_or_path

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def headers(self) -> list[str]:
        if not self._manager.headers:
            raise ValueError("Headers not set")
        return self._manager.headers
    
    @headers.setter
    def headers(self, headers: Iterable[str|Column]):
        if self._manager.headers:
            raise ValueError("Headers already set")
        self._manager._columns = [Column(header) if not isinstance(header, Column) else header for header in headers]
        self._manager._headers_invalidated = True
        self._prepare_headers()

    @property
    def rowcount(self):
        return self._rowcount

    def _prepare_headers(self):
        self._manager.prepare()
        if not self.append or not self._manager.file_headers:
            self._actual_write(self.headers)
        self.flush()

    def flush(self):
        if not self._delayed_rows:
            return
        
        if not self._manager.headers:
            self.headers = get_headers_from_rows(self._delayed_rows)
            return # NOTE: _prepare_headers (including _actual_write and then another flush) will be called from headers.setter
        
        for row in self._delayed_rows:
            self._actually_written_rowcount += 1
            self._actual_write(row)
        self._delayed_rows.clear()
        self.delay = False

    def writerow(self, row: Mapping[str,Any]|Sequence[Any]):
        self._rowcount += 1
        if self.delay:
            self._delayed_rows.append(row)
        else:
            self._actually_written_rowcount += 1
            self._actual_write(row)
    
    def _actual_write(self, row: Mapping[str,Any]|Sequence[Any]):
        if isinstance(row, Mapping):
            row = self._dict_to_row(row)
        else:
            row_dict = getattr(row, '__dict__', None)
            if row_dict is not None:
                row = self._dict_to_row(row_dict)
            else:
                self._check_sequence_length(row)

        row = self._manager.reindex_and_convert_values(row)
        
        row = format_csv_row(row, fmt=self.fmt, tz=self._manager.tz, as_string=True)
        self.file.write(row)
        self.file.write('\n')
        self.file.flush()

    def _check_sequence_length(self, row: Sequence[Any]):
        if not self._manager.headers:
            return
        
        if len(row) != len(self._manager.headers):
            self._logger.warning(f"Invalid length for row {self._actually_written_rowcount}: {len(row)} (headers length: {len(self._manager.headers)})")
    
    def _dict_to_row(self, row: Mapping[str,Any]):
        if not self._manager.headers:
            self.headers = [str(key) for key in row] # NOTE: _prepare_headers (including _actual_write) will be called from headers.setter
        
        actual_row = []
        missing_keys = []
        for header in self.headers:
            if header in row:
                value = row[header]
            else:
                value = None
                if not self.delay and not header in self._missing_keys: # (if we have been delaying, no reason to warn: we actually expect to have missing keys, that's why we waited for more dicts to come)
                    missing_keys.append(header)
            actual_row.append(value)

        if missing_keys:
            self._logger.warning(f"Missing key(s) from row {self._actually_written_rowcount}: {', '.join(missing_keys)} (file: {self.name}). Rows will be appended with null values for these columns.")
            for key in missing_keys:
                self._missing_keys.append(key)

        for key in self._additional_keys:
            actual_row.append(row.get(key))

        additional_keys = []
        for key in row:
            if not key in self.headers and not key in self._additional_keys:
                actual_row.append(row[key])
                additional_keys.append(key)

        if additional_keys:
            self._logger.warning(f"Additional key(s) from row {self._actually_written_rowcount}: {', '.join(additional_keys)} (file: {self.name}). Rows will be appended with additional values but without column names.")
            for key in additional_keys:
                self._additional_keys.append(key)

        return actual_row


@overload
def format_csv_row(row: Iterable, *, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|None = None, as_string: Literal[False] = ...) -> list[Any]:
    ...

@overload
def format_csv_row(row: Iterable, *, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|None = None, as_string: Literal[True]) -> str:
    ...

def format_csv_row(row: Iterable, *, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|None = None, as_string = False) -> list[Any]|str:
    """
    :param tz: If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone.
    """    
    if fmt is None or not isinstance(fmt, CsvFormat):
        fmt = CsvFormat.parse(fmt)
    
    if as_string:
        target = ''
    else:
        target = []

    first = True
    for value in row:
        formatted_value = format_csv_value(value, fmt=fmt, tz=tz)
        if as_string:
            if first:
                first = False
            else:
                target += fmt.delimiter # type: ignore (as_string => target is a string)
            target += escape_csv_value(formatted_value, delimiter=fmt.delimiter)
        else:
            target.append(formatted_value) # type: ignore (not as_string => target is a list)
    return target


def format_csv_value(value, *, fmt: CsvFormat|str|None = None, tz: tzinfo|Literal['local','utc']|None = None):
    """
    Format a CSV value.

    :param value:               Value to format.
    :param decimal_separator:   Decimal separator to use.
    :param tz:                  If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone.
    :param no_microseconds:     If true, output datetimes have no microseconds. They have hours, minutes and seconds.
    :param visual:              If true, the following changes are made in the output format:
        - Enums: use name instead of value
        - List: use 'A|B|C' format instead of postgresql array literal or json format
        - Enum names are used instead of enum values, and lists and dicts will be e
    """
    if fmt is None or not isinstance(fmt, CsvFormat):
        fmt = CsvFormat.parse(fmt)

    if not tz and fmt.use_local_tz_by_default:
        tz = 'local'

    def format_value(value, *, root):    
        if value is None:
            return None

        if tz:
            if isinstance(value, str):
                if is_iso_datetime(value):
                    value = datetime.fromisoformat(value)

        if isinstance(value, str):
            return value

        elif isinstance(value, (Enum,Flag)):
            return value.name if fmt.enums == 'name' else value.value
            
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        
        elif isinstance(value, int):
            return value
        
        elif isinstance(value, (float,Decimal)):
            from zut.convert import get_number_str
            str_value = get_number_str(value, no_scientific_notation=True if fmt.no_scientific_notation else False)

            if fmt.decimal_separator != '.':
                return str_value.replace('.', fmt.decimal_separator)

            return str_value
        
        elif isinstance(value, (datetime,time)):
            if tz:
                if value.tzinfo and isinstance(value, datetime): # make the datetime naive if it is not already
                    value = make_naive(value, tz)
            if fmt.no_microsecond:
                return value.replace(microsecond=0)
            return value
        
        elif isinstance(value, Mapping):
            if root and fmt.dicts == 'visual':
                from zut.convert import get_visual_dict_str
                return get_visual_dict_str(value)
            
            else:
                from zut.json import ExtendedJSONEncoder
                return json.dumps(value, ensure_ascii=False, cls=ExtendedJSONEncoder)

        elif isinstance(value, (Sequence,Set)):
            if root and fmt.lists == 'visual':
                if len(value) == 1:
                    return format(next(iter(value)))
                
                from zut.convert import get_visual_list_str
                return get_visual_list_str(value)
        
            elif fmt.lists == 'pg':
                from zut.convert import get_pg_array_str
                return get_pg_array_str(value)
            
            else:
                from zut.json import ExtendedJSONEncoder
                return json.dumps(value, ensure_ascii=False, cls=ExtendedJSONEncoder)
                
        else:
            return value

    return format_value(value, root=True)


def escape_csv_value(value, *, delimiter = ',', quotechar = '"', nullval: str|None = None):
    if value is None:    
        return nullval if nullval is not None else ''
    if not isinstance(value, str):
        value = str(value)
    if value == '':
        return f'{quotechar}{quotechar}'

    need_escape = False
    result = ''
    for c in value:
        if c == delimiter:
            result += c
            need_escape = True
        elif c == quotechar:
            result += f'{c}{c}'
            need_escape = True
        elif c == '\n' or c == '\r':
            result += c
            need_escape = True
        else:
            result += c

    if need_escape:
        result = f'{quotechar}{result}{quotechar}'
    else:
        result = result

    return result

#endregion


#region Read CSV

class CsvReader:
    def __init__(self, file: str|os.PathLike|IO[str], headers: Sequence[str|Column]|dict[str,Converter]|None = None, *, no_headers = False, tz: tzinfo|Literal['local','utc']|None = None, delimiter: str|None = None, encoding = 'utf-8-sig', null_if_empty = True):
        """
        :param tz: If set, naive datetimes read from the CSV file are considered as aware datetimes in the given timezone.
        """        
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__qualname__}")

        self._file_or_path: Path|IO[str]
        self._name: str
        if isinstance(file, (str, os.PathLike)):
            self._file_or_path  = Path(file) if not isinstance(file, Path) else file
            self._name = self._file_or_path.name
        else:
            self._file_or_path = file
            self._name = getattr(file, 'name', f'<{type(file).__name__}>')

        self._file_manager: AbstractContextManager[IO[str]]|None = None
        self._file: IO[str]|None = None

        self._manager = CsvReadWriteManager(headers, is_reading=True, no_headers=no_headers, tz=tz)
        self._require_headers_read = False if no_headers else True
        self.encoding = encoding
        self.delimiter = delimiter
        self.null_if_empty = null_if_empty

        self._actual_reader = None
        self._reader_distinguishes_null_from_empty = None
        self._rowcount = 0

    def close(self):
        if self._file_manager:
            self._file_manager.__exit__(None, None, None)

    def __enter__(self):
        if self._file is not None:
            raise ValueError(f"Context manager {type(self).__name__} already entered")

        if isinstance(self._file_or_path, Path):
            self._file_manager = open(self.path, 'r', encoding=self.encoding, newline='')
            self._file = self._file_manager.__enter__()
        else:
            self._file_manager = None # managed externally
            self._file = self._file_or_path
        
        return self
    
    def __exit__(self, *exc_info):
        self.close()

    @property
    def file(self) -> IO[str]:
        if self._file is None:
            raise ValueError(f"Context manager {type(self).__name__} not entered")   
        return self._file

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> Path:
        if not isinstance(self._file_or_path, Path):
            raise ValueError("Not reading from a path")
        return self._file_or_path
    
    @property
    def rowcount(self) -> int:
        """ Number of rows read for now. """
        return self._rowcount
    
    @property
    def actual_reader(self):
        if self._actual_reader is None:
            if self.delimiter is None:
                self.delimiter = examine_csv_file(self.file, encoding=self.encoding).delimiter

            if sys.version_info >= (3, 13) and self.null_if_empty: # NOTE: QUOTE_NOTNULL does not seem to work correctly on Python 3.12
                self._actual_reader = csv.reader(self.file, delimiter=self.delimiter, quoting=csv.QUOTE_NOTNULL)
                self._reader_distinguishes_null_from_empty = True
            else:
                self._actual_reader = csv.reader(self.file, delimiter=self.delimiter)
                self._reader_distinguishes_null_from_empty = False
        
        return self._actual_reader
    
    def _ensure_headers_read(self):
        if not self._require_headers_read:
            return # already read
        
        file_headers = next(self.actual_reader)
        self._manager.set_existing_file_headers(file_headers, self.name)
        self._manager.prepare()
        self._require_headers_read = False
    
    @property
    def file_headers(self) -> list[str]|None:
        self._ensure_headers_read()
        return self._manager.file_headers
    
    @property
    def headers(self) -> list[str]:
        self._ensure_headers_read()
        return self._manager.headers # type: ignore (cannot be None)
    
    def __iter__(self):
        return self

    def __next__(self):
        self._ensure_headers_read()
        row = next(self.actual_reader)
        self._rowcount += 1
        return self._manager.reindex_and_convert_values(row)
    
    def iter_dicts(self):
        for row in self:
            yield self._row_to_dict(row)

    def _row_to_dict(self, row: Sequence[Any]) -> dict[str,Any]:
        if len(row) < len(self.headers):
            missing_columns = self.headers[len(row):]
            self._logger.warning(f"Missing column{'s' if len(missing_columns) > 1 else ''} in row {self._rowcount}: {', '.join(missing_columns)} (file: {self.name}). Row will contain null values for {'these columns' if len(missing_columns) > 1 else 'this column'}.")

        elif len(row) > len(self.headers):
            if len(row) > len(self.headers)+1:
                message = f"Additional columns in row {self._rowcount}: columns n°{len(self.headers)+1} to {len(row)} (file: {self.name}). Row will not contain a value for these columns."
            else:
                message = f"Additional column in row {self._rowcount}: column n°{len(self.headers)+1} (file: {self.name}). Row will not contain a value for this column."
            self._logger.warning(message)

        def convert(value: str):
            if value == '' and self.null_if_empty and self._reader_distinguishes_null_from_empty:
                return None
            else:
                return value
        
        return {header: convert(row[i]) if i < len(row) else None for i, header in enumerate(self.headers)}
    

def get_csv_columns(file: str|os.PathLike|IO[str], *, encoding = 'utf-8-sig', quotechar = '"'):
    return examine_csv_file(file, encoding=encoding, quotechar=quotechar, need_ends_with_newline=False).headers


def examine_csv_file(file: str|os.PathLike|IO[str], *, encoding = 'utf-8-sig', quotechar = '"', need_ends_with_newline = True) -> ExaminedCsvFile:
    """
    Returns `(headers, delimiter, newline, ends_with_newline)`
    """
    if isinstance(file, (str,os.PathLike)):
        if not os.path.exists(file):
            raise FileNotFoundError(f"CSV file not found: {file}")
        initial_pos = None
    else:
        initial_pos = file.tell()
        file.seek(0)

    first_line_io = StringIO()
    newline = '\n'
    ends_with_newline = None

    with open(file, 'r', encoding=encoding, newline='') if isinstance(file, (str,os.PathLike)) else nullcontext(file) as fp:
        first_line_ended = False
        buf_size = 65536
        while True:
            chunk = fp.read(buf_size)
            if not chunk:
                break

            if not first_line_ended:
                pos = chunk.find('\n')
                if pos >= 0:
                    if pos > 0 and chunk[pos-1] == '\r':
                        newline = '\r\n'
                    else:
                        newline = '\n'
                else:
                    pos = chunk.find('\r')
                    if pos >= 0:
                        newline = '\r'

                if pos >= 0:
                    first_line_io.write(chunk[:pos])
                    first_line_ended = True
                    if not need_ends_with_newline:
                        break
                else:
                    first_line_io.write(chunk)

            if need_ends_with_newline:
                ends_with_newline = chunk[-1] == '\n'

    if first_line_io.tell() == 0:
        return ExaminedCsvFile() # No content

    # Guess the delimiter
    first_line_str = first_line_io.getvalue()

    comma_count = first_line_str.count(',')
    semicolon_count = first_line_str.count(';')
    if semicolon_count > comma_count:
        delimiter = ';'
    elif comma_count > 0:
        delimiter = ','
    else:
        delimiter = '.'

    # Retrieve column names
    first_line_io.seek(0)
    reader = csv.reader(first_line_io, delimiter=delimiter, quotechar=quotechar, doublequote=True)
    columns = next(reader)

    # Ensure we move back the fp were it was
    if not isinstance(file, (str,os.PathLike))and initial_pos is not None:
        file.seek(initial_pos)

    return ExaminedCsvFile(columns, delimiter, newline, ends_with_newline)


@dataclass
class ExaminedCsvFile:
    headers: list[str] = field(default_factory=list)
    delimiter: str = ','
    newline: str = '\n'
    ends_with_newline: bool|None = None

#endregion


#region Helpers

class CsvReadWriteManager:
    def __init__(self, headers: Sequence[str|Column]|dict[str,Converter]|None, *, is_reading: bool, no_headers = False, tz: tzinfo|Literal['local','utc']|str|None = None):
        """
        Compare given headers with actual headers in a file, return reorder list if needed.

        Given headers may contain a wildcard character ('*'). If so, the headers object is completed with actual headers from the file.

        :param no_headers: Indicate that the existing file will be considered as having no headers.
        :param tz: If set, aware datetimes are written to the CSV file as naive datetimes in the given timezone, and naive datetimes read from the CSV files (after converters are applied) are considered as aware datetimes in the given timezone.
        """
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__qualname__}")

        self._columns: list[Column]|None
        if not headers:
            self._columns = None
        elif isinstance(headers, dict):
            self._columns = [Column(header, converter=converter) for header, converter in headers.items()]
        else:
            self._columns = [Column(header) if not isinstance(header, Column) else header for header in headers]

        self._headers: list[str]|None = None
        self._headers_invalidated = True

        self.file_headers: list[str]|None = None
        self._name: str|None = None

        self._no_headers = no_headers
        if self._no_headers:
            if not self._columns:
                raise ValueError("Argument `headers` is required when the existing file has no headers")
            elif any(column.name == '*' for column in self._columns):
                raise ValueError("Argument `headers` cannot contain `*` when the existing file has no headers")

        self.tz: tzinfo|Literal['local']|None
        if not tz:
            self.tz = None
        else:
            if tz == 'local' or tz == 'localtime':
                self.tz = 'local'
            elif isinstance(tz, tzinfo):
                self.tz = tz
            else:
                self.tz = parse_tz(tz)

        self._is_reading = is_reading
        self._empty_to_null = self._is_reading and sys.version_info < (3, 13) # NOTE: QUOTE_NOTNULL does not seem to work correctly on Python 3.12
        self._reindex: list[int|None]|None = None

    @property
    def is_reading(self):
        return self._is_reading

    @property
    def is_writing(self):
        return not self._is_reading

    @property
    def headers(self) -> list[str]|None:
        if self._headers_invalidated:
            self._headers = [column.name for column in self._columns] if self._columns is not None else None
            self._headers_invalidated = False
        return self._headers

    @property
    def columns(self) -> list[Column]|None:
        return self._columns

    def set_existing_file_headers(self, file_headers: list[str], name: str):
        self.file_headers = file_headers
        self._name = name
         
    def prepare(self):
        if not self.file_headers:
            return
        
        # Remove UTF-8 BOM if any
        if len(self.file_headers) >= 1 and len(self.file_headers[0]) >= 1 and self.file_headers[0][0] == '\ufeff':
            self.file_headers[0] = self.file_headers[0][1:]

        if not self._columns:
            self._columns = [Column(column) for column in self.file_headers]
            self._headers_invalidated = True
            return
        
        if self.headers == self.file_headers:
            return # Nothing to do
        
        # Remove wildcard from given headers
        _columns = []
        wildcard_pos = None
        wildcard_column = None
        for pos, column in enumerate(self._columns):
            if column.name == '*':
                if wildcard_pos is not None:
                    raise ValueError("Headers cannot contain several `*` wildcards")
                wildcard_pos = pos
                wildcard_column = column
            else:
                _columns.append(column)
        self._columns = _columns
        self._headers_invalidated = True

        # Determine reindex from source to target  
        if self.headers is None:
            raise InternalError("headers is None")
        elif self.is_reading:
            source_headers = self.file_headers
            target_headers = self.headers
        else:
            source_headers = self.headers
            target_headers = self.file_headers
        
        source_indexes = {header: index for index, header in enumerate(source_headers)}
        self._reindex = []
        missing_in_source = []
        for pos, header in enumerate(target_headers):
            index = source_indexes.get(header)
            if index is None:
                missing_in_source.append(header)
            self._reindex.append(index)

        missing_in_target: dict[str,int] = {}
        for header, source_index in source_indexes.items():
            if not header in target_headers:
                missing_in_target[header] = source_index

        # Determine what to do in case of wildcard
        if self.is_reading:
            if wildcard_pos is not None:
                if wildcard_column is None:
                    raise InternalError('wildcard_column is None')
                if missing_in_target:
                    self._columns = self._columns[0:wildcard_pos] + list(wildcard_column.replace(name=name) for name in missing_in_target.keys()) + self._columns[wildcard_pos:]
                    self._headers_invalidated = True
                    self._reindex = self._reindex[0:wildcard_pos] + list(missing_in_target.values()) + self._reindex[wildcard_pos:]

                    # All headers read will be used thanks to the wildcard
                    missing_in_target.clear()
        else:
            if wildcard_pos is not None:
                # No warning if the existing file contains additional columns
                missing_in_source = None

        # Report warnings
        if missing_in_source:
            if self.is_reading:
                self._logger.warning(f"Missing header(s) in CSV file: {', '.join(missing_in_source)} (file: {self._name}). Rows will always contain null values for these columns.")
            else:
                self._logger.debug(f"Additional header(s) in existing CSV file: {', '.join(missing_in_source)} (file: {self._name}). Rows will be appended with a null value for these columns.")

        if missing_in_target:
            if self.is_reading:
                self._logger.debug(f"Additional header(s) in CSV file: {', '.join(missing_in_target.keys())} (file: {self._name}). Rows will not contain a value for these columns.")
            else:
                self._logger.warning(f"Missing header(s) in existing CSV file: {', '.join(missing_in_target.keys())} (file: {self._name}). Rows will be appended with additional values but without column names.")
                for source_index in missing_in_target.values():
                    self._reindex.append(source_index)

    def reindex_and_convert_values(self, row: Sequence[Any]) -> Sequence[Any]:
        if self._reindex is not None:
            row = [row[index] if index is not None and index < len(row) else None for index in self._reindex]

        for i in range(len(row)):
            value = row[i]
            must_assign = False

            if self.is_reading and self._empty_to_null:
                if value == '':
                    value = None
                    must_assign = True

            if value is not None and self._columns is not None and len(self._columns) > i:
                column = self._columns[i]
                if column.converter is not None:
                    if callable(column.converter):
                        newvalue = column.converter(value)
                    else:
                        newvalue = column.converter
                    
                    if newvalue != value:
                        value = newvalue
                        must_assign = True

            if self.is_reading:
                if isinstance(value, str):
                    if is_iso_datetime(value):
                        value = datetime.fromisoformat(value)
                        must_assign = True

                if self.tz and isinstance(value, datetime) and not value.tzinfo:
                    value = make_aware(value, self.tz)
                    must_assign = True

            if self.is_writing and self.tz and isinstance(value, datetime) and value.tzinfo:
                value = make_naive(value, self.tz)
                must_assign = True

            if must_assign:
                if not isinstance(row, list):
                    row = list(row)
                row[i] = value

        return row


def get_headers_from_rows(rows: Mapping[str,Any]|Sequence[Any]) -> list[str]:
    headers: list[str] = []

    def insert_header(header: str, following_keys: list[str]):
        # Try to keep the global order of headers: insert just before the first existing that we know is after the given header
        pos = len(headers)
        for key in following_keys:
            try:
                pos = headers.index(key)
                break
            except ValueError:
                continue
        headers.insert(pos, header)
        
    for row in rows:
        if not isinstance(row, Mapping):
            continue

        keys = list(row.keys())
        for i, key in enumerate(keys):
            if key in headers:
                continue                
            insert_header(key, keys[i+1:])

    return headers

#endregion
