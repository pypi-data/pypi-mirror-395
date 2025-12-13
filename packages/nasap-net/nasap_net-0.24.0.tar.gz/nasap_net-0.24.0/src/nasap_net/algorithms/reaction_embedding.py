from collections.abc import Mapping
from typing import TypeVar

from nasap_net import Assembly, ReactionBase

T_co = TypeVar("T_co", covariant=True)


def embed_assemblies_into_reaction(
        reaction: ReactionBase[T_co],
        id_to_assembly: Mapping[int, Assembly],
) -> T_co:
    """Embed the assemblies into the reaction."""
    return reaction.to_rich_reaction(id_to_assembly)
