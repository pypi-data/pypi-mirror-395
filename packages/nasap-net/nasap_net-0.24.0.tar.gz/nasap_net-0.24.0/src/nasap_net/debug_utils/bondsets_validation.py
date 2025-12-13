from collections.abc import Hashable, Iterable
from typing import TypeVar


def validate_bondsets(
        bondsets: Iterable[Iterable[int]]
        ) -> None:
    """Validate bondsets.

    Check if bondsets contain duplicate bonds or duplicates among them.

    Parameters
    ----------
    bondsets : Iterable[Iterable[int]]
        Bondsets to validate.

    Raises
    ------
    ValueError
        If bondsets contain duplicate bonds or duplicates among them.
    """
    for bondset in bondsets:
        duplicate_bonds = _find_duplicates(bondset)
        if duplicate_bonds:
            raise ValueError(
                f'Bondset contains duplicate bonds: '
                f'bondset={sorted(bondset)}, '
                f'duplicate_bonds={sorted(duplicate_bonds)}')
    bondsets = [frozenset(bondset) for bondset in bondsets]
    duplicate_bondsets = _find_duplicates(bondsets)
    if duplicate_bondsets:
        raise ValueError(
            f'Duplicate bondset found: '
            f'{sorted(sorted(bondset) for bondset in duplicate_bondsets)}')


T = TypeVar('T')

def _find_duplicates(items: Iterable[T]) -> list[T]:
    duplicates: set[T] | list[T]
    seen: set[T] | list[T]

    if isinstance(next(iter(items)), Hashable):
        duplicates = set()
        seen = set()
        add_dup = duplicates.add
        add_seen = seen.add
    else:
        duplicates = []
        seen = []
        add_dup = duplicates.append
        add_seen = seen.append

    for item in items:
        if item in seen:
            add_dup(item)
        add_seen(item)

    return list(duplicates)
