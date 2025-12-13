from collections.abc import Mapping

from nasap_net import Assembly, Component, is_isomorphic

__all__ = ['is_new']


def is_new(
        hash_: str,
        assembly: Assembly,
        hash_to_uniques: Mapping[str, list[Assembly]],
        component_structures: Mapping[str, Component]
        ) -> bool:
    """Check if the assembly is new."""
    if hash_ not in hash_to_uniques:
        return True
    for unique in hash_to_uniques[hash_]:
        if is_isomorphic(
                assembly, unique, component_structures):
            return False
    return True
