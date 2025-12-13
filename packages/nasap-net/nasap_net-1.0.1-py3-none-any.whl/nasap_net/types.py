from typing import Protocol, TypeAlias, TypeVar

S = TypeVar('S', int, str)  # Site ID
C = TypeVar('C', int, str)  # Component ID
A = TypeVar('A', int, str)  # Assembly ID
R = TypeVar('R', int, str)  # Reaction ID
ID: TypeAlias = int | str


class SupportsDunderLt(Protocol):
    def __lt__(self, other: object) -> bool:
        ...
