import re

__all__ = ['validate_name_of_binding_site']


def validate_name_of_binding_site(binding_site: str) -> None:
    """Check if the binding site is valid.

    The binding site should be a string that follows the pattern 
    '[A-Za-z0-9_-]+'.
    'core' is a reserved keyword for the core binding site.
    """
    if not re.fullmatch(r'[A-Za-z0-9_-]+', binding_site):
        raise ValueError(
            'The binding site should follow the pattern [A-Za-z0-9_-]+.')
    if binding_site == 'core':
        raise ValueError(
            '"core" is a reserved keyword for the core binding site.')
