from collections.abc import Iterable, Mapping
from functools import cached_property

from nasap_net.bondset_enumeration import normalize_bondset_under_sym_ops

from .bondsets_validation import validate_bondsets


class BondsetsComparer:
    """Compare bondsets under symmetry operations."""
    def __init__(
            self,
            first_bondsets: Iterable[Iterable[int]],
            second_bondsets: Iterable[Iterable[int]],
            sym_ops: Mapping[str, Mapping[int, int]] | None = None,
            ) -> None:
        first_bondsets = list(first_bondsets)
        second_bondsets = list(second_bondsets)
        validate_bondsets(first_bondsets)
        validate_bondsets(second_bondsets)
        self._first_bondsets = {
            frozenset(bondset) for bondset in first_bondsets}
        self._second_bondsets = {
            frozenset(bondset) for bondset in second_bondsets}
        self.sym_ops = sym_ops

    @property
    def first_bondsets(self) -> set[frozenset[int]]:
        return self._first_bondsets
    
    @property
    def second_bondsets(self) -> set[frozenset[int]]:
        return self._second_bondsets

    @cached_property
    def are_equal(self) -> bool:
        return not self.only_in_first and not self.only_in_second
    
    @cached_property
    def only_in_first(self) -> set[frozenset[int]]:
        return self.first_bondsets - self.first_to_second.keys()
    
    @cached_property
    def only_in_second(self) -> set[frozenset[int]]:
        return self.second_bondsets - self.second_to_first.keys()
    
    @cached_property
    def first_to_second(self) -> dict[frozenset[int], frozenset[int]]:
        return {
            first: self.normalized_to_second[normalized]
            for first, normalized in self.first_to_normalized.items()
            if normalized in self.normalized_to_second.keys()
            }
    
    @cached_property
    def second_to_first(self) -> dict[frozenset[int], frozenset[int]]:
        return {
            second: self.normalized_to_first[normalized]
            for second, normalized in self.second_to_normalized.items()
            if normalized in self.normalized_to_first.keys()
            }
    
    @cached_property
    def first_to_normalized(self) -> dict[frozenset[int], frozenset[int]]:
        return _bondsets_to_normalized(self.first_bondsets, self.sym_ops)
    
    @cached_property
    def second_to_normalized(self) -> dict[frozenset[int], frozenset[int]]:
        return _bondsets_to_normalized(self.second_bondsets, self.sym_ops)
    
    @cached_property
    def normalized_to_first(self) -> dict[frozenset[int], frozenset[int]]:
        # Assert that there are no duplicate normalized bondsets,
        # i.e., there are no duplicate values in self.first_to_normalized.
        unique_normalized = set(self.first_to_normalized.values())
        assert len(unique_normalized) == len(self.first_to_normalized)
        return {v: k for k, v in self.first_to_normalized.items()}
    
    @cached_property
    def normalized_to_second(self) -> dict[frozenset[int], frozenset[int]]:
        # Assert that there are no duplicate normalized bondsets.
        unique_normalized = set(self.second_to_normalized.values())
        assert len(unique_normalized) == len(self.second_to_normalized)
        return {v: k for k, v in self.second_to_normalized.items()}


def _bondsets_to_normalized(
        bondsets: Iterable[Iterable[int]],
        sym_ops: Mapping[str, Mapping[int, int]] | None = None
        ) -> dict[frozenset[int], frozenset[int]]:
    return {
        frozenset(bondset): frozenset(normalize_bondset_under_sym_ops(
            bondset, sym_ops))
        for bondset in bondsets}
