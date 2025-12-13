import os
from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from nasap_net import convert_bondset_to_assembly
from nasap_net.pipelines.lib import read_file, write_output

_T = TypeVar('_T', bound=Hashable)



# ============================================================
# Main Process
# ============================================================

def bondsets_to_assemblies_pipeline(
        bondsets_path: os.PathLike | str,
        structure_data_path: os.PathLike | str,
        output_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = False
        ) -> None:
    # Input
    id_to_bondset = read_file(bondsets_path, verbose=verbose)
    structure_input = read_file(structure_data_path, verbose=verbose)

    validate_bond_id_to_bindsites(
        structure_input['bonds_and_their_binding_sites'],
        structure_input['components_and_their_kinds'].keys())
    
    # Main process
    if verbose:
        print('Converting bondsets to assemblies...')
    
    id_to_assembly = {
        id_: convert_bondset_to_assembly(
            bondset, structure_input['components_and_their_kinds'],
            structure_input['bonds_and_their_binding_sites'])
        for id_, bondset in id_to_bondset.items()
        }
    if verbose:
        print('Conversion completed.')
    
    # Output
    write_output(
        output_path, id_to_assembly, overwrite=overwrite, verbose=verbose,
        header='Converted assemblies')


# ============================================================
# Input Processing
# ============================================================


def validate_bond_id_to_bindsites(
        bond_id_to_bindsites: Mapping,
        comp_ids: Iterable[str]
        ) -> None:
    for bond_id, (bs1, bs2) in bond_id_to_bindsites.items():
        if not isinstance(bs1, str) or not isinstance(bs2, str):
            raise ValueError(
                'Values in "bonds_and_their_binding_sites" must be '
                'strings.')
        if bs1 == bs2:
            raise ValueError(
                'Values in "bonds_and_their_binding_sites" must be '
                'different.')
        # bs1 and bs2 must be the form of 'comp_id.local_bindsite_id'
        if not bs1.count('.') == 1 or not bs2.count('.') == 1:
            raise ValueError(
                'Values in "bonds_and_their_binding_sites" must be in the '
                'form of "comp_id.local_bindsite_id", e.g., "M1.a".')
        comp_id1, bs_id1 = bs1.split('.')
        comp_id2, bs_id2 = bs2.split('.')
        for comp_id in (comp_id1, comp_id2):
            if comp_id not in comp_ids:
                raise ValueError(
                    f'Unknown component ID "{comp_id}" in '
                    f'"bonds_and_their_binding_sites".')
        if comp_id1 == comp_id2:
            raise ValueError(
                'The two components in a bond must be different.')
