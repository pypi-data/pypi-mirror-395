import logging
from collections.abc import Iterable
from itertools import chain, product
from typing import Iterator, TypeVar

from nasap_net.helpers import validate_unique_ids
from nasap_net.models import Assembly, MLEKind, Reaction
from nasap_net.reaction_classification import \
    get_min_forming_ring_size_including_temporary
from nasap_net.types import ID
from .explorer import InterReactionExplorer, IntraReactionExplorer
from .reaction_resolver import ReactionOutOfScopeError, ReactionResolver

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_T = TypeVar('_T', bound=ID)

def enumerate_reactions(
        assemblies: Iterable[Assembly],
        mle_kinds: Iterable[MLEKind],
        *,
        min_temp_ring_size: int | None = None,
        ) -> Iterator[Reaction]:
    """Enumerate possible reactions among given assemblies.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        The assemblies to consider during reaction enumeration.
    mle_kinds : Iterable[MLEKind]
        The kinds of MLEs to consider during reaction enumeration.
    min_temp_ring_size : int | None, optional
        Minimum size of temporary rings to consider during intra-molecular
        reactions. Reactions forming temporary rings smaller than this size
        will be ignored. If None, no filtering is applied. Default is None.

    Yields
    ------
    Reaction
        The enumerated and resolved reactions.
    """
    logger.debug('Starting reaction enumeration.')
    assemblies = list(assemblies)

    validate_unique_ids(assemblies)

    reaction_iters: list[Iterator[Reaction]] = []
    for mle_kind in mle_kinds:
        # Intra-molecular reactions
        for assem in assemblies:
            intra_explorer = IntraReactionExplorer(assem, mle_kind)
            reaction_iters.append(intra_explorer.explore())

        # Inter-molecular reactions
        for init_assem, entering_assem in product(assemblies, repeat=2):
            inter_explorer = InterReactionExplorer(
                init_assem, entering_assem, mle_kind)
            reaction_iters.append(inter_explorer.explore())

    resolver = ReactionResolver(assemblies)

    counter = 0

    for reaction in chain.from_iterable(reaction_iters):
        # Filter by minimum temporary ring size if specified
        # TODO: Optimize by integrating into intra explorer
        if min_temp_ring_size is not None and reaction.is_intra():
            actual_ring_size = get_min_forming_ring_size_including_temporary(
                reaction,
            )
            if (actual_ring_size is not None
                    and actual_ring_size < min_temp_ring_size):
                continue

        try:
            resolved = resolver.resolve(reaction)
            logger.debug('Reaction Found (%d): %s', counter, resolved)
            counter += 1
            yield resolved
        except ReactionOutOfScopeError:
            continue
    logger.debug('Reaction enumeration completed.')
