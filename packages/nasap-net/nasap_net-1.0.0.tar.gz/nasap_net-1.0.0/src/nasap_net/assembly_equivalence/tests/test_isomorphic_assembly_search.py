import pytest

from nasap_net.assembly_equivalence import AssemblyNotFoundError, \
    EquivalentAssemblyFinder
from nasap_net.models import Assembly, Bond, Component


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X():
    return Component(kind='X', sites=[0])


def test_find(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)
    MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    another_MLX = Assembly(
        components={'X1': X, 'M1': M, 'L1': L},
        bonds=[Bond('X1', 0, 'M1', 0), Bond('M1', 1, 'L1', 0)]
    )

    finder = EquivalentAssemblyFinder(search_space=[another_MLX])
    result = finder.find(MLX)
    assert result == another_MLX


def test_not_found_error(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)
    MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    # X0(0)-(0)M0(1)
    MX = Assembly(
        components={'X0': X, 'M0': M},
        bonds=[Bond('X0', 0, 'M0', 0)]
    )

    finder = EquivalentAssemblyFinder(search_space=[MX])
    with pytest.raises(AssemblyNotFoundError):
        finder.find(MLX)


def test_duplicate_assemblies_not_raise_error(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)
    MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    another_MLX = Assembly(
        components={'X1': X, 'M1': M, 'L1': L},
        bonds=[Bond('X1', 0, 'M1', 0), Bond('M1', 1, 'L1', 0)]
    )
    duplicate_MLX = Assembly(
        components={'X2': X, 'M2': M, 'L2': L},
        bonds=[Bond('X2', 0, 'M2', 0), Bond('M2', 1, 'L2', 0)]
    )

    finder = EquivalentAssemblyFinder(
        search_space=[another_MLX, duplicate_MLX],
    )
    result = finder.find(MLX)
    assert result in {another_MLX, duplicate_MLX}
