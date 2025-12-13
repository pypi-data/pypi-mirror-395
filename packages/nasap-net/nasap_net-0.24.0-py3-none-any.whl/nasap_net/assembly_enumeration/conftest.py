import pytest

from nasap_net.assembly_enumeration import SymmetryOperations
from nasap_net.models import Assembly, AuxEdge, Bond, Component


@pytest.fixture
def X():
    return Component(kind='X', sites=[0])


@pytest.fixture
def M4L4():
    #  M3---L2---M2
    #  |         |
    #  L3        L1
    #  |         |
    #  M0---L0---M1
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    return Assembly(
        components={
            'M0': M, 'M1': M, 'M2': M, 'M3': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M2', 0),
            Bond('M2', 1, 'L2', 0), Bond('L2', 1, 'M3', 0),
            Bond('M3', 1, 'L3', 0), Bond('L3', 1, 'M0', 0),
        ]
    )


@pytest.fixture
def M4L4_symmetry_operations():
    sym_ops = SymmetryOperations()
    sym_ops.add_cyclic_permutation(
        'C_4', [['M0', 'M1', 'M2', 'M3'], ['L0', 'L1', 'L2', 'L3']]
    )
    sym_ops.add_product('C_2', ['C_4', 'C_4'])
    sym_ops.add_product('C_4^3', ['C_4', 'C_4', 'C_4'])
    sym_ops.add_cyclic_permutation(
        'C_2x', [['M0', 'M1'], ['M2', 'M3'], ['L0'], ['L1', 'L3'], ['L2']]
    )
    sym_ops.add_product('C_2y', ['C_2x', 'C_2'])
    sym_ops.add_product('C_2(1)', ['C_2x', 'C_4'])
    sym_ops.add_product('C_2(2)', ['C_2x', 'C_4^3'])
    return sym_ops


@pytest.fixture
def M2L4():
    #                 |                                     |
    #                (1)                                   (0)
    #                 L2                                    L2
    #                (0)                                   (1)
    #                 |                                     |
    #                (2)                                   (2)
    # --(1)L3(0)---(3)M0(1)---(0)L1(1)--    --(0)L3(1)---(3)M1(1)---(1)L1(0)--
    #                (0)                                   (0)
    #                 |                                     |
    #                (0)                                   (1)
    #                 L0                                    L0
    #                (1)                                   (0)
    #                 |                                     |
    M = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])
    L = Component(kind='L', sites=[0, 1])
    return Assembly(
        components={
            'M0': M, 'M1': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 0, 'L0', 0), Bond('M0', 1, 'L1', 0),
            Bond('M0', 2, 'L2', 0), Bond('M0', 3, 'L3', 0),
            Bond('M1', 0, 'L0', 1), Bond('M1', 1, 'L1', 1),
            Bond('M1', 2, 'L2', 1), Bond('M1', 3, 'L3', 1),
        ]
    )


@pytest.fixture
def M2L4_symmetry_operations():
    sym_ops = SymmetryOperations()
    sym_ops.add_cyclic_permutation(
        'C_4', [['M0'], ['M1'], ['L0', 'L1', 'L2', 'L3']]
    )
    sym_ops.add_product('C_2', ['C_4', 'C_4'])
    sym_ops.add_product('C_4^3', ['C_4', 'C_4', 'C_4'])
    sym_ops.add_cyclic_permutation(
        'C_2x', [['M0', 'M1'], ['L0', 'L2'], ['L1'], ['L3']]
    )
    sym_ops.add_product('C_2y', ['C_2x', 'C_2'])
    sym_ops.add_product('C_2(1)', ['C_2x', 'C_4'])
    sym_ops.add_product('C_2(2)', ['C_2x', 'C_4^3'])
    sym_ops.add_cyclic_permutation(
        'i', [['M0', 'M1'], ['L0', 'L2'], ['L1', 'L3']]
    )
    sym_ops.add_product('S_4', ['i', 'C_4'])
    sym_ops.add_product('sigma', ['i', 'C_2'])
    sym_ops.add_product('S_4^3', ['i', 'C_4^3'])
    sym_ops.add_product('sigma_x', ['i', 'C_2x'])
    sym_ops.add_product('sigma_y', ['i', 'C_2y'])
    sym_ops.add_product('sigma_1', ['i', 'C_2(1)'])
    sym_ops.add_product('sigma_2', ['i', 'C_2(2)'])
    return sym_ops


