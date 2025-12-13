import pytest

from nasap_net import enum_bond_subsets


def test_enum_bond_subsets_linear_M2L3():
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right

    # WITHOUT symmetry operations
    BONDS = [1, 2, 3, 4]
    BOND_TO_ADJ_BONDS = {
        1: {2},
        2: {1, 3},
        3: {2, 4},
        4: {3},
    }

    subsets = enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS)
    
    assert subsets == {
        frozenset({1}),
        frozenset({2}),
        frozenset({3}),
        frozenset({4}),
        frozenset({1, 2}),
        frozenset({2, 3}),
        frozenset({3, 4}),
        frozenset({1, 2, 3}),
        frozenset({2, 3, 4}),
        frozenset({1, 2, 3, 4}),
    }

    # WITH symmetry operations
    SYM_OPS = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    EXPECTED = {
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
        frozenset({2, 3}),
        frozenset({1, 2, 3}),
        frozenset({1, 2, 3, 4}),
    }
    assert EXPECTED == enum_bond_subsets(
        BONDS, BOND_TO_ADJ_BONDS, SYM_OPS)


def test_enum_bond_subsets_triangle():
    # Triangle with three bonds: 1, 2, 3
    BONDS = [1, 2, 3]
    BOND_TO_ADJ_BONDS = {
        1: {2, 3},
        2: {1, 3},
        3: {1, 2}
    }
    SYM_OPS = {
        'C3': {1: 2, 2: 3, 3: 1},
        'C3^2': {1: 3, 2: 1, 3: 2},
        'sigma1': {1: 1, 2: 3, 3: 2},
        'sigma2': {1: 2, 2: 1, 3: 3},
        'sigma3': {1: 3, 2: 2, 3: 1}
    }
    EXPECTED = {
        frozenset({1}),
        frozenset({1, 2}),
        frozenset({1, 2, 3})
    }
    assert EXPECTED == enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS, SYM_OPS)


def test_enum_bond_subsets_M4L4_square():
    # M4L4 square:
    # (): bond id

    #  M4-(6)-L3-(5)-M3
    #  |             |
    # (7)           (4)
    #  |             |
    #  L4            L2
    #  |             |
    # (8)           (3)
    #  |             |
    #  M1-(1)-L1-(2)-M2

    BONDS = [1, 2, 3, 4, 5, 6, 7, 8]
    BOND_TO_ADJ_BONDS = {
        1: {8, 2},
        2: {1, 3},
        3: {2, 4},
        4: {3, 5},
        5: {4, 6},
        6: {5, 7},
        7: {6, 8},
        8: {7, 1},
    }
    SYMMETRY_OPS = {
        'C_4': {
            1: 3, 2: 4, 3: 5, 4: 6,
            5: 7, 6: 8, 7: 1, 8: 2},
        'C_2': {
            1: 5, 2: 6, 3: 7, 4: 8,
            5: 1, 6: 2, 7: 3, 8: 4},
        'C_4^3': {
            1: 7, 2: 8, 3: 1, 4: 2,
            5: 3, 6: 4, 7: 5, 8: 6},
        'C_2x': {
            1: 2, 2: 1, 3: 8, 4: 7,
            5: 6, 6: 5, 7: 4, 8: 3},
        'C_2y': {
            1: 6, 2: 5, 3: 4, 4: 3,
            5: 2, 6: 1, 7: 8, 8: 7},
        'C_2(1)': {
            1: 4, 2: 3, 3: 2, 4: 1,
            5: 8, 6: 7, 7: 6, 8: 5},
        'C_2(2)': {
            1: 8, 2: 7, 3: 6, 4: 5,
            5: 4, 6: 3, 7: 2, 8: 1},
    }
    EXPECTED = {
        frozenset({1}),
        frozenset({1, 2}), frozenset({1, 8}),
        frozenset({1, 2, 3}),
        frozenset({1, 2, 3, 4}), frozenset({1, 2, 3, 8}),
        frozenset({1, 2, 3, 4, 5}),
        frozenset({1, 2, 3, 4, 5, 6}),
        frozenset({1, 2, 3, 4, 5, 8}),
        frozenset({1, 2, 3, 4, 5, 6, 7}),
        frozenset({1, 2, 3, 4, 5, 6, 7, 8}),
    }

    assert enum_bond_subsets(
        BONDS, BOND_TO_ADJ_BONDS, SYMMETRY_OPS) == EXPECTED


def test_string():
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right

    # WITHOUT symmetry operations
    BONDS = ['1', '2', '3', '4']
    BOND_TO_ADJ_BONDS = {
        '1': {'2'},
        '2': {'1', '3'},
        '3': {'2', '4'},
        '4': {'3'},
    }
    
    subsets = enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS)

    assert subsets == {
        frozenset({'1'}),
        frozenset({'2'}),
        frozenset({'3'}),
        frozenset({'4'}),
        frozenset({'1', '2'}),
        frozenset({'2', '3'}),
        frozenset({'3', '4'}),
        frozenset({'1', '2', '3'}),
        frozenset({'2', '3', '4'}),
        frozenset({'1', '2', '3', '4'}),
    }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
