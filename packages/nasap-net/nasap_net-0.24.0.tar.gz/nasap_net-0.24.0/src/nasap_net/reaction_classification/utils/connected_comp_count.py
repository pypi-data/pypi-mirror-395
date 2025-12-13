from collections.abc import Mapping

from nasap_net import Assembly, BindsiteIdConverter, Component


def count_connected(
        assembly: Assembly, comp_id: str, target_comp_kind: str,
        comp_kind_to_obj: Mapping[str, Component]
        ) -> int:
    """Count the number of connected components of a certain kind."""
    id_converter = BindsiteIdConverter()
    num = 0

    for bindsite in assembly.get_bindsites_of_component(
            comp_id, comp_kind_to_obj):
        connected = assembly.get_connected_bindsite(bindsite)
        if connected is None:
            continue
        if target_comp_kind is not None:
            if assembly.get_component_kind_of_bindsite(connected) == target_comp_kind:
                num += 1
        else:
            num += 1

    return num