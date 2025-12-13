import pytest

from nasap_net.utils.frozen_unordered_pair import FrozenUnorderedPair


def test_init_with_two_elements():
    pair = FrozenUnorderedPair(1, 2)
    assert pair.first == 1
    assert pair.second == 2


def test_init_with_iterable():
    pair = FrozenUnorderedPair([1, 2])
    assert pair.first == 1
    assert pair.second == 2


def test_init_with_invalid_iterable_length():
    with pytest.raises(ValueError):
        FrozenUnorderedPair([1])


def test_init_with_invalid_number_of_arguments():
    with pytest.raises(ValueError):
        FrozenUnorderedPair(1, 2, 3)  # type: ignore


def test_equality():
    pair1 = FrozenUnorderedPair(1, 2)
    pair2 = FrozenUnorderedPair(2, 1)
    assert pair1 == pair2


def test_inequality():
    pair1 = FrozenUnorderedPair(1, 2)
    pair2 = FrozenUnorderedPair(1, 3)
    assert pair1 != pair2


def test_hash():
    pair1 = FrozenUnorderedPair(1, 2)
    pair2 = FrozenUnorderedPair(2, 1)
    assert hash(pair1) == hash(pair2)


def test_repr():
    pair = FrozenUnorderedPair(1, 2)
    assert repr(pair) == 'FrozenUnorderedPair(1, 2)'


def test_iteration():
    pair = FrozenUnorderedPair(1, 2)
    elements = list(pair)
    assert elements == [1, 2]


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
