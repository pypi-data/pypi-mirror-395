import pytest

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component, \
    Reaction
from nasap_net.reaction_equivalence import reactions_equivalent


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


def test_inter_equivalence(M, L, X):
    # MX2 + L -> MLX + X
    MX2 = Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(components={'L0': L}, bonds=[])
    MLX = Assembly(
        components={'M0': M, 'L0': L, 'X1': X},
        bonds=[Bond('M0', 0, 'L0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_X = Assembly(components={'X0': X}, bonds=[])

    reaction1 = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )

    # Renamed components
    MX2_renamed = Assembly(
        components={'init_M0': M, 'init_X0': X, 'init_X1': X},
        bonds=[Bond('init_M0', 0, 'init_X0', 0), Bond('init_M0', 1, 'init_X1', 0)]
    )
    free_L_renamed = Assembly(components={'entering_L0': L}, bonds=[])
    MLX_renamed = Assembly(
        components={'init_M0': M, 'entering_L0': L, 'init_X1': X},
        bonds=[Bond('init_M0', 0, 'entering_L0', 0), Bond('init_M0', 1, 'init_X1', 0)]
    )
    free_X_renamed = Assembly(components={'init_X0': X}, bonds=[])

    reaction2 = Reaction(
        init_assem=MX2_renamed,
        entering_assem=free_L_renamed,
        product_assem=MLX_renamed,
        leaving_assem=free_X_renamed,
        metal_bs=BindingSite('init_M0', 0),
        leaving_bs=BindingSite('init_X0', 0),
        entering_bs=BindingSite('entering_L0', 0),
        duplicate_count=4
    )

    assert reactions_equivalent(reaction1, reaction2)