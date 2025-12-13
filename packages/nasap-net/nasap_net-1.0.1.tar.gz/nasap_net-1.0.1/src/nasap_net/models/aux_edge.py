from dataclasses import dataclass, field
from functools import total_ordering

from nasap_net.types import ID, SupportsDunderLt
from .binding_site import BindingSite


@total_ordering
@dataclass(frozen=True, init=False)
class AuxEdge(SupportsDunderLt):
    """An auxiliary edge between two binding sites on the same component."""
    site_ids: frozenset[ID]
    kind: str | None = field(kw_only=True, default=None)

    def __init__(
            self, site_id1: ID, site_id2: ID, kind: str | None = None):
        if site_id1 == site_id2:
            raise ValueError("Sites in an auxiliary edge must be different.")
        object.__setattr__(
            self, 'site_ids',
            frozenset({site_id1, site_id2}))
        object.__setattr__(self, 'kind', kind)

    def __lt__(self, other):
        if not isinstance(other, AuxEdge):
            return NotImplemented
        self_values = [sorted(self.site_ids), self.kind]
        other_values = [sorted(other.site_ids), other.kind]
        return self_values < other_values

    def get_binding_sites(
            self, comp_id: ID,
    ) -> frozenset[BindingSite]:
        """Return the binding sites of this auxiliary edge."""
        site_id1, site_id2 = self.site_ids
        return frozenset({
            BindingSite(component_id=comp_id, site_id=site_id1),
            BindingSite(component_id=comp_id, site_id=site_id2)
        })

    def to_tuple(self) -> tuple[ID, ID] | tuple[ID, ID, str]:
        """Return a tuple representation of the auxiliary edge."""
        site_id1, site_id2 = sorted(self.site_ids)
        if self.kind is None:
            return site_id1, site_id2
        return site_id1, site_id2, self.kind
