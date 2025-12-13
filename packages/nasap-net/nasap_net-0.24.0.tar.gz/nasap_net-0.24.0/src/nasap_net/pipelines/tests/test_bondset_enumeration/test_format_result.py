import pytest

from nasap_net.pipelines.bondset_enumeration import sort_bond_subsets


def test_empty():
    result = sort_bond_subsets([])  # type: ignore
    assert result == []


def test_single_element():
    result = sort_bond_subsets([frozenset({1})])
    assert result == [[1]]


def test_multiple_elements():
    result = sort_bond_subsets([
        frozenset({1, 2, 3}),
        frozenset({1}),
        frozenset({2, 3}),
        frozenset({1, 2}),
    ])
    assert result == [
        [1],
        [1, 2],
        [2, 3],
        [1, 2, 3],
    ]


def test_with_strings():
    result = sort_bond_subsets([
        frozenset({'a', 'b', 'c'}),
        frozenset({'a'}),
        frozenset({'b', 'c'}),
        frozenset({'a', 'b'}),
    ])
    assert result == [
        ['a'],
        ['a', 'b'],
        ['b', 'c'],
        ['a', 'b', 'c'],
    ]


if __name__ == '__main__':
    pytest.main(['-v', __file__])
