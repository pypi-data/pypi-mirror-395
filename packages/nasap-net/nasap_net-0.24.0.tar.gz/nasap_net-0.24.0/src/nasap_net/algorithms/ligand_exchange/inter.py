from nasap_net import Assembly, BindsiteIdConverter
from nasap_net.algorithms.assembly_separation import separate_product_if_possible
from nasap_net.algorithms.union import union_assemblies


def perform_inter_exchange(
        init_assem: Assembly, entering_assem: Assembly,
        metal_bs: str, leaving_bs: str, entering_bs: str,
        ) -> tuple[Assembly, Assembly | None]:
    """Perform an inter-molecular ligand exchange reaction.

    This function returns the resulting assembly(ies) after performing
    a ligand exchange reaction between two assemblies.

    The ligand exchange process can be summarized as follows:
    - The bond between the metal center (metal_bs) and the leaving ligand
        (leaving_bs) in init_assem is broken.
    - A new bond is formed between the metal center (metal_bs) and the
        entering ligand (entering_bs) before or after the bond breaking,
        depending on the specific mechanism (dissociative or associative).

    Parameters
    ----------
    init_assem : Assembly
        The assembly containing the metal center and the leaving ligand.
    entering_assem : Assembly
        The assembly containing the entering ligand.
    metal_bs : str
        The binding site ID of the metal center (on init_assem).
    leaving_bs : str
        The binding site ID of the leaving ligand (on init_assem).
        This binding site should be bonded to metal_bs in init_assem.
    entering_bs : str
        The binding site ID of the entering ligand (on entering_assem).
        This binding site should not be bonded to any other binding site
        in entering_assem.

    Returns
    -------
    main_assembly : Assembly
        The assembly containing the metal center and the entering ligand.
        The leaving ligand may be part of this assembly or may be
        contained in a separated assembly (leaving_assembly).
    leaving_assembly : Assembly or None
        The separated leaving assembly, if it exists; otherwise None.

    Notes
    -----
    - This function renames component IDs in the input assemblies to
      avoid ID conflicts when merging them, by prefixing them with
      'init_' and 'entering_' respectively.
    """
    init_relabel = {
        comp_id: f'init_{comp_id}'
        for comp_id in init_assem.component_ids}
    init_assem = init_assem.rename_component_ids(init_relabel)

    entering_relabel = {
        comp_id: f'entering_{comp_id}'
        for comp_id in entering_assem.component_ids}
    entering_assem = entering_assem.rename_component_ids(entering_relabel)

    metal_bs = f'init_{metal_bs}'
    leaving_bs = f'init_{leaving_bs}'
    entering_bs = f'entering_{entering_bs}'

    init_assem = union_assemblies(init_assem, entering_assem)

    init_assem.remove_bond(metal_bs, leaving_bs)
    init_assem.add_bond(entering_bs, metal_bs)

    # Separate the leaving assembly if possible
    id_converter = BindsiteIdConverter()
    metal_comp, rel_bindsite = id_converter.global_to_local(metal_bs)
    main_assem, leaving_assem = separate_product_if_possible(
        init_assem, metal_comp)
    return main_assem, leaving_assem
