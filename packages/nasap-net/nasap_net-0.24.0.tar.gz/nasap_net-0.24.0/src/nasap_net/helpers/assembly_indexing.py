from collections.abc import Iterable, Sequence

from nasap_net.models import Assembly
from nasap_net.utils import deduplicate_ids
from .composition_formula import generate_composition_formula


def assign_composition_formula_ids(
        assemblies: Iterable[Assembly],
        *,
        order: Sequence[str] | None = None,
) -> list[Assembly]:
    """Assign composition formula strings as IDs to the given assemblies."""
    assigned_assemblies = [
        assembly.copy_with(
            id_=generate_composition_formula(assembly, order=order)
        )
        for assembly in assemblies
    ]
    return deduplicate_ids(assigned_assemblies)  # type: ignore
