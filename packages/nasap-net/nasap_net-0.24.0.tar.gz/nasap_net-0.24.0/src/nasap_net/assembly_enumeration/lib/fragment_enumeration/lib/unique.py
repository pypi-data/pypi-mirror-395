from collections import defaultdict
from collections.abc import Hashable, Iterable, Iterator, Mapping
from typing import Any

from nasap_net.types import ID
from .is_new import is_new
from .key import get_key
from ..models import Fragment


def extract_unique_fragments(
        fragments: Iterable[Fragment],
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None
) -> Iterator[Fragment]:
    unique_fragments: dict[Hashable, set[Fragment]] = defaultdict(set)
    for fragment in fragments:
        if is_new(fragment, unique_fragments, symmetry_operations):
            unique_fragments[get_key(fragment)].add(fragment)
            yield fragment
