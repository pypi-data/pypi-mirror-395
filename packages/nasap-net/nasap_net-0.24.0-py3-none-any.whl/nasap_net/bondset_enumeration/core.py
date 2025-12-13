from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from .lib import enum_multi_bond_subsets, enum_single_bond_subsets

__all__ = ['enum_bond_subsets']

_T = TypeVar('_T', bound=Hashable)


def enum_bond_subsets(
        bonds: Iterable[_T],
        bond_to_adj_bonds: Mapping[_T, Iterable[_T]], 
        sym_ops: Mapping[str, Mapping[_T, _T]] | None = None
        ) -> set[frozenset[_T]]:
    """Enumerate connected subsets of bonds excluding symmetry-equivalent ones.

    When an assembly is represented as a set of bonds, subsets of 
    the bonds can be considered as fragments of the assembly.
    Considering the M2L3 linear assembly, L-M-L-M-L, with bonds named
    1, 2, 3, and 4 from left to right, for example, the assembly is 
    represented as {1, 2, 3, 4}, and its subsets such as {1}, {1, 2}, 
    and {2, 3} can be considered as fragments of the assembly, i.e.,
    L-M, L-M-L, and M-L-M, respectively.
    
    In this function, such subsets of bonds are enumerated
    under the following conditions:

    - Only connected subsets are enumerated.
    In the previous example, {1, 3} is not considered as a fragment.

    - Symmetry-equivalent fragments are excluded.
    If two fragments are superimposable under at least one symmetry 
    operation provided as `sym_ops`, only one of them is included 
    in the result.
    In the previous example, {1, 2} and {3, 4} are symmetry-equivalent
    under the C2 operation, thus only one of them is included in the
    result.

    Note that the result includes the assembly itself as a fragment,
    i.e., {1, 2, 3, 4} in the previous example.

    In summary, this function enumerates *connected* subsets of bonds
    *excluding symmetry-equivalent ones*.

    Parameters
    ----------
    bonds : Iterable[_T]
        An iterable of bond IDs.
        The resulting bondsets are dependent on the order of the bonds.
    bond_to_adj_bonds : Mapping[_T, Iterable[_T]]
        A dictionary mapping a bond to its adjacent bonds.
        Each key is the ID of a bond, and its value is an iterable
        of IDs of adjacent bonds.
        This dictionary is used for connectivity check.
    sym_ops : Mapping[str, Mapping[_T, _T]] | None, optional
        A dictionary of symmetry operations.
        Each key is the name of a symmetry operation, and its value is
        a mapping of bond IDs to their images under the symmetry operation.
        This dictionary is used for symmetry-equivalence check.
        If not provided, no symmetry-equivalence check is performed, 
        in other words, all the fragments are included in the result
        regardless of their symmetry equivalence.
        Identity operation 'E' is not necessary to be included.

    Returns
    -------
    set[frozenset[_T]]
        A set of connected subsets of bonds excluding symmetry-equivalent
        ones. Each subset is represented as a frozenset of bond IDs.

    Notes
    -----
    Equivalent fragments which are not superimposable under symmetry
    operations are not removed during the enumeration. In the previous
    example, {1, 2} (M-L) and {2, 3} (L-M) are equivalent but not
    superimposable under any symmetry operation of the complete
    assembly, thus both of them are included in the result.

    Examples
    --------
    M2L3 linear assembly (L-M-L-M-L) with bonds 1, 2, 3, and 4
    *without* symmetry operations.
    >>> import nasap_net
    >>> BONDS = [1, 2, 3, 4]
    >>> BOND_TO_ADJ_BONDS = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]}
    >>> nasap_net.enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS)
    {
        frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}),
        frozenset({1, 2}), frozenset({2, 3}), frozenset({3, 4}),
        frozenset({1, 2, 3}), frozenset({2, 3, 4}),
        frozenset({1, 2, 3, 4})
    }

    Same assembly with symmetry operations.
    >>> SYM_OPS = {'C2': {1: 4, 2: 3, 3: 2, 4: 1}}
    >>> nasap_net.enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS, SYM_OPS)
    {
        frozenset({1}), frozenset({2}), 
        frozenset({1, 2}), frozenset({2, 3}),
        frozenset({1, 2, 3}), 
        frozenset({1, 2, 3, 4})
    }

    Triangle with three bonds, 1, 2, and 3.
    >>> BONDS = [1, 2, 3]
    >>> BOND_TO_ADJ_BONDS = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    >>> SYM_OPS = {
    ...     'C3': {1: 2, 2: 3, 3: 1}, 
    ...     'C3^2': {1: 3, 2: 1, 3: 2},
    ...     'sigma1': {1: 1, 2: 3, 3: 2},
    ...     'sigma2': {1: 2, 2: 1, 3: 3},
    ...     'sigma3': {1: 3, 2: 2, 3: 1}
    ... }
    >>> nasap_net.enum_bond_subsets(BONDS, BOND_TO_ADJ_BONDS, SYM_OPS)
    {frozenset({1}), frozenset({1, 2}), frozenset({1, 2, 3})}
    """
    found: set[frozenset[_T]] = set()

    single_bond_subsets = enum_single_bond_subsets(bonds, sym_ops)
    found.update(single_bond_subsets)

    prev_assems = single_bond_subsets
    while prev_assems:
        # Subsets are explored by adding one bond to one of the
        # previously found subsets.
        cur_found = enum_multi_bond_subsets(
            prev_assems, bond_to_adj_bonds, sym_ops)
        prev_assems = cur_found
        found.update(cur_found)

    return found
