from __future__ import annotations

from dataclasses import dataclass

from nasap_net.types import ID
from .light_bond import LightBond


@dataclass(frozen=True)
class GrowingStep:
    bond_to_add: LightBond
    component_to_add: ID | None
