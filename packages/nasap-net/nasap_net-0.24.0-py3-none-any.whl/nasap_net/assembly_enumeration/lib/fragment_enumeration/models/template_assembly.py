from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType
from typing import Iterable

from nasap_net.models import Assembly
from nasap_net.types import ID
from .light_bond import LightBond


@dataclass(frozen=True)
class TemplateAssembly:
    assembly: Assembly

    @property
    def components(self) -> frozenset[ID]:
        return frozenset(self.assembly.components.keys())

    @property
    def bonds(self) -> frozenset[LightBond]:
        return frozenset(
            LightBond.from_bond(bond) for bond in self.assembly.bonds
        )

    def get_bonds_involving_components(
            self, components_ids: Iterable[ID]
    ) -> frozenset[LightBond]:
        """Return all bonds that involve at least one component ID from the
        specified set.
        """
        result_bonds: set[LightBond] = set()
        for comp_id in components_ids:
            bonds = self._component_id_to_bonds.get(comp_id, frozenset())
            result_bonds.update(bonds)
        return frozenset(result_bonds)

    @cached_property
    def _component_id_to_bonds(
            self
    ) -> MappingProxyType[ID, frozenset[LightBond]]:
        comp_id_to_bonds: dict[ID, set[LightBond]] = defaultdict(set)
        for bond in self.bonds:
            for comp_id in bond.component_ids:
                comp_id_to_bonds[comp_id].add(bond)
        return MappingProxyType({
            comp_id: frozenset(bonds)
            for comp_id, bonds in comp_id_to_bonds.items()
        })
