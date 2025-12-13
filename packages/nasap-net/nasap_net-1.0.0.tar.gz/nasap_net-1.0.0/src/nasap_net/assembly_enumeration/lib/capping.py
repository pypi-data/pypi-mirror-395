from collections.abc import Iterable

from nasap_net.models import Assembly, BindingSite, Bond, Component
from nasap_net.types import ID


def cap_assemblies_with_ligand(
        fragments: Iterable[Assembly],
        component: Component,
        component_site_id: ID | None,
        metal_kinds: Iterable[str],
) -> set[Assembly]:
    """Cap all free metal sites in the assemblies with the given component"""
    if component_site_id is None:
        component_site_id = next(iter(sorted(component.site_ids)))

    return {
        cap_assembly(
            assembly=fragment,
            component=component,
            component_site_id=component_site_id,
            metal_kinds=metal_kinds,
        )
        for fragment in fragments
    }


def cap_assembly(
        assembly: Assembly,
        component: Component,
        component_site_id: ID,
        metal_kinds: Iterable[str],
) -> Assembly:
    """Add the leaving ligand to all free coordination sites of the metals"""
    free_metal_sites = get_free_metal_sites(assembly, metal_kinds)
    for i, site in enumerate(free_metal_sites):
        comp_id = f'{component.kind}{i}'
        assembly = add_component(
            assembly=assembly,
            assembly_site=site,
            component=component,
            component_site=BindingSite(comp_id, component_site_id),
            adding_component_id=comp_id,
        )
    return assembly


def get_free_metal_sites(
        assembly: Assembly,
        metal_kinds: Iterable[str]
) -> set[BindingSite]:
    free_sites: set[BindingSite] = set()
    for metal_kind in metal_kinds:
        free_sites.update(
            assembly.find_sites(
                has_bond=False,
                component_kind=metal_kind,
            )
        )
    return free_sites


def add_component(
        assembly: Assembly,
        assembly_site: BindingSite,
        component: Component,
        component_site: BindingSite,
        adding_component_id: ID,
) -> Assembly:
    components = dict(assembly.components)
    components[adding_component_id] = component
    bonds = set(assembly.bonds)
    bonds.add(Bond.from_sites(assembly_site, component_site))
    return Assembly(
        components=components,
        bonds=bonds,
        id_=assembly.id_or_none
    )
