from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Self

from nasap_net.exceptions import IDNotSetError
from nasap_net.models import Assembly, Bond
from nasap_net.types import ID
from nasap_net.utils import construct_repr


@dataclass(frozen=True, init=False)
class SemiLightAssembly:
    components: dict[ID, str]
    bonds: frozenset[Bond]
    _id: ID | None

    def __init__(
            self,
            components: Mapping[ID, str],
            bonds: Iterable[Bond],
            id_: ID | None = None,
            ):
        object.__setattr__(self, 'components', components)
        object.__setattr__(self, 'bonds', frozenset(bonds))
        object.__setattr__(self, '_id', id_)

    def __repr__(self):
        fields: dict[str, Any] = {}
        if self._id is not None:
            fields['id_'] = self._id
        fields['components'] = self.components
        fields['bonds'] = [bond.to_tuple() for bond in sorted(self.bonds)]
        return construct_repr(self.__class__, fields)

    @property
    def id_(self) -> ID:
        if self._id is None:
            raise IDNotSetError('SemiLightAssembly ID is not set.')
        return self._id

    @property
    def id_or_none(self) -> ID | None:
        return self._id

    @classmethod
    def from_assembly(cls, assembly: Assembly) -> Self:
        components = {
            comp_id: comp.kind
            for comp_id, comp in assembly.components.items()
        }
        return cls(
            components=components,
            bonds=assembly.bonds,
            id_=assembly.id_or_none,
        )
