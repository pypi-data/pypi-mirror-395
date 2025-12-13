"""
Type and Python language utilities.
"""
from __future__ import annotations

import sys
from typing import Sequence, Set

#region Inspect types

def get_single_generic_argument(gentype: type[Sequence|Set]) -> type|None:
    if not isinstance(gentype, type):
        raise TypeError(f"Not a type variable: {gentype}")

    try:
        from types import GenericAlias
    except ImportError:
        # GenericAlias: was introducted in Python 3.9
        return None

    if isinstance(gentype, GenericAlias):
        from typing import get_args, get_origin
        type_args = get_args(gentype)
        gentype = get_origin(gentype)
        if len(type_args) != 1:
            raise ValueError(f"Only one generic type parameter may be used for {gentype}")
        return type_args[0]
    else:
        return None

#endregion


#region Polyfills

if sys.version_info >= (3, 8):
    from functools import cached_property

else:
    _NOT_FOUND = object()

    class cached_property:
        def __init__(self, func):
            self.func = func
            self.attrname = None
            self.__doc__ = func.__doc__

        def __set_name__(self, owner, name):
            if self.attrname is None:
                self.attrname = name
            elif name != self.attrname:
                raise TypeError(
                    "Cannot assign the same cached_property to two different names "
                    f"({self.attrname!r} and {name!r})."
                )

        def __get__(self, instance, owner=None):
            if instance is None:
                return self
            if self.attrname is None:
                raise TypeError(
                    "Cannot use cached_property instance without calling __set_name__ on it.")
            try:
                cache = instance.__dict__
            except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
                msg = (
                    f"No '__dict__' attribute on {type(instance).__name__!r} "
                    f"instance to cache {self.attrname!r} property."
                )
                raise TypeError(msg) from None
            val = cache.get(self.attrname, _NOT_FOUND)
            if val is _NOT_FOUND:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
            return val
                                        
__shortcuts__ = (cached_property,)

#endregion
