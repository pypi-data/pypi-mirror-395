import pytest

from nasap_net import Assembly
from nasap_net.reaction_classification.utils import find_shortest_path


def test():
    assembly = Assembly()
    assembly.add_components([('M0', 'M'), ('L0', 'L'), ('X0', 'X')])
    assembly.add_bonds([('M0.a', 'L0.a'), ('M0.b', 'X0.a')])

    assert find_shortest_path(assembly, 'M0', 'X0') == ['M0', 'X0']
    assert find_shortest_path(assembly, 'M0', 'L0') == ['M0', 'L0']
    assert find_shortest_path(assembly, 'L0', 'X0') == ['L0', 'M0', 'X0']


def test_no_path():
    assembly = Assembly()
    assembly.add_components([('M0', 'M'), ('L0', 'L'), ('X0', 'X')])
    assembly.add_bonds([('M0.a', 'L0.a')])

    assert find_shortest_path(assembly, 'M0', 'X0') is None
    assert find_shortest_path(assembly, 'M0', 'L0') == ['M0', 'L0']
    assert find_shortest_path(assembly, 'L0', 'X0') is None


def test_not_in_assembly():
    assembly = Assembly()
    assembly.add_components([('M0', 'M'), ('L0', 'L'), ('X0', 'X')])
    assembly.add_bonds([('M0.a', 'L0.a')])

    with pytest.raises(ValueError):
        find_shortest_path(assembly, 'M0', 'Y0')
    with pytest.raises(ValueError):
        find_shortest_path(assembly, 'Y0', 'M0')


if __name__ == '__main__':
    pytest.main(['-v', __file__])
