from nasap_net.types import ID


class IncorrectReactionResultError(ValueError):
    """
    Exception raised when the reproduced reaction result is inconsistent with
    the given result.
    """


class DuplicateReactionError(ValueError):
    """
    Exception raised when there are duplicate reactions in the input.
    """
    def __init__(self, reaction_id1: ID, reaction_id2: ID) -> None:
        message = (
            f"Duplicate reactions found: '{reaction_id1}' and "
            f"'{reaction_id2}'."
        )
        super().__init__(message)
        self.reaction_id1 = reaction_id1
        self.reaction_id2 = reaction_id2
