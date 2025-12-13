from typing import Literal, TypeAlias

from nasap_net import InterReactionRich, IntraReactionRich

ReactionEmbedded: TypeAlias = (
        IntraReactionRich | InterReactionRich)


def inter_or_intra(
        reaction: ReactionEmbedded) -> Literal["inter", "intra"]:
    if isinstance(reaction, IntraReactionRich):
        return "intra"
    return "inter"
