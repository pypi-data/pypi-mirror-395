import pytest

from nasap_net import Assembly
from nasap_net.algorithms.isomorphism import rough_isomorphisms_iter
from nasap_net.utils import compare_mapping_iterables


def test_rough_isomorphisms_iter():
    ML2X2 = Assembly(
        {'M1': 'M', 'L1': 'L', 'L2': 'L', 'X1': 'X', 'X2': 'X'},
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'), ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])
    
    isomorphisms = list(rough_isomorphisms_iter(ML2X2, ML2X2))

    expected = [
        {'M1': 'M1', 'L1': 'L1', 'L2': 'L2', 'X1': 'X1', 'X2': 'X2'},
        {'M1': 'M1', 'L1': 'L1', 'L2': 'L2', 'X1': 'X2', 'X2': 'X1'},
        {'M1': 'M1', 'L1': 'L2', 'L2': 'L1', 'X1': 'X1', 'X2': 'X2'},
        {'M1': 'M1', 'L1': 'L2', 'L2': 'L1', 'X1': 'X2', 'X2': 'X1'},
    ]

    assert len(isomorphisms) == 4
    assert {'M1': 'M1', 'L1': 'L1', 'L2': 'L2', 'X1': 'X1', 'X2': 'X2'} in isomorphisms
    assert {'M1': 'M1', 'L1': 'L1', 'L2': 'L2', 'X1': 'X2', 'X2': 'X1'} in isomorphisms
    assert {'M1': 'M1', 'L1': 'L2', 'L2': 'L1', 'X1': 'X1', 'X2': 'X2'} in isomorphisms
    assert {'M1': 'M1', 'L1': 'L2', 'L2': 'L1', 'X1': 'X2', 'X2': 'X1'} in isomorphisms
    assert compare_mapping_iterables(isomorphisms, expected)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
