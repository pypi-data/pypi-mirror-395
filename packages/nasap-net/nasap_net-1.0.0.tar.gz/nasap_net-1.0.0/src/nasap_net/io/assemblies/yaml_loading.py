from nasap_net.io.assemblies.helper import split_yaml_documents
from nasap_net.io.assemblies.lib import load_components, load_semi_light_assemblies
from nasap_net.models import Assembly, Component
from .semi_light_assembly import SemiLightAssembly, \
    convert_semi_light_assemblies_to_rich_ones


def load_assemblies_from_str(yaml_str: str) -> list[Assembly]:
    components, light_assemblies = _load_components_and_semi_light_assemblies(
        yaml_str=yaml_str,
    )
    assembly_map = convert_semi_light_assemblies_to_rich_ones(
        dict(enumerate(light_assemblies)), components
    )
    return list(assembly_map.values())


def _load_components_and_semi_light_assemblies(
        yaml_str: str,
) -> tuple[dict[str, Component], list[SemiLightAssembly]]:
    docs = list(split_yaml_documents(yaml_str))
    if len(docs) != 2:
        raise ValueError(
            f"Expected exactly 2 YAML documents, found {len(docs)}.")
    components = load_components(docs[0])
    semi_light_assemblies = load_semi_light_assemblies(docs[1])
    return components, semi_light_assemblies
