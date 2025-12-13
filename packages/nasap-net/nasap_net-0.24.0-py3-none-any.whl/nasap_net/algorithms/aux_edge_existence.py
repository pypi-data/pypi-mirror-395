from collections.abc import Mapping

from nasap_net import Assembly, Component

__all__ = ['has_aux_edges']


def has_aux_edges(
        assem: Assembly,
        component_structures: Mapping[str, Component]
        ) -> bool:
    """Check if the assembly has auxiliary edges."""
    comps_with_aux_edges = {
        comp_kind for comp_kind, comp_struct in component_structures.items()
        if comp_struct.aux_edges}
    return any(
        comp_kind in comps_with_aux_edges
        for comp_kind in assem.component_kinds)
