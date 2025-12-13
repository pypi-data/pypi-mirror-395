"""
Encoding helpers: skip UTF8 BOM, fix encoding issues for files opened with surrogateescape, etc.
"""
from __future__ import annotations

from io import UnsupportedOperation
from typing import IO

UTF8_BOM = '\ufeff'
UTF8_BOM_BINARY = UTF8_BOM.encode('utf-8')

SURROGATE_MIN_ORD = ord('\uDC80')
SURROGATE_MAX_ORD = ord('\uDCFF')


def skip_utf8_bom(fp: IO, encoding: str|None = None):
    """
    Skip UTF8 byte order mark, if any.
    - `fp`: open file pointer.
    - `encoding`: if given, do nothing unless encoding is utf-8 or alike.
    """
    if encoding and not encoding in {'utf8', 'utf-8', 'utf-8-sig'}:
        return False

    try:
        start_pos = fp.tell()
    except UnsupportedOperation: # e.g. empty file
        start_pos = 0

    try:
        data = fp.read(1)
    except UnsupportedOperation: # e.g. empty file
        return False
    
    if isinstance(data, str): # text mode
        if len(data) >= 1 and data[0] == UTF8_BOM:
            return True
        
    elif isinstance(data, bytes): # binary mode
        if len(data) >= 1 and data[0] == UTF8_BOM_BINARY[0]:
            data += fp.read(2) # type: ignore (data bytes => fp reads bytes)
            if data[0:3] == UTF8_BOM_BINARY:
                return True
    
    fp.seek(start_pos)
    return False


def fix_utf8_surrogateescape(text: str, potential_encoding = 'cp1252') -> tuple[str,bool]:
    """
    Fix potential encoding issues for files opened with `open('r', encoding='utf-8', errors='surrogateescape')`.
    """
    fixed = False
    for c in text:
        c_ord = ord(c)
        if c_ord >= SURROGATE_MIN_ORD and c_ord <= SURROGATE_MAX_ORD:
            fixed = True
            break

    if not fixed:
        return text, False
    
    return text.encode('utf-8', 'surrogateescape').decode(potential_encoding, 'replace'), fixed


def fix_restricted_xml_control_characters(text: str, replace = '?'):
    """
    Replace invalid XML control characters. See: https://www.w3.org/TR/xml11/#charsets.
    """
    if text is None:
        return None
    
    replaced_line = ''
    for c in text:
        n = ord(c)
        if (n >= 0x01 and n <= 0x08) or (n >= 0x0B and n <= 0x0C) or (n >= 0x0E and n <= 0x1F) or (n >= 0x7F and n <= 0x84) or (n >= 0x86 and n <= 0x9F):
            c = replace
        replaced_line += c
    return replaced_line
