from nasap_net.isomorphism import is_isomorphic
from nasap_net.models import Assembly, Bond, Component


def test():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MLX = Assembly(
        components={'M1': M, 'L1': L, 'X1': X},
        bonds=[Bond('M1', 0, 'L1', 0), Bond('M1', 1, 'X1', 0)]
    )
    MLX_permuted = Assembly(
        components={'L1': L, 'X1': X, 'M1': M},
        bonds=[Bond('M1', 1, 'X1', 0), Bond('M1', 0, 'L1', 0)]
    )
    assert is_isomorphic(MLX, MLX_permuted)


def test_same_component_but_different_objects():
    M = Component(kind='M', sites=[1, 2])
    X = Component(kind='X', sites=[1])
    MX = Assembly(
        components={'M1': M, 'X1': X}, bonds=[Bond('M1', 1, 'X1', 1)])

    ANOTHER_M = Component(kind='M', sites=[10, 20])
    ANOTHER_X = Component(kind='X', sites=[10])
    ANOTHER_MX = Assembly(
        components={'M2': ANOTHER_M, 'X2': ANOTHER_X},
        bonds=[Bond('M2', 10, 'X2', 10)])

    assert is_isomorphic(MX, ANOTHER_MX)


def test_different_component_kinds():
    """Components with different kinds should be considered as different,
    even if their structures are identical.
    """
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX = Assembly(
        components={'M1': M, 'X1': X}, bonds=[Bond('M1', 0, 'X1', 0)])

    FAKE_M = Component(kind='ANOTHER_KIND', sites=[0, 1])
    FAKE_MX = Assembly(
        components={'M1': FAKE_M, 'X1': X}, bonds=[Bond('M1', 0, 'X1', 0)])

    assert not is_isomorphic(MX, FAKE_MX)
