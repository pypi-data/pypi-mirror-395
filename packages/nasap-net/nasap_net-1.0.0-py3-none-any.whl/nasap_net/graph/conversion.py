from dataclasses import dataclass
from typing import Mapping

import igraph as ig
from bidict import frozenbidict

from nasap_net.models import Assembly, BindingSite
from nasap_net.types import ID


@dataclass(frozen=True, init=False)
class GraphConversionResult:
    graph: ig.Graph
    core_mapping: frozenbidict[ID, int]
    binding_site_mapping: frozenbidict[BindingSite, int]

    def __init__(
            self,
            graph: ig.Graph,
            core_mapping: Mapping[ID, int],
            binding_site_mapping: Mapping[BindingSite, int],
    ) -> None:
        object.__setattr__(self, 'graph', graph)
        object.__setattr__(
            self, 'core_mapping', frozenbidict(core_mapping))
        object.__setattr__(
            self, 'binding_site_mapping',
            frozenbidict(binding_site_mapping))


def convert_assembly_to_graph(assembly: Assembly) -> GraphConversionResult:
    g = ig.Graph()
    core_mapping = {}
    binding_site_mapping = {}

    for comp_id, comp in assembly.components.items():
        # Add the core node
        g.add_vertices(  # More efficient than add_vertex
            1,
            {
                'comp_id': [comp_id],
                'comp_kind': [comp.kind],
                'core_or_site': ['core'],
            }
        )
        core_mapping[comp_id] = g.vcount() - 1

        # Add the binding sites
        g.add_vertices(
            len(comp.site_ids),
            {
                'comp_id': [comp_id] * len(comp.site_ids),
                'comp_kind': [comp.kind] * len(comp.site_ids),
                'core_or_site': ['site'] * len(comp.site_ids),
                'site_id': list(comp.site_ids),
            }
        )
        start_id = g.vcount() - len(comp.site_ids)
        for i, site in enumerate(comp.get_binding_sites(comp_id)):
            binding_site_mapping[site] = start_id + i

        # Add the edges between core and sites
        g.add_edges(
            [(core_mapping[comp_id], binding_site_mapping[site])
                for site in comp.get_binding_sites(comp_id)]
        )

        # Add the auxiliary edges
        for aux in comp.aux_edges:
            site1, site2 = aux.get_binding_sites(comp_id)
            if aux.kind is None:
                g.add_edges(
                    [(
                        binding_site_mapping[site1],
                        binding_site_mapping[site2]
                    )]
                )
            else:
                g.add_edges(
                    [(
                        binding_site_mapping[site1],
                        binding_site_mapping[site2]
                    )],
                    {'aux_kind': [aux.kind]}
                )

    # Add the bonds
    for bond in assembly.bonds:
        site1, site2 = bond.sites
        g.add_edge(
            binding_site_mapping[site1],
            binding_site_mapping[site2]
        )

    return GraphConversionResult(
        graph=g,
        core_mapping=core_mapping,
        binding_site_mapping=binding_site_mapping
    )
