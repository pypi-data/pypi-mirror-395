from collections.abc import Hashable, Mapping
from typing import TypeVar

from .symmetry_application import apply_symmetry_operation

__all__ = ['is_new_under_symmetry']

_T = TypeVar('_T', bound=Hashable)


def is_new_under_symmetry(
        found_assems: set[frozenset[_T]],
        new_assem: set[_T],
        sym_ops: Mapping[str, Mapping[_T, _T]] | None = None
        ) -> bool:
    """Check if a new assembly is not symmetry-equivalent to the found ones.

    Identity operation 'E' is not necessary to be included in sym_ops,
    because the existence of the assembly itself is checked first.
    """
    found_assems = set(found_assems)

    # Existence of the assembly itself is checked first.
    # This is why the sym_ops does not nessarily contain 'E'.

    # According to the Python 3.12.5 Documentation,
    # comparison of set and frozenset is based on their members,
    # e.g., set('abc') == frozenset('abc') returns True,
    # and set('abc') in set([frozenset('abc')]) returns True.
    # Therefore, the following line can check if the new_assem is
    # already found in found_assems even if the new_assem is set type.
    if new_assem in found_assems:
        return False
    if sym_ops is None:
        return True
    for sym_op in sym_ops.values():
        transformed_assem = apply_symmetry_operation(new_assem, sym_op)
        if transformed_assem in found_assems:
            return False
    return True
