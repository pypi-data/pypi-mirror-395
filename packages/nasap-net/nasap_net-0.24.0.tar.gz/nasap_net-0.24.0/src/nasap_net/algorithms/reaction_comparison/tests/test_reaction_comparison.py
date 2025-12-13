import pytest

from nasap_net import Assembly, Component, InterReaction, IntraReaction
from nasap_net.algorithms import are_equivalent_reactions


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


def test_inter_equivalence(component_structures, id_to_assembly):
    # MX2 + L -> MLX + X
    reaction1 = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=3,
        leaving_assem_id=2,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=4,
    )
    # Same as above, but with different binding sites
    reaction2 = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=3,
        leaving_assem_id=2,
        metal_bs='M0.b',  # Different metal binding site
        leaving_bs='X1.a',  # Different leaving binding site
        entering_bs='L0.a',
        duplicate_count=4,
    )
    # Although the metal and leaving binding sites are different,
    # the pair of binding sites (metal, leaving) are equivalent, i.e.,
    # (M0.a, X0.a) is equivalent to (M0.b, X1.a).
    assert are_equivalent_reactions(
        reaction1, reaction2, id_to_assembly, component_structures)


def test_intra_equivalence(component_structures, id_to_assembly):
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
    reaction1 = IntraReaction(
        init_assem_id=8,
        product_assem_id=7,
        leaving_assem_id=1,
        metal_bs='M0.a',
        leaving_bs='L0.b',
        entering_bs='L2.b',
        duplicate_count=2,
    )
    # Same as above, but with different binding sites
    reaction2 = IntraReaction(
        init_assem_id=8,
        product_assem_id=7,
        leaving_assem_id=1,
        metal_bs='M1.b',  # Different metal binding site
        leaving_bs='L2.a',  # Different leaving binding site
        entering_bs='L0.a',
        duplicate_count=2,
    )
    # Although the metal and leaving binding sites are different,
    # the trio of binding sites (metal, leaving, entering) are equivalent, 
    # i.e., (M0.a, L0.b, L2.b) is equivalent to (M1.b, L2.a, L0.a).
    assert are_equivalent_reactions(
        reaction1, reaction2, id_to_assembly, component_structures)


def test_inter_intra_difference(component_structures, id_to_assembly):
    # MX2 + L -> MLX + X
    inter = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=3,
        leaving_assem_id=2,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1,
    )
    # M2L2X -> M2L2-ring + X
    intra = IntraReaction(  # intra-molecular reaction
        init_assem_id=5,
        product_assem_id=7,
        leaving_assem_id=2,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L1.b',
        duplicate_count=1,
    )
    # IntraReaction should not be equivalent to InterReaction
    assert not are_equivalent_reactions(
        inter, intra, id_to_assembly, component_structures)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
