import pytest

from nasap_net import Assembly, Component
from nasap_net.duplicate_exclusion import group_assemblies_by_isomorphism


def test_group_assemblies_by_isomorphism():
    id_to_graph = {
        0: Assembly(  # MLX-1
            {'M1': 'M', 'L1': 'L', 'X1': 'X'}, 
            [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        1: Assembly(  # MLX-2
            {'M2': 'M', 'L2': 'L', 'X2': 'X'}, 
            [('M2.a', 'L2.a'), ('M2.b', 'X2.a')]),
        2: Assembly(  # MLX-3
            {'M3': 'M', 'L3': 'L', 'X3': 'X'}, 
            [('M3.a', 'L3.a'), ('M3.b', 'X3.a')]),
        3: Assembly(  # MX2
            {'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('M1.a', 'X1.a'), ('M1.b', 'X2.a')]),
        4: Assembly(  # L
            {'L1': 'L'}, 
            []),
    }
    component_structures = {
        'M': Component({'a', 'b'}),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

    grouped_ids = group_assemblies_by_isomorphism(id_to_graph, component_structures)

    assert grouped_ids == {
        0: {0, 1, 2},
        3: {3},
        4: {4},
    }


def test_group_assemblies_by_isomorphism_with_non_isomorphic_groups():
    id_to_graph = {
        0: Assembly(  # MLX
            {'M1': 'M', 'L1': 'L', 'X1': 'X'}, 
            [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        1: Assembly(  # MLX
            {'M2': 'M', 'L2': 'L', 'X2': 'X'}, 
            [('M2.a', 'L2.a'), ('M2.b', 'X2.a')]),
        2: Assembly(  # MLX
            {'M3': 'M', 'L3': 'L', 'X3': 'X'}, 
            [('M3.a', 'L3.a'), ('M3.b', 'X3.a')]),
        3: Assembly(  # MX2
            {'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('M1.a', 'X1.a'), ('M1.b', 'X2.a')]),
        4: Assembly(  # MX2
            {'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('M1.a', 'X1.a'), ('M1.b', 'X2.a')]),
        5: Assembly(  # L
            {'L1': 'L'}, 
            []),
        6: Assembly(  # L
            {'L1': 'L'}, 
            []),
    }
    component_structures = {
        'M': Component({'a', 'b'}),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }
    non_isomorphic_groups = [{0, 1, 2}, {3, 4}]

    grouped_ids = group_assemblies_by_isomorphism(id_to_graph, component_structures, non_isomorphic_groups=non_isomorphic_groups)

    assert grouped_ids == {
        # Although 0, 1, 2 are isomorphic, since they are in the same
        # non-isomorphic group, their isomorphism check is skipped, thus
        # they are grouped to different isomorphic groups.
        0: {0},
        1: {1},
        2: {2},
        # The same applies to 3, 4.
        3: {3},
        4: {4},
        # 5, 6 are not in any non-isomorphic group, so they are checked
        # for isomorphism. They are isomorphic, so they are grouped together.
        5: {5, 6},
    }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
