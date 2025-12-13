from collections.abc import Mapping

import networkx as nx
from networkx.algorithms.isomorphism import (categorical_edge_match,
                                             categorical_node_match)

from nasap_net import Assembly, Component

__all__ = ['pure_is_isomorphic']


def pure_is_isomorphic(
        assem1: Assembly, assem2: Assembly,
        component_kinds: Mapping[str, Component]
        ) -> bool:
    """Check if two assemblies are isomorphic."""
    node_match = categorical_node_match('component_kind', None)
    edge_match = categorical_edge_match('aux_kind', None)
    # QUESTION: Should we use VF2++ instead of VF2?
    return nx.is_isomorphic(
        assem1.g_snapshot(component_kinds), assem2.g_snapshot(component_kinds),
        node_match=node_match, edge_match=edge_match)
