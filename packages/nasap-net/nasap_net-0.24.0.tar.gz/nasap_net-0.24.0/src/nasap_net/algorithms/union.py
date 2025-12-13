from nasap_net import Assembly

__all__ = ['union_assemblies']


def union_assemblies(
        assembly1: Assembly, assembly2: Assembly,
        rename_prefix1: str | None = None,
        rename_prefix2: str | None = None
        ) -> Assembly:
    """Union two assemblies.

    Parameters
    ----------
    assembly1
        The first assembly.
    assembly2
        The second assembly.
    rename_map1
        A mapping from the component ids of the first assembly to the new
        component ids. If `None`, the component ids are not changed.
    rename_map2
        A mapping from the component ids of the second assembly to the new
        component ids. If `None`, the component ids are not changed.

    Returns
    -------
    Assembly
        The union of the two assemblies.
    
    Raises
    ------
    ValueError
        If the assemblies have overlapping nodes.

    Examples
    --------
    >>> from nasap_net import Assembly
    >>> from nasap_net.assem_class.assem import Assembly
    """
    if rename_prefix1 is not None:
        rename_map1 = {
            comp_id: f'{rename_prefix1}{comp_id}'
            for comp_id in assembly1.component_ids}
        assembly1 = assembly1.rename_component_ids(rename_map1)

    if rename_prefix2 is not None:
        rename_map2 = {
            comp_id: f'{rename_prefix2}{comp_id}'
            for comp_id in assembly2.component_ids}
        assembly2 = assembly2.rename_component_ids(rename_map2)

    if set(assembly1.component_ids) & set(assembly2.component_ids):
        raise ValueError('The assemblies have overlapping component IDs.')

    component_id_to_kind = (
        assembly1.comp_id_to_kind | assembly2.comp_id_to_kind)
    bonds = assembly1.bonds | assembly2.bonds

    return Assembly(component_id_to_kind, bonds)
