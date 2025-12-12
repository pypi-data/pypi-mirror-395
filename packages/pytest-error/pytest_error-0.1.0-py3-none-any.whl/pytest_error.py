"""
Decorators for validating pytest tests that are expected to raise exceptions
----------
This module provide decorators that can be used to check that pytest tests raise
exceptions with expected characteristics. The decorators build off the pytest.raises
context manager, and also add support for validating raised error messages using
string (rather than the regular expressions).

Motivation:
* Validate error messages without needing to know regular expressions
* Quickly identify tests that examine error states
* Action code remains at the same indent level for tests that examine error states
----------
Decorator:
    error               - Checks a test raises an exception with expected characteristics

Aliases:
    error_with_notes    - Alias for @error(..., *, check_notes = True)
    error_no_format     - Alias for @error(..., *, format = False)
    error_no_message    - Alias for @error(exception_type, None)

Internal:
    _check_error    - Checks a function call raises an expected exception
    _check_test     - Checks a pytest test raises an expected exception
"""

from __future__ import annotations

import typing
from functools import wraps

import pytest

if typing.TYPE_CHECKING:
    import re
    from typing import Callable, Optional

    Match = str | re.Pattern[str]


#####
# Utilities
#####


def _check_error(
    # Function call
    func: Callable,
    func_args: tuple | list = (),
    func_kwargs: dict = {},
    # Pytest API
    exception_type: type | tuple[type] = Exception,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
    # pytest-error
    message: list[str] | tuple[str] = [],
    check_notes: bool = False,
) -> Exception:
    """
    Checks a function call generates an Exception with expected characteristics
    ----------
    _check_error(func)
    _check_error(func, func_args, func_kwargs)
    Checks that a function raises an Exception when called and returns the Exception.

    _check_error(..., exception_type)
    Checks that the raised exception matches the expected type (subclasses are
    considered matches). If a tuple, checks the exception matches at least one of the
    indicated types. Default is Exception.

    _check_error(..., match)
    If provided, a regular expression that must match either (1) the exception's string
    representation `str(exc)`, or (2) one of the exception's notes (if present). Consult
    the pytest.raises API for more details. Note that this argument is inherited from
    the pytest API, but the pytest-error package is more focused on the `message` input
    detailed below. Also note that `match` is *always* compared to the exception's
    __notes__, regardless of the status of the `check_notes` input.

    _check_error(..., check)
    If provided, a callable that will be called with the exception as a parameter (after
    checking the `exception_type` and `match` inputs). If the callable returns True,
    then the exception is considered a match. Otherwise, the exception is considered a
    failed match. Consult the pytest.raises API for more details.

    _check_error(..., message)
    _check_error(..., message, check_notes=True)
    A list/tuple of strings that should appear in the exception error message. By
    default, only compares strings to the exception's string representation `str(exc)`.
    Set check_notes=True to also compare strings to the exception's __notes__ (if present).
    ----------
    Inputs:
        func: The function (or method) to be called
        func_args: A list of positional arguments used to call the function
        func_kwargs: A dict of keyword arguments used to call the function
        exception_type: The expected exception type, or a tuple of allowed types
        match: An optional regular expression string or compiled regex
        check: An optional callable that will be passed the exception as input
        message: A sequence of string that should appear in the error message
        check_notes: True to check for `message` strings in both the exception's string
            representation and __notes__. False (default) to only compare `message`
            strings to the exception's string representation.

    Outputs:
        Exception: The raised exception

    Raises:
        AssertionError: If the function does not raise an Exception that matches the
            given criteria.
    """

    # Generate and validate the exception. Extract from ExceptionInfo
    with pytest.raises(exception_type, match=match, check=check) as error:
        func(*func_args, **func_kwargs)

    # Get the error message and check for notes as needed
    exception = error.value
    raised_message = str(exception)
    check_notes = check_notes & hasattr(exception, "__notes__")

    # Check the error message includes the expected strings
    for string in message:
        if (string not in raised_message) and (
            not check_notes or not any(string in note for note in exception.__notes__)
        ):
            assert False, (
                f"Error message did not contain expected string."
                f"\n\n"
                f"**Expected string**\n{string}"
                f"\n\n"
                f"**Actual message**\n{raised_message}"
            )
    return exception


