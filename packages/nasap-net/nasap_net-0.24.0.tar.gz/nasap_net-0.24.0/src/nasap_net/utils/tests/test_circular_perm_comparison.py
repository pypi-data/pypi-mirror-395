import pytest

from nasap_net.utils import are_same_circular_perm


def test_same_permutation():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [1, 2, 3, 4]) is True


def test_rotated_permutation():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [3, 4, 1, 2]) is True


def test_different_permutation():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [1, 2, 3, 5]) is False


def test_reverse_permutation_considered():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [4, 3, 2, 1], consider_reverse=True) is True


def test_reverse_permutation_not_considered():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [4, 3, 2, 1], consider_reverse=False) is False


def test_reverse_rotated_permutation_considered():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [3, 2, 1, 4], consider_reverse=True) is True


def test_reverse_rotated_permutation_not_considered():
    assert are_same_circular_perm(
        [1, 2, 3, 4], [3, 2, 1, 4], consider_reverse=False) is False


def test_different_lengths():
    assert are_same_circular_perm(
        [1, 2, 3], [1, 2, 3, 4]) is False


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
