from nasap_net.models import Reaction
from nasap_net.reaction_performance import perform_inter_reaction, \
    perform_intra_reaction, reindex_components_for_inter_reaction


def generate_sample_rev_reaction(reaction: Reaction) -> Reaction:
    """Generate a sample reverse reaction for a given reaction.

    Parameters
    ----------
    reaction : Reaction
        The reaction to generate a sample reverse reaction for.

    Returns
    -------
    Reaction
        A sample reverse reaction.

    Raises
    ------
    IncorrectReactionResultError
        If the reproduced reaction result is inconsistent with the given
        result.
    """
    if reaction.is_inter():
        renamed = reindex_components_for_inter_reaction(
            init_assembly=reaction.init_assem,
            entering_assembly=reaction.entering_assem_strict,
            mle=reaction.mle,
            init_prefix='init_',
            entering_prefix='entering_',
        )
        product, leaving = perform_inter_reaction(
            init_assem=renamed.init_assembly,
            entering_assem=renamed.entering_assembly,
            mle=renamed.mle,
        )
        return Reaction(
            init_assem=product,
            entering_assem=leaving,
            product_assem=reaction.init_assem,
            leaving_assem=reaction.entering_assem,
            metal_bs=renamed.mle.metal,
            leaving_bs=renamed.mle.entering,
            entering_bs=renamed.mle.leaving,
        )
    else:
        assert reaction.is_intra()
        product, leaving = perform_intra_reaction(
            assembly=reaction.init_assem,
            mle=reaction.mle,
        )
        return Reaction(
            init_assem=product,
            entering_assem=leaving,
            product_assem=reaction.init_assem,
            leaving_assem=None,
            metal_bs=reaction.mle.metal,
            leaving_bs=reaction.mle.entering,
            entering_bs=reaction.mle.leaving,
        )
