import re

__all__ = ['validate_name_of_component_kind']


def validate_name_of_component_kind(component_type: str) -> None:
    """Check if the component type is valid.

    The component type should be a string that follows the pattern 
    '[A-Za-z_-]+'.
    """
    if not re.fullmatch(r'[A-Za-z_-]+', component_type):
        raise ValueError(
            'The component type should follow the pattern [A-Za-z_-]+.')
