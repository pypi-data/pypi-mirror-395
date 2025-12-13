import yaml

from nasap_net.models import AuxEdge, Component


def load_components(yaml_str: str) -> dict[str, Component]:
    """Load components from a YAML string."""
    return yaml.load(yaml_str, Loader=_ComponentLoader)  # type: ignore


class _ComponentLoader(yaml.SafeLoader):
    def ignore_aliases(self, _):
        return True


def _component_constructor(
        loader: _ComponentLoader,
        node: yaml.Node,
) -> Component:
    assert isinstance(node, yaml.MappingNode)
    mapping = loader.construct_mapping(node, deep=True)
    kind = mapping['kind']
    sites = mapping['sites']
    aux_edges = []
    for m in mapping.get('aux_edges', []):
        site1, site2 = m['sites']
        aux_kind = m.get('kind')
        aux_edges.append(AuxEdge(site1, site2, kind=aux_kind))
    return Component(kind=kind, sites=sites, aux_edges=aux_edges)


yaml.add_constructor(
    '!Component', _component_constructor, Loader=_ComponentLoader
)
