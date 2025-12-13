import pytest
import yaml

from nasap_net import AuxEdge, Component


def test_typical_usage():
    binding_sites = ['a', 'b', 'c', 'd']
    aux_edges = [('a', 'b', 'cis'), ('b', 'c', 'cis'),
                 ('c', 'd', 'cis'), ('d', 'a', 'cis')]
    M = Component(binding_sites, aux_edges)
    assert M.binding_sites == set(binding_sites)
    assert M.aux_edges == {AuxEdge(*edge) for edge in aux_edges}


def test_init():
    binding_sites = {'a', 'b'}
    M = Component(binding_sites)
    assert M.binding_sites == binding_sites
    assert M.aux_edges == set()


def test_init_with_binding_sites_of_type_tuple():
    binding_sites = ['a', 'b']
    M = Component(binding_sites)
    assert M.binding_sites == set(binding_sites)
    assert M.aux_edges == set()


def test_init_with_aux_edges():
    binding_sites = {'a', 'b'}
    aux_edges = {AuxEdge('a', 'b', 'cis')}
    M = Component(binding_sites, aux_edges)
    assert M.binding_sites == binding_sites
    assert M.aux_edges == aux_edges


def test_init_with_aux_edges_of_type_tuple():
    binding_sites = {'a', 'b'}
    aux_edges = [('a', 'b', 'cis')]
    M = Component(binding_sites, aux_edges)
    assert M.binding_sites == binding_sites
    assert M.aux_edges == {AuxEdge(*edge) for edge in aux_edges}


def test_init_with_empty_binding_sites():
    # Raises no error.
    M = Component(set())
    assert M.binding_sites == set()


def test_init_with_empty_aux_edges():
    # Raises no error.
    M = Component({'a', 'b'}, set())
    assert M.aux_edges == set()


def test_init_with_invalid_aux_edge():
    with pytest.raises(ValueError):
        # The binding site 'c' is not in the binding sites.
        Component({'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_eq():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    assert M1 == M2


def test_eq_with_different_binding_sites():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'c'}, {AuxEdge('a', 'c', 'cis')})
    assert M1 != M2


def test_eq_with_different_aux_edges():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'trans')})
    assert M1 != M2


def test_yaml_serialization():
    M = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M_yaml = yaml.dump(M, default_flow_style=None)
    loaded_M = yaml.safe_load(M_yaml)
    assert M == loaded_M


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
