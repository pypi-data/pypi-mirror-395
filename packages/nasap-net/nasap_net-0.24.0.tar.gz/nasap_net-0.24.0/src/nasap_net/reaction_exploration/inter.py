import itertools
from collections.abc import Iterable, Iterator, Mapping

from nasap_net import (Assembly, Component, find_isomorphic_assembly,
                       perform_inter_exchange)
from nasap_net.classes.reaction import InterReaction

from .lib import (compute_unique_bindsites_or_bindsite_sets,
                  enum_valid_entering_bindsites, enum_valid_ml_pairs)

__all__ = ['explore_inter_reactions']


def explore_inter_reactions(
        init_assem_id: int, entering_assem_id: int,
        metal_kind: str, leaving_kind: str, entering_kind: str,
        id_to_assembly: Mapping[int, Assembly],
        hash_to_ids: Mapping[str, Iterable[int]],
        component_structures: Mapping[str, Component],
        ) -> Iterator[InterReaction]:
    init_assem = id_to_assembly[init_assem_id]
    entering_assem = id_to_assembly[entering_assem_id]

    valid_ml_pairs = enum_valid_ml_pairs(
        init_assem_id, init_assem,
        metal_kind, leaving_kind,
        component_structures)
    valid_entering_bindsites = enum_valid_entering_bindsites(
        entering_assem_id, entering_assem,
        entering_kind, component_structures)

    unique_ml_pairs_and_dup_cnts = compute_unique_bindsites_or_bindsite_sets(
        init_assem_id, init_assem, valid_ml_pairs, component_structures)
    unique_entering_bindsites_and_dup_cnts = compute_unique_bindsites_or_bindsite_sets(
        entering_assem_id, entering_assem, valid_entering_bindsites,
        component_structures)

    for ml_pair_and_dup_cnt, entering_bs_and_dup_cnt in itertools.product(
            unique_ml_pairs_and_dup_cnts, unique_entering_bindsites_and_dup_cnts):
        (metal_bs, leaving_bs), ml_pair_dup_cnt = ml_pair_and_dup_cnt
        entering_bs, entering_bs_dup_cnt = entering_bs_and_dup_cnt

        duplicate_count = ml_pair_dup_cnt * entering_bs_dup_cnt
        if init_assem_id == entering_assem_id:
            duplicate_count *= 2

        product, leaving = perform_inter_exchange(
            init_assem, entering_assem, metal_bs, leaving_bs, entering_bs)

        product_id = find_isomorphic_assembly(
            product, id_to_assembly, hash_to_ids, component_structures)

        if product_id is None:
            continue

        if leaving is None:
            yield InterReaction(
                init_assem_id, entering_assem_id, product_id,
                None, metal_bs, leaving_bs, entering_bs,
                duplicate_count)
            continue

        leaving_id = find_isomorphic_assembly(
            leaving, id_to_assembly, hash_to_ids,
            component_structures)
        if leaving_id is None:
            continue

        yield InterReaction(
            init_assem_id, entering_assem_id, product_id, leaving_id,
            metal_bs, leaving_bs, entering_bs,
            duplicate_count)
