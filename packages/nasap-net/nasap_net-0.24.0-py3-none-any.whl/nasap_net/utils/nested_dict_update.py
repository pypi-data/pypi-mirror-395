from collections.abc import Mapping

__all__ = ['update_nested_dict']


def update_nested_dict(original: Mapping, new: Mapping) -> dict:
    """Updates the first dictionary with the second dictionary.

    Nested dictionaries are updated recursively.

    Parameters
    ----------
    d1 : Mapping
        The dictionary to update.
    d2 : Mapping
        The dictionary to update with.

    Returns
    -------
    dict
        The updated dictionary.

    Examples
    --------
    >>> d1 = {'a': 1, 'b': {'c': 2, 'd': 3}}
    >>> d2 = {'b': {'c': 4}}
    >>> deep_update(d1, d2)
    {'a': 1, 'b': {'c': 4, 'd': 3}}
    """
    original = dict(original)
    for k, v in new.items():
        if isinstance(v, dict):
            original[k] = update_nested_dict(original.get(k, {}), v)
        else:
            original[k] = v
    return original
