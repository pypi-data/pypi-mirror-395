from dataclasses import dataclass
from typing import Mapping

import igraph as ig
from bidict import frozenbidict

from nasap_net.models import Assembly
from nasap_net.types import ID


@dataclass(frozen=True, init=False)
class RoughGraphConversionResult:
    graph: ig.Graph
    core_mapping: frozenbidict[ID, int]

    def __init__(
            self,
            graph: ig.Graph,
            core_mapping: Mapping[ID, int],
    ) -> None:
        object.__setattr__(self, 'graph', graph)
        object.__setattr__(
            self, 'core_mapping', frozenbidict(core_mapping))


def convert_assembly_to_rough_graph(assembly: Assembly) -> RoughGraphConversionResult:
    g = ig.Graph()
    core_mapping = {}

    for comp_id, comp in assembly.components.items():
        # Add the core node
        g.add_vertices(  # More efficient than add_vertex
            1,
            {
                'comp_id': [comp_id],
                'comp_kind': [comp.kind],
            }
        )
        core_mapping[comp_id] = g.vcount() - 1

    # Add the bonds
    for bond in assembly.bonds:
        comp_id1, comp_id2 = bond.component_ids
        g.add_edge(core_mapping[comp_id1], core_mapping[comp_id2])

    return RoughGraphConversionResult(
        graph=g,
        core_mapping=core_mapping,
    )
