import os
import tempfile
from collections.abc import Hashable
from pathlib import Path
from typing import TypeVar

from .assembly_list_concatenation import \
    concatenate_assemblies_without_isom_checks
from .bindsite_capping import cap_bindsites_pipeline
from .bondset_enumeration import enum_bond_subsets_pipeline
from .bondset_to_assembly import bondsets_to_assemblies_pipeline
from .duplicate_exclusion import find_unique_assemblies_pipeline


def enumerate_assemblies_pipeline(
        input_path: os.PathLike | str,
        output_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = False,
        wip_dir: os.PathLike | str | None = None
        ) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        if wip_dir is None:
            wip_dir = temp_dir
        wip_dir = Path(wip_dir)

        resolved_sym_ops_path = wip_dir / 'resolved_sym_ops.yaml'
        wip1_bondsets_path = wip_dir / 'wip1_bondsets.yaml'
        wip2_assemblies_path = wip_dir / 'wip2_assemblies.yaml'
        wip3_unique_assemblies_path = wip_dir / 'wip3_unique_assemblies.yaml'
        wip4_capped_assemblies_path = wip_dir / 'wip4_capped_assemblies.yaml'

        if verbose:
            print('Enumerating assemblies...')
            
        enum_bond_subsets_pipeline(
            input_path, wip1_bondsets_path, overwrite=overwrite,
            path_to_output_resolved_sym_ops=resolved_sym_ops_path)
        bondsets_to_assemblies_pipeline(
            wip1_bondsets_path, input_path, wip2_assemblies_path,
            overwrite=overwrite)
        find_unique_assemblies_pipeline(
            wip2_assemblies_path, input_path, wip3_unique_assemblies_path,
            overwrite=overwrite)
        cap_bindsites_pipeline(
            wip3_unique_assemblies_path, input_path, input_path, wip4_capped_assemblies_path,
            overwrite=overwrite)
        concatenate_assemblies_without_isom_checks(
            [wip4_capped_assemblies_path], output_path, overwrite=overwrite)
        

        if verbose:
            print('Assembly enumeration completed.')
            print(f'Successfully saved to {output_path}.')
