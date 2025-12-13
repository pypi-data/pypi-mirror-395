from collections.abc import Mapping
from functools import reduce


def resolve_chain_map(*maps: Mapping) -> Mapping:
    """
    Resolve a chain of mappings into one.

    Parameters
    ----------
    *maps : Mapping
        Mappings to resolve.

    Returns
    -------
    Mapping
        The resolved mapping.

    Examples
    --------
    >>> input1 = {1: 10, 2: 20}
    >>> input2 = {10: 100, 20: 200}
    >>> input3 = {100: 1000, 200: 2000}
    >>> resolve_chain_map(input1, input2, input3)
    {1: 1000, 2: 2000}

    >>> resolve_chain_map()
    {}

    >>> resolve_chain_map({1: 10})
    {1: 10}
    """
    if not maps:
        return {}

    return reduce(
        lambda x, y: {k: x[v] for k, v in y.items()}, 
        reversed(maps))

    # ==============================
    # Explanation of the logic:

    # Example:
    # m1 = {1: 10, 2: 20}
    # m2 = {10: 100, 20: 200}
    # m3 = {100: 1000, 200: 2000}

    # The following code:
    # ```
    # reduce(
    #     lambda x, y: {k: x[v] for k, v in y.items()},
    #     [m3, m2, m1])
    # ```
    # is equivalent to:
    # ```
    # x = m3  # {100: 1000, 200: 2000}
    # y = m2  # {10: 100, 20: 200}
    # result = {k: x[v] for k, v in y.items()}  # {10: 1000, 20: 2000}
    # x = result  # {10: 1000, 20: 2000}
    # y = m1  # {1: 10, 2: 20}
    # result = {k: x[v] for k, v in y.items()}  # {1: 1000, 2: 2000}
    # ```
