from collections import UserDict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from nasap_net.types import ID
from nasap_net.utils import resolve_chain_map


@dataclass
class SymmetryOperations(UserDict):
    data: dict[str, Mapping[Any, ID]] = field(default_factory=dict)

    def add_mapping(self, name: str, mapping: Mapping[Any, ID]) -> None:
        self.data[name] = mapping

    def add_cyclic_permutation(
            self,
            name: str,
            cyclic_permutation: Iterable[Sequence[ID]]
    ) -> None:
        self.add_mapping(name, cyclic_perms_to_map(cyclic_permutation))

    def add_product(
            self,
            name: str,
            mapping_names: Iterable[str]
    ) -> None:
        mappings = [
            self.data[mapping_name]
            for mapping_name in list(mapping_names)
        ]
        self.add_mapping(name, resolve_chain_map(*mappings))


def cyclic_perm_to_map(
        cyclic_permutation: Sequence[ID]) -> dict[ID, ID]:
    mapping: dict[ID, ID] = {}
    for i, source in enumerate(cyclic_permutation):
        # (i + 1) % N maps as follows:
        # 0 -> 1, 1 -> 2, ..., N-1 -> 0
        target = cyclic_permutation[(i + 1) % len(cyclic_permutation)]
        mapping[source] = target
    return mapping


def cyclic_perms_to_map(
        cyclic_permutations: Iterable[Sequence[ID]]) -> dict[ID, ID]:
    mapping = {}
    for perm in cyclic_permutations:
        mapping.update(cyclic_perm_to_map(perm))
    return mapping
