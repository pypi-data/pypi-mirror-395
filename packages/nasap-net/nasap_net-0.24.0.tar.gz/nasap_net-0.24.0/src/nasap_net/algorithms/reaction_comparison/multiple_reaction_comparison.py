from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import TypeAlias, cast

from nasap_net import Assembly, Component, InterReaction, IntraReaction

from .reaction_comparison import are_equivalent_reactions

Reaction: TypeAlias = IntraReaction | InterReaction


def are_equivalent_reaction_sets(
        reaction_set1: Iterable[Reaction],
        reaction_set2: Iterable[Reaction],
        id_to_assembly: Mapping[int, Assembly],
        component_structures: Mapping[str, Component],
        ) -> bool:
    """Check if the two sets of reactions are equivalent.
    """
    reactions1 = list(reaction_set1)  # e.g. [r1-0, r1-1, r1-2]
    reactions2 = list(reaction_set2)  # e.g. [r2-1, r2-2, r2-0]

    if len(reactions1) != len(reactions2):
        return False

    grouped1 = _group_reactions(reactions1)  
    # e.g. {key1: [r1-0, r1-1], key2: [r1-2]}

    grouped2 = _group_reactions(reactions2)
    # e.g. {key1: [r2-1, r2-0], key2: [r2-2]}

    if grouped1.keys() != grouped2.keys():
        return False
    # Reasoning: If either of the sets has an extra key, then its
    # reactions have no counterpart in the other set.
    
    for key in grouped1.keys():
        cur_key_reactions1 = grouped1[key]  # e.g. [r1-0, r1-1]
        cur_key_reactions2 = grouped2[key]  # e.g. [r2-1, r2-0]

        if len(cur_key_reactions1) != len(cur_key_reactions2):
            return False
        
        reaction_count = len(cur_key_reactions1)

        if reaction_count == 1:
            # If there is only one reaction in the set, we can compare
            # them directly.
            if not are_equivalent_reactions(
                    cur_key_reactions1[0], cur_key_reactions2[0],
                    id_to_assembly, component_structures):
                return False
            continue

        # If there are multiple reactions in the set, we need to check
        # if there are one-to-one matches between them.

        # Cached function
        # This prevents recomputing the equivalence for the same pair.
        cached_eq = _make_cached_eq(
            cur_key_reactions1, cur_key_reactions2,
            id_to_assembly, component_structures)

        used2 = [False] * reaction_count  # e.g. [False, False]
        for i1 in range(reaction_count):  # e.g. (0 -> 1)
            for i2 in range(reaction_count):  # e.g. (0 -> 1)
                if not used2[i2] and cached_eq(i1, i2):
                    # i.e. If equivalent reactions are found...
                    used2[i2] = True  # Mark the reaction as used
                    break  # i.e. Move to the next reaction in set 1
            else:
                # If we didn't find a match for reaction i1, then the sets
                # are not equivalent.
                return False
        # If we reach here, it means all reactions in set 1 have a match
        # in set 2.
    return True


def _make_cached_eq(
        reactions1: Sequence[Reaction], reactions2: Sequence[Reaction],
        id_to_assembly: Mapping[int, Assembly],
        component_structures: Mapping[str, Component]
        ) -> Callable[[int, int], bool]:
    cache: dict[tuple[int, int], bool] = {}

    def cached_eq(index1: int, index2: int) -> bool:
        raw_key = tuple(sorted((index1, index2)))
        key = cast(tuple[int, int], raw_key)  # Only for type checking
        if key in cache:
            return cache[key]
        result = are_equivalent_reactions(
            reactions1[index1], reactions2[index2], 
            id_to_assembly, component_structures)
        cache[key] = result
        return result
    
    return cached_eq


def _group_reactions(reactions: Iterable[Reaction]) -> Mapping[tuple, list]:
    """Group reactions by their initial, entering, product, 
    and leaving assemblies.
    """
    grouped = defaultdict(list)

    grouping_key = lambda r: (
        r.init_assem_id, r.entering_assem_id,
        r.product_assem_id, r.leaving_assem_id)
    
    for reaction in reactions:
        grouped[grouping_key(reaction)].append(reaction)
    return grouped
