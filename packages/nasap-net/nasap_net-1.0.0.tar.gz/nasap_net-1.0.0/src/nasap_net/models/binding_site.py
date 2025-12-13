from dataclasses import dataclass
from functools import total_ordering

from nasap_net.types import ID, SupportsDunderLt


@total_ordering
@dataclass(frozen=True)
class BindingSite(SupportsDunderLt):
    """A specific binding site on a specific component."""
    component_id: ID
    site_id: ID

    def __lt__(self, other):
        if not isinstance(other, BindingSite):
            return NotImplemented
        self_values = (self.component_id, self.site_id)
        other_values = (other.component_id, other.site_id)
        return self_values < other_values

    def __repr__(self):
        return f'BindingSite({self.component_id!r}, {self.site_id!r})'
