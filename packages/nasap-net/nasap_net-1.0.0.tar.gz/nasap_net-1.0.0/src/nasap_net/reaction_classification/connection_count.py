from nasap_net.models import Assembly
from nasap_net.types import ID


def get_connection_count_of_kind(
        assembly: Assembly,
        source_component_id: ID,
        target_kind: str,
) -> int:
    """Get the number of connections from a source component to components of a target kind.

    Parameters
    ----------
    assembly : Assembly
        The assembly containing the components and their connections.
    source_component_id : ID
        The ID of the source component.
    target_kind : str
        The kind of the target components.

    Returns
    -------
    int
        The number of connections from the source component to components of the target kind.
    """
    count = 0
    for bond in assembly.bonds:
        comp_id1, comp_id2 = bond.component_ids
        if source_component_id == comp_id1:
            other_comp_id = comp_id2
        elif source_component_id == comp_id2:
            other_comp_id = comp_id1
        else:
            continue
        if assembly.components[other_comp_id].kind == target_kind:
            count += 1
    return count
