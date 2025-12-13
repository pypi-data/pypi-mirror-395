from collections.abc import Mapping
from typing import Any, Type


def construct_repr(class_obj: Type, fields: Mapping[str, Any]) -> str:
    """Construct a repr string for a class with given fields."""
    field_strs = [f'{key}={value!r}' for key, value in fields.items()]
    field_str = ', '.join(field_strs)
    return f'<{class_obj.__name__} {field_str}>'
