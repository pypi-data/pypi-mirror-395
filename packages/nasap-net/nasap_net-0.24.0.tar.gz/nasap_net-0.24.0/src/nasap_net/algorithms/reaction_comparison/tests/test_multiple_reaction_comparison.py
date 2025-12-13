import random
from copy import deepcopy
from typing import TypeAlias

import pytest

from nasap_net import Assembly, Component, InterReaction, IntraReaction
from nasap_net.algorithms import are_equivalent_reaction_sets
from nasap_net.algorithms.reaction_comparison.multiple_reaction_comparison import \
    _group_reactions

Reaction: TypeAlias = IntraReaction | InterReaction


@pytest.fixture
def component_structures():
    return {
        'L': Component(['a', 'b']),
        'M': Component(['a', 'b']),
        'X': Component(['a']),
    }


@pytest.fixture
def id_to_assembly():
    return {
        # MX2: X0(a)-(a)M0(b)-(a)X1
        0: Assembly(
            {'M0': 'M', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'X1.a')]
        ),
        1: Assembly({'L0': 'L'}),  # L: (a)L0(b)
        2: Assembly({'X0': 'X'}),  # X: (a)X0
        # MLX: (a)L0(b)-(a)M0(b)-(a)X0
        3: Assembly(
            {'M0': 'M', 'L0': 'L', 'X0': 'X'},
            [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
        ),
        # ML2: (a)L0(b)-(a)M0(b)-(a)L1(b)
        4: Assembly(
            {'M0': 'M', 'L0': 'L', 'L1': 'L'},
            [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
        ),
        # M2L2X: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)
        5: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'X0': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'L1.a')]
        ),
        # M2LX2: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)X1
        6: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'X1.a')]
        ),
        # M2L2-ring: //-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)-//
        7: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L'},
            [('M0.b', 'L0.a'), ('L0.b', 'M1.a'), ('M1.b', 'L1.a'),
             ('L1.b', 'M0.a')]
        ),
    }


def test_list_with_single_reaction(component_structures, id_to_assembly):
    # MX2 + L -> MLX + X
    reaction1 = InterReaction(
        init_assem_id=0, entering_assem_id=1,
        product_assem_id=3, leaving_assem_id=2,
        metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
        duplicate_count=4,
    )
    # Equivalent reaction
    reaction2 = InterReaction(
        init_assem_id=0, entering_assem_id=1,
        product_assem_id=3, leaving_assem_id=2,
        metal_bs='M0.b',  # Different metal binding site
        leaving_bs='X1.a',  # Different leaving binding site
        entering_bs='L0.a',
        duplicate_count=4,
    )

    assert are_equivalent_reaction_sets(
        [reaction1], [reaction2], id_to_assembly, component_structures)


def test_list_with_multiple_reactions(component_structures, id_to_assembly):
    # MX2 + L -> MLX + X
    reaction1 = InterReaction(
        init_assem_id=0, entering_assem_id=1,
        product_assem_id=3, leaving_assem_id=2,
        metal_bs='M0.a', leaving_bs='X0.a',
        entering_bs='L0.a', duplicate_count=4,
    )
    # Equivalent reaction
    reaction2 = InterReaction(
        init_assem_id=0, entering_assem_id=1,
        product_assem_id=3, leaving_assem_id=2,
        metal_bs='M0.b',  # Different metal binding site
        leaving_bs='X1.a',  # Different leaving binding site
        entering_bs='L0.a',
        duplicate_count=4,
    )

    # Add an additional assembly M2L3
    # M2L3: (a)L0(b)-(a)M0(b)-(a)L1(b)-(a)M1(b)-(a)L2(b)
    id_to_assembly[8] = Assembly(
        {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'L2': 'L'},
        [('L0.b', 'M0.a'), ('M0.b', 'L1.a'), ('L1.b', 'M1.a'),
         ('M1.b', 'L2.a')]
    )

    # M2L3 is needed for "the equivalent intra-molecular reactions
    # with different binding sites" described below.

    # M2L3 -> M2L2-ring + L
    reaction3 = IntraReaction(
        init_assem_id=8, product_assem_id=7,
        leaving_assem_id=1, metal_bs='M0.a',
        leaving_bs='L0.b', entering_bs='L2.b', duplicate_count=2,
    )
    # Equivalent reaction
    reaction4 = IntraReaction(
        init_assem_id=8, product_assem_id=7, leaving_assem_id=1,
        metal_bs='M1.b',  # Different metal binding site
        leaving_bs='L2.a',  # Different leaving binding site
        entering_bs='L0.a',
        duplicate_count=2,
    )

    assert are_equivalent_reaction_sets(
        [reaction1, reaction3], [reaction2, reaction4], id_to_assembly,
        component_structures)


