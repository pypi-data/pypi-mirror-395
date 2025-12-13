import pytest

from nasap_net import Assembly, InterReactionRich, ReactionClassifier


def test():
    def classification_rule(reaction):
        if (reaction.leaving_kind == 'X'
                and reaction.entering_kind == 'L'):
            return 'X-L exchange'
        else:
            return 'other'
        
    classifier = ReactionClassifier(classification_rule)

    MX = Assembly({'M1': 'M', 'X1': 'X'}, [('M1.a', 'X1.a')])
    L = Assembly({'L1': 'L'})
    ML = Assembly({'M1': 'M', 'L1': 'L'}, [('M1.a', 'L1.a')])
    X = Assembly({'X1': 'X'})
    
    X_to_L = InterReactionRich(
        init_assem=MX, entering_assem=L,
        product_assem=ML, leaving_assem=X,
        metal_bs='M1.a', leaving_bs='X1.a', entering_bs='L1.a',
        duplicate_count=1
        )
    L_to_X = InterReactionRich(
        init_assem=ML, entering_assem=X,
        product_assem=MX, leaving_assem=L,
        metal_bs='M1.a', leaving_bs='L1.a', entering_bs='X1.a',
        duplicate_count=1
        )
    assert classifier.classify(X_to_L) == 'X-L exchange'
    assert classifier.classify(L_to_X) == 'other'


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
