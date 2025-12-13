from collections.abc import Hashable
from functools import lru_cache

from ..models import Fragment


@lru_cache
def get_key(fragment: Fragment) -> Hashable:
    return len(fragment.components), len(fragment.bonds)
