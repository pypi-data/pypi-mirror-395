from dataclasses import dataclass, field
from typing import Iterable

from nasap_net.models import Assembly, BindingSite
from .grouping import group_equivalent_binding_site_combs


@dataclass(frozen=True)
class UniqueComb:
    """A unique binding site or binding site set with duplication count."""
    site_comb: tuple[BindingSite, ...]
    duplication: int = field(kw_only=True)


def extract_unique_binding_site_combs(
        binding_site_combs: Iterable[tuple[BindingSite, ...]],
        assembly: Assembly,
        ) -> set[UniqueComb]:
    """Compute unique binding sites or binding site sets."""
    grouped_node_combs = group_equivalent_binding_site_combs(
        binding_site_combs, assembly)

    return {
        UniqueComb(
            site_comb=sorted(comb_group)[0],
            duplication=len(comb_group))
        for comb_group in grouped_node_combs
    }
