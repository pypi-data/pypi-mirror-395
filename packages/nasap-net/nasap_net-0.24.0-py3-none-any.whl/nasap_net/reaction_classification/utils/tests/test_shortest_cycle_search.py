import pytest

from nasap_net import Assembly
from nasap_net.reaction_classification.utils import find_shortest_cycle
from nasap_net.utils import are_same_circular_perm


def test_no_ring():
    # M1-L1 (linear)
    ML_NO_RING = Assembly({'M1': 'M', 'L1': 'L'})
    assert find_shortest_cycle(ML_NO_RING) == None


def test_one_ring():
    # M1---L1
    # |    |
    # L2---M2

    # One cycle: 
    # 1. M1-L1-M2-L2-(M1)  (length 4)

    M2L2_RING = Assembly(
        {'M1': 'M', 'M2': 'M', 'L1': 'L', 'L2': 'L'},
        [('M1.b', 'L1.a'), ('L1.b', 'M2.a'),
         ('M2.b', 'L2.a'), ('L2.b', 'M1.a')])
    result = find_shortest_cycle(M2L2_RING)
    assert result is not None
    assert are_same_circular_perm(
        result, ['M1', 'L1', 'M2', 'L2'], consider_reverse=True)


def test_one_parallel():
    # Parallel bonds are also considered as a cycle.

    #   M1
    #  /  \  <- parallel bonds
    #  \  /
    #   L1

    # One cycle:
    # 1. M1-L1-(M1)  (length 2, parallel-bond pair)

    ML_RING = Assembly({'M1': 'M', 'L1': 'L'},
                       [('M1.a', 'L1.a'), ('M1.b', 'L1.b')])
    
    result = find_shortest_cycle(ML_RING)
    assert result is not None
    assert are_same_circular_perm(
        result, ['M1', 'L1'], consider_reverse=True)


def test_multi_rings_of_same_length():
    #   -- M1--
    #  /   |   \
    # L1   L2   L3
    #  \   |   /
    #   -- M2--

    # Three cycles with the same length 4:
    # 1. M1-L1-M2-L2-(M1)  (length 4)
    # 2. M1-L2-M2-L3-(M1)  (length 4)
    # 3. M1-L3-M2-L1-(M1)  (length 4)
    M2L3_CAGE = Assembly(
        {'M1': 'M', 'M2': 'M', 'L1': 'L', 'L2': 'L', 'L3': 'L'},
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'), ('M1.c', 'L3.a'),
         ('M2.a', 'L1.b'), ('M2.b', 'L2.b'), ('M2.c', 'L3.b')])

    result = find_shortest_cycle(M2L3_CAGE)

    assert result is not None
    # Which cycle is returned is not guaranteed.
    assert are_same_circular_perm(
        result, ['M1', 'L1', 'M2', 'L2'], consider_reverse=True)\
        or are_same_circular_perm(
            result, ['M1', 'L2', 'M2', 'L3'], consider_reverse=True)\
        or are_same_circular_perm(
            result, ['M1', 'L3', 'M2', 'L1'], consider_reverse=True)


def test_multi_rings_of_different_length():
    #  -- M1----L3
    # /   |     |
    # L1  L2    M3
    # \   |     |
    #  -- M2----L4

    # Three cycles with different lengths:
    # 1. M1-L1-M2-L2-(M1)  (length 4)
    # 2. M1-L1-M2-L4-M3-L3-(M1)  (length 6)
    # 3. M1-L2-M2-L4-M3-L3-(M1)  (length 6)
    M3L3_RING = Assembly(
        {'M1': 'M', 'M2': 'M', 'M3': 'M',
         'L1': 'L', 'L2': 'L', 'L3': 'L', 'L4': 'L'},
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'),
         ('M2.a', 'L1.b'), ('M2.b', 'L2.b'),
         ('M1.c', 'L3.a'), ('L3.b', 'M3.a'),
         ('M3.b', 'L4.a'), ('L4.b', 'M2.c'),
         ])

    result = find_shortest_cycle(M3L3_RING)

    assert result is not None
    assert are_same_circular_perm(
        result, ['M1', 'L1', 'M2', 'L2'], consider_reverse=True)


def test_one_ring_and_one_parallel():
    #  L2----M1
    #  |    /  \  <- parallel bonds
    #  |    \  /
    #  M2----L1

    # Three cycles:
    # 1. M1-L1-(M1)  (length 2, parallel-bond pair)
    # 2. M1-L2-M2-L1-(M1)  (length 4, using one of the parallel bonds)
    # 3. M2-L2-M1-L1-(M2)  (length 4, using the other parallel bond)
    ML_PARALLEL_RING = Assembly(
        {'M1': 'M', 'M2': 'M', 'L1': 'L', 'L2': 'L'},
        [('M1.a', 'L1.a'), ('M1.b', 'L1.b'),  # parallel bonds
         ('M1.c', 'L2.a'), ('L2.b', 'M2.a'),
         ('M2.b', 'L1.c')])

    result = find_shortest_cycle(ML_PARALLEL_RING)

    assert result is not None
    assert are_same_circular_perm(
        result, ['M1', 'L1'], consider_reverse=True)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
