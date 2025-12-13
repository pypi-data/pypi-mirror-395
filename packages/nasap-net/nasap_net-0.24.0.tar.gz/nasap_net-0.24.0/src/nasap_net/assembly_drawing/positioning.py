from collections.abc import Iterable, Mapping
from typing import Literal, TypeAlias, overload

import networkx as nx

from nasap_net import Assembly, Component

LAYOUT_NAME_TO_FUNC = {
    'spring': nx.spring_layout,
}


PosMap2D: TypeAlias = Mapping[str, tuple[float, float]]
PosMap3D: TypeAlias = Mapping[str, tuple[float, float, float]]
PosDict2D: TypeAlias = dict[str, tuple[float, float]]
PosDict3D: TypeAlias = dict[str, tuple[float, float, float]]


@overload
def calc_positions(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        *,
        dimensions: Literal['2d'] = '2d',
        layout_name: Literal['spring'] = 'spring', 
        init_pos: PosMap2D = {},
        fixed: Iterable[str] | Literal['auto'] | None = 'auto',
        other_layout_kwargs: Mapping = {}
        ) -> PosDict2D:
    ...
@overload
def calc_positions(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        *,
        dimensions: Literal['3d'],
        layout_name: Literal['spring'] = 'spring', 
        init_pos: PosMap3D = {},
        fixed: Iterable[str] | Literal['auto'] | None = 'auto',
        other_layout_kwargs: Mapping = {}
        ) -> PosDict3D:
    ...
def calc_positions(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        *,
        dimensions: Literal['2d', '3d'] = '2d',
        layout_name: Literal['spring'] = 'spring', 
        init_pos: PosMap2D | PosMap3D | None = {},
        fixed: Iterable[str] | Literal['auto'] | None = 'auto',
        other_layout_kwargs: Mapping = {}
        ) -> PosDict2D | PosDict3D:
    """Calculates the positions of the nodes in the assembly graph."""
    layout_func = LAYOUT_NAME_TO_FUNC[layout_name]

    g = assembly.g_snapshot(component_structures)

    init_pos, fixed = format_init_pos_and_fixed(init_pos, fixed)
    if not init_pos:
        init_pos = None
    if not fixed:
        fixed = None

    if dimensions == '2d':
        return layout_func(
            g, pos=init_pos, fixed=fixed, dim=2, 
            **other_layout_kwargs)
    elif dimensions == '3d':
        return layout_func(
            g, pos=init_pos, fixed=fixed, dim=3, 
            **other_layout_kwargs)
    else:
        raise ValueError(
            f"Invalid value for 'dimensions': {dimensions}. "
            "It must be either '2d' or '3d'.")


@overload
def format_init_pos_and_fixed(
        init_pos: None,
        fixed: Iterable[str] | Literal['auto'] | None,
        ) -> tuple[None, None]: ...
@overload
def format_init_pos_and_fixed(
        init_pos: PosMap2D, fixed: None,
        ) -> tuple[PosDict2D, None]: ...
@overload
def format_init_pos_and_fixed(
        init_pos: PosMap3D, fixed: None,
        ) -> tuple[PosDict3D, None]: ...
@overload
def format_init_pos_and_fixed(
        init_pos: PosMap2D,
        fixed: Iterable[str] | Literal['auto'],
        ) -> tuple[PosDict2D, set[str]]: ...
@overload
def format_init_pos_and_fixed(
        init_pos: PosMap3D,
        fixed: Iterable[str] | Literal['auto'],
        ) -> tuple[PosDict3D, set[str]]: ...
def format_init_pos_and_fixed(init_pos, fixed):
    if init_pos is None:
        return None, None
    
    if fixed is None:
        return dict(init_pos), None
    
    if fixed == 'auto':
        return dict(init_pos), set(init_pos.keys())
    
    if isinstance(fixed, Iterable) and init_pos:
        # Since nodes without initial position cannot be fixed, 
        # exclude them from the fixed set. 
        # (Otherwise, nx.spring_layout will raise an error.)
        fixed = set(fixed) & init_pos.keys()
        return dict(init_pos), fixed
    
    raise ValueError(
        f"Invalid value for 'fixed': {fixed}. "
        "It must be either 'auto' or an iterable of node IDs.")
