import logging
import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Literal

import pandas as pd

from nasap_net.helpers import validate_unique_ids
from nasap_net.models import Assembly, BindingSite, Reaction
from nasap_net.types import ID
from .models import ReactionRow

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def load_reactions(
        file_path: os.PathLike | str,
        assemblies: Iterable[Assembly],
        *,
        assembly_id_type: Literal['str', 'int'] = 'str',
        component_id_type: Literal['str', 'int'] = 'str',
        site_id_type: Literal['str', 'int'] = 'str',
        reaction_id_type: Literal['str', 'int'] = 'str',
        has_index_column: bool = False,
) -> list[Reaction]:
    """Load reactions from a CSV file and convert to Reaction objects."""
    validate_unique_ids(assemblies)
    id_to_assembly = {assembly.id_: assembly for assembly in assemblies}

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f'File "{str(file_path)}" does not exist.')

    df = pd.read_csv(
        file_path,
        index_col=0 if has_index_column else None,
    )
    df = df.astype(object).where(pd.notnull(df), None)

    types = {'int': int, 'str': str}

    reaction_rows = [
        ReactionRow.from_dict(
            row,
            assembly_id_type=types[assembly_id_type],
            component_id_type=types[component_id_type],
            site_id_type=types[site_id_type],
            reaction_id_type=types[reaction_id_type],
        )
        for row in df.to_dict(orient="records")
    ]

    reactions = [
        reaction_row_to_reaction(reaction_row, id_to_assembly)
        for reaction_row in reaction_rows
    ]

    logger.info('Loaded %d reactions from "%s"', len(reactions), str(file_path))

    return reactions


def reaction_row_to_reaction(
        reaction_row: ReactionRow,
        id_to_assemblies: Mapping[ID, Assembly],
) -> Reaction:
    """Convert a ReactionRow to a Reaction object."""
    init_assem = id_to_assemblies[reaction_row.init_assem_id]
    entering_assem = (
        None if reaction_row.entering_assem_id is None
        else id_to_assemblies[reaction_row.entering_assem_id]
    )
    product_assem = id_to_assemblies[reaction_row.product_assem_id]
    leaving_assem = (
        None if reaction_row.leaving_assem_id is None
        else id_to_assemblies[reaction_row.leaving_assem_id]
    )

    return Reaction(
        init_assem=init_assem,
        entering_assem=entering_assem,
        product_assem=product_assem,
        leaving_assem=leaving_assem,
        metal_bs=BindingSite(
            component_id=reaction_row.metal_bs_component,
            site_id=reaction_row.metal_bs_site,
        ),
        leaving_bs=BindingSite(
            component_id=reaction_row.leaving_bs_component,
            site_id=reaction_row.leaving_bs_site,
        ),
        entering_bs=BindingSite(
            component_id=reaction_row.entering_bs_component,
            site_id=reaction_row.entering_bs_site,
        ),
        duplicate_count=reaction_row.duplicate_count,
        id_=reaction_row.id_,
    )
