from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import total_ordering
from typing import Self

from nasap_net.types import ID, SupportsDunderLt
from .binding_site import BindingSite


@total_ordering
@dataclass(frozen=True, init=False)
class Bond(Iterable, SupportsDunderLt):
    """A bond between two binding sites on two components."""
    sites: frozenset[BindingSite]

    def __init__(self, comp_id1: ID, site1: ID, comp_id2: ID, site2: ID):
        if comp_id1 == comp_id2:
            raise ValueError("Components in a bond must be different.")
        comp_and_site1 = BindingSite(component_id=comp_id1, site_id=site1)
        comp_and_site2 = BindingSite(component_id=comp_id2, site_id=site2)
        object.__setattr__(
            self, 'sites',
            frozenset((comp_and_site1, comp_and_site2))
        )

    def __iter__(self) -> Iterator[BindingSite]:
        return iter(sorted(self.sites))

    def __lt__(self, other):
        if not isinstance(other, Bond):
            return NotImplemented
        self_values = sorted(self.sites)
        other_values = sorted(other.sites)
        return self_values < other_values

    @property
    def component_ids(self) -> frozenset[ID]:
        """Return the component IDs involved in the bond."""
        return frozenset(site.component_id for site in self.sites)

    def to_tuple(self) -> tuple[ID, ID, ID, ID]:
        """Return the bond as a tuple of component and site IDs."""
        site1, site2 = sorted(self.sites)
        return (
            site1.component_id, site1.site_id,
            site2.component_id, site2.site_id,
        )

    @classmethod
    def from_sites(cls, site1: BindingSite, site2: BindingSite) -> Self:
        """Create a Bond from two BindingSite instances."""
        return cls(
            comp_id1=site1.component_id,
            comp_id2=site2.component_id,
            site1=site1.site_id,
            site2=site2.site_id
            )