def _check_test(
    # Function call
    func: Callable,
    func_args: tuple | list = (),
    func_kwargs: dict = {},
    # Pytest API
    exception_type: type | tuple[type] = Exception,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
    # pytest-error
    message: list[str] | None = [],
    check_notes: bool = False,
    format: bool = True,
) -> None:
    """
    This function is similar to _check_error, but is designed to be more aware of
    pytest testing environments. As such, the function will call str.format on
    message strings, allowing injection of pytest parameters into expected error
    messages (set format=False to disable this behavior).

    The function also implements the opinion that error tests should usually examine
    the error message. Specifically, the function will raise an AssertionError if the
    test does not include an expected error message (indicated by `message` being an
    empty list). This behavior can be disabled by setting `message` explicitly to None.
    """

    # Convert message to list and optionally disable message checking
    disabled = message is None
    message = [] if disabled else list(message)

    # Optionally format message strings
    if format:
        for s, string in enumerate(message):
            message[s] = string.format(**func_kwargs)

    # Validate the exception and optionally enforce error message checking
    exception = _check_error(
        func, func_args, func_kwargs, exception_type, match, check, message, check_notes
    )
    if len(message) == 0 and not disabled:
        assert (
            False
        ), f"Undeclared error message\n\n**Raised message**\n{str(exception)}"


#####
# Main Decorator
#####


def error(
    exception_type: type | tuple[type],
    *message: str | None,
    format: bool = True,
    check_notes: bool = False,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
):
    """
    Decorator that checks a pytest test raises an expected exception
    ----------
    @error(exception_type, *message)
    Requires the following test function to raise an exception that matches the
    indicated type (subclasses are considered a match). If `exception_type` is a tuple,
    then the exception is required to match at least one of the provided types. The
    exception is also required to include any provided error message strings in its
    string representation `str(exception)`.

    @error(exception_type)
    @error(exception_type, None)
    By default, raises an AssertionError if no error message strings are provided. The
    AssertionError will report the raised error message, which can be useful for
    examining error messages when writing tests. To disable this behavior (effectively
    disabling error message validation), set the message explicitly to None.

    @error(..., *, format = False)
    @error(..., *, check_notes = True)
    Additional options for validating error messages. By default, the decorator calls
    `message.format(**test_kwargs)` on the provided error message strings. This allows
    the injection of pytest parameters into error messages, but means that curly braces
    {} will be interpreted as string formatting placeholders. Set format=False to
    disable this behavior, retaining {} as literal strings.

    By default, the decorator will only check for error message strings in the
    exception's string representation `str(exception)`. Set check_notes=True to also
    check for error message strings in the exception's __notes__ (if present).

    @error(..., *, match)
    @error(..., *, check)
    Options inherited from the pytest.raises API. When provided, `match` should be
    a string containing a regular expression, or a regular expression object, that is
    tested against the string representation of the exception and its __notes__ (if
    present) using re.search. Note that that `match` is not affected by the
    `check_notes` option, so is always tested against the exception's __notes__ when
    possible.

    When provided, `check` should be a callable that will be called with the exception
    as a parameter after checking the `exception_type` and the `match` regex (if
    specified). If `check` returns True, then the exception is considered a match.
    Otherwise, the exception is treated as a failed match.
    ----------
    Inputs:
        exception_type: An type or tuple of types that the raised exception should match
        *message: Error message strings that must be contained in the exception's string
            representation (or optionally in its __notes__). At least one value must be
            provided - set to None to disable error message checking entirely.
        format: True (default) to call message.format(**test_kwargs) on the provided
            error message strings. False to skip this step.
        check_notes: True to compare error message strings to both the exception's
            string representation and its __notes__. False (default) to only check the
            string representation.
        match: Regular expression string or compiled regex object that will be tested
            against the exception's string representation and __notes__ using re.search
        check: Callable that will be called with the raised exception as a parameter.
            Should return True to indicate the exception is as expected.

    Raises:
        TypeError: If an error message input is neither a string, nor None
        AssertionError: If no error message input is provided
        AssertionError: If the raised exception does not match the expected criteria
    """

    # Parse and validate the expected error message strings
    if message == (None,):
        message = None
    else:
        for s, string in enumerate(message):
            if not isinstance(string, str):
                raise TypeError(f"error message[{s}] is not a string")

    # Build the decorator
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _check_test(
                # function call
                func,
                args,
                kwargs,
                # pytest.raises
                exception_type,
                match,
                check,
                # message checking
                message,
                check_notes,
                format,
            )

        return wrapper

    return decorator


#####
# Aliases
#####


def error_with_notes(
    exception_type: type | tuple[type],
    *message: str | None,
    format: bool = True,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
) -> None:
    "Alias for `@error(..., *, check_notes=True)`"
    return error(
        exception_type,
        *message,
        format=format,
        check_notes=True,
        match=match,
        check=check,
    )


def error_no_format(
    exception_type: type | tuple[type],
    *message: str | None,
    check_notes: bool = False,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
) -> None:
    "Alias for @error(..., format=False)"
    return error(
        exception_type,
        *message,
        format=False,
        check_notes=check_notes,
        match=match,
        check=check,
    )


def error_no_message(
    exception_type: type | tuple[type],
    *,
    match: Optional[Match] = None,
    check: Optional[Callable] = None,
) -> None:
    "Alias for `@error(..., message=None)`"
    return error(exception_type, None, match=match, check=check)
