import pandas as pd
import pytest

from nasap_net import InterReaction, IntraReaction
from nasap_net.pipelines.lib import reactions_to_df
from nasap_net.pipelines.lib.reactions_df_conversion import reaction_to_dict


def test_reaction_to_dict_inter():
    inter = InterReaction(
        0, 1, 2, 3,
        'metal_bs', 'leave_bs', 'enter_bs',
        2)
    d = reaction_to_dict(inter)
    assert d == {
        'init_assem_id': 0,
        'entering_assem_id': 1,
        'product_assem_id': 2,
        'leaving_assem_id': 3,
        'metal_bs': 'metal_bs',
        'leaving_bs': 'leave_bs',
        'entering_bs': 'enter_bs',
        'duplicate_count': 2
    }


def test_reaction_to_dict_intra():
    intra = IntraReaction(
        0, 1, 2,
        'metal_bs', 'leave_bs', 'enter_bs',
        1)
    d = reaction_to_dict(intra)
    assert d == {
        'init_assem_id': 0,
        'entering_assem_id': None,
        'product_assem_id': 1,
        'leaving_assem_id': 2,
        'metal_bs': 'metal_bs',
        'leaving_bs': 'leave_bs',
        'entering_bs': 'enter_bs',
        'duplicate_count': 1
    }


def test_basic():
    reactions: list[IntraReaction | InterReaction] = [
        IntraReaction(
            0, 1, 2, 
            'metal_bs1', 'leave_bs1', 'enter_bs1', 
            1),
        InterReaction(
            3, 4, 5, None,
            'metal_bs2', 'leave_bs2', 'enter_bs2',
            2)
    ]

    df = reactions_to_df(reactions)

    assert df.columns.tolist() == [
        'init_assem_id', 'entering_assem_id', 'product_assem_id',
        'leaving_assem_id', 'metal_bs', 'leaving_bs', 'entering_bs',
        'duplicate_count'
    ]
    assert df['init_assem_id'].tolist() == [0, 3]
    assert df['entering_assem_id'].tolist() == [pd.NA, 4]
    assert df['product_assem_id'].tolist() == [1, 5]
    assert df['leaving_assem_id'].tolist() == [2, pd.NA]
    assert df['metal_bs'].tolist() == ['metal_bs1', 'metal_bs2']
    assert df['leaving_bs'].tolist() == ['leave_bs1', 'leave_bs2']
    assert df['entering_bs'].tolist() == ['enter_bs1', 'enter_bs2']
    assert df['duplicate_count'].tolist() == [1, 2]


if __name__ == '__main__':
    pytest.main(['-v', __file__])
