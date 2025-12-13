import pytest

from nasap_net import Assembly, Component, assemblies_equal, perform_inter_exchange


def test_inter_exchange() -> None:
    # X1(a)--(a)M1(a)--(a)X2
    MX2 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X'},
        [('X1.a', 'M1.a'), ('M1.b', 'X2.a')])
    # (a)L1(b)
    L = Assembly({'L1': 'L'}, [])
    # expected product: MLX
    # (b)L1(a)--(a)M1(b)--(a)X2
    MLX = Assembly(
        {'M1': 'M', 'L1': 'L', 'X2': 'X'},
        [('L1.a', 'M1.a'), ('M1.b', 'X2.a')])
    MLX = MLX.rename_component_ids(
        {'M1': 'init_M1', 'L1': 'entering_L1', 'X2': 'init_X2'})
    X = Assembly({'X1': 'X'}, [])
    X = X.rename_component_ids({'X1': 'init_X1'})
    
    COMPONENT_KINDS = {
        'M': Component({'a', 'b'}),
        'L': Component({'a'}),
        'X': Component({'a'})}
    
    product, leaving = perform_inter_exchange(
        MX2, L, 'M1.a', 'X1.a', 'L1.a')

    assert assemblies_equal(product, MLX, COMPONENT_KINDS)
    assert leaving is not None
    assert assemblies_equal(leaving, X, COMPONENT_KINDS)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
