from collections.abc import Iterable, Iterator, Mapping

from nasap_net import (Assembly, Component, find_isomorphic_assembly,
                       perform_intra_exchange)
from nasap_net.classes.reaction import IntraReaction

from .lib import (compute_unique_bindsites_or_bindsite_sets,
                  enum_valid_mles_for_intra)


def explore_intra_reactions(
        init_assem_id: int,
        metal_kind: str, leaving_kind: str, entering_kind: str,
        id_to_assembly: Mapping[int, Assembly],
        hash_to_ids: Mapping[str, Iterable[int]],
        component_structures: Mapping[str, Component],
        ) -> Iterator[IntraReaction]:
    init_assem = id_to_assembly[init_assem_id]

    valid_mle_trios = enum_valid_mles_for_intra(
        init_assem_id, init_assem,
        metal_kind, leaving_kind, entering_kind,
        component_structures)

    for mle_bindsites, duplicate_count in compute_unique_bindsites_or_bindsite_sets(
            init_assem_id, init_assem, valid_mle_trios,
            component_structures):
        metal_bs, leaving_bs, entering_bs = mle_bindsites

        product, leaving = perform_intra_exchange(
            init_assem, metal_bs, leaving_bs, entering_bs)

        product_id = find_isomorphic_assembly(
            product, id_to_assembly, hash_to_ids,
            component_structures)
        if product_id is None:
            continue

        if leaving is None:
            yield IntraReaction(
                init_assem_id, product_id, None,
                metal_bs, leaving_bs, entering_bs, 
                duplicate_count)
            continue

        leaving_id = find_isomorphic_assembly(
            leaving, id_to_assembly, hash_to_ids,
            component_structures)
        if leaving_id is None:
            continue

        yield IntraReaction(
            init_assem_id, product_id, leaving_id,
            metal_bs, leaving_bs, entering_bs, 
            duplicate_count)
