import os
from collections.abc import Hashable, Mapping
from typing import TypeVar

from nasap_net import Assembly, Component, group_assemblies_by_isomorphism
from nasap_net.pipelines.lib import read_file, write_output

_T = TypeVar('_T', bound=Hashable)



# ============================================================
# Main Process
# ============================================================

def find_unique_assemblies_pipeline(
        assemblies_path: os.PathLike | str,
        components_path: os.PathLike | str,
        output_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = False
        ) -> None:
    # Input
    id_to_assembly: Mapping[Hashable, Assembly] = read_file(
        assemblies_path, verbose=verbose)
    components: Mapping[str, Component] = read_file(
        components_path, verbose=verbose)['component_kinds']
    
    # Main process
    if verbose:
        print('Enumerating unique assemblies...')
    
    unique_id_to_dup_ids = group_assemblies_by_isomorphism(
        id_to_assembly, components)
    id_to_unique_assembly = {
        unique_id: id_to_assembly[unique_id]
        for unique_id in unique_id_to_dup_ids
    }
    
    if verbose:
        print('Finished enumeration.')
    
    # Output
    write_output(
        output_path, id_to_unique_assembly, 
        overwrite=overwrite, verbose=verbose,
        header='Unique assemblies')
