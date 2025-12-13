from collections.abc import Iterable, Mapping

__all__ = ['compare_mapping_iterables']


def compare_mapping_iterables(
        iterable1: Iterable[Mapping], iterable2: Iterable[Mapping]
        ) -> bool:
    """
    Compare two iterables of mappings.

    Args:
        iterable1: First iterable of mappings.
        iterable2: Second iterable of mappings.

    Returns:
        bool: True if both iterables contain the same mappings, False otherwise.
    """
    set1 = set(frozenset(d.items()) for d in iterable1)
    set2 = set(frozenset(d.items()) for d in iterable2)
    return set1 == set2
