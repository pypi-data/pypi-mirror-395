from typing import Callable

from nasap_net.models import Assembly, Bond
from nasap_net.types import ID


def reindex_components_in_assembly(
        assembly: Assembly, reindexing_func: Callable[[ID], ID]
) -> Assembly:
    """Reindex components in an assembly using the provided reindexing function.

    Parameters
    ----------
    assembly : Assembly
        The assembly whose component IDs are to be reindexed.
    reindexing_func : Callable[[ID], ID]
        A function that takes a component ID and returns the reindexed component ID.

    Returns
    -------
    Assembly
        A new assembly with reindexed component IDs.

    Raises
    ------
    ValueError
        If the reindexing function causes ID collisions.

    Notes
    -----
    Assembly ID is preserved.
    """
    renamed_components = {
        reindexing_func(id_): comp
        for id_, comp in assembly.components.items()}

    # Check no collision occurs
    if len(renamed_components) != len(assembly.components):
        raise ValueError('Reindexing function caused ID collisions.')

    renamed_bonds = {
        Bond(
            comp_id1=reindexing_func(site1.component_id), site1=site1.site_id,
            comp_id2=reindexing_func(site2.component_id), site2=site2.site_id
        )
        for (site1, site2) in assembly.bonds
    }

    return assembly.copy_with(
        components=renamed_components,
        bonds=renamed_bonds,
        id_=assembly.id_or_none
    )
