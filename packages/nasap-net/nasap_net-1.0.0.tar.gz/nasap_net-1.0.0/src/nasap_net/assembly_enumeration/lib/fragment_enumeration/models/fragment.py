from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import Iterable, Iterator, Self

from nasap_net.models import Assembly
from nasap_net.types import ID
from .growing_step import GrowingStep
from .light_bond import LightBond
from .template_assembly import TemplateAssembly


@total_ordering
@dataclass(frozen=True, init=False)
class Fragment:
    components: frozenset[ID]
    bonds: frozenset[LightBond]
    template: TemplateAssembly

    def __init__(
            self,
            components: Iterable[ID],
            bonds: Iterable[LightBond],
            template: Assembly,
    ) -> None:
        object.__setattr__(self, 'components', frozenset(components))
        object.__setattr__(self, 'bonds', frozenset(bonds))
        object.__setattr__(
            self,
            'template',
            TemplateAssembly(assembly=template),
        )
        self._validate()

    def __lt__(self, other):
        if not isinstance(other, Fragment):
            return NotImplemented
        if self.components != other.components:
            return sorted(self.components) < sorted(other.components)
        return sorted(self.bonds) < sorted(other.bonds)

    def enumerate_possible_growing_steps(self) -> Iterator[GrowingStep]:
        """Return possible growing steps that add bonds between existing
        components.
        """
        possible_bonds = self.template.get_bonds_involving_components(
            self.components
        ) - self.bonds
        for bond in sorted(possible_bonds):
            missing_comps = bond.component_ids - self.components
            if len(missing_comps) == 0:
                # Type 1 growing step: bond between existing components
                yield GrowingStep(bond_to_add=bond, component_to_add=None)
            elif len(missing_comps) == 1:
                # Type 2 growing step: bond involving one new component
                new_comp_id = list(missing_comps)[0]
                yield GrowingStep(
                    bond_to_add=bond, component_to_add=new_comp_id
                )

    def copy_with(
            self,
            components: Iterable[ID] | None = None,
            bonds: Iterable[LightBond] | None = None,
    ) -> Self:
        return self.__class__(
            components=(
                components if components is not None else self.components
            ),
            bonds=bonds if bonds is not None else self.bonds,
            template=self.template.assembly,
        )

    def to_assembly(self) -> Assembly:
        """Convert the fragment back to an Assembly.

        Returns
        -------
        Assembly
            The Assembly representation of the Fragment.

        Notes
        -----
        The conversion from Fragment to Assembly assumes that
        a pair of component IDs uniquely identifies a bond,
        which holds true as long as there are no parallel bonds (chelate).
        This logic needs to be revisited if parallel bonds are to be supported.
        """
        components = {
            comp_id: self.template.assembly.components[comp_id]
            for comp_id in self.components
        }
        bonds = [
            self.template.assembly.get_bond_by_comp_ids(*bond.component_ids)
            for bond in self.bonds
        ]
        return Assembly(components=components, bonds=bonds)

    def _validate(self):
        for bond in self.bonds:
            for comp_id in bond.component_ids:
                if comp_id not in self.components:
                    raise ValueError(
                        f"Bond references non-existent component ID: {comp_id}"
                    )


def create_complete_fragment(assembly: Assembly) -> Fragment:
    """Create a complete fragment from an assembly."""
    components = assembly.components.keys()
    bonds = [LightBond.from_bond(bond) for bond in assembly.bonds]
    return Fragment(components=components, bonds=bonds, template=assembly)
