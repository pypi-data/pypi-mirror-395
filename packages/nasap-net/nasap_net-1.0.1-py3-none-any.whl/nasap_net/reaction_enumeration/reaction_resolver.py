from collections.abc import Iterable
from dataclasses import dataclass, field

from nasap_net.assembly_equivalence import AssemblyNotFoundError, \
    EquivalentAssemblyFinder
from nasap_net.exceptions import NasapNetError
from nasap_net.models import Assembly
from nasap_net.models.reaction import Reaction


class ReactionOutOfScopeError(NasapNetError):
    """Exception raised when a reaction cannot be resolved to the assembly space."""
    pass


@dataclass(frozen=True, init=False)
class ReactionResolver:
    """Class to resolve reactions to a given assembly space.

    Parameters
    ----------
    assembly_space : Iterable[Assembly]
        The assembly space to resolve reactions against.

    Methods
    -------
    resolve(reaction: Reaction) -> Reaction
        Resolve a reaction to the assembly space.
    """
    assembly_space: frozenset[Assembly]
    finder: EquivalentAssemblyFinder = field(init=False)

    def __init__(self, assembly_space: Iterable[Assembly]) -> None:
        object.__setattr__(
            self, 'assembly_space', frozenset(assembly_space))
        object.__setattr__(
            self, 'finder',
            EquivalentAssemblyFinder(self.assembly_space))

    def resolve(self, reaction: Reaction) -> Reaction:
        """Resolve a reaction to the assembly space.

        "Resolving" a reaction means ensuring that the product and leaving
        assemblies exist in the provided assembly space, and replacing them
        with the corresponding isomorphic assemblies from the assembly space.

        Parameters
        ----------
        reaction : Reaction
            The reaction to resolve.

        Returns
        -------
        Reaction
            The resolved reaction with assemblies from the assembly space.

        Raises
        ------
        ReactionOutOfScopeError
            If the reaction cannot be resolved to the assembly space.
        """
        # Cond-1: The product assembly must exist in the provided assemblies.
        try:
            isom_product_assem = self.finder.find(reaction.product_assem)
        except AssemblyNotFoundError as e:
            raise ReactionOutOfScopeError("Product assembly not found") from e

        if reaction.leaving_assem is None:
            return Reaction(
                init_assem=reaction.init_assem,
                entering_assem=reaction.entering_assem,
                product_assem=isom_product_assem,
                leaving_assem=None,
                metal_bs=reaction.metal_bs,
                leaving_bs=reaction.leaving_bs,
                entering_bs=reaction.entering_bs,
                duplicate_count=reaction.duplicate_count
            )

        # Cond-2: The leaving assembly must exist in the provided assemblies.
        try:
            isom_leaving_assem = self.finder.find(reaction.leaving_assem)
        except AssemblyNotFoundError as e:
            raise ReactionOutOfScopeError("Leaving assembly not found") from e

        return Reaction(
            init_assem=reaction.init_assem,
            entering_assem=reaction.entering_assem,
            product_assem=isom_product_assem,
            leaving_assem=isom_leaving_assem,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
            duplicate_count=reaction.duplicate_count
        )
