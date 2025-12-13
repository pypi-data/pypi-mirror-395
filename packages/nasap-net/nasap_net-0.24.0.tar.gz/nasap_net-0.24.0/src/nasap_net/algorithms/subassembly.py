from collections.abc import Iterable

from nasap_net import Assembly


def bond_induced_sub_assembly(
        assembly: Assembly, bonds: Iterable[Iterable[str]]) -> Assembly:
    """Create a sub-assembly induced by the bonds.

    The induced sub-assembly contains all the bonds in the `bonds` and
    all the components connected by any bond in the `bonds`.
    """
    component_ids: set[str] = set()
    for bond in bonds:
        component_ids.update(assembly.bond_to_rough_bond(bond))

    components = {
        comp_id: assembly.get_component_kind(comp_id)
        for comp_id in component_ids}

    return Assembly(components, bonds)


def component_induced_sub_assembly(
        assembly: Assembly, component_ids: set[str]) -> Assembly:
    """Create a sub-assembly induced by the components.

    The induced sub-assembly contains all the components in the 
    `component_ids` and all the bonds between the components in the 
    `component_ids`.
    """
    components = {
        comp_id: assembly.get_component_kind(comp_id) for comp_id in component_ids}
    bonds = {
        bond for bond in assembly.bonds
        if set(assembly.bond_to_rough_bond(bond)) <= component_ids}
    # i.e., if the both binding sites of a bond are in the component_ids

    return Assembly(components, bonds)
