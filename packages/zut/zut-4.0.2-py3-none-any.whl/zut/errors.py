"""
Error classes.
"""
from __future__ import annotations

from http import HTTPStatus

try:
    from django.http import Http404 as _NotFoundBaseException
except ModuleNotFoundError:
    _NotFoundBaseException = Exception
    

class SimpleError(ValueError):
    """
    An error that should result to only an error message being printed on the console, without a stack trace.
    """


class InternalError(ValueError):
    """
    Mark a condition which should not happen, except in case of logical/algorithmic/programming error.
    """
    code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    reason = "Internal Error"

    def __init__(self, message: str|None = None):
        super().__init__(message if message else self.reason)


class NotFound(_NotFoundBaseException): # pyright: ignore[reportGeneralTypeIssues]
    code = HTTPStatus.NOT_FOUND.value
    reason = HTTPStatus.NOT_FOUND.phrase

    def __init__(self, message: str|None = None):
        super().__init__(message if message else self.reason)


class BadRequest(Exception):
    code = HTTPStatus.BAD_REQUEST.value
    reason = HTTPStatus.BAD_REQUEST.phrase

    def __init__(self, message: str|None = None):
        super().__init__(message if message else self.reason)


class SeveralFound(Exception):
    code = HTTPStatus.CONFLICT.value
    reason = "Several Found"

    def __init__(self, message: str|None = None):
        super().__init__(message if message else self.reason)


class NotImplementedBy(NotImplementedError):
    code = HTTPStatus.NOT_IMPLEMENTED.value
    reason = HTTPStatus.NOT_IMPLEMENTED.phrase

    def __init__(self, by: type|str, feature: str|None = None):
        self.by = by
        if not feature:
            import inspect
            feature = f"{inspect.stack()[1].function}()"
        self.feature = feature
        by_name = self.by.__name__ if isinstance(self.by, type) else self.by
        super().__init__(f"Not implemented by {by_name}: {self.feature}")


class NotSupportedBy(Exception):
    code = HTTPStatus.NOT_IMPLEMENTED.value
    reason = "Not Supported"

    def __init__(self, by: type|str, feature: str|None = None):
        self.by = by
        if not feature:
            import inspect
            feature = f"{inspect.stack()[1].function}()"
        self.feature = feature
        by_name = self.by.__name__ if isinstance(self.by, type) else self.by
        super().__init__(f"Not supported by {by_name}: {self.feature}")
