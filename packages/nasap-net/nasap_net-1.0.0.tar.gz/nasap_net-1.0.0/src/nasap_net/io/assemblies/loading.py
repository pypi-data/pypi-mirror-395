import logging
import os
from pathlib import Path

from nasap_net.io.assemblies.yaml_loading import load_assemblies_from_str
from nasap_net.models import Assembly

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def load_assemblies(
        file_path: os.PathLike | str,
) -> list[Assembly]:
    """Load assemblies and components from a YAML file.

    Parameters
    ----------
    file_path : os.PathLike | str
        Path to the YAML file to load.

    Returns
    -------
    list[Assembly]
        List of loaded assemblies.
    """
    file_path = Path(file_path)

    yaml_str = file_path.read_text(encoding="utf-8")
    assemblies = load_assemblies_from_str(yaml_str)
    logger.info('Loaded %d assemblies from "%s"', len(assemblies), str(file_path))
    return assemblies
