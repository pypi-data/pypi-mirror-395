from nasap_net.binding_site_equivalence import binding_site_combs_equivalent
from nasap_net.models import Reaction


def inter_reaction_mles_equivalent(
        reaction1: Reaction,
        reaction2: Reaction,
    ) -> bool:
    """Check if the MLEs of two inter-molecular reactions are equivalent.

    Returns True if both of the following conditions are met:
        1. The two reactions have equivalent initial (metal, leaving) binding
            site pairs in their initial assemblies.
        2. The two reactions have equivalent entering binding sites in their
            entering assemblies.

    Parameters
    ----------
    reaction1 : Reaction
        The first inter-molecular reaction to compare.
    reaction2 : Reaction
        The second inter-molecular reaction to compare.

    Returns
    -------
    bool
        True if the MLEs are equivalent, False otherwise.
    """
    # Check for initial assembly
    if not binding_site_combs_equivalent(
            assembly1=reaction1.init_assem,
            site_comb1=(reaction1.metal_bs, reaction1.leaving_bs),
            assembly2=reaction2.init_assem,
            site_comb2=(reaction2.metal_bs, reaction2.leaving_bs),
    ):
        return False
    # Check for entering assembly
    if not binding_site_combs_equivalent(
            assembly1=reaction1.entering_assem_strict,
            site_comb1=(reaction1.entering_bs,),
            assembly2=reaction2.entering_assem_strict,
            site_comb2=(reaction2.entering_bs,),
    ):
        return False
    return True


def intra_reaction_mles_equivalent(reaction1, reaction2):
    """Check if the MLEs of two intra-molecular reactions are equivalent.

    Returns True if the two reactions have equivalent (metal, leaving, entering)
    binding site trios in their initial assemblies.

    "Equivalent" here means that there exists at least one isomorphism
    which maps each binding site in the first trio to a binding site in the
    second trio. The order of the binding sites in the trio DOES matter.

    Parameters
    ----------
    reaction1 : Reaction
        The first intra-molecular reaction to compare.
    reaction2 : Reaction
        The second intra-molecular reaction to compare.

    Returns
    -------
    bool
        True if the MLEs are equivalent, False otherwise.
    """
    return binding_site_combs_equivalent(
        assembly1=reaction1.init_assem,
        site_comb1=(
            reaction1.metal_bs,
            reaction1.leaving_bs,
            reaction1.entering_bs
        ),
        assembly2=reaction2.init_assem,
        site_comb2=(
            reaction2.metal_bs,
            reaction2.leaving_bs,
            reaction2.entering_bs
        ),
    )
