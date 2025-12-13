from nasap_net.graph import color_vertices_and_edges, \
    convert_assembly_to_graph, decode_mapping
from nasap_net.models import Assembly
from .exceptions import IsomorphismNotFoundError
from .models import Isomorphism
from .utils import reverse_mapping_seq


def get_isomorphism(assem1: Assembly, assem2: Assembly) -> Isomorphism:
    """Get an isomorphism between two assemblies."""
    conv_res1 = convert_assembly_to_graph(assem1)
    conv_res2 = convert_assembly_to_graph(assem2)

    g1 = conv_res1.graph
    g2 = conv_res2.graph

    try:
        colors = color_vertices_and_edges(g1, g2)
    except IsomorphismNotFoundError:
        raise IsomorphismNotFoundError() from None

    mapping: list[int]
    _, mapping, _ = g1.isomorphic_vf2(
        g2,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
        return_mapping_12=True,
    )

    return decode_mapping(mapping, conv_res1, conv_res2)


def get_all_isomorphisms(
        assem1: Assembly, assem2: Assembly
) -> set[Isomorphism]:
    """Get all isomorphisms between two assemblies."""
    conv_res1 = convert_assembly_to_graph(assem1)
    conv_res2 = convert_assembly_to_graph(assem2)

    try:
        colors = color_vertices_and_edges(conv_res1.graph, conv_res2.graph)
    except IsomorphismNotFoundError:
        raise IsomorphismNotFoundError() from None

    # NOTE: returned mappings are from graph2 to graph1
    res: list[list[int]] = conv_res1.graph.get_isomorphisms_vf2(
        conv_res2.graph,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
    )

    isomorphisms = set()
    for second_to_first_mapping in res:
        first_to_second_mapping = reverse_mapping_seq(second_to_first_mapping)
        isomorphism = decode_mapping(
            first_to_second_mapping, conv_res1, conv_res2
        )
        isomorphisms.add(isomorphism)

    return isomorphisms
