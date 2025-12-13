from nasap_net import Assembly, BindsiteIdConverter
from nasap_net.algorithms.assembly_separation import separate_product_if_possible


def perform_intra_exchange(
        assembly: Assembly,
        metal_bs: str, leaving_bs: str, entering_bs: str,
        ) -> tuple[Assembly, Assembly | None]:
    """Perform an intra-molecular ligand exchange reaction.

    This function returns the resulting assembly(ies) after performing
    a ligand exchange reaction within a single assembly.

    The ligand exchange process can be summarized as follows:
    - The bond between the metal center (metal_bs) and the leaving ligand
      (leaving_bs) in the assembly is broken.
    - A new bond is formed between the metal center (metal_bs) and the
      entering ligand (entering_bs) in the same assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly.
    metal_bs : str
        The binding site ID of the metal center.
    leaving_bs : str
        The binding site ID of the leaving ligand.
        This binding site should be bonded to metal_bs.
    entering_bs : str
        The binding site ID of the entering ligand.
        This binding site should not be bonded to any other binding site.

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
    - This function preserves the component IDs in the input assembly;
        no renaming or prefixing is performed.
    """
    assembly = assembly.deepcopy()
    assembly.remove_bond(metal_bs, leaving_bs)
    assembly.add_bond(entering_bs, metal_bs)

    id_converter = BindsiteIdConverter()
    metal_comp, _ = id_converter.global_to_local(metal_bs)
    # Separate the leaving assembly if possible
    assembly, leaving_assem = separate_product_if_possible(
        assembly, metal_comp)
    return assembly, leaving_assem
