import pytest

from nasap_net import Assembly, Component
from nasap_net.reaction_classification.utils import count_connected


def test():
    MLX = Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                   [('M1.a', 'L1.a'), ('M1.b', 'X1.a')])
    COMP_KIND_TO_OBJ = {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a'])
    }
    
    connected_num = count_connected(
        MLX, 'M1', 'L', COMP_KIND_TO_OBJ)
    
    assert connected_num == 1


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
