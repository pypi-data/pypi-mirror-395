import networkx as nx
import pytest
import yaml

from nasap_net import Assembly, AuxEdge, Component


@pytest.fixture
def M_COMP() -> Component:
    return Component({'a', 'b', 'c', 'd'})


@pytest.fixture
def M_WITH_AUX_EDGES() -> Component:
    return Component(
        {'a', 'b', 'c', 'd'}, 
        {
            AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
            AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')
        })


@pytest.fixture
def L_COMP() -> Component:
    return Component({'a', 'b'})


@pytest.fixture
def X_COMP() -> Component:
    return Component({'a'})


def test_init_with_no_args() -> None:
    assembly = Assembly()
    assert assembly.comp_id_to_kind == {}
    assert assembly.bonds == set()


def test_init() -> None:
    components = {
        'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'}
    bonds = {
        frozenset(['M1.a', 'X1.a']), frozenset(['M1.b', 'X1.a']),
        frozenset(['M1.c', 'X2.a']), frozenset(['M1.d', 'X3.a']),}
    assembly = Assembly(components, bonds)

    assert assembly.comp_id_to_kind == components
    assert assembly.bonds == set(bonds)


def test_init_with_name() -> None:
    assembly = Assembly(name='MX')
    assert assembly.name == 'MX'


def test_add_component() -> None:
    assembly = Assembly()
    assembly.add_component('M1', 'M')
    assembly.add_component('L1', 'L')
    assembly.add_components([('X1', 'X'), ('X2', 'X'), ('X3', 'X')])
    assembly.add_bond('M1.a', 'X1.a')
    assembly.add_bonds([
        ('M1.b', 'X1.a'), ('M1.c', 'X2.a'), ('M1.d', 'X3.a')])

    assert assembly.comp_id_to_kind == {
        'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'}
    assert assembly.bonds == {
        frozenset(['M1.a', 'X1.a']), frozenset(['M1.b', 'X1.a']),
        frozenset(['M1.c', 'X2.a']), frozenset(['M1.d', 'X3.a'])}


def test_rough_g_snapshot():
    # Test for Issue #31: 
    # https://github.com/Hiraoka-Group/nasap-net/issues/31#issue-2617886112
    
    # In cases where the assembly has parallel bonds, i.e., multiple bonds
    # between the same pair of components, the rough_g_snapshot method 
    # should return a MultiGraph with multiple edges between the same pair
    # of nodes.

    ML_RING = Assembly({'M1': 'M', 'L1': 'L'},
                       [('M1.a', 'L1.a'), ('M1.b', 'L1.b')])

    rough_g = ML_RING.rough_g_snapshot
    
    assert isinstance(rough_g, nx.MultiGraph)
    assert [set(e) for e in rough_g.edges()] == [
        {'M1', 'L1'}, {'M1', 'L1'}]


def test_yaml():
    assembly = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])

    assembly_yaml = yaml.dump(assembly)
    loaded_assembly = yaml.safe_load(assembly_yaml)

    assert assembly == loaded_assembly


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
