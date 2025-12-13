from collections.abc import Iterable, Mapping

from nasap_net import Assembly
from nasap_net.algorithms.subassembly import bond_induced_sub_assembly

__all__ = ['convert_bondset_to_assembly']


def convert_bondset_to_assembly(
        bond_subset: Iterable[str],
        comp_id_to_kind: Mapping[str, str],
        bond_id_to_bindsites: Mapping[str, Iterable[str]]
        ) -> Assembly:
    """Converts the connected bonds to a graph."""
    
    connected_bindsite_pairs = {
        frozenset(bond_id_to_bindsites[bond]) for bond in bond_subset}
    
    template = Assembly(comp_id_to_kind, bond_id_to_bindsites.values())
    
    return bond_induced_sub_assembly(template, connected_bindsite_pairs)