@pytest.fixture
def M9L6():
    # upper half             //                           lower half             //
    #                        |                                                   |
    #                       (1)                                                 (a)
    #                        M7                                                  M7
    #                       (0)                                                 (1)
    #                        |                                                   |
    #                       (2)                                                 (2)
    #              M2(1)--(0)L1(1)--(0)M1                              M5(1)--(0)L4(1)--(0)M4
    #              (0)               (1)                               (0)               (1)
    #                \               /                                   \               /
    #                (1)           (0)                                   (1)           (0)
    # //--(1)M8(0)--(2)L2          L0(2)--(0)M6(1)--//    //--(0)M8(1)--(2)L5          L3(2)--(1)M6(0)--//
    #                  (0)       (1)                                       (0)       (1)
    #                    \       /                                            \       /
    #                    (1)   (0)                                           (1)   (0)
    #                        M0                                                  M3
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1, 2])
    return Assembly(
        components={
            'M0': M, 'M1': M, 'M2': M,
            'M3': M, 'M4': M, 'M5': M,
            'M6': M, 'M7': M, 'M8': M,
            'L0': L, 'L1': L, 'L2': L,
            'L3': L, 'L4': L, 'L5': L,
        },
        bonds=[
            Bond('M0', 0, 'L0', 1), Bond('L0', 0, 'M1', 1),
            Bond('M1', 0, 'L1', 1), Bond('L1', 0, 'M2', 1),
            Bond('M2', 0, 'L2', 1), Bond('L2', 0, 'M0', 1),
            Bond('L0', 2, 'M6', 0), Bond('L1', 2, 'M7', 0),
            Bond('L2', 2, 'M8', 0),
            Bond('M3', 0, 'L3', 1), Bond('L3', 0, 'M4', 1),
            Bond('M4', 0, 'L4', 1), Bond('L4', 0, 'M5', 1),
            Bond('M5', 0, 'L5', 1), Bond('L5', 0, 'M3', 1),
            Bond('L3', 2, 'M6', 1), Bond('L4', 2, 'M7', 1),
            Bond('L5', 2, 'M8', 1),
        ]
    )


@pytest.fixture
def M9L6_symmetry_operations():
    sym_ops = SymmetryOperations()
    sym_ops.add_cyclic_permutation(
        'C_3',
        [
            ['M0', 'M1', 'M2'], ['M3', 'M4', 'M5'], ['M6', 'M7', 'M8'],
            ['L0', 'L1', 'L2'], ['L3', 'L4', 'L5'],
        ]
    )
    sym_ops.add_product('C_3^2', ['C_3', 'C_3'])
    sym_ops.add_cyclic_permutation(
        'C_2x',
        [
            ['M0', 'M3'], ['M1', 'M5'], ['M2', 'M4'],
            ['M6', 'M8'], ['M7'],
            ['L0', 'L5'], ['L1', 'L4'], ['L2', 'L3'],
        ]
    )
    sym_ops.add_product('C_2y', ['C_2x', 'C_3^2'])
    sym_ops.add_product('C_2xy', ['C_2x', 'C_3'])
    sym_ops.add_cyclic_permutation(
        'sigma_h',
        [
            ['M0', 'M3'], ['M1', 'M4'], ['M2', 'M5'],
            ['M6'], ['M7'], ['M8'],
            ['L0', 'L3'], ['L1', 'L4'], ['L2', 'L5'],
        ]
    )
    sym_ops.add_product('sigma_1', ['sigma_h', 'C_2x'])
    sym_ops.add_product('sigma_2', ['sigma_h', 'C_2y'])
    sym_ops.add_product('sigma_3', ['sigma_h', 'C_2xy'])
    sym_ops.add_product('S_3', ['sigma_h', 'C_3'])
    sym_ops.add_product('S_3^5', ['sigma_h', 'C_3^2'])
    return sym_ops
