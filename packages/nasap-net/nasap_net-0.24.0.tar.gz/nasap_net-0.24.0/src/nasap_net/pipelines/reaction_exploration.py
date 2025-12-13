import os

import pandas as pd

from nasap_net import explore_reactions

from .lib import reactions_to_df, read_file


def explore_reactions_pipeline(
        assemblies_path: os.PathLike | str,
        components_path: os.PathLike | str,
        config_path: os.PathLike | str,
        output_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None:
    id_to_assembly = read_file(assemblies_path)
    config = read_file(config_path)
    components = read_file(components_path)
    
    metal_kind = config['mle_kinds']['metal']
    leaving_kind = config['mle_kinds']['leaving']
    entering_kind = config['mle_kinds']['entering']

    component_kinds = components['component_kinds']

    if verbose:
        print('Enumerating reactions...')
        
    result = explore_reactions(
        id_to_assembly,
        metal_kind=metal_kind,
        leaving_kind=leaving_kind,
        entering_kind=entering_kind,
        component_structures=component_kinds,
        verbose=verbose,
    )

    if verbose:
        print('Reaction enumeration completed.')

    # Output
    _write_output(
        output_path, reactions_to_df(result),
        overwrite=overwrite,
        verbose=verbose,
    )


def _write_output(
        output_path: os.PathLike | str, reaction_df: pd.DataFrame,
        *,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None:
    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(f'Output file "{output_path}" already exists.')
    if verbose:
        print(f'Saving the results to "{output_path}"...')
    dir_ = os.path.dirname(output_path)
    if dir_:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    reaction_df.to_csv(output_path, index=False)
    if verbose:
        print(f'Successfully saved to "{output_path}".')
