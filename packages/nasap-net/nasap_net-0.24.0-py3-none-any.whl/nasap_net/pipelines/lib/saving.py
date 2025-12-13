import os
from typing import Any

import yaml


def write_output(
        output_path: os.PathLike | str, data: Any,
        *,
        overwrite: bool = False,
        default_flow_style: bool | None = None,
        verbose: bool = False,
        header: str | None = None,
        ) -> None:
    """Write the output data to a file using YAML format."""
    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(f'Output file "{output_path}" already exists.')
    if verbose:
        print(f'Saving the results to "{output_path}"...')
    dir_ = os.path.dirname(output_path)
    if dir_:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=default_flow_style)
    if verbose:
        if header:
            print(f'{header}: Successfully saved to "{output_path}".')
        else:
            print(f'Successfully saved to "{output_path}".')
