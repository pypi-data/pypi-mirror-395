import os
from typing import Any

import yaml


def read_file(
        input_path: os.PathLike | str,
        *,
        verbose: bool = False
        ) -> Any:
    """Read the input file."""
    if verbose:
        print(f'Reading from "{input_path}"...')
    with open(input_path, 'r') as f:
        data = yaml.safe_load(f)
    if verbose:
        print(f'Finished reading from "{input_path}".')
    return data
