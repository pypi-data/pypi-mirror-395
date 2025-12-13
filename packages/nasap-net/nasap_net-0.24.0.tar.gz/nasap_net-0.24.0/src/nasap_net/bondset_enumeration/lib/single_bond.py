from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from .is_new_check import is_new_under_symmetry

__all__ = ['enum_single_bond_subsets']

_T = TypeVar('_T', bound=Hashable)


def enum_single_bond_subsets(
        bonds: Iterable[_T],
        sym_ops: Mapping[str, Mapping[_T, _T]] | None = None
        ) -> set[frozenset[_T]]:
    """Enumerate single-bond subsets of bonds 
    excluding disconnected ones and symmetry-equivalent ones.
    """
    found: set[frozenset[_T]] = set()

    # NOTE: The order of the iteration should be fixed to make the
    # result deterministic.
    for bond in bonds:
        assembly = {bond}
        if is_new_under_symmetry(found, assembly, sym_ops):
            found.add(frozenset(assembly))

    return set(found)
