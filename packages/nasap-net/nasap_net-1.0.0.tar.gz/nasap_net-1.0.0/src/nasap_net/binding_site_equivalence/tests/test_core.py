import pytest

from nasap_net.binding_site_equivalence import \
    binding_site_combs_equivalent
from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component


@pytest.fixture
def M() -> Component:
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])

@pytest.fixture
def Msq() -> Component:
    return Component(
        kind='Msq',
        sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)]
    )


def test_single_sites(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)
    MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    # X100(0)-(0)M100(1)-(0)L100(1)
    MLX_2 = Assembly(
        components={'X100': X, 'M100': M, 'L100': L},
        bonds=[Bond('X100', 0, 'M100', 0), Bond('M100', 1, 'L100', 0)]
    )
    assert binding_site_combs_equivalent(
        MLX, [BindingSite('M0', 0)],
        MLX_2, [BindingSite('M100', 0)]
    )
    assert not binding_site_combs_equivalent(
        MLX, [BindingSite('M0', 0)],
        MLX_2, [BindingSite('M0', 1)]
    )


def test_component_kinds(M, X):
    DummyX = Component(kind='dummyX', sites=[0])
    # X0(0)-(0)M0(1)-(0)DummyX0
    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'DummyX0': DummyX},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'DummyX0', 0)]
    )
    assert not binding_site_combs_equivalent(
        MX2, [BindingSite('X0', 0)],
        MX2, [BindingSite('DummyX0', 0)]
    )
    assert not binding_site_combs_equivalent(
        MX2, [BindingSite('M0', 0)],
        MX2, [BindingSite('M0', 1)]
    )
