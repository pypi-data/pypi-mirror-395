from nasap_net.models import Reaction
from nasap_net.rough_graph import convert_assembly_to_rough_graph


def get_min_forming_ring_size_including_temporary(
        reaction: Reaction
) -> int | None:
    """Determine the minimum ring size formed during a reaction,
    including temporary rings.

    The "ring size" is defined as half the number of components involved
    in the ring.

    Examples:
     - M4L4 ring = size of 4
     - M3L3 ring = size of 3

    Returns None if the reaction does not form a ring.

    Parameters
    ----------
    reaction : Reaction
        The reaction to analyze.

    Returns
    -------
    int | None
        The minimum ring size formed, or None if no ring is formed.

    Notes
    -----
    "Temporary ring" includes rings that may be broken later in the reaction.
    Example:
    X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    metal_bs = M0(1), leaving_bs = L0(0), entering_bs = L1(1)
    This reaction temporarily forms a ring of size 2, even though the ring is broken
    when L0 leaves.
    """
    # Ring formation can only occur in intra reactions
    if reaction.is_inter():
        return None

    # Convert assemblies to igraph objects
    conv_res = convert_assembly_to_rough_graph(reaction.init_assem)

    # Minimum ring size can be determined from the shortest path between
    # the metal binding site and the entering binding site in the initial assembly.
    shortest_path_vertices = conv_res.graph.get_shortest_paths(
        conv_res.core_mapping[reaction.metal_bs.component_id],
        conv_res.core_mapping[reaction.entering_bs.component_id],
    )

    length = len(shortest_path_vertices[0])

    if length == 0:
        return None
    assert length % 2 == 0
    return length // 2
