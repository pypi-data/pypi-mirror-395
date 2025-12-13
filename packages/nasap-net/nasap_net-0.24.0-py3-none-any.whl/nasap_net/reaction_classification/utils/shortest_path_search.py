from math import inf

import networkx as nx

from nasap_net import Assembly


def find_shortest_path(
        assembly: Assembly,
        comp_id1: str, comp_id2: str,
        ) -> list | None:
    """Find one of the shortest paths between two components in the assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly object.
    comp_id1 : str
        The component ID of the first component.
    comp_id2 : str
        The component ID of the second component.

    Returns
    -------
    list | None
        The list of component IDs in the shortest path between the two components.
        If no path exists, return None.
    """
    if comp_id1 not in assembly.component_ids:
        raise ValueError(f"Component {comp_id1} is not in the assembly")
    if comp_id2 not in assembly.component_ids:
        raise ValueError(f"Component {comp_id2} is not in the assembly")
    g = assembly.rough_g_snapshot
    try:
        path = nx.shortest_path(g, comp_id1, comp_id2)
        return path
    except nx.NetworkXNoPath:
        return None
