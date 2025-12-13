from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Self

from nasap_net.models import Reaction
from nasap_net.types import ID


@dataclass(frozen=True)
class ReactionSignature:
    """
    A canonical, hashable signature used to group reactions by coarse identity.

    - Reactions with identical signatures *may* represent the same reaction.
    - Reactions with different signatures are guaranteed to be distinct.
    """
    init_assem_id: ID
    entering_assem_id: ID | None
    product_assem_id: ID
    leaving_assem_id: ID | None

    @classmethod
    def from_reaction(cls, reaction: Reaction) -> Self:
        return cls(
            init_assem_id=reaction.init_assem_id,
            entering_assem_id=reaction.entering_assem_id,
            product_assem_id=reaction.product_assem_id,
            leaving_assem_id=reaction.leaving_assem_id
        )


def group_reactions_by_signature(
        reactions: Iterable[Reaction]
) -> dict[ReactionSignature, set[Reaction]]:
    """Group reactions by their reaction signatures."""
    sig_to_reactions = defaultdict(set)
    for reaction in reactions:
        sig_to_reactions[
            ReactionSignature.from_reaction(reaction)
        ].add(reaction)
    return sig_to_reactions
