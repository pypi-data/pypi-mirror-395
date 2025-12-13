from collections.abc import Iterable
from typing import Protocol, TypeVar, cast

from nasap_net.exceptions import DuplicateIDError, IDNotSetError
from nasap_net.types import ID


class IDProvider(Protocol):
    @property
    def id_(self) -> ID:
        ...

    @property
    def id_or_none(self) -> ID | None:
        ...


_T = TypeVar('_T', bound=IDProvider)


def validate_unique_ids(items: Iterable[_T]) -> None:
    """Validate that all items have IDs set and that all IDs are unique.

    Parameters
    ----------
    items : Iterable[IDProvider]
        The items to validate.

    Raises
    ------
    IDNotSetError
        If any item does not have an ID set.
    DuplicateIDError
        If any duplicate IDs are found.
    """
    seen_ids: set[ID] = set()
    # All items must have IDs and unique IDs
    for item in items:
        if item.id_or_none is None:
            raise IDNotSetError(
                'All items must have IDs.'
            )
        if item.id_ in seen_ids:
            raise DuplicateIDError(
                f'Duplicate ID found: {item.id_} '
                f'(object type: {type(item).__name__})'
            )
        seen_ids.add(cast(ID, item.id_))
