from collections.abc import Mapping

import networkx as nx

from nasap_net import Assembly, Component
from nasap_net.algorithms.aux_edge_existence import has_aux_edges


def calc_graph_hash_of_assembly(
        assembly: Assembly, 
        component_structures: Mapping[str, Component]
        ) -> str:
    """Calculate the hash of the graph of the assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly to calculate the hash of.
    component_structures : Mapping[str, Component]
        The structures of the components in the assembly.

    Returns
    -------
    str
        The hash of the graph of the assembly.

    Notes
    -----
    The hash is calculated using the Weisfeiler-Lehman graph hash
    algorithm. The hash is calculated based on the rough graph if the
    assembly does not have auxiliary edges, and based on the detailed
    graph if the assembly has auxiliary edges.
    """
    if has_aux_edges(assembly, component_structures):
        return calc_detailed_graph_hash(assembly, component_structures)
    else:
        return calc_rough_graph_hash(assembly)


def calc_rough_graph_hash(assembly: Assembly) -> str:
    # Since nx.weisfeiler_lehman_graph_hash() is not supported for
    # MultiGraph, which is used for the rough graph, we need to convert
    # it to Graph, i.e., remove parallel edges.
    # Consequently, the result of this function will be the same for
    # assemblies with the same rough graph except for the existence of
    # parallel edges.
    rough_g = assembly.rough_g_snapshot
    rough_g_without_parallel_edges = _multi_graph_to_graph(rough_g)
    return nx.weisfeiler_lehman_graph_hash(
        rough_g_without_parallel_edges, node_attr='component_kind')


def _multi_graph_to_graph(G_multi: nx.MultiGraph) -> nx.Graph:
    G_single = nx.Graph()
    for node, data in G_multi.nodes(data=True):
        G_single.add_node(node, **data)
    for u, v, data in G_multi.edges(data=True):
        G_single.add_edge(u, v)
    return G_single


def calc_detailed_graph_hash(
        assembly: Assembly, 
        component_structures: Mapping[str, Component]
        ) -> str:
    g = assembly.g_snapshot(component_structures)
    _add_attr_for_hash(g)
    
    return nx.weisfeiler_lehman_graph_hash(
        g, node_attr='for_hash', edge_attr='for_hash')


def _add_attr_for_hash(g: nx.Graph) -> None:
    for node, data in g.nodes(data=True):
        if data['core_or_bindsite'] == 'core':
            data['for_hash'] = data['component_kind']
        else:
            data['for_hash'] = None

    for u, v, data in g.edges(data=True):
        if 'aux_kind' in data:
            data['for_hash'] = data['aux_kind']
        else:
            data['for_hash'] = None
