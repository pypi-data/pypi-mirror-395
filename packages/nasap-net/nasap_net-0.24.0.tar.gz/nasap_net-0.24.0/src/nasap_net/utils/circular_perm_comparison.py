from typing import TypeVar

T = TypeVar('T')


def are_same_circular_perm(
        perm1: list[T], perm2: list[T],
        consider_reverse: bool = False) -> bool:
    """Check if two circular permutations are the same.

    Two circular permutations are the same if they are the same
    when rotated. If consider_reverse is True, the function will
    also check if the second permutation is the reverse of some
    rotation of the first permutation.

    For example, the circular permutations [1, 2, 3, 4] and [3, 2, 1, 4]
    are considered the same if consider_reverse is True, but not
    if consider_reverse is False.

    Parameters
    ----------
    perm1 : list[T]
        The first circular permutation.
    perm2 : list[T]
        The second circular permutation.
    consider_reverse : bool, optional
        Whether to consider the reverse of the second permutation,
        by default False.
    
    Returns
    -------
    bool
        True if the two circular permutations are the same.
    """
    if len(perm1) != len(perm2):
        return False

    for i in range(len(perm1)):
        rotated_perm2 = perm2[i:] + perm2[:i]
        if perm1 == rotated_perm2:
            return True
        if consider_reverse and perm1 == rotated_perm2[::-1]:
            return True

    return False
