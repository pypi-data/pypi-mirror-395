from nasap_net.assembly_equivalence import assemblies_equivalent
from nasap_net.models import Reaction
from .mle_equivalence import \
    inter_reaction_mles_equivalent, \
    intra_reaction_mles_equivalent


class DuplicateCountMismatchError(Exception):
    """Raised when two equivalent reactions have different duplicate counts."""
    pass


def reactions_equivalent(
        reaction1: Reaction,
        reaction2: Reaction,
        ) -> bool:
    """
    Check if two reactions are equivalent.

    Two reactions are equivalent if they meet the following conditions:
        1-1. They have the same number of reactants.
        2-1. They have the same initial assembly.
        2-2. They have the same entering assembly, or both are None.
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

    Returns
    -------
    bool
        True if the reactions are equivalent, False otherwise.

    Notes
    -----
    Reaction equivalence can be determined only by the left-hand side
    information (i.e., initial assembly, entering assembly, and MLE),
    so the right-hand side information (i.e., product assembly, leaving assembly)
    is not considered in this function.
    """
    if reaction1 == reaction2:
        return True

    # Condition 1: Same number of reactants
    if reaction1.is_inter() != reaction2.is_inter():
        return False

    # Condition 2: Same assemblies (only left-hand side)
    if not assemblies_equivalent(reaction1.init_assem, reaction2.init_assem):
        return False
    if reaction1.is_inter():
        assert reaction2.is_inter()
        if not assemblies_equivalent(
                reaction1.entering_assem_strict,
                reaction2.entering_assem_strict
        ):
            return False

    # Condition 3: Equivalent pair/trio of binding sites
    if reaction1.is_intra():
        if not intra_reaction_mles_equivalent(reaction1, reaction2):
            return False
    else:
        assert reaction1.is_inter()
        if not inter_reaction_mles_equivalent(reaction1, reaction2):
            return False
    return True
