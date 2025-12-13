from itertools import product

import networkx as nx
import pytest

from nasap_net.utils.node_equivalence import group_equivalent_nodes_or_nodesets


@pytest.fixture
def graph_data():
    G = nx.Graph()
    G.add_nodes_from(['1', '2', '3', '4', '5'])
    G.add_edges_from([('1', '2'), ('1', '3'), ('1', '4'), ('1', '5')])
    
    ISOMORPHISMS = [
        {'1': '1', '2': '3', '3': '4', '4': '5', '5': '2'},  # C_4
    ]
    
    return G, ISOMORPHISMS


def test_node_equivalence_single_nodes(graph_data):
    G, ISOMORPHISMS = graph_data
    NODES = {'1', '2', '3', '4', '5'}
    
    node_equiv = group_equivalent_nodes_or_nodesets(NODES, ISOMORPHISMS)
    
    assert node_equiv == {frozenset(['1']), frozenset(['2', '3', '4', '5'])}


def test_node_equivalence_node_sets(graph_data):
    G, ISOMORPHISMS = graph_data
    NODESETS = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '1'), ('2', '2')]

    nodeset_equiv = group_equivalent_nodes_or_nodesets(NODESETS, ISOMORPHISMS)

    assert nodeset_equiv == {
        frozenset([('1', '2'), ('1', '3')]),
        frozenset([('2', '3')]),
        frozenset([('1', '1')]),
        frozenset([('2', '2')]),
    }


def test_node_equivalence_product_node_sets(graph_data):
    G, ISOMORPHISMS = graph_data
    NODES = {'1', '2', '3', '4', '5'}
    NODESETS2 = product(NODES, repeat=2)  # total 25 pairs

    nodeset_equiv2 = group_equivalent_nodes_or_nodesets(NODESETS2, ISOMORPHISMS)

    assert nodeset_equiv2 == {
        frozenset([('1', '1')]),
        frozenset([('1', '2'), ('1', '3'), ('1', '4'), ('1', '5')]),
        frozenset([('2', '1'), ('3', '1'), ('4', '1'), ('5', '1')]),
        frozenset([('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]),
        frozenset([('2', '3'), ('3', '4'), ('4', '5'), ('5', '2')]),
        frozenset([('2', '4'), ('3', '5'), ('4', '2'), ('5', '3')]),
        frozenset([('2', '5'), ('3', '2'), ('4', '3'), ('5', '4')]),
    }


if __name__ == '__main__':
    pytest.main(['-v', __file__])
