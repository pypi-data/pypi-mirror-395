import os
from collections.abc import Hashable, Mapping
from typing import TypedDict

from nasap_net import Assembly, Component, cap_bindsites
from nasap_net.pipelines.lib import read_file, write_output


class CappingConfig(TypedDict):
    target_component_kind: str
    capping_component_kind: str
    capping_binding_site: str


# ============================================================
# Main Process
# ============================================================

def cap_bindsites_pipeline(
        assemblies_path: os.PathLike | str,
        components_path: os.PathLike | str,
        config_path: os.PathLike | str,
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
    config: CappingConfig = read_file(
        config_path, verbose=verbose)['capping_config']
    
    # Main process
    if verbose:
        print('Capping binding sites...')

    capped_assemblies = {}
    for id_, assembly in id_to_assembly.items():
        capped_assemblies[id_] = cap_bindsites(
            assembly, components, 
            config['target_component_kind'],
            config['capping_component_kind'],
            config['capping_binding_site'],
            copy=True)
        
    if verbose:
        print('Capping completed.')
    
    # Output
    write_output(
        output_path, capped_assemblies, 
        overwrite=overwrite, verbose=verbose,
        header='Capped assemblies')
