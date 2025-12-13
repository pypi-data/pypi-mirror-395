from nasap_net.assembly_enumeration import enumerate_assemblies
from nasap_net.helpers import assign_composition_formula_ids
from nasap_net.models import Assembly, AuxEdge, Bond, Component, MLEKind
from nasap_net.reaction_exploration_im import explore_reactions


def test_M4L4():
    #  M3---L2---M2
    #  |         |
    #  L3        L1
    #  |         |
    #  M0---L0---M1
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M4L4 = Assembly(
        components={
            'M0': M, 'M1': M, 'M2': M, 'M3': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M2', 0),
            Bond('M2', 1, 'L2', 0), Bond('L2', 1, 'M3', 0),
            Bond('M3', 1, 'L3', 0), Bond('L3', 1, 'M0', 0),
        ]
    )

    assemblies = enumerate_assemblies(
        template=M4L4,
        leaving_ligand=X,
        metal_kinds=['M'],
    )
    assert len(assemblies) == 14

    indexed_assemblies = assign_composition_formula_ids(
        assemblies=assemblies,
        order=['M', 'L', 'X'],
    )

    reactions = explore_reactions(
        assemblies=indexed_assemblies,
        mle_kinds=[MLEKind(metal='M', leaving='X', entering='L')],
    )
    reactions_list = list(reactions)
    assert len(reactions_list) == 29


def test_M2L4():
    #                 |                                     |
    #                (1)                                   (0)
    #                 L2                                    L2
    #                (0)                                   (1)
    #                 |                                     |
    #                (2)                                   (2)
    # --(1)L3(0)---(3)M0(1)---(0)L1(1)--    --(0)L3(1)---(3)M1(1)---(1)L1(0)--
    #                (0)                                   (0)
    #                 |                                     |
    #                (0)                                   (1)
    #                 L0                                    L0
    #                (1)                                   (0)
    #                 |                                     |
    M = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M2L4 = Assembly(
        components={
            'M0': M, 'M1': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 0, 'L0', 0), Bond('M0', 1, 'L1', 0),
            Bond('M0', 2, 'L2', 0), Bond('M0', 3, 'L3', 0),
            Bond('M1', 0, 'L0', 1), Bond('M1', 1, 'L1', 1),
            Bond('M1', 2, 'L2', 1), Bond('M1', 3, 'L3', 1),
        ]
    )

    assemblies = enumerate_assemblies(
        template=M2L4,
        leaving_ligand=X,
        metal_kinds=['M'],
    )
    assert len(assemblies) == 29

    indexed_assemblies = assign_composition_formula_ids(
        assemblies=assemblies,
        order=['M', 'L', 'X'],
    )

    reactions = explore_reactions(
        assemblies=indexed_assemblies,
        mle_kinds=[MLEKind(metal='M', leaving='X', entering='L')],
    )
    reactions_list = list(reactions)
    assert len(reactions_list) == 68
