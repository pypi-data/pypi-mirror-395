from collections.abc import Mapping

from cachetools import cached
from cachetools.keys import hashkey

from nasap_net import Assembly, Component

_cache = {}  # type: ignore

def clear_cache_for_enum_valid_entering_bindsites():
    """Clear the cache used by `enum_valid_entering_bindsites`."""
    _cache.clear()


def _cache_key(
        assembly_id: str | int,
        assembly: Assembly,
        entering_kind: str,
        component_structures: Mapping[str, Component],
        ) -> tuple:
    return hashkey(assembly_id, entering_kind)


@cached(cache=_cache, key=_cache_key)
def enum_valid_entering_bindsites(
        assembly_id: str | int,  # only used for caching
        assembly: Assembly,
        entering_kind: str,
        component_structures: Mapping[str, Component],
        ) -> list[str]:
    """Enumerate valid entering bindsites.

    "Valid" here means that the bindsite is free and the component kind
    of the bindsite is entering_kind.
    
    Parameters
    ----------
    assembly_id : str
        The ID of the assembly. Used for caching.
    assembly : Assembly
        The assembly containing the bindsites.
    entering_kind : str
        The kind of the entering bindsite.
    component_structures : Mapping[str, ComponentStructure]
        A mapping of component names to their structures.
    
    Returns
    -------
    list of str
        A list of valid entering bindsites.

    Note
    -----
    The result is cached to avoid redundant computation.
    The key for caching is based on the assembly_id, and entering_kind, 
    i.e., assembly and component_structures are not used.
    Make sure to provide the same assembly_id for the same assembly, and not to
    change the component_structures between calls.
    """
    # Entering bindsites that meet the following conditions:
    # - The bindsite is free
    # - The component kind of the entering bindsite is entering_kind
    entering_bindsites = [
        bs for bs in assembly.get_all_bindsites_of_kind(
        entering_kind, component_structures)
        if assembly.is_free_bindsite(bs)]
    return entering_bindsites
