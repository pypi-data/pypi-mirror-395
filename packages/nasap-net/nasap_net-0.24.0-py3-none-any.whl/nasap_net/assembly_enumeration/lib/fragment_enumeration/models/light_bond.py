from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import Self

from nasap_net.models import Bond
from nasap_net.types import ID


@total_ordering
@dataclass(frozen=True, init=False)
class LightBond:
    component_ids: frozenset[ID]

    def __init__(self, comp_id1: ID, comp_id2: ID) -> None:
        object.__setattr__(
            self, 'component_ids', frozenset({comp_id1, comp_id2})
        )

    def __lt__(self, other):
        if not isinstance(other, LightBond):
            return NotImplemented
        return sorted(self.component_ids) < sorted(other.component_ids)

    @classmethod
    def from_bond(cls, bond: Bond) -> Self:
        site1, site2 = bond.sites
        return cls(site1.component_id, site2.component_id)
