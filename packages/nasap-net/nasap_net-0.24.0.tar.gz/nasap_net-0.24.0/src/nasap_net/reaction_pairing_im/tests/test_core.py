import pytest

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component, \
    Reaction
from nasap_net.reaction_pairing_im import pair_reverse_reactions


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


def test_basic(M, L, X):
    MX2 = Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(id_='free_L', components={'L0': L}, bonds=[])
    MLX = Assembly(
        id_='MLX',
        components={'L0': L, 'M0': M, 'X1': X},
        bonds=[Bond('L0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])

    forward = Reaction(
        id_='forward',
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )
    backward = Reaction(
        id_='backward',
        init_assem=MLX,
        entering_assem=free_X,
        product_assem=MX2,
        leaving_assem=free_L,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('L0', 0),
        entering_bs=BindingSite('X0', 0),
        duplicate_count=1
    )

    assert pair_reverse_reactions([forward, backward]) == {
        'forward': 'backward',
        'backward': 'forward',
    }
