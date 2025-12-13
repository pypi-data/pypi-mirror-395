import logging
import os
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from nasap_net.models import Reaction
from .models import ReactionRow

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def save_reactions(
        reactions: Iterable[Reaction],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        index: bool = False,
        ) -> None:
    """Save reactions to a CSV file.

    Resulting CSV columns:
    - init_assem_id : str | int
    - entering_assem_id : str | int | None
    - product_assem_id : str | int
    - leaving_assem_id : str | int | None
    - metal_bs_component : str | int
    - metal_bs_site : str | int
    - leaving_bs_component : str | int
    - leaving_bs_site : str | int
    - entering_bs_component : str | int
    - entering_bs_site : str | int
    - duplicate_count : int
    - id : str | int | None

    Parameters
    ----------
    reactions : Iterable[Reaction]
        Reactions to save.
    file_path : os.PathLike | str
        Path to the CSV file to write.
    overwrite : bool, optional
        If True, overwrite the file if it already exists.
        If False, raise an error if the file already exists.
        Default is False.
    index : bool, optional
        If True, write row names (index). Default is False.
    """
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )

    reactions = list(reactions)
    df = reactions_to_df(reactions)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=index)
    logger.info('Saved %d reactions to "%s"', len(reactions), str(file_path))


def reactions_to_df(reactions: Iterable[Reaction]) -> pd.DataFrame:
    """Convert an iterable of Reaction objects to a pandas DataFrame.

    Parameters
    ----------
    reactions : Iterable[Reaction]
        Iterable of Reaction objects to convert.

    Returns
    -------
    pd.DataFrame
        DataFrame representation of the reactions.

    Raises
    ------
    IDNotSetError
        If any assembly ID in the reactions is not set.
    """
    rows = [
        _rename_id_key(ReactionRow.from_reaction(reaction).to_dict())
        for reaction in reactions
    ]

    return pd.DataFrame(rows)


def _rename_id_key(d: dict) -> dict:
    """Rename the 'id_' key in the dictionary to 'id'."""
    if 'id_' in d:
        d['id'] = d.pop('id_')
    return d
