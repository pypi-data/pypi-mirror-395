import pytest

from nasap_net.algorithms import sort_bondsets, sort_bondsets_and_bonds

# TODO: Add more test cases.


def test_sort_bondsets():
    BOND_SUBSETS = [
        ['1', '3'],
        ['2', '1'],
        ['2', '3', '1'],
        ['1', '2', '3'],
        ['1'],
        ['2'],
    ]
    EXPECTED = [
        ['1'],
        ['2'],
        ['2', '1'],
        ['1', '3'],
        ['2', '3', '1'],
        ['1', '2', '3'],
    ]
    # Notes:
    # - ['2', '1'] < ['1', '3'] because they are sorted before comparison.
    # - ['2', '3', '1'] < ['1', '2', '3'] because they are equal after sorting,
    # and the order of the equal elements is preserved.
    assert sort_bondsets(BOND_SUBSETS) == EXPECTED


def test_sort_bondsets_and_bonds():
    BOND_SUBSETS = [
        ['1', '3'],
        ['2', '1'],
        ['2', '3', '1'],
        ['1', '2', '3'],
        ['1'],
        ['2'],
    ]
    EXPECTED = [
        ['1'],
        ['2'],
        ['1', '2'],
        ['1', '3'],
        ['1', '2', '3'],
        ['1', '2', '3'],
    ]
    # Bonds in each bondset are also sorted.
    assert sort_bondsets_and_bonds(BOND_SUBSETS) == EXPECTED


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
