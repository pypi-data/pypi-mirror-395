import pytest

from nasap_net.debug_utils import BondsetsComparer

# Sample structure:
# M2L2-ring
# []: bond name
# 
#         M1
# [1] -> /  \ <- [4]
#      L1    L2
# [2] -> \  / <- [3]
#         M2

def test_equal():
    FIRST_BONDSETS = [[1], [1, 2]]
    SECOND_BONDSETS = [[1], [2, 1]]
    comparer = BondsetsComparer(FIRST_BONDSETS, SECOND_BONDSETS)
    assert comparer.are_equal


def test_inequal():
    FIRST_BONDSETS = [[1], [1, 2]]
    SECOND_BONDSETS = [[1], [2, 3]]
    comparer = BondsetsComparer(FIRST_BONDSETS, SECOND_BONDSETS)
    assert not comparer.are_equal


def test_equal_with_sym_ops():
    FIRST_BONDSETS = [[1], [1, 2]]
    SECOND_BONDSETS = [[2], [3, 4]]
    SYM_OPS = {
        'sigma': {1: 2, 2: 1, 3: 4, 4: 3},  # [1] -> [2]
        'C2': {1: 3, 2: 4, 3: 1, 4: 2},  # [1, 2] -> [3, 4]
        }
    comparer = BondsetsComparer(FIRST_BONDSETS, SECOND_BONDSETS, SYM_OPS)
    assert comparer.are_equal


def test_mapping_and_diffs():
    FIRST_BONDSETS = [[1], [1, 2]]
    SECOND_BONDSETS = [[2], [2, 3]]
    SYM_OPS = {
        'sigma': {1: 2, 2: 1, 3: 4, 4: 3},  # [1] -> [2]
        'C2': {1: 3, 2: 4, 3: 1, 4: 2},  # [1, 2] -> [3, 4]
        }
    comparer = BondsetsComparer(FIRST_BONDSETS, SECOND_BONDSETS, SYM_OPS)
    assert comparer.first_to_second == {frozenset([1]): frozenset([2])}
    assert comparer.only_in_first == {frozenset([1, 2])}
    assert comparer.only_in_second == {frozenset([2, 3])}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
