from unittest.mock import patch

import pytest

import nasap_net.algorithms.hashing as hashing
from nasap_net import Assembly, Component, calc_graph_hash_of_assembly
from nasap_net.algorithms.hashing import (_multi_graph_to_graph,
                                          calc_detailed_graph_hash,
                                          calc_rough_graph_hash)

# ==========================================
# Tests for calc_wl_hash_of_assembly
# ==========================================

def test_calc_wl_hash_of_assembly_with_aux_edges():
    assembly = Assembly()
    components = dict[str, Component]()

    with (
            patch('nasap_net.algorithms.hashing.has_aux_edges',
                  return_value=True) as mock_has_aux_edges,
            patch('nasap_net.algorithms.hashing.calc_detailed_graph_hash')\
                as mock_detailed_wl_hash,
            patch('nasap_net.algorithms.hashing.calc_rough_graph_hash')\
                as mock_rough_wl_hash):
        calc_graph_hash_of_assembly(assembly, components)
        
        mock_has_aux_edges.assert_called_once_with(assembly, components)
        mock_detailed_wl_hash.assert_called_once_with(assembly, components)
        mock_rough_wl_hash.assert_not_called()


def test_calc_wl_hash_of_assembly_without_aux_edges():
    assembly = Assembly()
    components = dict[str, Component]()

    with (
            patch('nasap_net.algorithms.hashing.has_aux_edges',
                  return_value=False) as mock_has_aux_edges,
            patch('nasap_net.algorithms.hashing.calc_detailed_graph_hash')\
                as mock_detailed_wl_hash,
            patch('nasap_net.algorithms.hashing.calc_rough_graph_hash')\
                as mock_rough_wl_hash):
        calc_graph_hash_of_assembly(assembly, components)
        
        mock_has_aux_edges.assert_called_once_with(assembly, components)
        mock_detailed_wl_hash.assert_not_called()
        mock_rough_wl_hash.assert_called_once_with(assembly)


# ==========================================
# Fixtures
# ==========================================

@pytest.fixture
def COMP_KIND_TO_OBJ():
    return {
        'M_WITHOUT_AUX': Component({'a', 'b', 'c', 'd'}),
        'M_WITH_AUX': Component(
            {'a', 'b', 'c', 'd'}, 
            [('a', 'b', 'cis'), ('b', 'c', 'cis'),
             ('c', 'd', 'cis'), ('d', 'a', 'cis')]),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

@pytest.fixture
def MX4_WITHOUT_AUX():
    return Assembly(
        {'M1': 'M_WITHOUT_AUX', 
         'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'),
         ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])

@pytest.fixture
def ML2X2_CIS():
    return Assembly(
        {'M1': 'M_WITH_AUX', 
         'L1': 'L', 'L2': 'L',
         'X1': 'X', 'X2': 'X'},
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'),
         ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])

@pytest.fixture
def ML2X2_TRANS():
    return Assembly(
        {'M1': 'M_WITH_AUX', 
         'L1': 'L', 'L2': 'L',
         'X1': 'X', 'X2': 'X'},
        [('M1.a', 'L1.a'), ('M1.b', 'X1.a'),
         ('M1.c', 'L2.a'), ('M1.d', 'X2.a')])


# ==========================================
# Tests for calc_detailed_wl_hash
# ==========================================

