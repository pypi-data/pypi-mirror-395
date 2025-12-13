from typing import TypeAlias

import pytest

from nasap_net import (Assembly, Component, InterReaction, IntraReaction,
                       explore_reactions)
from nasap_net.algorithms import are_equivalent_reaction_sets
from nasap_net.reaction_exploration import (
    clear_cache_for_compute_unique_bindsites_or_bindsite_sets,
    clear_cache_for_enum_valid_entering_bindsites,
    clear_cache_for_enum_valid_ml_pairs,
    clear_cache_for_enum_valid_mles_for_intra,
    clear_cache_for_iter_self_isomorphisms)

Reaction: TypeAlias = IntraReaction | InterReaction


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear caches before each test to ensure independence."""
    clear_cache_for_compute_unique_bindsites_or_bindsite_sets()
    clear_cache_for_iter_self_isomorphisms()
    clear_cache_for_enum_valid_entering_bindsites()
    clear_cache_for_enum_valid_ml_pairs()
    clear_cache_for_enum_valid_mles_for_intra()


def test_comprehensive_reaction_sets():
    component_structures = {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

    id_to_assembly = {
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

    # All "X to L" reactions among the assemblies in id_to_assembly
    # including intra- and inter-molecular reactions:
    expected: dict[str, Reaction] = {
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

    result = explore_reactions(
        id_to_assembly,
        metal_kind='M', leaving_kind='X', entering_kind='L',
        component_structures=component_structures
    )

    assert are_equivalent_reaction_sets(
        result, list(expected.values()),
        id_to_assembly=id_to_assembly,
        component_structures=component_structures
    ), "The reaction sets are not equivalent."


def test_aux_edges():
    component_structures = {
        'M': Component(  # component with auxiliary edges
            ['a', 'b', 'c', 'd'], 
            [('a', 'b', 'cis'), ('b', 'c', 'cis'), 
             ('c', 'd', 'cis'), ('d', 'a', 'cis')]),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

    id_to_assembly = {
        0: Assembly(  # MX4
            {'M0': 'M', 'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
            [('M0.a', 'X0.a'), ('M0.b', 'X1.a'), 
             ('M0.c', 'X2.a'), ('M0.d', 'X3.a')]
        ),
        1: Assembly({'L0': 'L'}),  # L
        2: Assembly({'X0': 'X'}),  # X
        3: Assembly(  # MLX3
            {'M0': 'M', 'L0': 'L', 
             'X0': 'X', 'X1': 'X', 'X2': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'X0.a'), 
             ('M0.c', 'X1.a'), ('M0.d', 'X2.a')]
        ),
        4: Assembly(  # cis-ML2X2
            {'M0': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'L1.a'), 
             ('M0.c', 'X0.a'), ('M0.d', 'X1.a')]
        ),
        5: Assembly(  # trans-ML2X2
            {'M0': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'X0.a'), 
             ('M0.c', 'L1.a'), ('M0.d', 'X1.a')]
        ),
    }

    expected: dict[str, Reaction] = {
        'MX4 + L -> MLX3 + X': InterReaction(
            init_assem_id=0, entering_assem_id=1,
            product_assem_id=3, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=8,
        ),
        'MLX3 + L -> cis-ML2X2 + X': InterReaction(
            init_assem_id=3, entering_assem_id=1,
            product_assem_id=4, leaving_assem_id=2,
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
        'MLX3 + L -> trans-ML2X2 + X': InterReaction(
            init_assem_id=3, entering_assem_id=1,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.c', leaving_bs='X1.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
    }

    result = explore_reactions(
        id_to_assembly,
        metal_kind='M', leaving_kind='X', entering_kind='L',
        component_structures=component_structures
    )
    assert are_equivalent_reaction_sets(
        result, list(expected.values()),
        id_to_assembly=id_to_assembly,
        component_structures=component_structures
    ), "The reaction sets with auxiliary edges are not equivalent."


def test_intra_reactions():
    component_structures = {
        'M': Component(  # component with auxiliary edges
            ['a', 'b', 'c', 'd'], 
            [('a', 'b', 'cis'), ('b', 'c', 'cis'), 
             ('c', 'd', 'cis'), ('d', 'a', 'cis')]),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

    id_to_assembly = {
        0: Assembly({'X0': 'X'}),  # X
        # trans-M2L2X5
        1: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'X0.a'), 
             ('M0.c', 'L1.a'), ('M0.d', 'X1.a'),
             ('M1.a', 'L0.b'), ('M1.b', 'X2.a'),
             ('M1.c', 'X3.a'), ('M1.d', 'X4.a')]
        ),
        # cis-M2L2X5
        2: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'L1.a'), 
             ('M0.c', 'X0.a'), ('M0.d', 'X1.a'),
             ('M1.a', 'L0.b'), ('M1.b', 'X2.a'),
             ('M1.c', 'X3.a'), ('M1.d', 'X4.a')]
            ),
        # trans-trans-M2L2X4-ring
        3: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'X0.a'), 
             ('M0.c', 'L1.a'), ('M0.d', 'X1.a'),
             ('M1.a', 'L0.b'), ('M1.b', 'X2.a'),
             ('M1.c', 'L1.b'), ('M1.d', 'X3.a')]
            ),
        # cis-cis-M2L2X4-ring
        4: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 
             'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
            [('M0.a', 'L0.a'), ('M0.b', 'L1.a'), 
             ('M0.c', 'X0.a'), ('M0.d', 'X1.a'),
             ('M1.a', 'L0.b'), ('M1.b', 'L1.b'),
             ('M1.c', 'X2.a'), ('M1.d', 'X3.a')]
            ),
    }

    expected: dict[str, Reaction] = {
        'trans-M2L2X5 -> trans-trans-M2L2X4-ring + X': IntraReaction(
            init_assem_id=1, product_assem_id=3, leaving_assem_id=0,
            metal_bs='M1.c', leaving_bs='X3.a', entering_bs='L1.b',
            duplicate_count=1,
        ),
        'cis-M2L2X5 -> cis-cis-M2L2X4-ring + X': IntraReaction(
            init_assem_id=2, product_assem_id=4, leaving_assem_id=0,
            metal_bs='M1.b', leaving_bs='X2.a', entering_bs='L1.b',
            duplicate_count=2,
        ),
    }

    result = explore_reactions(
        id_to_assembly,
        metal_kind='M', leaving_kind='X', entering_kind='L',
        component_structures=component_structures
    )
    assert are_equivalent_reaction_sets(
        result, list(expected.values()),
        id_to_assembly=id_to_assembly,
        component_structures=component_structures
    ), "The reaction sets with auxiliary edges are not equivalent."


def test_verbose(capsys):
    component_structures = {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

    id_to_assembly = {
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

    # All "X to L" reactions among the assemblies in id_to_assembly
    # including intra- and inter-molecular reactions:
    expected: dict[str, Reaction] = {
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
    
    expected_logs = [
        'Reaction Found (0): 5 -> 7 + 2 (metal=M0.a, leaving=X0.a, entering=L1.b) (x1)',
        'Reaction Found (1): 0 + 1 -> 3 + 2 (metal=M0.a, leaving=X0.a, entering=L0.a) (x4)',
        'Reaction Found (2): 0 + 3 -> 6 + 2 (metal=M0.a, leaving=X0.a, entering=L0.a) (x2)',
        'Reaction Found (3): 0 + 4 -> 5 + 2 (metal=M0.a, leaving=X0.a, entering=L0.a) (x4)',
        'Reaction Found (4): 3 + 1 -> 4 + 2 (metal=M0.b, leaving=X0.a, entering=L0.a) (x2)',
        'Reaction Found (5): 3 + 3 -> 5 + 2 (metal=M0.b, leaving=X0.a, entering=L0.a) (x2)',
        'Reaction Found (6): 6 + 1 -> 5 + 2 (metal=M0.a, leaving=X0.a, entering=L0.a) (x4)',
    ]

    result = explore_reactions(
        id_to_assembly,
        metal_kind='M', leaving_kind='X', entering_kind='L',
        component_structures=component_structures,
        verbose=True
    )

    assert are_equivalent_reaction_sets(
        result, list(expected.values()),
        id_to_assembly=id_to_assembly,
        component_structures=component_structures
    ), "The reaction sets with verbose output are not equivalent."

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')
    assert output_lines == expected_logs, "Verbose output does not match expected logs."


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
