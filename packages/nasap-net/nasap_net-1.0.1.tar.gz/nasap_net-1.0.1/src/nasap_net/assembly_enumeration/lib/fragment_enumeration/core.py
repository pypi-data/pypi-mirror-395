from collections import defaultdict, deque
from collections.abc import Hashable, Iterable, Mapping
from typing import Any

from nasap_net.models import Assembly
from nasap_net.types import ID
from .lib import enumerate_one_step_grown_fragments, get_key, \
    get_unique_starting_fragments, is_new, validate_symmetry_operation
from .models import Fragment
from .models.fragment import create_complete_fragment


def enumerate_fragments(
        template: Assembly,
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None
) -> set[Assembly]:
    template_fragment = create_complete_fragment(template)
    if symmetry_operations is not None:
        for sym_op in symmetry_operations:
            validate_symmetry_operation(template_fragment, sym_op)

    found: defaultdict[Hashable, set[Fragment]] = defaultdict(set)

    starting_fragments = set(get_unique_starting_fragments(
        template_fragment, symmetry_operations)
    )
    for frag in starting_fragments:
        found[get_key(frag)].add(frag)
    queue = deque(sorted(starting_fragments))

    while queue:
        cur_frag = queue.popleft()
        one_step_grown_frags = enumerate_one_step_grown_fragments(cur_frag)
        for frag in one_step_grown_frags:
            if is_new(frag, found, symmetry_operations):
                found[get_key(frag)].add(frag)
                queue.append(frag)

    result: set[Assembly] = set()
    for frags in found.values():
        result.update(frag.to_assembly() for frag in frags)
    return result
