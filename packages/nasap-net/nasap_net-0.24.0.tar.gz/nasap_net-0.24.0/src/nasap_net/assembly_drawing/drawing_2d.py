from collections.abc import Mapping
from typing import Literal

import matplotlib.pyplot as plt
import networkx as nx

from nasap_net import Assembly, Component

from .color_map import make_complete_color_map

__all__ = ['draw_2d']


def draw_2d(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        positions: Mapping[str, tuple[float, float]],
        *,
        show: bool = True,
        # Sizes and colors
        core_node_size: int = 1600,
        bindsite_node_size: int = 400,
        component_colors: Mapping[str, str] = {},
        # Layout
        figsize: tuple[float, float] = (6, 6),
        x_lim: tuple[float, float] | None = None,
        y_lim: tuple[float, float] | None = None,
        # Labels
        node_labeling_mode: Literal[
            'component_kind', 'component_id', 'core_and_bindsite_ids',
            None] = 'component_kind',
        node_labeling_args: Mapping = {'font_size': 12},
        label_aux_edges: bool = True,
        aux_edge_labeling_args: Mapping = {'font_size': 12},
        # Others
        show_axes: bool = False,
        show_grid: bool = False,
        ) -> None:
    component_colors = make_complete_color_map(assembly, component_colors)

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_position((0, 0, 1, 1))
    ax.set_aspect('equal')

    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)
    
    g = assembly.g_snapshot(component_structures)

    # ========= Draw the graph =========

    # Draw cores
    cores = list(assembly.iter_all_cores())

    core_fill_colors = [
        component_colors[assembly.get_component_kind_of_core(n)] 
        for n in cores]
    
    nx.draw_networkx_nodes(
        g, positions, ax=ax, nodelist=cores,
        node_color=core_fill_colors, node_size=core_node_size)

    # Draw bindsite
    bindsites = list(assembly.get_all_bindsites(component_structures))

    bindsite_edge_colors = [
        component_colors[assembly.get_component_kind_of_bindsite(n)] 
        for n in bindsites]
    
    nx.draw_networkx_nodes(
        g, positions, ax=ax, nodelist=bindsites,
        node_color='white', edgecolors=bindsite_edge_colors, linewidths=2,
        node_size=bindsite_node_size)
    
    # Draw core-to-bindsite edges
    for comp_id, comp_kind in assembly.comp_id_to_kind.items():
        color = component_colors[comp_kind]
        core = assembly.get_core_of_the_component(comp_id)
        bindsites_of_the_comp = assembly.get_bindsites_of_component(
            comp_id, component_structures)
        
        for bindsite in bindsites_of_the_comp:
            nx.draw_networkx_edges(
                g, positions, edgelist=[(core, bindsite)], edge_color=color, 
                style='solid', width=12)
    
    # Draw bonds
    for bindsite1, bindsite2 in assembly.bonds:
        nx.draw_networkx_edges(
            g, positions, edgelist=[(bindsite1, bindsite2)], edge_color='grey', 
            style=(0, (2, 1)), width=2)
        
    # Draw aux edges
    for aux_edge in assembly.iter_aux_edges(component_structures):
        nx.draw_networkx_edges(
            g, positions, edgelist=[(aux_edge.bindsite1, aux_edge.bindsite2)], 
            edge_color='black', style='dotted')
    
    # Draw the labels
    labels = {}
    match node_labeling_mode:
        case 'component_kind':
            for comp_id, comp_kind in assembly.comp_id_to_kind.items():
                core = assembly.get_core_of_the_component(comp_id)
                labels[core] = comp_kind
        case 'component_id':
            for comp_id in assembly.component_ids:
                core = assembly.get_core_of_the_component(comp_id)
                labels[core] = comp_id
        case 'core_and_bindsite_ids':
            for core in cores:
                labels[core] = core
            for bindsite in bindsites:
                labels[bindsite] = bindsite

    if node_labeling_mode is not None:
        nx.draw_networkx_labels(
            g, positions, labels=labels, **node_labeling_args)

    if label_aux_edges:
        edge_labels = {}
        for aux_edge in assembly.iter_aux_edges(component_structures):
            edge_labels[
                (aux_edge.bindsite1, aux_edge.bindsite2)] = aux_edge.aux_type
        nx.draw_networkx_edge_labels(
            g, positions, edge_labels=edge_labels, **aux_edge_labeling_args)

    # ========= Set the plot =========
    
    core_width_pt = core_node_size ** 0.5  # 40 (pt)
    inch_per_pt = 1 / 72  # 0.014 (inch/pt)
    px_per_inches = fig.dpi  # 100 (px/inch)
    core_width_px = core_width_pt * inch_per_pt * px_per_inches  # 40 * 1/72 * 100 = 56 (px)
    
    fig_size_px = fig.get_size_inches() * fig.dpi  # np.array([600, 600])
    fig_width_px = fig_size_px[0]  # 600 (px)
    fig_height_px = fig_size_px[1]  # 600 (px)

    data_x_min = min([x for x, _ in positions.values()])
    data_x_max = max([x for x, _ in positions.values()])
    data_y_min = min([y for _, y in positions.values()])
    data_y_max = max([y for _, y in positions.values()])

    data_x_range = data_x_max - data_x_min
    data_y_range = data_y_max - data_y_min

    if data_x_range > data_y_range:
        x_fig_width_px = fig_width_px
        y_fig_width_px = fig_width_px * data_y_range / data_x_range
    else:
        x_fig_width_px = fig_height_px * data_x_range / data_y_range
        y_fig_width_px = fig_height_px

    x_core_width_norm = core_width_px / x_fig_width_px
    if y_fig_width_px == 0:
        y_core_width_norm = 0
    else:
        y_core_width_norm = core_width_px / y_fig_width_px

    margin_scale = .8
    ax.margins(x_core_width_norm * margin_scale, y_core_width_norm * margin_scale)

    # show axis ticks
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

    if not show_axes:
        ax.set_axis_off()
    if not show_grid:
        ax.grid(False)

    plt.tight_layout()

    # plt.axis('off')

    if show:
        plt.show()
