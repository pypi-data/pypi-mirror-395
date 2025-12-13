import networkx as nx
import pytest

from nasap_net import Assembly, AuxEdge, Component, draw_2d


@pytest.mark.skip(reason='This is a visual test.')
def test_draw_2d():
    MLX3 = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'L1.a')],
    )
    COMPONENT_STRUCTURES = {
        'M': Component(
            {'a', 'b', 'c', 'd'}, {
                AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
                AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

    positions = nx.spring_layout(MLX3.g_snapshot(COMPONENT_STRUCTURES))
    draw_2d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='component_kind')
    draw_2d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='component_id')
    draw_2d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='core_and_bindsite_ids')
    draw_2d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode=None)
    draw_2d(
        MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode=None,
        label_aux_edges=False)


if __name__ == '__main__':
    test_draw_2d()
