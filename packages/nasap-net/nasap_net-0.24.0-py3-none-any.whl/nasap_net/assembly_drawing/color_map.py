from collections.abc import Mapping
from itertools import cycle

from nasap_net import Assembly

__all__ = ['make_complete_color_map']


def make_complete_color_map(
        assembly: Assembly, color_map: Mapping[str, str]
        ) -> dict[str, str]:
    color_undefined_component_kinds = (
        assembly.component_kinds - set(color_map.keys()))
    if not color_undefined_component_kinds:
        return dict(color_map)

    # infinity iterator
    DEFAULT_COLORS = cycle([
        '#FE7F6E', '#C89F38', '#4CBB51', '#53AFDC', '#9A9EEC',
        '#9AA6B5', '#A5A5A5'])

    # Convert to dict to allow modification
    complete_map = dict(color_map)

    # Use sorted to make the order of colors deterministic
    for comp_kind in sorted(color_undefined_component_kinds):
        complete_map[comp_kind] = next(DEFAULT_COLORS)

    return complete_map