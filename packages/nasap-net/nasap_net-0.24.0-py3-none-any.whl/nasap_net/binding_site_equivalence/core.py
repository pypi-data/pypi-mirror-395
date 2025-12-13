from typing import Sequence

from nasap_net.isomorphism import get_all_isomorphisms
from nasap_net.models import Assembly, BindingSite


def binding_site_combs_equivalent(
        assembly1: Assembly,
        site_comb1: Sequence[BindingSite],
        assembly2: Assembly,
        site_comb2: Sequence[BindingSite],
        ) -> bool:
    """Check if two binding site combinations are equivalent.

    Two binding site combinations are considered equivalent if there exists at
    least one isomorphism between the two assemblies that maps each binding site
    in the first combination to the corresponding binding site in the second
    combination. The order of the binding sites in the combinations DOES matter.

    Parameters
    ----------
    assembly1 : Assembly
        The first assembly.
    site_comb1 : Sequence[BindingSite]
        The binding site combination in the first assembly.
    assembly2 : Assembly
        The second assembly.
    site_comb2 : Sequence[BindingSite]
        The binding site combination in the second assembly.

    Returns
    -------
    bool
        True if the binding site combinations are equivalent, False otherwise.
    """
    site_comb1 = tuple(site_comb1)
    site_comb2 = tuple(site_comb2)

    if len(site_comb1) != len(site_comb2):
        return False

    isomorphisms = get_all_isomorphisms(assembly1, assembly2)

    for isom in isomorphisms:
        binding_site_mapping = isom.binding_site_mapping
        mapped_comb = tuple(binding_site_mapping[site] for site in site_comb1)
        if mapped_comb == site_comb2:
            return True
    return False
