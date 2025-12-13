"""Integration tests for reaction classification.

Each test utilizes the functions from nasap_net.reaction_classification.utils
to construct a rule for reaction classification. The rule is then used to 
create a ReactionClassifier object, which is used to classify reactions.
"""

import pytest

from nasap_net import (Assembly, Component, InterReactionRich,
                       IntraReactionRich, ReactionClassifier)
from nasap_net.reaction_classification.utils import inter_or_intra

ReactionEmbedded = IntraReactionRich | InterReactionRich


def test_classification_by_inter_or_intra():
    def rule(reaction: ReactionEmbedded):
        if inter_or_intra(reaction) == "intra":
            return "intra"
        return "inter"
    
    classifier = ReactionClassifier(rule)

    intra = IntraReactionRich(
        init_assem=Assembly(), product_assem=Assembly(),
        leaving_assem=Assembly(), 
        metal_bs='', leaving_bs='', entering_bs='',
        duplicate_count=0
        )
    result = classifier.classify(intra)
    assert result == "intra"

    inter = InterReactionRich(
        init_assem=Assembly(), entering_assem=Assembly(),
        product_assem=Assembly(), leaving_assem=Assembly(),
        metal_bs='', leaving_bs='', entering_bs='',
        duplicate_count=0
        )
    result = classifier.classify(inter)
    assert result == "inter"


@pytest.fixture
def MLX():
    return Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                    [('M1.a', 'L1.a'), ('M1.b', 'X1.a')])

@pytest.fixture
def L():
    return Assembly({'L1': 'L'})

@pytest.fixture
def ML2():
    return Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},
                    [('M1.a', 'L1.a'), ('M1.b', 'L2.a')])

@pytest.fixture
def X():
    return Assembly({'X1': 'X'})

@pytest.fixture
def X_to_L(MLX, L, ML2, X):
    """MLX + L -> ML2 + X (L-X exchange)"""
    return InterReactionRich(
        init_assem=MLX, entering_assem=L,
        product_assem=ML2, leaving_assem=X,
        metal_bs='M1.a', leaving_bs='X1.a', entering_bs='L1.a',
        duplicate_count=2  # 1 (dup. on MLX) * 2 (dup. on L)
    )

@pytest.fixture
def L_to_L(MLX, L):
    """MLX + L -> MLX + L (L-L exchange)"""
    return InterReactionRich(
        init_assem=MLX, entering_assem=L,
        product_assem=MLX, leaving_assem=L,
        metal_bs='M1.a', leaving_bs='L1.a', entering_bs='L1.a',
        duplicate_count=2  # 1 (dup. on MLX) * 2 (dup. on L)
    )

@pytest.fixture
def comp_kind_to_obj():
    return {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }


def test_classification_by_comp_kinds(X_to_L, L_to_L):
    def rule(reaction: ReactionEmbedded):
        entering = reaction.entering_kind
        leaving = reaction.leaving_kind
        return f'{leaving}_to_{entering}'
    
    classifier = ReactionClassifier(rule)

    result = classifier.classify(X_to_L)
    assert result == "X_to_L"

    result = classifier.classify(L_to_L)
    assert result == "L_to_L"


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
