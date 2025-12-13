import pytest

from nasap_net import Assembly, Component, assemblies_equal, perform_intra_exchange


def test_intra_exchange() -> None:
    # X1(a)--(a)M1(b)--(a)L1(b)
    MLX = Assembly(
        {'M1': 'M', 'X1': 'X', 'L1': 'L'},
        [('X1.a', 'M1.a'), ('M1.b', 'L1.a')])
    # Expected product: ML ring
    ML_RING = Assembly(
        {'M1': 'M', 'L1': 'L'},
        [('M1.b', 'L1.a'), ('L1.b', 'M1.a')])
    # Expected leaving: X
    X = Assembly({'X1': 'X'}, [])

    COMPONENT_KINDS = {
        'M': Component({'a', 'b'}),
        'L': Component({'a', 'b'}),
        'X': Component({'a'})}
    
    product, leaving = perform_intra_exchange(
        MLX, 'M1.a', 'X1.a', 'L1.b')

    assert assemblies_equal(product, ML_RING, COMPONENT_KINDS)
    assert leaving is not None
    assert assemblies_equal(leaving, X, COMPONENT_KINDS)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
