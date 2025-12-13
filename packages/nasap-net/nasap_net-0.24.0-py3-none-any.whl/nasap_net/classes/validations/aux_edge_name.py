import re

__all__ = ['validate_name_of_aux_type']


def validate_name_of_aux_type(aux_type: str) -> None:
    """Check if the auxiliary type is valid.

    The auxiliary type should be a string that follows the pattern 
    '[A-Za-z0-9_-]+'.
    """
    if not re.fullmatch(r'[A-Za-z0-9_-]+', aux_type):
        raise ValueError(
            'The auxiliary type should follow the pattern [A-Za-z0-9_-]+.')