def test_comprehensive_reaction_sets(component_structures, id_to_assembly):

    # All "X to L" reactions among the assemblies in id_to_assembly
    # including intra- and inter-molecular reactions:
    reactions1: dict[str, Reaction] = {
        # Intra-molecular reactions
        'M2L2X -> M2L2-ring + X': IntraReaction(
            init_assem_id=5, 
            product_assem_id=7, leaving_assem_id=2, 
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L1.b',
            duplicate_count=1,
        ),
        # Inter-molecular reactions
        'MX2 + L -> MLX + X': InterReaction(
            init_assem_id=0, entering_assem_id=1,
            product_assem_id=3, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
        'MX2 + MLX -> M2LX2 + X': InterReaction(
            init_assem_id=0, entering_assem_id=3,
            product_assem_id=6, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'MX2 + ML2 -> M2L2X + X': InterReaction(
            init_assem_id=0, entering_assem_id=4,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
        'MLX + L -> ML2 + X': InterReaction(
            init_assem_id=3, entering_assem_id=1,
            product_assem_id=4, leaving_assem_id=2,
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'MLX + MLX -> M2L2X + X': InterReaction(
            init_assem_id=3, entering_assem_id=3,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'M2LX2 + L -> M2L2X + X': InterReaction(
            init_assem_id=6, entering_assem_id=1,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
    }
    
    reactions2 = deepcopy(reactions1)

    # Use different binding sites for some reactions
    reactions2['MX2 + L -> MLX + X'] = InterReaction(
            init_assem_id=0, entering_assem_id=1,
            product_assem_id=3, leaving_assem_id=2,
            # Different metal and leaving binding sites
            metal_bs='M0.b', leaving_bs='X1.a', entering_bs='L0.a',
            duplicate_count=4,
        )
    reactions2['MLX + L -> ML2 + X'] = InterReaction(
            init_assem_id=3, entering_assem_id=1,
            product_assem_id=4, leaving_assem_id=2,
            # Different entering binding site
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.b',
            duplicate_count=2,
        )
    reactions2['M2LX2 + L -> M2L2X + X'] = InterReaction(
            init_assem_id=6, entering_assem_id=1,
            product_assem_id=5, leaving_assem_id=2,
            # Different metal, leaving, and entering binding sites
            metal_bs='M1.b', leaving_bs='X1.a', entering_bs='L0.b',
            duplicate_count=4,
        )
    
    reaction_list1 = list(reactions1.values())
    reaction_list2 = list(reactions2.values())

    # Randomly shuffle the reaction_list2
    random.shuffle(reaction_list2)

    assert are_equivalent_reaction_sets(
        reaction_list1, reaction_list2, id_to_assembly,
        component_structures
    ), "The two sets of reactions should be equivalent."


def test_group_reactions_basic():
    # Two reactions with the same grouping key, one with a different key
    r1 = InterReaction(
        init_assem_id=1, entering_assem_id=2,
        product_assem_id=3, leaving_assem_id=4,
        metal_bs='a', leaving_bs='a', entering_bs='a',
        duplicate_count=1,
    )
    r2 = InterReaction(
        # same assemblies
        init_assem_id=1, entering_assem_id=2,
        product_assem_id=3, leaving_assem_id=4,
        # different binding sites
        metal_bs='b', leaving_bs='b', entering_bs='b',
        # different duplicate count
        duplicate_count=2,
    )
    r3 = InterReaction(
        # different assemblies
        init_assem_id=5, entering_assem_id=6,
        product_assem_id=7, leaving_assem_id=8,
        # same binding sites
        metal_bs='a', leaving_bs='a', entering_bs='a',
        # same duplicate count
        duplicate_count=1,
    )
    grouped = _group_reactions([r1, r2, r3])
    assert len(grouped) == 2
    key1 = (1, 2, 3, 4)
    key3 = (5, 6, 7, 8)
    assert key1 in grouped and key3 in grouped
    assert grouped[key1] == [r1, r2] or grouped[key1] == [r2, r1]
    assert grouped[key3] == [r3]


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
