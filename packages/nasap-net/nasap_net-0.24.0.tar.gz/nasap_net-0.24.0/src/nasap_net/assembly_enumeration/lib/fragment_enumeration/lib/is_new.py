from collections.abc import Hashable, Iterable, Mapping
from typing import Any

from nasap_net.types import ID
from .key import get_key
from .symmetry_operation import apply_symmetry_operation
from ..models import Fragment


def is_new(
        target: Fragment,
        found: Mapping[Hashable, set[Fragment]],
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None
) -> bool:
    key = get_key(target)
    if key not in found:
        return True
    candidates = found[key]
    if target in candidates:
        return False
    if symmetry_operations is None:
        return True
    for sym_op in symmetry_operations:
        transformed_fragment = apply_symmetry_operation(target, sym_op)
        if transformed_fragment in candidates:
            return False
    return True
