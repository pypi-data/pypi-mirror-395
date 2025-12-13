from collections.abc import Mapping

from nasap_net import Assembly, Component
from nasap_net.algorithms.aux_edge_existence import has_aux_edges
from nasap_net.algorithms.isomorphism.pure_isomorphism_check import \
    pure_is_isomorphic
from nasap_net.algorithms.isomorphism.rough_isomorphism_check import \
    is_roughly_isomorphic

__all__ = ['is_isomorphic']


def is_isomorphic(
        assem1: Assembly, assem2: Assembly,
        component_structures: Mapping[str, Component]
        ) -> bool:
    """Check if two assemblies are isomorphic."""
    if assem1.component_kinds != assem2.component_kinds:
        return False
    
    if has_aux_edges(assem1, component_structures):
        return pure_is_isomorphic(assem1, assem2, component_structures)
    else:
        return is_roughly_isomorphic(assem1, assem2)
