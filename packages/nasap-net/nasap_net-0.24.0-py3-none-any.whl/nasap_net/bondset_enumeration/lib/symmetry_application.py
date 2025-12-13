from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

__all__ = ['apply_symmetry_operation']

_T = TypeVar('_T', bound=Hashable)


def apply_symmetry_operation(
        bondset: Iterable[_T],
        sym_op: Mapping[_T, _T]
        ) -> set[_T]:
    """Apply a symmetry operation to an assembly."""
    return set(sym_op[bond] for bond in bondset)
