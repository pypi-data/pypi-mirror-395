from collections.abc import Callable
from typing import TypeAlias

from nasap_net import InterReactionRich, IntraReactionRich

ReactionDetailed: TypeAlias = IntraReactionRich | InterReactionRich


class ReactionClassifier:
    def __init__(
            self, 
            classification_rule: Callable[[ReactionDetailed], str]
            ) -> None:
        self.classification_rule = classification_rule

    def classify(self, reaction: ReactionDetailed) -> str:
        return self.classification_rule(reaction)
