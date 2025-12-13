from collections import defaultdict
from collections.abc import Hashable, Iterable

from nasap_net.isomorphism import is_isomorphic
from nasap_net.models import Assembly
from .signature import get_assembly_signature


def extract_unique_assemblies(
        assemblies: Iterable[Assembly]
) -> set[Assembly]:
    """Extract unique assemblies by isomorphism from a collection of assemblies.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        The collection of assemblies to extract unique assemblies from.

    Returns
    -------
    set[Assembly]
        A set of unique assemblies by isomorphism.
    """
    sig_to_unique_assembly: dict[Hashable, set[Assembly]] = defaultdict(set)
    for assembly in assemblies:
        sig = get_assembly_signature(assembly)
        is_unique = True
        for unique_assembly in sig_to_unique_assembly[sig]:
            if is_isomorphic(assembly, unique_assembly):
                is_unique = False
                break
        if is_unique:
            sig_to_unique_assembly[sig].add(assembly)
    unique_assemblies = set()
    for assemblies_set in sig_to_unique_assembly.values():
        unique_assemblies.update(assemblies_set)
    return unique_assemblies
