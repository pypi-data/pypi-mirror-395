from typing import Hashable

from nasap_net.models import Assembly


def get_assembly_signature(assembly: Assembly) -> Hashable:
    """Compute a light signature of the assembly for quick filtering.

    Assemblies with different signatures are guaranteed to be non-isomorphic.
    Assemblies with the same signature may or may not be isomorphic.

    The signature consists of:
    - A sorted tuple of component kinds.
    - A sorted tuple of sorted tuples of bond component kinds.

    Parameters
    ----------
    assembly : Assembly
        The assembly to compute the signature for.

    Returns
    -------
    Hashable
        The light signature of the assembly.
    """
    return (
        # component kinds
        tuple(sorted(comp.kind for comp in assembly.components.values())),
        # bond component kinds
        tuple(sorted(
            tuple(sorted([
                assembly.get_component_kind_of_site(site1),
                assembly.get_component_kind_of_site(site2),
            ]))
            for site1, site2 in assembly.bonds
        ))
    )
