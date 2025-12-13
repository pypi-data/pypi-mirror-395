from collections.abc import Iterable, Mapping
from typing import Any

from nasap_net.assembly_equivalence import \
    extract_unique_assemblies
from nasap_net.models import Assembly, Component
from nasap_net.types import ID
from .lib import cap_assemblies_with_ligand, enumerate_fragments


def enumerate_assemblies(
        template: Assembly,
        *,
        leaving_ligand: Component,
        leaving_ligand_site: ID | None = None,
        metal_kinds: Iterable[str],
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None,
) -> set[Assembly]:
    """Enumerate assemblies which can be formed by adding the leaving ligand
    to the fragments of the template assembly.

    This function generates all possible assemblies by attaching the
    specified leaving ligand to each fragment in the template assembly. It
    ensures that the resulting assemblies are unique by excluding duplicates
    based on symmetry operations and isomorphism checks.

    Any two assemblies that meet either of the following conditions are
    considered duplicates, and only one of them is included in the output list:
    - One can be transformed into the other by applying a symmetry operation
      from the provided list.
    - They are isomorphic, i.e., they have the same connectivity structure.

    Providing symmetry operations is strongly recommended to reduce the
    computational cost of duplicate exclusion.

    Parameters
    ----------
    template : Assembly
        The template assembly to base the enumeration on.
    leaving_ligand : Component
        The ligand to be added to the fragments of the template assembly.
    leaving_ligand_site : ID | None, optional
        The site ID on the leaving ligand where it will be attached.
        If None, the first site ID of the leaving ligand will be used.
        Default is None.
    metal_kinds : Iterable[str]
        The kinds of metal components in the assembly. All binding sites on
        these components will be considered for attaching the leaving ligand.
    symmetry_operations : Iterable[Mapping[Any, ID]] | None, optional
        A list of symmetry operations to consider when excluding duplicate
        assemblies. Each symmetry operation is represented as a mapping from
        original site IDs to transformed site IDs.

    Returns
    -------
    set[Assembly]
        A set of unique assemblies formed by adding the leaving ligand
        to the fragments of the template assembly.
        Also includes the free leaving ligand as an assembly.
    """
    fragments = enumerate_fragments(
        template,
        symmetry_operations=symmetry_operations,
    )
    unique_fragments = extract_unique_assemblies(
        fragments,
    )
    capped_assemblies = cap_assemblies_with_ligand(
        unique_fragments,
        component=leaving_ligand,
        component_site_id=leaving_ligand_site,
        metal_kinds=metal_kinds,
    )
    # Also include the free leaving ligand as an assembly
    capped_assemblies.add(
        Assembly(
            components={f'{leaving_ligand.kind}0': leaving_ligand},
            bonds=[],
        )
    )
    return capped_assemblies
