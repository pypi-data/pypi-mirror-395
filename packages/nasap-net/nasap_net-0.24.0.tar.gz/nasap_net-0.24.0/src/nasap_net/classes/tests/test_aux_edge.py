import pytest
import yaml

import nasap_net as rx
from nasap_net import AuxEdge


def test_LocalAuxEdge_initialization():
    edge = AuxEdge('site1', 'site2', 'cis')
    assert edge.local_binding_site1 == 'site1'
    assert edge.local_binding_site2 == 'site2'
    assert edge.aux_kind == 'cis'


def test_LocalAuxEdge_same_binding_sites():
    with pytest.raises(ValueError):
        AuxEdge('site1', 'site1', 'cis')


def test_LocalAuxEdge_equality():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site2', 'site1', 'cis')
    assert edge1 == edge2


def test_LocalAuxEdge_inequality():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site1', 'site3', 'cis')
    assert edge1 != edge2


def test_LocalAuxEdge_hash():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site2', 'site1', 'cis')
    assert hash(edge1) == hash(edge2)


def test_LocalAuxEdge_repr():
    edge = AuxEdge('site1', 'site2', 'cis')
    assert repr(edge) == "AuxEdge('site1', 'site2', 'cis')"


def test_lt():
    edge1 = AuxEdge('d', 'a', 'cis')
    edge2 = AuxEdge('b', 'c', 'cis')
    assert edge1 < edge2
    assert not edge2 < edge1


def test_yaml():
    edge = AuxEdge('a', 'b', 'cis')
    edge_yaml = yaml.dump(edge, default_flow_style=None)
    loaded_edge = yaml.safe_load(edge_yaml)
    assert edge == loaded_edge


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
