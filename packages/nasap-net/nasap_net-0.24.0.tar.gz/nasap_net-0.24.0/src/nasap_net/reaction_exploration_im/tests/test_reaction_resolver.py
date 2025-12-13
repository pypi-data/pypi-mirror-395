import pytest

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component, \
    Reaction
from nasap_net.reaction_exploration_im.reaction_resolver import \
    ReactionOutOfScopeError, ReactionResolver


@pytest.fixture
def M() -> Component:
    return Component(
        kind='M', sites=[0, 1],
        aux_edges=[AuxEdge(0, 1)])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X) -> Assembly:
    """X0(0)-(0)M0(1)-(0)X1"""
    return Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )

@pytest.fixture
def free_L(L) -> Assembly:
    return Assembly(id_='free_L', components={'L0': L}, bonds=[])

@pytest.fixture
def MLX(M, L, X) -> Assembly:
    """X0(0)-(0)M0(1)-(0)L0(1)"""
    return Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)
        ]
    )

@pytest.fixture
def unresolved_MLX(M, L, X) -> Assembly:
    """X0#(0)-(0)M0#(1)-(0)L0#(1)"""
    return Assembly(
        components={'X0#': X, 'M0#': M, 'L0#': L},
        bonds=[Bond('X0#', 0, 'M0#', 0), Bond('M0#', 1, 'L0#', 0)
        ]
    )

@pytest.fixture
def free_X(X) -> Assembly:
    return Assembly(id_='free_X', components={'X0': X}, bonds=[])

@pytest.fixture
def unresolved_free_X(X) -> Assembly:
    # No Assembly ID
    return Assembly(components={'X0#': X}, bonds=[])


def test_inter(MX2, free_L, MLX, unresolved_MLX, free_X, unresolved_free_X):
    resolver = ReactionResolver([MX2, free_L, MLX, free_X])
    reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=unresolved_MLX,
        leaving_assem=unresolved_free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )
    result = resolver.resolve(reaction)
    assert result == Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )


def test_reaction_out_of_scope_error(
        MX2, free_L, MLX, unresolved_MLX,
        free_X, unresolved_free_X):
    reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=unresolved_free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )
    resolver1 = ReactionResolver([MX2, free_L, MLX])  # missing free_X
    resolver2 = ReactionResolver([MX2, free_L, free_X])  # missing MLX
    resolver3 = ReactionResolver([MX2, free_L])  # missing both
    with pytest.raises(ReactionOutOfScopeError):
        resolver1.resolve(reaction)
    with pytest.raises(ReactionOutOfScopeError):
        resolver2.resolve(reaction)
    with pytest.raises(ReactionOutOfScopeError):
        resolver3.resolve(reaction)


@pytest.fixture
def M2L2X(M, L, X) -> Assembly:
    """
    X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(0)-(0)L1(1)
    """
    return Assembly(
        id_='ML2X',
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ]
    )


@pytest.fixture
def ring(M, L, X) -> Assembly:
    """
    /-(0)M0(1)-(0)L0(1)-(0)M1(0)-(0)L1(1)-/
    """
    return Assembly(
        id_='ML2_ring',
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
            Bond('L1', 1, 'M0', 0),
        ]
    )


@pytest.fixture
def unresolved_ring(M, L, X) -> Assembly:
    """
    /-(0)M0#(1)-(0)L0#(1)-(0)M1#(0)-(0)L1#(1)-/
    """
    # No Assembly ID
    return Assembly(
        components={'M0#': M, 'L0#': L, 'M1#': M, 'L1#': L},
        bonds=[
            Bond('M0#', 1, 'L0#', 0),
            Bond('L0#', 1, 'M1#', 0),
            Bond('M1#', 1, 'L1#', 0),
            Bond('L1#', 1, 'M0#', 0),
        ]
    )


def test_intra(
        M2L2X, free_X, unresolved_free_X,
        ring, unresolved_ring):
    resolver = ReactionResolver([M2L2X, free_X, ring])
    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=unresolved_ring,
        leaving_assem=unresolved_free_X,
        metal_bs=BindingSite('M0', 1),
        leaving_bs=BindingSite('X1', 0),
        entering_bs=BindingSite('L1', 1),
        duplicate_count=2
    )
    result = resolver.resolve(reaction)
    assert result == Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=ring,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 1),
        leaving_bs=BindingSite('X1', 0),
        entering_bs=BindingSite('L1', 1),
        duplicate_count=2
    )
