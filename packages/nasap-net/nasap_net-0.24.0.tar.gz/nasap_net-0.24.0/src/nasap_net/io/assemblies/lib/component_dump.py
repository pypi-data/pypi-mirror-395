from typing import Any

import yaml

from nasap_net.models import AuxEdge, BindingSite, Component


def dump_components(components: Any) -> str:
    """Dump components to a YAML string."""
    return yaml.dump(
        components,
        Dumper=ComponentDumper,
        sort_keys=False,
        default_flow_style=None,
    )


class ComponentDumper(yaml.SafeDumper):
    def ignore_aliases(self, _):
        return True


def _component_representer(
        dumper: ComponentDumper, data: Component
) -> yaml.MappingNode:
    mapping: dict = {
        'kind': data.kind,
        'sites': sorted(data.site_ids),
    }
    if data.aux_edges:
        mapping['aux_edges'] = sorted(data.aux_edges)
    return dumper.represent_mapping('!Component', mapping)

def _binding_site_representer(
        dumper: ComponentDumper, data: BindingSite
) -> yaml.MappingNode:
    return dumper.represent_mapping('!BindingSite', {
        'component_id': data.component_id,
        'site_id': data.site_id,
    })

def _aux_edge_representer(
        dumper: ComponentDumper, data: AuxEdge
) -> yaml.MappingNode:
    mapping: dict = {'sites': list(data.site_ids)}
    if data.kind is not None:
        mapping['kind'] = data.kind
    return dumper.represent_dict(mapping)


yaml.add_representer(Component, _component_representer, Dumper=ComponentDumper)
yaml.add_representer(BindingSite, _binding_site_representer, Dumper=ComponentDumper)
yaml.add_representer(AuxEdge, _aux_edge_representer, Dumper=ComponentDumper)
