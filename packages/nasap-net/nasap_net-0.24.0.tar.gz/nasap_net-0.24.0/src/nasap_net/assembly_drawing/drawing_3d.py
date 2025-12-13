from collections.abc import Mapping
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from nasap_net import Assembly, Component

from .color_map import make_complete_color_map

__all__ = ['draw_3d']


def draw_3d(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        positions: Mapping[str, tuple[float, float, float]],
        *,
        show: bool = True,
        # Sizes and colors
        core_node_size: int = 1600,
        bindsite_node_size: int = 400,
        component_colors: Mapping[str, str] = {},
        node_alpha: float = .8,
        edge_alpha: float = .8,
        core_to_bindsite_edge_width: float = 8,
        bond_edge_width: float = 2,
        # Layout
        figsize: tuple[float, float] = (6, 6),
        x_lim: tuple[float, float] | None = None,
        y_lim: tuple[float, float] | None = None,
        z_lim: tuple[float, float] | None = None,
        projection_type: Literal['ortho', 'persp'] = 'ortho',
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

    fig = plt.figure(figsize=figsize)
    ax: Axes3D = fig.add_subplot(111, projection='3d')
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
    
    core_pos = np.array([positions[n] for n in cores])
    
    ax.scatter(
        *core_pos.T, alpha=node_alpha, s=core_node_size,
        color=core_fill_colors
        )  # type: ignore
    
    # Draw bindsite
    bindsites = list(assembly.get_all_bindsites(component_structures))

    bindsite_edge_colors = [
        component_colors[assembly.get_component_kind_of_bindsite(n)] 
        for n in bindsites]
    
    bindsite_pos = np.array([positions[n] for n in bindsites])
    
    ax.scatter(
        *bindsite_pos.T, alpha=node_alpha, s=bindsite_node_size,
        color='#FFF', 
        edgecolors=bindsite_edge_colors, linewidths=2
        )  # type: ignore
    
    # Draw core-to-bindsite edges
    for comp_id, comp_kind in assembly.comp_id_to_kind.items():
        color = component_colors[comp_kind]
        core = assembly.get_core_of_the_component(comp_id)
        bindsites_of_the_comp = assembly.get_bindsites_of_component(
            comp_id, component_structures)
        
        for bindsite in bindsites_of_the_comp:
            xs = [positions[core][0], positions[bindsite][0]]
            ys = [positions[core][1], positions[bindsite][1]]
            zs = [positions[core][2], positions[bindsite][2]]
            
            ax.plot(
                xs, ys, zs, color=color, alpha=edge_alpha, 
                linewidth=core_to_bindsite_edge_width)
    
    # Draw bonds
    for bindsite1, bindsite2 in assembly.bonds:
        xs = [positions[bindsite1][0], positions[bindsite2][0]]
        ys = [positions[bindsite1][1], positions[bindsite2][1]]
        zs = [positions[bindsite1][2], positions[bindsite2][2]]

        ax.plot(
            xs, ys, zs, color='grey', alpha=edge_alpha, 
            linestyle=(0, (2, 1)), linewidth=bond_edge_width)
        
    # Draw aux edges
    for aux_edge in assembly.iter_aux_edges(component_structures):
        bs1 = aux_edge.bindsite1
        bs2 = aux_edge.bindsite2
        xs = [positions[bs1][0], positions[bs2][0]]
        ys = [positions[bs1][1], positions[bs2][1]]
        zs = [positions[bs1][2], positions[bs2][2]]

        ax.plot(
            xs, ys, zs, color='darkgrey', alpha=edge_alpha, 
            linestyle='dotted')

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

    node_labeling_ax_text_args = {}
    node_labeling_ax_text_args['fontsize'] = node_labeling_args.get('font_size', 12)
    node_labeling_ax_text_args['horizontalalignment'] = node_labeling_args.get(
        'horizontalalignment', 'center')
    node_labeling_ax_text_args['verticalalignment'] = node_labeling_args.get(
        'verticalalignment', 'center')

    if node_labeling_mode is not None:
        for node, label in labels.items():
            x, y, z = positions[node]
            ax.text(x, y, z, label, **node_labeling_ax_text_args)

    aux_labeling_ax_text_args = {}
    aux_labeling_ax_text_args['fontsize'] = aux_edge_labeling_args.get('font_size', 12)
    aux_labeling_ax_text_args['horizontalalignment'] = aux_edge_labeling_args.get(
        'horizontalalignment', 'center')
    aux_labeling_ax_text_args['verticalalignment'] = aux_edge_labeling_args.get(
        'verticalalignment', 'center')
    
    if label_aux_edges:
        for aux_edge in assembly.iter_aux_edges(component_structures):
            bs1 = aux_edge.bindsite1
            bs2 = aux_edge.bindsite2
            aux_kind = aux_edge.aux_type
            x = (positions[bs1][0] + positions[bs2][0]) / 2
            y = (positions[bs1][1] + positions[bs2][1]) / 2
            z = (positions[bs1][2] + positions[bs2][2]) / 2
            ax.text(x, y, z, aux_kind, **aux_labeling_ax_text_args)

    if not show_axes:
        ax.set_axis_off()
    if not show_grid:
        ax.grid(False)
    plt.tight_layout()

    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_zlim(z_lim)

    if projection_type == 'ortho':
        ax.set_proj_type('ortho')
    elif projection_type == 'persp':
        ax.set_proj_type('persp')

    if show:
        plt.show()
