from collections.abc import Mapping

from nasap_net import Assembly, Component, InterOrIntra, InterReaction, \
    IntraReaction
from ..bindsite_equivalence import are_equivalent_binding_site_lists


def are_equivalent_reactions(
        reaction1: IntraReaction | InterReaction,
        reaction2: IntraReaction | InterReaction,
        id_to_assembly: Mapping[int, Assembly],
        component_structures: Mapping[str, Component],
        ) -> bool:
    """
    Check if two reactions are equivalent.

    Two reactions are equivalent if they meet the following conditions:
        1-1. They have the same number of reactants.
        1-2. They have the same number of products.
        2-1. They have the same initial assembly.
        2-2. They have the same entering assembly, or both are None.
        2-3. They have the same product assembly.
        2-4. They have the same leaving assembly, or both are None.
        3-1. If the reaction is intra-molecular, the trio of binding sites
            [metal, leaving, entering] must be equivalent.
        3-2. If the reaction is inter-molecular, the pair of binding sites
            [metal, leaving] of the initial assembly must be equivalent,
            and the entering binding site of the entering assembly must be
            equivalent to the entering binding site of the other reaction.
    
    Here, two binding site lists (e.g. [metal1, leaving1] and 
    [metal2, leaving2]) are equivalent if there is at least one isomorphism
    which maps each binding site in the first list to a binding site in 
    the second list. The order of the binding sites in the list DOES matter.
    
    Parameters
    ----------
    reaction1 : IntraReaction | InterReaction
        The first reaction to compare.
    reaction2 : IntraReaction | InterReaction
        The second reaction to compare.
    id_to_assembly : Mapping[int, Assembly]
        A mapping from assembly IDs to assemblies. This must not include
        duplicate assemblies since this function only uses the IDs to
        compare the assemblies, not the assembly structures.
    component_structures : Mapping[str, Component]
        A mapping from component IDs to components.

    Returns
    -------
    bool
        True if the reactions are equivalent, False otherwise.
    
    Warnings
    --------
    This function treats assemblies with different IDs as distinct, 
    even if they are structurally identical. Please ensure that the 
    assemblies in `id_to_assembly` are not duplicates.
    """
    # Condition 1: Same number of reactants and products
    if len(reaction1.reactants) != len(reaction2.reactants):
        return False
    if len(reaction1.products) != len(reaction2.products):
        return False
    
    # Condition 2: Same assemblies
    if reaction1.init_assem_id != reaction2.init_assem_id:
        return False
    if reaction1.entering_assem_id is not None:
        if reaction1.entering_assem_id != reaction2.entering_assem_id:
            return False
    if reaction1.product_assem_id != reaction2.product_assem_id:
        return False
    if reaction1.leaving_assem_id is not None:
        if reaction1.leaving_assem_id != reaction2.leaving_assem_id:
            return False

    # Condition 3: Equivalent pair/trio of binding sites
    if reaction1.inter_or_intra == InterOrIntra.INTRA:
        if not are_equivalent_binding_site_lists(
                id_to_assembly[reaction1.init_assem_id],
                (reaction1.metal_bs, reaction1.leaving_bs,
                 reaction1.entering_bs),
                (reaction2.metal_bs, reaction2.leaving_bs,
                 reaction2.entering_bs),
                component_structures
                ):
            return False
    elif reaction1.inter_or_intra == InterOrIntra.INTER:
        assert reaction1.entering_assem_id is not None
        # Check for initial assembly
        if not are_equivalent_binding_site_lists(
                id_to_assembly[reaction1.init_assem_id],
                (reaction1.metal_bs, reaction1.leaving_bs),
                (reaction2.metal_bs, reaction2.leaving_bs),
                component_structures
                ):
            return False
        # Check for entering assembly
        if not are_equivalent_binding_site_lists(
                id_to_assembly[reaction1.entering_assem_id],
                (reaction1.entering_bs,), (reaction2.entering_bs,),
                component_structures
                ):
            return False
    
    assert reaction1.duplicate_count == reaction2.duplicate_count
    return True
