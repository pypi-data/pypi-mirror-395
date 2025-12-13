import logging
import os
from collections.abc import Iterable
from pathlib import Path

from nasap_net.io.assemblies.yaml_dumping import dump_assemblies_to_str
from nasap_net.models import Assembly

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def save_assemblies(
        assemblies: Iterable[Assembly],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        ) -> None:
    """Dump assemblies and components into a YAML file.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        Assemblies to dump.
    file_path : os.PathLike | str
        Path to the YAML file to write.
    overwrite : bool, optional
        If True, overwrite the file if it already exists.
        If False, raise an error if the file already exists.
        Default is False.
    """
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )

    assemblies = list(assemblies)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = dump_assemblies_to_str(assemblies)
    file_path.write_text(yaml_str, encoding="utf-8")
    logger.info('Saved %d assemblies to "%s"', len(assemblies), str(file_path))
