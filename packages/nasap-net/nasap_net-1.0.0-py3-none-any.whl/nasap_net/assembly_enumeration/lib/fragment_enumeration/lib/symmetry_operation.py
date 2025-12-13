from collections.abc import Mapping
from typing import Any, TypeVar

from nasap_net.exceptions import NasapNetError
from nasap_net.types import ID
from ..models import Fragment, LightBond

_T = TypeVar('_T', bound=ID)


def validate_symmetry_operation(
        fragment: Fragment,
        symmetry_operation: Mapping[_T, _T]
) -> None:
    if set(symmetry_operation.keys()) != set(fragment.components):
        raise InvalidSymmetryOperationError()
    if set(symmetry_operation.values()) != set(fragment.components):
        raise InvalidSymmetryOperationError()


def apply_symmetry_operation(
        fragment: Fragment,
        symmetry_operation: Mapping[Any, ID]
) -> Fragment:
    components = {
        symmetry_operation[comp_id] for comp_id in fragment.components
    }
    bonds = [
        LightBond(
            *(symmetry_operation[comp_id] for comp_id in bond.component_ids)
        )
        for bond in fragment.bonds
    ]
    return fragment.copy_with(
        components=components,
        bonds=bonds,
    )


class InvalidSymmetryOperationError(NasapNetError):
    pass
