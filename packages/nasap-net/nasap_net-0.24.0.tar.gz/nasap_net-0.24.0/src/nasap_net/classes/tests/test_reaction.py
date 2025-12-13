import pytest

from nasap_net import InterReaction, IntraReaction


def test_reactants():
    intra_reaction = IntraReaction(
        init_assem_id=0,
        product_assem_id=1,
        leaving_assem_id=None,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )
    inter_reaction = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=2,
        leaving_assem_id=None,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )

    assert intra_reaction.reactants == [0]
    assert inter_reaction.reactants == [0, 1]


def test_products_of_intra():
    intra_with_leaving = IntraReaction(
        init_assem_id=0,
        product_assem_id=1,
        leaving_assem_id=2,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )
    intra_without_leaving = IntraReaction(
        init_assem_id=0,
        product_assem_id=1,
        leaving_assem_id=None,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )

    assert intra_with_leaving.products == [1, 2]
    assert intra_without_leaving.products == [1]


def test_products_of_inter():
    inter_with_leaving = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=2,
        leaving_assem_id=3,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )
    inter_without_leaving = InterReaction(
        init_assem_id=0,
        entering_assem_id=1,
        product_assem_id=2,
        leaving_assem_id=None,
        metal_bs='M0.a',
        leaving_bs='X0.a',
        entering_bs='L0.a',
        duplicate_count=1
    )

    assert inter_with_leaving.products == [2, 3]
    assert inter_without_leaving.products == [2]


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
