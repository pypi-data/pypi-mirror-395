from collections.abc import Mapping

from networkx.utils import graphs_equal

from nasap_net import Assembly, Component

__all__ = ['assemblies_equal']


def assemblies_equal(
        assem1: Assembly, assem2: Assembly,
        component_kinds: Mapping[str, Component]
        ) -> bool:
    """Check if two assemblies are equal.

    Equality here means equal as Python objects, not isomorphism of the
    underlying graphs. Component names, binding site names, and the 
    auxiliary edge types must match.

    See Also
    --------
    nasap_net.is_isomorphic
    """
    return graphs_equal(
        assem1.g_snapshot(component_kinds),
        assem2.g_snapshot(component_kinds))
