import pytest

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component, \
    MLE, MLEKind, Reaction
from nasap_net.reaction_enumeration.explorer import IntraReactionExplorer


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
def M2L2X5(M, L, X) -> Assembly:
    """
    .. code-block::

                 X2                 X3
                (0)                (0)
                 |                  |
                (2)                (1)
        X1(0)-(1)M0(3)-(0)L0(1)-(0)M1(2)-(0)L1(1)
                (0)                (3)
                 |                  |
                (0)                (0)
                 X0                 X4
    """
    return Assembly(
        id_='M2L2X5',
        components={
            'M0': M, 'X0': X, 'X1': X, 'X2': X,
            'L0': L,
            'M1': M, 'X3': X, 'L1': L, 'X4': X
        },
        bonds=[
            Bond('M0', 0, 'X0', 0),
            Bond('M0', 1, 'X1', 0),
            Bond('M0', 2, 'X2', 0),
            Bond('M0', 3, 'L0', 0),
            Bond('M1', 0, 'L0', 1),
            Bond('M1', 1, 'X3', 0),
            Bond('M1', 2, 'L1', 0),
            Bond('M1', 3, 'X4', 0),
        ]
    )

@pytest.fixture
def trans_ring(M, L, X) -> Assembly:
    """
    .. code-block::

             X2                 X3
            (0)                (0)
             |                  |
            (2)                (1)
        /-(1)M0(3)-(0)L0(1)-(0)M1(2)-(0)L1(1)-/
            (0)                (3)
             |                  |
            (0)                (0)
             X0                 X4
    """
    return Assembly(
        components={
            'M0': M, 'X0': X, 'X2': X,
            'L0': L,
            'M1': M, 'X3': X, 'L1': L, 'X4': X
        },
        bonds=[
            Bond('M0', 0, 'X0', 0),
            Bond('M0', 1, 'L1', 1),
            Bond('M0', 2, 'X2', 0),
            Bond('M0', 3, 'L0', 0),
            Bond('M1', 0, 'L0', 1),
            Bond('M1', 1, 'X3', 0),
            Bond('M1', 2, 'L1', 0),
            Bond('M1', 3, 'X4', 0),
        ]
    )

@pytest.fixture
def cis_ring(M, L, X) -> Assembly:
    """
    .. code-block::

                 X2                 X3
                (0)                (0)
                 |                  |
                (2)                (1)
        X1(0)-(1)M0(3)-(0)L0(1)-(0)M1(2)-(0)L1(1)-/
                (0)                (3)
                 |                  |
                 /                 (0)
                                    X4
    """
    return Assembly(
        components={
            'M0': M, 'X1': X, 'X2': X,
            'L0': L,
            'M1': M, 'X3': X, 'L1': L, 'X4': X
        },
        bonds=[
            Bond('M0', 0, 'L1', 1),
            Bond('M0', 1, 'X1', 0),
            Bond('M0', 2, 'X2', 0),
            Bond('M0', 3, 'L0', 0),
            Bond('M1', 0, 'L0', 1),
            Bond('M1', 1, 'X3', 0),
            Bond('M1', 2, 'L1', 0),
            Bond('M1', 3, 'X4', 0),
        ]
    )


@pytest.fixture
def free_X0(X) -> Assembly:
    return Assembly(
        components={'X0': X},
        bonds=[]
    )


@pytest.fixture
def free_X1(X) -> Assembly:
    return Assembly(
        components={'X1': X},
        bonds=[]
    )


def test_explore(M2L2X5, trans_ring, cis_ring, free_X0, free_X1):
    explorer = IntraReactionExplorer(M2L2X5, MLEKind('M', 'X', 'L'))
    assert set(explorer.explore()) == {
        Reaction(
            init_assem=M2L2X5,
            entering_assem=None,
            product_assem=trans_ring,
            leaving_assem=free_X1,
            metal_bs=BindingSite('M0', 1),
            leaving_bs=BindingSite('X1', 0),
            entering_bs=BindingSite('L1', 1),
            duplicate_count=1
        ),
        Reaction(
            init_assem=M2L2X5,
            entering_assem=None,
            product_assem=cis_ring,
            leaving_assem=free_X0,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('X0', 0),
            entering_bs=BindingSite('L1', 1),
            duplicate_count=2
        )
    }


def test__iter_mles(M2L2X5):
    explorer = IntraReactionExplorer(M2L2X5, MLEKind('M', 'X', 'L'))
    mles = set(explorer._iter_mles())
    assert mles == {
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L1', 1)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L1', 1)),
        MLE(BindingSite('M0', 2), BindingSite('X2', 0), BindingSite('L1', 1)),
    }


def test__get_unique_mles(M2L2X5):
    explorer = IntraReactionExplorer(M2L2X5, MLEKind('M', 'X', 'L'))
    mles = {
        MLE(BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L1', 1)),
        MLE(BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L1', 1)),
        MLE(BindingSite('M0', 2), BindingSite('X2', 0), BindingSite('L1', 1)),
    }
    assert set(explorer._get_unique_mles(mles)) == {
        MLE(
            BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L1', 1),
            duplication=2
        ),
        MLE(
            BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L1', 1),
            duplication=1
        ),
    }


def test__perform_reaction(M2L2X5, trans_ring, free_X1):
    explorer = IntraReactionExplorer(M2L2X5, MLEKind('M', 'X', 'L'))
    mle_with_dup = MLE(
        BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L1', 1),
        duplication=1
    )

    assert explorer._perform_reaction(mle_with_dup) == Reaction(
        init_assem=M2L2X5,
        entering_assem=None,
        product_assem=trans_ring,
        leaving_assem=free_X1,
        metal_bs=BindingSite('M0', 1),
        leaving_bs=BindingSite('X1', 0),
        entering_bs=BindingSite('L1', 1),
        duplicate_count=1
    )
