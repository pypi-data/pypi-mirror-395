from collections.abc import Mapping
from typing import TypeVar

from nasap_net.io.assemblies.semi_light_assembly import SemiLightAssembly
from nasap_net.models import Assembly, Component
from nasap_net.types import ID

_T = TypeVar('_T', bound=ID)

def convert_semi_light_assembly_to_rich_one(
        semi_light_assembly: SemiLightAssembly,
        components: Mapping[str, Component],
) -> Assembly:
    return Assembly(
        components={
            comp_id: components[comp_kind]
            for comp_id, comp_kind in semi_light_assembly.components.items()
        },
        bonds=semi_light_assembly.bonds,
        id_=semi_light_assembly.id_or_none,
    )


def convert_semi_light_assemblies_to_rich_ones(
        semi_light_assemblies: Mapping[_T, SemiLightAssembly],
        components: Mapping[str, Component],
) -> dict[ID, Assembly]:
    return {
        assembly_id: convert_semi_light_assembly_to_rich_one(
            semi_light_assembly, components
        )
        for assembly_id, semi_light_assembly in semi_light_assemblies.items()
    }
