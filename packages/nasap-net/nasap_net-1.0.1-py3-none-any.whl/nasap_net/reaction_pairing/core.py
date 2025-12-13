from collections.abc import Iterable, MutableMapping

from nasap_net.helpers import validate_unique_ids
from nasap_net.models import Reaction
from nasap_net.reaction_equivalence import reactions_equivalent
from nasap_net.types import ID
from .exceptions import DuplicateReactionError, IncorrectReactionResultError
from .sample_rev_generation import generate_sample_rev_reaction
from .signature import ReactionSignature, group_reactions_by_signature
from .utils import NoOverwriteDict, ValueConflictError


def pair_reverse_reactions(
        reactions: Iterable[Reaction],
        ) -> dict[ID, ID | None]:
    """Pair reactions with their reverse reactions.

    Parameters
    ----------
    reactions : Iterable[Reaction]
        The reactions to be paired.

    Returns
    -------
    dict[ID, ID | None]
        A mapping from each reaction ID to its reverse reaction ID, or None if
        no reverse reaction exists.
        If reaction A is the reverse of reaction B, then the mapping will
        include both A -> B and B -> A.

    Raises
    ------
    IncorrectReactionResultError
        If the reproduced reaction result is inconsistent with the given
        result.
    DuplicateReactionError
        If there are duplicate reactions in the input.

    Notes
    -----
    This function assumes that assemblies with different IDs are distinct,
    even if they are structurally identical. Please ensure that there are
    no structurally duplicate assemblies in the reactions.
    """
    validate_unique_ids(reactions)

    # to reduce the search space
    sig_to_reactions = group_reactions_by_signature(reactions)

    reaction_to_reverse: MutableMapping[ID, ID | None] = NoOverwriteDict()

    for reaction in reactions:
        if reaction.id_ in reaction_to_reverse:
            continue

        rev_index = reaction_to_rev_sig(reaction)
        candidate_revs = sig_to_reactions.get(rev_index)
        if not candidate_revs:
            reaction_to_reverse[reaction.id_] = None
            continue

        try:
            sample_rev = generate_sample_rev_reaction(reaction)
        except IncorrectReactionResultError:
            raise IncorrectReactionResultError() from None

        # Any reaction equivalent to the sample_rev is a reverse reaction.
        for candidate in candidate_revs:
            if reactions_equivalent(sample_rev, candidate):
                try:
                    reaction_to_reverse[reaction.id_] = candidate.id_
                except ValueConflictError:
                    first = reaction_to_reverse[reaction.id_]
                    assert first is not None
                    raise DuplicateReactionError(
                        first, candidate.id_
                    ) from None

                try:
                    reaction_to_reverse[candidate.id_] = reaction.id_
                except ValueConflictError:
                    first = reaction_to_reverse[candidate.id_]
                    assert first is not None
                    raise DuplicateReactionError(
                        first, reaction.id_
                    ) from None

                break
        else:
            reaction_to_reverse[reaction.id_] = None

    return dict(reaction_to_reverse)


def reaction_to_rev_sig(reaction: Reaction) -> ReactionSignature:
    """Get the index of the reverse reaction for a given reaction."""
    return ReactionSignature(
        init_assem_id=reaction.product_assem_id,
        entering_assem_id=reaction.leaving_assem_id,
        product_assem_id=reaction.init_assem_id,
        leaving_assem_id=reaction.entering_assem_id
    )
