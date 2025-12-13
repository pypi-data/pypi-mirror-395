from dataclasses import dataclass
from typing import Hashable

import igraph as ig

from nasap_net.exceptions import NasapNetError
from nasap_net.isomorphism.exceptions import IsomorphismNotFoundError


@dataclass(frozen=True)
class Colors:
    v_color1: tuple[int, ...]
    v_color2: tuple[int, ...]
    e_color1: tuple[int, ...]
    e_color2: tuple[int, ...]


def color_vertices_and_edges(g1: ig.Graph, g2: ig.Graph) -> Colors:
    try:
        v_color1, v_color2 = _vertex_color_lists(g1, g2)
    except _NotIsomorphicError:
        raise IsomorphismNotFoundError() from None

    try:
        e_color1, e_color2 = _edge_color_lists(g1, g2)
    except _NotIsomorphicError:
        raise IsomorphismNotFoundError() from None

    return Colors(
        v_color1=tuple(v_color1),
        v_color2=tuple(v_color2),
        e_color1=tuple(e_color1),
        e_color2=tuple(e_color2),
    )


class _NotIsomorphicError(NasapNetError):
    pass


def _vertex_color_lists(
        g1: ig.Graph, g2: ig.Graph) -> tuple[list[int], list[int]]:
    def _readable_v_color(vertex: ig.Vertex) -> Hashable:
        return vertex['core_or_site'], vertex['comp_kind']

    colors1 = {_readable_v_color(v) for v in g1.vs}
    colors2 = {_readable_v_color(v) for v in g2.vs}
    if colors1 != colors2:
        raise _NotIsomorphicError()

    color_to_int: dict[Hashable, int] = {c: i for i, c in enumerate(colors1)}
    color_list1 = [color_to_int[_readable_v_color(v)] for v in g1.vs]
    color_list2 = [color_to_int[_readable_v_color(v)] for v in g2.vs]
    return color_list1, color_list2


def _edge_color_lists(
        g1: ig.Graph, g2: ig.Graph) -> tuple[list[int], list[int]]:
    def _readable_edge_color(edge: ig.Edge) -> Hashable | None:
        return edge['aux_kind'] if 'aux_kind' in edge.attributes() else None

    colors1 = {_readable_edge_color(e) for e in g1.es}
    colors2 = {_readable_edge_color(e) for e in g2.es}
    if colors1 != colors2:
        raise _NotIsomorphicError()

    color_to_int: dict[Hashable | None, int] = {
        c: i for i, c in enumerate(colors1)}
    color_list1 = [color_to_int[_readable_edge_color(e)] for e in g1.es]
    color_list2 = [color_to_int[_readable_edge_color(e)] for e in g2.es]
    return color_list1, color_list2
