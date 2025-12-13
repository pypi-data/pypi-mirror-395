import itertools
from collections import defaultdict
from collections.abc import Iterator, Mapping
from functools import wraps

from nasap_net import (Assembly, Component, InterReaction, IntraReaction,
                       calc_graph_hash_of_assembly)
from nasap_net.algorithms.hashing import calc_graph_hash_of_assembly

from .inter import explore_inter_reactions
from .intra import explore_intra_reactions


def _verbose(func):
    """Decorator to add verbose logging to a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        verbose = kwargs.get('verbose', False)
        reaction_iterator = func(*args, **kwargs)
        for i, reaction in enumerate(reaction_iterator):
            if verbose:
                print(f'Reaction Found ({i}): {_reaction_to_str(reaction)}')
            yield reaction
    return wrapper


@_verbose
def explore_reactions(
        id_to_assembly: Mapping[int, Assembly],
        metal_kind: str, leaving_kind: str, entering_kind: str,
        component_structures: Mapping[str, Component],
        verbose: bool = False,  # Used in the decorator
        ) -> Iterator[IntraReaction | InterReaction]:
    hash_to_ids = defaultdict(list)
    for assem_id, assembly in id_to_assembly.items():
        hash_ = calc_graph_hash_of_assembly(assembly, component_structures)
        hash_to_ids[hash_].append(assem_id)
    
    # Intra-molecular ligand exchange
    for assem_id in id_to_assembly.keys():
        yield from explore_intra_reactions(
            assem_id, metal_kind, leaving_kind, entering_kind,
            id_to_assembly, hash_to_ids, component_structures)
    
    # Inter-molecular ligand exchange
    for init_assem_id, entering_assem_id in itertools.product(
            id_to_assembly.keys(), repeat=2):
        yield from explore_inter_reactions(
            init_assem_id, entering_assem_id, 
            metal_kind, leaving_kind, entering_kind,
            id_to_assembly, hash_to_ids, component_structures)


def _reaction_to_str(
        reaction: IntraReaction | InterReaction,
        ) -> str:
    init = reaction.init_assem_id
    entering = reaction.entering_assem_id
    product = reaction.product_assem_id
    leaving = reaction.leaving_assem_id
    
    left = f'{init}' if entering is None else f'{init} + {entering}'
    right = f'{product}' if leaving is None else f'{product} + {leaving}'
    equation = f'{left} -> {right}'

    metal_bs = reaction.metal_bs
    leaving_bs = reaction.leaving_bs
    entering_bs = reaction.entering_bs

    binding_sites = (
        f'metal={metal_bs}, leaving={leaving_bs}, entering={entering_bs}')
    
    dup = reaction.duplicate_count

    return f'{equation} ({binding_sites}) (x{dup})'
