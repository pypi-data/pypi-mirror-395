import pytest

from nasap_net import (Assembly, InterReaction, InterReactionRich,
                       IntraReaction, IntraReactionRich,
                       embed_assemblies_into_reaction)


def test_inter():
    REACTION = InterReaction(
        0, 1, 2, 3,
        'M1.a', 'X1.a', 'L1.a', 2)

    ID_TO_ASSEMBLY = {
        0: Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},  # MLX
                        [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        1: Assembly({'L1': 'L'}),  # L
        2: Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},  # ML2
                        [('M1.a', 'L1.a'), ('M1.b', 'L2.a')]),
        3: Assembly({'X1': 'X'}),  # X
    }
        
    embed_reaction = embed_assemblies_into_reaction(
        REACTION, ID_TO_ASSEMBLY)
    
    assert embed_reaction == InterReactionRich(
        ID_TO_ASSEMBLY[0], ID_TO_ASSEMBLY[1],
        ID_TO_ASSEMBLY[2], ID_TO_ASSEMBLY[3],
        'M1.a', 'X1.a', 'L1.a', 2)


def test_intra():
    REACTION = IntraReaction(
        0, 1, 2,
        'M1.a', 'X1.a', 'L1.b', 1)

    ID_TO_ASSEMBLY = {
        0: Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},  # MLX
                        [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        1: Assembly({'M1': 'M', 'L1': 'L'},  # ML
                        [('M1.a', 'L1.a'), ('M1.b', 'L1.b')]),
        2: Assembly({'X1': 'X'}),  # X
    }
    
    embed_reaction = embed_assemblies_into_reaction(
        REACTION, ID_TO_ASSEMBLY)
    
    assert embed_reaction == IntraReactionRich(
        ID_TO_ASSEMBLY[0], ID_TO_ASSEMBLY[1], ID_TO_ASSEMBLY[2],
        'M1.a', 'X1.a', 'L1.b', 1)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
