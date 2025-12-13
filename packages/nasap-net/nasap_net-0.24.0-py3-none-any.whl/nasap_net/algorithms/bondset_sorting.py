from collections.abc import Iterable
from typing import TypeVar

__all__ = ['sort_bondsets']


T = TypeVar('T', bound=Iterable[str])


def sort_bondsets(bondsets: Iterable[T]) -> list[T]:
    """Sort bondsets by the number of bonds and the sorted bond IDs.

    The number of bonds is the primary key, and the sorted bond IDs 
    is the secondary key.

    The order of the equal elements is preserved.
    """
    return sorted(
        bondsets,
        key=lambda bondset: (len(list(bondset)), sorted(bondset))
        )


def sort_bondsets_and_bonds(bondsets: Iterable[Iterable[str]]) -> list[list[str]]:
    """Sort bondsets and bonds in the bondsets."""
    return sort_bondsets(
        (sorted(bondset) for bondset in bondsets)
        )
