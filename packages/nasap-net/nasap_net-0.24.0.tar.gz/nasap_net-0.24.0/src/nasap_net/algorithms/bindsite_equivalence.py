from collections.abc import Mapping, Sequence
from itertools import chain

from nasap_net import Assembly, Component
from nasap_net.algorithms.isomorphism import isomorphisms_iter


def are_equivalent_binding_site_lists(
        assembly: Assembly,
        binding_site_list1: Sequence[str],
        binding_site_list2: Sequence[str],
        component_structures: Mapping[str, Component],
        ) -> bool:
    """
    Check if the pair of binding site lists are equivalent.

    "Equivalent" means that there is at least one isomorphism 
    which maps each binding site in the first list to a binding site
    in the second list.
    The order of the binding sites in the list DOES matter.

    Parameters
    ----------
    assembly : Assembly
        The assembly to which the binding sites belong.
    binding_site_list1 : Sequence[str]
        The first list of binding sites.
    binding_site_list2 : Sequence[str]
        The second list of binding sites.
    component_structures : Mapping[str, Component]
        The component structures of the assembly.

    Returns
    -------
    bool
        True if the binding site lists are equivalent, False otherwise.
    """
    # Input validation
    if len(binding_site_list1) != len(binding_site_list2):
        raise ValueError(
            "The length of the binding site lists must be the same.")
    if not binding_site_list1:
        raise ValueError("The binding site lists must not be empty.")
    
    # Check if the binding sites are in the assembly
    for bs in chain(binding_site_list1, binding_site_list2):
        if bs not in assembly.get_all_bindsites(component_structures):
            raise ValueError(f"Binding site {bs} not found in assembly.")

    # ---
    # Main logic
    for isom in isomorphisms_iter(
            assembly, assembly, component_structures):
        for (bs1, bs2) in zip(binding_site_list1, binding_site_list2):
            if isom[bs1] != bs2:
                break
        else:
            return True
    return False
