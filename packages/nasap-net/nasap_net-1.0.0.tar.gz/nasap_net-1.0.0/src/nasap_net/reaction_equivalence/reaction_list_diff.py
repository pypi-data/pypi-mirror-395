from collections import defaultdict
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Iterable

from nasap_net.assembly_equivalence.signature import get_assembly_signature
from nasap_net.models import Reaction
from .core import reactions_equivalent


@dataclass(frozen=True)
class ReactionListDiff:
    first_only: set[Reaction]
    second_only: set[Reaction]


def compute_reaction_list_diff(
        reactions1: Iterable[Reaction],
        reactions2: Iterable[Reaction],
        ) -> ReactionListDiff:
    """
    Compute the difference between two lists of reactions.

    Parameters
    ----------
    reactions1 : Iterable[Reaction]
        The first list of reactions.
    reactions2 : Iterable[Reaction]
        The second list of reactions.

    Returns
    -------
    ReactionListDiff
        An object containing reactions only in the first list and
        reactions only in the second list.
    """
    sig_to_reactions1 = defaultdict(set)
    for reaction in reactions1:
        sig = get_reaction_signature(reaction)
        sig_to_reactions1[sig].add(reaction)

    sig_to_reactions2 = defaultdict(set)
    for reaction in reactions2:
        sig = get_reaction_signature(reaction)
        sig_to_reactions2[sig].add(reaction)

    first_only = set()
    second_only = set()

    common_sigs = sig_to_reactions1.keys() & sig_to_reactions2.keys()
    first_only_sigs = sig_to_reactions1.keys() - common_sigs
    second_only_sigs = sig_to_reactions2.keys() - common_sigs

    for first_only_sig in first_only_sigs:
        first_only.update(sig_to_reactions1[first_only_sig])
    for second_only_sig in second_only_sigs:
        second_only.update(sig_to_reactions2[second_only_sig])

    for common_sig in common_sigs:
        unpaired_reactions1 = sig_to_reactions1[common_sig].copy()
        unpaired_reactions2 = sig_to_reactions2[common_sig].copy()

        for reaction1 in sorted(unpaired_reactions1):
            for reaction2 in sorted(unpaired_reactions2):
                if reactions_equivalent(reaction1, reaction2):
                    unpaired_reactions1.remove(reaction1)
                    unpaired_reactions2.remove(reaction2)
                    break

        first_only.update(unpaired_reactions1)
        second_only.update(unpaired_reactions2)

    return ReactionListDiff(
        first_only=first_only,
        second_only=second_only,
    )


def get_reaction_signature(reaction: Reaction) -> Hashable:
    """Get a signature of the reaction for quick filtering.

    Reactions with different signatures are guaranteed to be non-equivalent.
    Reactions with the same signature may or may not be equivalent.

    Parameters
    ----------
    reaction : Reaction
        The reaction to compute the signature for.

    Returns
    -------
    Hashable
        The signature of the reaction.
    """
    return (
        get_assembly_signature(reaction.init_assem),
        (
            get_assembly_signature(reaction.entering_assem_strict)
            if reaction.is_inter() else None
        )
    )
