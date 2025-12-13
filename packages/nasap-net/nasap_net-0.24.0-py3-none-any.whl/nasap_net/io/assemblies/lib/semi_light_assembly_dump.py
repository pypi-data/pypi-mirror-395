from typing import Any

import yaml

from nasap_net.io.assemblies.semi_light_assembly import SemiLightAssembly
from nasap_net.models import Bond


def dump_semi_light_assemblies(assemblies: Any) -> str:
    """Dump light assemblies to a YAML string."""
    return yaml.dump(
        assemblies,
        Dumper=_SemiLightAssemblyDumper,
        sort_keys=False,
        default_flow_style=None,
    )


class _SemiLightAssemblyDumper(yaml.SafeDumper):
    def ignore_aliases(self, _):
        return True


def _semi_light_assembly_representer(
        dumper: _SemiLightAssemblyDumper, data: SemiLightAssembly
) -> yaml.MappingNode:
    mapping: dict = {
        'components': dict(sorted(data.components.items())),
        'bonds': sorted(data.bonds),
    }
    if data.id_or_none is not None:
        mapping['id_'] = data.id_
    return dumper.represent_mapping('!Assembly', mapping)


def _bond_representer(
        dumper: _SemiLightAssemblyDumper, data: Bond
) -> yaml.SequenceNode:
    site1, site2 = sorted(data.sites)
    return dumper.represent_list([
        site1.component_id,
        site1.site_id,
        site2.component_id,
        site2.site_id,
    ])


yaml.add_representer(
    SemiLightAssembly,
    _semi_light_assembly_representer,
    Dumper=_SemiLightAssemblyDumper,
)
yaml.add_representer(Bond, _bond_representer, Dumper=_SemiLightAssemblyDumper)
