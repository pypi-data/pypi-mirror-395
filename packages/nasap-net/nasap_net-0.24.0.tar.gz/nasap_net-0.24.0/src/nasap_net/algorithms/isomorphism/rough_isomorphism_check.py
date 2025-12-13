import networkx as nx
from networkx.algorithms.isomorphism import categorical_node_match

from nasap_net import Assembly

__all__ = ['is_roughly_isomorphic']


def is_roughly_isomorphic(assem1: Assembly, assem2: Assembly) -> bool:
    """Check if two assemblies are roughly isomorphic."""
    node_match = categorical_node_match('component_kind', None)
    # QUESTION: Should we use VF2++ instead of VF2?
    return nx.is_isomorphic(
        assem1.rough_g_snapshot, assem2.rough_g_snapshot,
        node_match=node_match)
