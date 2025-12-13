from collections.abc import Iterator, Mapping

from networkx.algorithms.isomorphism import (GraphMatcher,
                                             categorical_edge_match,
                                             categorical_node_match)

from nasap_net import Assembly, Component

__all__ = ['isomorphisms_iter']


def isomorphisms_iter(
        assem1: Assembly, assem2: Assembly,
        component_structures: Mapping[str, Component]
        ) -> Iterator[dict[str, str]]:
    """Find all isomorphisms between two "g_snapshot" graphs of assemblies.

    Parameters
    ----------
    assem1 : Assembly
        The first assembly.
    assem2 : Assembly
        The second assembly.
    component_structures : Mapping[str, ComponentStructure]
        A mapping from component kind to its structure.

    Yields
    ------
    dict[str, str]
        A mapping from node (core or bindsite, e.g., 'M1.core', 'M1.a')
        in the first assembly to node in the second assembly.
    """
    g1 = assem1.g_snapshot(component_structures)
    g2 = assem2.g_snapshot(component_structures)

    node_match = categorical_node_match('component_kind', None)
    edge_match = categorical_edge_match('aux_kind', None)
    GM = GraphMatcher(
        g1, g2, node_match=node_match, edge_match=edge_match)
    yield from GM.isomorphisms_iter()
