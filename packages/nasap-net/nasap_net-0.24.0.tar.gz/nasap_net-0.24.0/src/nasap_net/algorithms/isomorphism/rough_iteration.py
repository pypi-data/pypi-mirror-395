from collections.abc import Iterator

from networkx.algorithms.isomorphism import (GraphMatcher,
                                             categorical_node_match)

from nasap_net import Assembly

__all__ = ['rough_isomorphisms_iter']


def rough_isomorphisms_iter(
        assem1: Assembly, assem2: Assembly
        ) -> Iterator[dict[str, str]]:
    """Find all isomorphisms between two "rough_g_snapshot" graphs of 
    assemblies.

    Parameters
    ----------
    assem1 : Assembly
        The first assembly.
    assem2 : Assembly
        The second assembly.

    Yields
    ------
    dict[str, str]
        A mapping from component ID (e.g., 'M1', 'L1') in the first assembly
        to component ID in the second assembly.
    """
    node_match = categorical_node_match('component_kind', None)
    GM = GraphMatcher(
        assem1.rough_g_snapshot, assem2.rough_g_snapshot, node_match=node_match)
    yield from GM.isomorphisms_iter()
