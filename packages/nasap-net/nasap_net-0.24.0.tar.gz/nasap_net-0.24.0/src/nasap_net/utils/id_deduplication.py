from collections.abc import Hashable, Iterable
from typing import Protocol, Self, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec('P')


class HasCopyWith(Protocol[P]):
    @property
    def id_(self) -> Hashable:
        ...

    # TODO: Use more specific signature when PyCharm fixes the issue PY-70838
    # copy_with(self, *, id_: Any) -> Self:
    def copy_with(self, **kwargs: P.kwargs) -> Self:
        ...


_T = TypeVar('_T', bound=HasCopyWith)

def deduplicate_ids(items: Iterable[_T]) -> list[_T]:
    """Deduplicate IDs of items by appending suffixes.

    If multiple items have the same ID, this function appends suffixes
    like '_2', '_3', etc.

    - The first occurrence of an ID remains unchanged.
    - The second occurrence gets '_2' appended.
    - The third occurrence gets '_3' appended, and so on.

    Parameters
    ----------
    items : Iterable[_T]
        An iterable of items with IDs.

    Returns
    -------
    list[_T]
        A list of items with deduplicated IDs.

    Notes
    -----
    This function assumes that each item has an 'id_' attribute and a
    'copy_with' method that allows creating a copy of the item with
    modified attributes.
    The `copy_with` method should accept keyword arguments of `id_`.
    """
    seen_ids: set[Hashable] = set()
    deduplicated_items: list[_T] = []

    for item in items:
        if item.id_ not in seen_ids:
            seen_ids.add(item.id_)
            deduplicated_items.append(item)
            continue

        suffix = 2
        new_id = f'{item.id_}_{suffix}'
        while new_id in seen_ids:
            suffix += 1
            new_id = f'{item.id_}_{suffix}'
        seen_ids.add(new_id)
        deduplicated_items.append(item.copy_with(id_=new_id))
    return deduplicated_items
