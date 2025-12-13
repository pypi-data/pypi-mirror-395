from nasap_net.graph import color_vertices_and_edges, \
    convert_assembly_to_graph
from nasap_net.models import Assembly
from .exceptions import IsomorphismNotFoundError


def is_isomorphic(assem1: Assembly, assem2: Assembly) -> bool:
    g1 = convert_assembly_to_graph(assem1).graph
    g2 = convert_assembly_to_graph(assem2).graph

    try:
        colors = color_vertices_and_edges(g1, g2)
    except IsomorphismNotFoundError:
        return False

    return g1.isomorphic_vf2(
        g2,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
    )
