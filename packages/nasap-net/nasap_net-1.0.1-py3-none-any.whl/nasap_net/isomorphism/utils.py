from typing import Sequence


def reverse_mapping_seq(
        mapping: Sequence[int]) -> list[int]:
    """Return the reverse of a mapping given as a sequence.

    For example, mapping [2, 0, 1] means {0: 2, 1: 0, 2: 1},
    and the reverse mapping is {2: 0, 0: 1, 1: 2}, i.e., [1, 2, 0].
    """
    rev_mapping = [0] * len(mapping)
    for i, mapped_i in enumerate(mapping):
        rev_mapping[mapped_i] = i
    return rev_mapping
