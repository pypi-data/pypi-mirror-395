import pytest

from nasap_net import Assembly, InterReactionRich, IntraReactionRich
from nasap_net.reaction_classification.utils.inter_or_intra_judgement import \
    inter_or_intra


def test_with_intra_reaction():
    reaction = IntraReactionRich(
        Assembly(), Assembly(), Assembly(), 
        '', '', '', 1
    )
    result = inter_or_intra(reaction)
    assert result == "intra"


def test_with_inter_reaction():
    reaction = InterReactionRich(
        Assembly(), Assembly(), Assembly(), Assembly(),
        '', '', '', 1
    )
    result = inter_or_intra(reaction)
    assert result == "inter"


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
