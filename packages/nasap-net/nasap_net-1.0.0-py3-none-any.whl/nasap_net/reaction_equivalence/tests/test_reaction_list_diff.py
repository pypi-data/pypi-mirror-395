from collections.abc import Iterable

from pytest_mock import MockerFixture

from nasap_net.models import Assembly, BindingSite, Reaction
from nasap_net.reaction_equivalence import ReactionListDiff, reaction_list_diff
from nasap_net.types import ID


def test_empty():
    diff = reaction_list_diff.compute_reaction_list_diff([], [])
    assert diff == ReactionListDiff(first_only=set(), second_only=set())


def test_identical(mocker):
    R1 = _get_empty_reaction(id_='R1')
    R2 = _get_empty_reaction(id_='R2')

    _stub_reactions_equivalent(
        mocker=mocker,
        equivalent_pairs=[('R1', 'R2')],
    )

    diff = reaction_list_diff.compute_reaction_list_diff([R1], [R2])
    assert diff == ReactionListDiff(first_only=set(), second_only=set())


def test_different(mocker):
    R1 = _get_empty_reaction(id_='R1')
    R2 = _get_empty_reaction(id_='R2')

    _stub_reactions_equivalent(
        mocker=mocker,
        equivalent_pairs=None,
    )

    diff = reaction_list_diff.compute_reaction_list_diff([R1], [R2])
    assert diff == ReactionListDiff(first_only={R1}, second_only={R2})


def test_partial_overlap(mocker):
    R1 = _get_empty_reaction(id_='R1')
    R2 = _get_empty_reaction(id_='R2')  # equivalent to R1
    R3 = _get_empty_reaction(id_='R3')  # different from R1 and R2

    _stub_reactions_equivalent(
        mocker=mocker,
        equivalent_pairs=[('R3', 'R3')],
    )

    diff = reaction_list_diff.compute_reaction_list_diff(
        [R1, R3],
        [R2, R3]
    )
    assert diff == ReactionListDiff(first_only={R1}, second_only={R2})


def _get_empty_reaction(id_: ID) -> Reaction:
    empty_assem = Assembly(id_='empty', components={}, bonds=[])
    return Reaction(
        init_assem=empty_assem,
        entering_assem=empty_assem,
        product_assem=empty_assem,
        leaving_assem=empty_assem,
        metal_bs=BindingSite('', ''),
        leaving_bs=BindingSite('', ''),
        entering_bs=BindingSite('', ''),
        duplicate_count=None,
        id_=id_,
    )


def _stub_reactions_equivalent(
        mocker: MockerFixture,
        equivalent_pairs: Iterable[tuple[ID, ID]] | None,
):
    """Stub the reactions_equivalent function to return True
    for the given equivalent reaction ID pairs.

    For example, if equivalent_pairs is [('R1', 'R2')], then
    reactions_equivalent(R1, R2) and reactions_equivalent(R2, R1) will return True.

    All other pairs will return False.
    """
    if equivalent_pairs is None:
        equivalent_pairs = []

    def dispatcher(r1: Reaction, r2: Reaction) -> bool:
        for id1, id2 in equivalent_pairs:
            if (r1.id_ == id1 and r2.id_ == id2)\
                    or (r1.id_ == id2 and r2.id_ == id1):
                return True
        return False

    mocker.patch(
        'nasap_net.reaction_equivalence.reaction_list_diff.reactions_equivalent',
        side_effect=dispatcher,
    )
