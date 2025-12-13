import pytest

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component, \
    MLE, MLEKind, Reaction
from nasap_net.reaction_exploration_im.explorer import InterReactionExplorer


@pytest.fixture
def M() -> Component:
    return Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X) -> Assembly:
    return Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)])

@pytest.fixture
def free_L(L) -> Assembly:
    return Assembly(components={'L0': L}, bonds=[])


def test_explore(MX2, free_L, M, L, X):
    renamed_MLX = Assembly(
        {'init_M0': M, 'entering_L0': L, 'init_X1': X},
        [Bond('init_M0', 0, 'entering_L0', 0),
         Bond('init_M0', 1, 'init_X1', 0)]
    )
    renamed_X = Assembly(
        {'init_X0': X},
        []
    )
    explorer = InterReactionExplorer(MX2, free_L, MLEKind('M', 'X', 'L'))
    reactions = list(explorer.explore())
    assert set(reactions) == {
        Reaction(
            init_assem=MX2,
            entering_assem=free_L,
            product_assem=renamed_MLX,
            leaving_assem=renamed_X,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('X0', 0),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=4
        )
    }


def test__iter_mles(MX2, free_L):
    explorer = InterReactionExplorer(MX2, free_L, MLEKind('M', 'X', 'L'))
    mles = set(explorer._iter_mles())
    assert mles == {
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 0)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L0', 0)),
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 1)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L0', 1)),
    }


def test__get_unique_mles(MX2, free_L):
    explorer = InterReactionExplorer(MX2, free_L, MLEKind('M', 'X', 'L'))
    mles = {
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 0)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L0', 0)),
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 1)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L0', 1)),
    }
    assert set(explorer._get_unique_mles(mles)) == {
        MLE(
            BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 0),
            duplication=4),
    }


def test__perform_reaction(MX2, free_L, M, L, X):
    # NOTE: Component IDs in the assemblies are renamed to avoid ID conflicts.
    renamed_MLX = Assembly(
        {'init_M0': M, 'entering_L0': L, 'init_X1': X},
        [Bond('init_M0', 0, 'entering_L0', 0),
         Bond('init_M0', 1, 'init_X1', 0)]
    )
    renamed_X = Assembly(
        {'init_X0': X},
        []
    )
    explorer = InterReactionExplorer(MX2, free_L, MLEKind('M', 'X', 'L'))
    mle_with_dup = MLE(
        BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 0),
        duplication=4)
    assert explorer._perform_reaction(mle_with_dup) == Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=renamed_MLX,
        leaving_assem=renamed_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4
    )
