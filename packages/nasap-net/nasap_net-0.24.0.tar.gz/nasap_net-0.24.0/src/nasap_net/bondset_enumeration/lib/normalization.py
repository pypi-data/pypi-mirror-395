from collections.abc import Iterable, Mapping

from .symmetry_application import apply_symmetry_operation

__all__ = ['normalize_bondset_under_sym_ops']


def normalize_bondset_under_sym_ops(
        bondset: Iterable[int],
        sym_ops: Mapping[str, Mapping[int, int]] | None = None
        ) -> set[int]:
    """Find a representative of an assembly under symmetry operations.

    There can be multiple symmetry-equivalent assemblies for a given
    assembly. This function finds the smallest one among them as a
    representative.

    # TODO: Add an example.
    """
    bondset = set(bondset)
    if sym_ops is None:
        return bondset
    for sym_op in sym_ops.values():
        transformed_assem = apply_symmetry_operation(bondset, sym_op)
        if sorted(transformed_assem) < sorted(bondset):
            bondset = transformed_assem
    return bondset
