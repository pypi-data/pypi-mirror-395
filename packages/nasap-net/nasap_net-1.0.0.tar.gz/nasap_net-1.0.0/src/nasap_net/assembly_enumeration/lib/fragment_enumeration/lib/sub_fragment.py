from collections.abc import Iterable

from nasap_net.types import ID
from ..models import Fragment


def create_sub_fragment(
        fragment: Fragment, comp_ids: Iterable[ID]
) -> Fragment:
    """Create a sub-assembly containing only the specified components."""
    new_components = {
        comp_id for comp_id in fragment.components
        if comp_id in comp_ids
    }
    new_bonds = [
        bond for bond in fragment.bonds
        if bond.component_ids <= set(comp_ids)
    ]
    return fragment.copy_with(components=new_components, bonds=new_bonds)
