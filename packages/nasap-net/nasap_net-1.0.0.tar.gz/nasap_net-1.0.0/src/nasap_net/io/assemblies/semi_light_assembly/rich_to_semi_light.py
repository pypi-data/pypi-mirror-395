from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from nasap_net.models import Assembly, Component
from nasap_net.models.component_consistency_check import \
    check_component_consistency
from nasap_net.types import ID
from .semi_light_assembly import SemiLightAssembly


@dataclass(frozen=True)
class ConversionResult:
    semi_light_assemblies: Mapping[ID, SemiLightAssembly]
    components: Mapping[str, Component]


_T = TypeVar('_T', bound=ID)

def convert_assemblies_to_semi_light_ones(
        assemblies: Mapping[_T, Assembly],
) -> ConversionResult:
    semi_light_assemblies = _assemblies_to_semi_light_assemblies(assemblies)

    check_component_consistency(assemblies.values())
    components = _extract_components(assemblies.values())

    return ConversionResult(
        semi_light_assemblies=semi_light_assemblies,
        components=components,
    )


def _extract_components(
        assemblies: Iterable[Assembly],
) -> dict[str, Component]:
    components: dict[str, Component] = {}
    for assembly in assemblies:
        for comp in assembly.components.values():
            if comp.kind in components:
                assert comp == components[comp.kind]
            else:
                components[comp.kind] = comp
    return components


def _assemblies_to_semi_light_assemblies(
        assemblies: Mapping[_T, Assembly],
        ) -> Mapping[ID, SemiLightAssembly]:
    return {
        assembly_id: SemiLightAssembly.from_assembly(assembly)
        for assembly_id, assembly in assemblies.items()
    }
