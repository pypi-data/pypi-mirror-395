from nasap_net.models import Assembly, BindingSite, Reaction
from nasap_net.rough_graph import convert_assembly_to_rough_graph


def forms_ring(reaction: Reaction) -> bool:
    """Determine if a reaction forms a ring.

    Parameters
    ----------
    reaction : Reaction
        The reaction to analyze.

    Returns
    -------
    bool
        True if the reaction forms a ring, False otherwise.
    """
    return get_min_forming_ring_size(reaction) is not None


def get_min_forming_ring_size(reaction: Reaction) -> int | None:
    """Determine the minimum ring size formed by a reaction.

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
    """
    # Ring formation can only occur in intra reactions
    if reaction.is_inter():
        return None

    return get_min_forming_ring_size_internal(
        assembly=reaction.init_assem,
        metal_bs=reaction.metal_bs,
        leaving_bs=reaction.leaving_bs,
        entering_bs=reaction.entering_bs,
    )


def get_min_forming_ring_size_internal(
        assembly: Assembly,
        metal_bs: BindingSite,
        leaving_bs: BindingSite,
        entering_bs: BindingSite,
) -> int | None:
    """Determine the minimum ring size formed between two binding sites
    within an assembly.
    """
    # Create a modified assembly by removing the bond between
    bond_removed_assem = assembly.remove_bond(metal_bs, leaving_bs)

    # The above bond removal ensures that
    # any path between the metal and entering binding sites
    # must form a ring in the original assembly.

    # Example:
    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    # metal_bs = M0(1), leaving_bs = L0(0), entering_bs = L1(1)
    # This reaction does not form a ring, and results in:
    # X0(0)-(0)M0(1)-(1)L1(0)-(1)M1(0)-(1)L0(0)

    # However, if we naively check the shortest path between M0 and L1,
    # we would find a path of length 4,
    # which incorrectly suggests a ring of size 4 is formed.

    # By removing the bond between M0 and L0 beforehand, we get:
    # X0(0)-(0)M0(1)    (0)L0(1)-(0)M1(1)-(0)L1(1)
    # There is no path between M0 and L1, so the function correctly returns None.

    # Convert assemblies to igraph objects
    conv_res = convert_assembly_to_rough_graph(bond_removed_assem)

    # Minimum ring size can be determined from the shortest path between
    # the metal binding site and the entering binding site in the initial assembly.
    shortest_path_vertices = conv_res.graph.get_shortest_paths(
        conv_res.core_mapping[metal_bs.component_id],
        conv_res.core_mapping[entering_bs.component_id],
    )

    length = len(shortest_path_vertices[0])

    if length == 0:
        return None
    assert length % 2 == 0
    return length // 2
