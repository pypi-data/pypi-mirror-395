from collections.abc import Mapping
from itertools import count
from typing import Literal, overload

from nasap_net import Assembly, Component

from .single_bindsite import cap_single_bindsite

__all__ = ['cap_bindsites']


@overload
def cap_bindsites(
        assembly: Assembly, 
        component_structures: Mapping[str, Component],
        component_kind_to_be_capped: str,
        cap_component_kind: str, cap_bindsite: str,
        copy: Literal[True] = True
        ) -> Assembly: ...
@overload
def cap_bindsites(
        assembly: Assembly, 
        component_structures: Mapping[str, Component],
        component_kind_to_be_capped: str,
        cap_component_kind: str, cap_bindsite: str,
        copy: Literal[False]
        ) -> None: ...
def cap_bindsites(
        assembly: Assembly, 
        component_structures: Mapping[str, Component],
        component_kind_to_be_capped: str,
        cap_component_kind: str, cap_bindsite: str,
        copy: bool = True
        ) -> Assembly | None:
    """Add leaving ligands to all free bindsites of a specific component kind."""
    if copy:
        assembly = assembly.deepcopy()

    target_bindsites: list[str] = []
    for comp_id, comp_kind in assembly.comp_id_to_kind.items():
        if comp_kind != component_kind_to_be_capped:
            continue
        for bindsite in assembly.get_bindsites_of_component(
                comp_id, component_structures):
            if assembly.is_free_bindsite(bindsite):
                target_bindsites.append(bindsite)

    cap_ids = (f'{cap_component_kind}{i}' for i in count())

    for target_bindsite in target_bindsites:
        cap_id = next(cap_ids)
        while cap_id in assembly.component_ids:
            cap_id = next(cap_ids)
        cap_single_bindsite(
            assembly, target_bindsite, cap_id, 
            cap_component_kind, cap_bindsite, copy=False)
    
    if copy:
        return assembly
    else:
        return None
