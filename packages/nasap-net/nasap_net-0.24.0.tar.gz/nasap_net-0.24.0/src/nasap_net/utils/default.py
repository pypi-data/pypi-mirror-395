from typing import Any, NewType, TypeVar, overload


Missing = NewType("Missing", object)
MISSING = Missing(object())

T = TypeVar('T')

@overload
def default_if_missing(value: Missing, default: T) -> T: ...
@overload
def default_if_missing(value: T, default: Any) -> T: ...
def default_if_missing(value, default):
    """Return the value if it is not MISSING, otherwise return the default.

    Note that None is considered a valid value and will not trigger the default.
    """
    return default if value is MISSING else value
