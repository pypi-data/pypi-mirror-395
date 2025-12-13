from collections.abc import Iterable, Mapping

import yaml

from nasap_net.io.assemblies.semi_light_assembly import SemiLightAssembly
from nasap_net.models import Bond, Component
from nasap_net.types import ID


def load_semi_light_assemblies(yaml_str: str) -> list[SemiLightAssembly]:
    """Load light assemblies from a YAML string."""
    return yaml.load(yaml_str, Loader=_SemiLightAssemblyLoader)  # type: ignore


class _SemiLightAssemblyLoader(yaml.SafeLoader):
    component_context: Mapping[str, Component] = {}

    def ignore_aliases(self, _):
        return True


def _semi_light_assembly_constructor(
        loader: _SemiLightAssemblyLoader,
        node: yaml.Node,
) -> SemiLightAssembly:
    assert isinstance(node, yaml.MappingNode)
    mapping = loader.construct_mapping(node, deep=True)
    components: dict[ID, str] = mapping['components']
    bonds: list[Bond] = [_construct_bond(b) for b in mapping['bonds']]
    assembly_id: str | None = mapping.get('id_')
    return SemiLightAssembly(
        components=components,
        bonds=bonds,
        id_=assembly_id,
    )


def _construct_bond(bonds: Iterable[ID]) -> Bond:
    comp_id1, site_id1, comp_id2, site_id2 = bonds
    return Bond(comp_id1, site_id1, comp_id2, site_id2)


yaml.add_constructor(
    '!Assembly', _semi_light_assembly_constructor,
    Loader=_SemiLightAssemblyLoader
)
