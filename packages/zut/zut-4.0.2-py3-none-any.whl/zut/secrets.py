"""
Definition and resolution of delayable secrets (specified with `file:`, `pass:` or `env:` prefixes) and other secret/password helpers.
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import Literal


#region Delayable secrets

@overload
def resolve_secret(spec: str|None, *, required: Literal[True]) -> str:
    ...

@overload
def resolve_secret(spec: str|None, *, required: Literal[False] = False) -> str|None:
    ...

def resolve_secret(spec: str|None, *, required = False) -> str|None:
    if spec is None:
        if required:
            raise ValueError("Missing required password")
        else:
            return None
    
    elif spec.startswith('file:'):
        path = Path(spec[len('file:'):])
        if path.exists():
            return path.read_text(encoding='utf-8')
        elif required:
            raise FileNotFoundError("Password file not found: '%s'" % path.absolute())
        else:
            return None
    
    elif spec.startswith('pass:'): # See https://www.passwordstore.org
        from zut.gpg import get_pass
        return get_pass(spec[len('pass:'):], required=required)
    
    elif spec.startswith('env:'):
        var = spec[len('env:'):]

        # Search in 'secrets' files
        path = Path.cwd().joinpath(f'secrets/{var.lower()}') # usefull during local development
        if path.exists():
            return path.read_text(encoding='utf-8')
        
        path = Path(f'/run/secrets/{var.lower()}') # usefull in Docker containers
        if path.exists():
            return path.read_text(encoding='utf-8')
        
        # Search in environment variables
        value = os.environ.get(var)
        if value:
            if value.startswith(('file:','pass:')):
                return resolve_secret(value, required=required)
            else:
                return value
        
        path = os.environ.get(f"{var}_{'file' if all(not str.upper(c) for c in var) else 'FILE'}")
        if path:
            return Path(path).read_text(encoding='utf-8')
        
        # Not found
        return None
    
    elif spec.startswith('value:'):
        return spec[len('value:'):]
    
    else:
        return spec


def is_secret_defined(spec: str|None) -> bool:
    if spec is None:
        return False
    
    elif spec.startswith('file:'):
        path = Path(spec[len('file:'):])
        return path.exists()
    
    elif spec.startswith('pass:'): # See https://www.passwordstore.org
        from zut.gpg import get_pass_path
        return get_pass_path(spec[len('pass:'):]).exists()
    
    elif spec.startswith('env:'):
        var = spec[len('env:'):]

        # Search in 'secrets' files
        path = Path.cwd().joinpath(f'secrets/{var.lower()}') # usefull during local development
        if path.exists():
            return True
        
        path = Path(f'/run/secrets/{var.lower()}') # usefull in Docker containers
        if path.exists():
            return True
        
        # Search in environment variables
        value = os.environ.get(var)
        if value:
            if value.startswith(('file:','pass:')):
                return is_secret_defined(value)
            else:
                return True
        
        path = os.environ.get(f"{var}_{'file' if all(not str.upper(c) for c in var) else 'FILE'}")
        if path:
            return True
        
        # Not found
        return False
    
    else:
        return True


class Secret(str):
    def __init__(self, spec: str, *, is_resolved = False):
        self.spec = spec
        self._is_resolved = is_resolved
        self._value = None
        super().__init__()
    
    def __str__(self):
        return self.get_value(required=True)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.spec})"

    @property
    def is_resolved(self):
        return self._is_resolved

    @overload
    def get_value(self, *, required: Literal[True]) -> str:
        ...

    @overload
    def get_value(self, *, required: Literal[False] = False) -> str|None:
        ...
        
    def get_value(self, *, required = False) -> str|None:
        if not self._is_resolved:
            self._value = resolve_secret(self.spec, required=required)
            self._is_resolved = True
        return self._value

#endregion


#region Random utils

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def get_random_string(length: int, *, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return "".join(secrets.choice(allowed_chars) for _ in range(length))

#endregion
