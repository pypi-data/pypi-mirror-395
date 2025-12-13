from collections.abc import Iterable
from dataclasses import dataclass

from nasap_net.exceptions import NasapNetError
from nasap_net.models import Assembly, Component


@dataclass(frozen=True)
class FoundComponent:
    component: Component
    source_assembly: Assembly


def check_component_consistency(assemblies: Iterable[Assembly]) -> None:
    """Check for consistent definitions of component kinds across assemblies.

    Components with the same kind name must have identical structures,
    including site IDs.

    The function raises an InconsistentComponentBetweenAssembliesError
    if it finds any inconsistencies.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        An iterable of Assembly instances to check for component consistency.

    Raises
    ------
    InconsistentComponentBetweenAssembliesError
        If there are inconsistent definitions for a component kind,
        i.e., the same kind name corresponds to different component structures.
    """
    found_components: dict[str, FoundComponent] = {}
    for assembly in assemblies:
        for comp in assembly.components.values():
            if comp.kind in found_components:
                if comp != found_components[comp.kind].component:
                    raise InconsistentComponentBetweenAssembliesError(
                        component_kind=comp.kind,
                        assembly1=found_components[comp.kind].source_assembly,
                        assembly2=assembly,
                    )
            else:
                found_components[comp.kind] = FoundComponent(
                    component=comp,
                    source_assembly=assembly
                )


@dataclass
class InconsistentComponentBetweenAssembliesError(NasapNetError):
    """Raised when there are inconsistent definitions for a component kind
    between different assemblies.
    """
    component_kind: str
    assembly1: Assembly
    assembly2: Assembly

    def __str__(self) -> str:
        return (
            f'Inconsistent definitions for component kind '
            f'"{self.component_kind}" between assemblies: '
            f'Assembly 1: {self.assembly1}, Assembly 2: {self.assembly2}.'
        )
