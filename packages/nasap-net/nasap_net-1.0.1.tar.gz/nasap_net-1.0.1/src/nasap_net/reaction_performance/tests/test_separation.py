import pytest

from nasap_net.models import Assembly, Bond, Component
from nasap_net.reaction_performance.separation import \
    SeparatedIntoMoreThanTwoPartsError, separate_if_possible


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X():
    return Component(kind='X', sites=[0])


def test_separation(M, L, X):
    # disconnected_MLX: X0(0)-(0)M0(1) + (0)L0(1)
    disconnected_MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0)]
    )
    MX = Assembly({'X0': X, 'M0': M}, [Bond('X0', 0, 'M0', 0)])
    L = Assembly({'L0': L}, [])
    result = separate_if_possible(disconnected_MLX, metal_comp_id='M0')
    assert result == (MX, L)


def test_no_separation(M, L, X):
    # connected_MLX: X0(0)-(0)M0(1)-(0)L0(1)
    connected_MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    MX = Assembly({'X0': X, 'M0': M}, [Bond('X0', 0, 'M0', 0)])
    result = separate_if_possible(connected_MLX, metal_comp_id='M0')
    assert result == (connected_MLX, None)


def test_separation_error(M, L, X):
    # invalid_MLX: (0)M0(1) + (0)X0 + (0)L0(1)
    invalid_MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[]
    )
    with pytest.raises(SeparatedIntoMoreThanTwoPartsError):
        separate_if_possible(invalid_MLX, metal_comp_id='M0')
