from collections.abc import Iterable, Sequence


# TODO: Add validation
# TODO: Use generic types
def cyclic_perm_to_map(
        cyclic_permutation: Sequence[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for i, source in enumerate(cyclic_permutation):
        # (i + 1) % N maps as follows:
        # 0 -> 1, 1 -> 2, ..., N-1 -> 0
        target = cyclic_permutation[(i + 1) % len(cyclic_permutation)]
        mapping[source] = target
    return mapping


def cyclic_perms_to_map(
        cyclic_permutations: Iterable[Sequence[str]]) -> dict[str, str]:
    mapping = {}
    for perm in cyclic_permutations:
        mapping.update(cyclic_perm_to_map(perm))
    return mapping
