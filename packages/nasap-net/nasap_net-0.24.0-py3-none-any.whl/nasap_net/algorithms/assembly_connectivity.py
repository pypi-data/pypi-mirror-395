from collections.abc import Iterator

import networkx as nx

from nasap_net import Assembly
from nasap_net.algorithms.subassembly import component_induced_sub_assembly

__all__ = ['extract_connected_assemblies']


def extract_connected_assemblies(assembly: Assembly) -> Iterator[Assembly]:
    g = assembly.rough_g_snapshot
    for connected_components in nx.connected_components(g):
        yield component_induced_sub_assembly(assembly, connected_components)
