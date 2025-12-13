from collections.abc import Iterable, Mapping
from typing import Any

from nasap_net.types import ID
from .sub_fragment import create_sub_fragment
from .unique import extract_unique_fragments
from ..models import Fragment


def get_unique_starting_fragments(
        template: Fragment,
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None
) -> set[Fragment]:
    raw_starting_frags = _get_raw_starting_fragments(template)
    return set(
        extract_unique_fragments(
            sorted(raw_starting_frags), symmetry_operations
        )
    )


def _get_raw_starting_fragments(template: Fragment) -> set[Fragment]:
    return {
        create_sub_fragment(template, [comp_id])
        for comp_id in sorted(template.components)
    }
