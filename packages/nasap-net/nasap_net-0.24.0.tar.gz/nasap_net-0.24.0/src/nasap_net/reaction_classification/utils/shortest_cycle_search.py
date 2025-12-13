from math import inf

import networkx as nx

from nasap_net import Assembly


def find_shortest_cycle(assembly: Assembly) -> list | None:
    """Find one of the shortest cycles in the assembly.

    The length of cycle is the number of components in the cycle.
    For example, the cycle ['M1', 'L1', 'M2', 'L2'] has length 4.

    Which of the shortest cycles is returned is not guaranteed.

    Parameters
    ----------
    assembly : Assembly
        The assembly to find the shortest cycle in.

    Returns
    -------
    list or None
        The shortest cycle in the assembly.
        If there is no cycle, return None.
    """
    g = assembly.rough_g_snapshot
    cycles = list(nx.simple_cycles(g))
    if not cycles:
        return None
    return min(cycles, key=len)
