from nasap_net.isomorphism import is_isomorphic
from nasap_net.models import Assembly


def assemblies_equivalent(
        assembly1: Assembly,
        assembly2: Assembly,
) -> bool:
    """Check if two assemblies are equivalent.

    Two assemblies are considered equivalent if they are isomorphic,
    meaning there exists a one-to-one mapping between their components and
    binding sites that preserves the following properties:
        - Component kinds
        - Bond connections
        - Auxiliary edges (if present)
        - Auxiliary edge types (if present)

    Parameters
    ----------
    assembly1 : Assembly
        The first assembly to compare.
    assembly2 : Assembly
        The second assembly to compare.

    Returns
    -------
    bool
        True if the assemblies are equivalent, False otherwise.
    """
    if assembly1 == assembly2:
        return True
    return is_isomorphic(assembly1, assembly2)
