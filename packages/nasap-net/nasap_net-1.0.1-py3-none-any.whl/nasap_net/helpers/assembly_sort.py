from collections.abc import Sequence

from nasap_net.models import Assembly


def sort_assemblies_by_component_kind_counts(
        assemblies: list[Assembly],
        kinds: Sequence[str],
) -> list[Assembly]:
    """Sort assemblies by the counts of specified component kinds.

    The order of sorting is determined by the order of `kinds`.
    The order of assemblies with the same counts for all specified kinds is
    preserved.

    Parameters
    ----------
    assemblies : list[Assembly]
        List of assemblies to sort.
    kinds : Sequence[str]
        Sequence of component kinds to consider for sorting.

    Returns
    -------
    list[Assembly]
        Sorted list of assemblies.
    """
    def sort_key(assembly: Assembly) -> tuple[int, ...]:
        count_map = assembly.component_kind_counts
        return tuple(count_map.get(kind, 0) for kind in kinds)

    return sorted(assemblies, key=sort_key)
