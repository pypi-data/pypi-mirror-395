from nasap_net.models import Assembly, MLE
from .separation import separate_if_possible


def perform_intra_reaction(
        assembly: Assembly,
        mle: MLE
) -> tuple[Assembly, Assembly | None]:
    """Perform an intra-molecular reaction within an assembly based on the given MLE.

    The following process is performed:
      1. Remove the bond between the metal and leaving binding sites.
      2. Add a bond between the metal and entering binding sites.

    Parameters
    ----------
    assembly : Assembly
        The assembly in which the intra-molecular reaction is to be performed.
    mle : MLE
        The MLE (metal, leaving, entering binding sites) defining the reaction.

    Returns
    -------
    product : Assembly
        The resulting assembly after the reaction.
    leaving : Assembly | None
        The leaving assembly if it can be separated; otherwise, None.
    """
    raw_product = (
        assembly
            .remove_bond(mle.metal, mle.leaving)
            .add_bond(mle.metal, mle.entering)
    )
    product, leaving = separate_if_possible(
        raw_product,
        metal_comp_id=mle.metal.component_id
    )
    return product, leaving
