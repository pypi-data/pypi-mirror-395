from collections import UserDict
from typing import Any


class ValueConflictError(Exception):
    """Exception raised when attempting to overwrite an existing key."""
    def __init__(
            self,
            key: Any,
            existing_value: Any,
            new_value: Any,
    ) -> None:
        message = (
            f"Attempted to overwrite existing key '{key}': "
            f"existing value '{existing_value}', new value '{new_value}'."
        )
        super().__init__(message)
        self.key = key
        self.existing_value = existing_value
        self.new_value = new_value


class NoOverwriteDict(UserDict):
    """A dict that raises an error when overwriting an existing key."""
    def __setitem__(
        self,
        key: Any,
        value: Any
    ) -> None:
        if key in self.data:
            raise ValueConflictError(
                key,
                existing_value=self.data[key],
                new_value=value
            )
        super().__setitem__(key, value)