def test_detailed_hash_with_same_assemblies():
    MX2_ALPHA = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                     [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MX2_BETA = Assembly({'M10': 'M', 'X10': 'X', 'X20': 'X'},
                     [('M10.a', 'X10.a'), ('M10.b', 'X20.a')])
    COMP_KIND_TO_OBJ = {
        'M': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

    hash_mx2_alpha = calc_detailed_graph_hash(MX2_ALPHA, COMP_KIND_TO_OBJ)
    hash_mx2_beta = calc_detailed_graph_hash(MX2_BETA, COMP_KIND_TO_OBJ)

    # Since the graphs of MX2_ALPHA and MX2_BETA are isomorphic 
    # considering the component kinds, the hashes of them should be 
    # the same.
    assert hash_mx2_alpha == hash_mx2_beta


def test_detailed_hash_with_different_component_kinds():
    MX2 = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                   [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MY2 = Assembly({'M1': 'M', 'Y1': 'Y', 'Y2': 'Y'},
                   [('M1.a', 'Y1.a'), ('M1.b', 'Y2.a')])
    COMP_KIND_TO_OBJ = {
        'M': Component({'a', 'b'}),
        'X': Component({'a'}),
        'Y': Component({'a'}),
    }

    hash_mx2 = calc_detailed_graph_hash(MX2, COMP_KIND_TO_OBJ)
    hash_my2 = calc_detailed_graph_hash(MY2, COMP_KIND_TO_OBJ)

    # Even though the graphs of MX2 and MY2 are isomorphic without
    # considering the component kinds, the hashes of them should be
    # different because the component kinds (i.e., 'X' and 'Y') are
    # different
    assert hash_mx2 != hash_my2


def test_detailed_hash_with_same_assemblies_and_same_aux_edges():
    MX2_ALPHA = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                        [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MX2_BETA = Assembly({'M10': 'M', 'X10': 'X', 'X20': 'X'},
                        [('M10.a', 'X10.a'), ('M10.b', 'X20.a')])
    COMP_KIND_TO_OBJ = {
        'M': Component({'a', 'b'}, [('a', 'b', 'cis')]),
        'X': Component({'a'}),
    }

    hash_mx2_alpha = calc_detailed_graph_hash(MX2_ALPHA, COMP_KIND_TO_OBJ)
    hash_mx2_beta = calc_detailed_graph_hash(MX2_BETA, COMP_KIND_TO_OBJ)

    # Since the graphs of MX2_ALPHA and MX2_BETA are isomorphic
    # considering the component kinds and the kinds of the aux edges,
    # the hashes of them should be the same.
    assert hash_mx2_alpha == hash_mx2_beta


def test_detailed_hash_with_different_connectivities():
    # X1---X2---X3
    LINEAR = Assembly(
        {'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('X1.a', 'X2.a'), ('X2.a', 'X3.a')])
    #    X1
    #  /   \
    # X4----X3
    RING = Assembly(
        {'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('X1.b', 'X2.a'), ('X2.b', 'X3.a'), ('X3.b', 'X1.a')])

    hash_linear = calc_rough_graph_hash(LINEAR)
    hash_ring = calc_rough_graph_hash(RING)

    assert hash_linear != hash_ring


def test_detailed_hash_with_different_aux_edge_existence():
    MX2_ALPHA = Assembly({'M1': 'M_WITH_AUX', 'X1': 'X', 'X2': 'X'},
                        [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MX2_BETA = Assembly({'M10': 'M_WITHOUT_AUX', 'X10': 'X', 'X20': 'X'},
                        [('M10.a', 'X10.a'), ('M10.b', 'X20.a')])
    COMP_KIND_TO_OBJ = {
        'M_WITH_AUX': Component({'a', 'b'}, [('a', 'b', 'cis')]),
        'M_WITHOUT_AUX': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

    hash_mx2_alpha = calc_detailed_graph_hash(MX2_ALPHA, COMP_KIND_TO_OBJ)
    hash_mx2_beta = calc_detailed_graph_hash(MX2_BETA, COMP_KIND_TO_OBJ)

    # Even though the graphs of MX2_ALPHA and MX2_BETA are isomorphic
    # considering only the component kinds, the hashes of them should be
    # different because the existence of the aux edges are different.
    assert hash_mx2_alpha != hash_mx2_beta


def test_detailed_hash_with_different_aux_edge_kinds():
    MX2_ALPHA = Assembly({'M1': 'M_CIS', 'X1': 'X', 'X2': 'X'},
                        [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MX2_BETA = Assembly({'M10': 'M_TRANS', 'X10': 'X', 'X20': 'X'},
                        [('M10.a', 'X10.a'), ('M10.b', 'X20.a')])
    COMP_KIND_TO_OBJ = {
        'M_CIS': Component({'a', 'b'}, [('a', 'b', 'cis')]),
        'M_TRANS': Component({'a', 'b'}, [('a', 'b', 'trans')]),
        'X': Component({'a'}),
    }

    hash_mx2_alpha = calc_detailed_graph_hash(MX2_ALPHA, COMP_KIND_TO_OBJ)
    hash_mx2_beta = calc_detailed_graph_hash(MX2_BETA, COMP_KIND_TO_OBJ)

    # Even though the graphs of MX2_ALPHA and MX2_BETA are isomorphic
    # considering only the component kinds, the hashes of them should be
    # different because the kinds of the aux edges are different.
    assert hash_mx2_alpha != hash_mx2_beta


def test_detailed_hash_with_different_configurations():
    COMP_ID_TO_KIND = {
        'M1': 'M', 'L1': 'L', 'L2': 'L',
        'X1': 'X', 'X2': 'X'}
    ML2X2_CIS = Assembly(
        COMP_ID_TO_KIND,
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'),
         ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])
    ML2X2_TRANS = Assembly(
        COMP_ID_TO_KIND,
        [('M1.a', 'L1.a'), ('M1.b', 'X1.a'),
         ('M1.c', 'L2.a'), ('M1.d', 'X2.a')])
    COMP_KIND_TO_OBJ = {
        'M': Component(
            {'a', 'b', 'c', 'd'}, 
            [('a', 'b', 'cis'), ('b', 'c', 'cis'),
             ('c', 'd', 'cis'), ('d', 'a', 'cis')]),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }
    hash_ml2x2_cis = calc_detailed_graph_hash(ML2X2_CIS, COMP_KIND_TO_OBJ)
    hash_ml2x2_trans = calc_detailed_graph_hash(ML2X2_TRANS, COMP_KIND_TO_OBJ)

    # Even though the graphs of ML2_CIS and ML_TRANS are isomorphic
    # considering only the component kinds, the hashes of them should be
    # different because the configurations of the aux edges are different.
    assert hash_ml2x2_cis != hash_ml2x2_trans


# ==========================================
# Tests for calc_rough_wl_hash
# ==========================================
def test_rough_hash_with_same_assemblies():
    MX2_ALPHA = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                     [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MX2_BETA = Assembly({'M10': 'M', 'X10': 'X', 'X20': 'X'},
                     [('M10.a', 'X10.a'), ('M10.b', 'X20.a')])
    hash_mx2_alpha = calc_rough_graph_hash(MX2_ALPHA)
    hash_mx2_beta = calc_rough_graph_hash(MX2_BETA)

    # Since the rough graphs of MX2_ALPHA and MX2_BETA are isomorphic 
    # considering the component kinds, the hashes of them should be 
    # the same.
    assert hash_mx2_alpha == hash_mx2_beta


def test_rough_hash_with_different_component_kinds():
    MX2 = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                   [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    MY2 = Assembly({'M1': 'M', 'Y1': 'Y', 'Y2': 'Y'},
                   [('M1.a', 'Y1.a'), ('M1.b', 'Y2.a')])
    hash_mx2 = calc_rough_graph_hash(MX2)
    hash_my2 = calc_rough_graph_hash(MY2)

    # Even though the rough graphs of MX2 and MY2 are isomorphic without
    # considering the component kinds, the hashes of them should be
    # different because the component kinds (i.e., 'X' and 'Y') are
    # different
    assert hash_mx2 != hash_my2


def test_rough_hash_with_different_connectivities():
    # X1---X2---X3
    LINEAR = Assembly(
        {'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('X1.a', 'X2.a'), ('X2.a', 'X3.a')])
    #    X1
    #  /   \
    # X4----X3
    RING = Assembly(
        {'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('X1.b', 'X2.a'), ('X2.b', 'X3.a'), ('X3.b', 'X1.a')])

    hash_linear = calc_rough_graph_hash(LINEAR)
    hash_ring = calc_rough_graph_hash(RING)

    assert hash_linear != hash_ring


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
