from typing import Literal, overload

from nasap_net import Assembly, BindsiteIdConverter

__all__ = ['cap_single_bindsite']


@overload
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str,
        copy: Literal[True] = True
        ) -> Assembly: ...
@overload
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str,
        copy: Literal[False]
        ) -> None: ...
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str, 
        copy: bool = True
        ) -> Assembly | None:
    """Add a leaving ligand (cap) to the assembly."""
    id_converter = BindsiteIdConverter()
    if copy:
        assembly = assembly.deepcopy()

    assembly.add_component(cap_id, cap_component_kind)
    assembly.add_bond(id_converter.local_to_global(cap_id, cap_bindsite), target_bindsite)

    return assembly
