from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Generic, Mapping, TypeVar

from .assembly import Assembly
from .rich_reaction import InterReactionRich, IntraReactionRich, \
    RichReactionBase


class InterOrIntra(Enum):
    INTER = auto()
    INTRA = auto()


R_co = TypeVar("R_co", bound=RichReactionBase, covariant=True)


class ReactionBase(ABC, Generic[R_co]):
    @property
    @abstractmethod
    def inter_or_intra(self) -> InterOrIntra:
        """Whether the reaction is intra- or inter-molecular."""
        pass

    @property
    @abstractmethod
    def reactants(self) -> list[int]:
        """List of reactant assembly IDs."""
        pass

    @property
    @abstractmethod
    def products(self) -> list[int]:
        """List of product assembly IDs."""
        pass

    @abstractmethod
    def to_rich_reaction(self, id_to_assembly: Mapping[int, Assembly]) -> R_co:
        """Convert to a rich reaction by embedding assemblies."""
        pass


@dataclass
class InterReaction(ReactionBase[InterReactionRich]):
    init_assem_id: int
    entering_assem_id: int
    product_assem_id: int
    leaving_assem_id: int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @property
    def inter_or_intra(self) -> InterOrIntra:
        return InterOrIntra.INTER

    @property
    def reactants(self) -> list[int]:
        return [self.init_assem_id, self.entering_assem_id]

    @property
    def products(self) -> list[int]:
        if self.leaving_assem_id is None:
            return [self.product_assem_id]
        return [self.product_assem_id, self.leaving_assem_id]

    def to_rich_reaction(
            self, id_to_assembly: Mapping[int, Assembly]
            ) -> InterReactionRich:
        return InterReactionRich.from_reaction(self, id_to_assembly)


@dataclass
class IntraReaction(ReactionBase[IntraReactionRich]):
    init_assem_id: int
    entering_assem_id: ClassVar[None] = None
    product_assem_id: int
    leaving_assem_id: int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @property
    def inter_or_intra(self) -> InterOrIntra:
        return InterOrIntra.INTRA

    @property
    def reactants(self) -> list[int]:
        return [self.init_assem_id]

    @property
    def products(self) -> list[int]:
        if self.leaving_assem_id is None:
            return [self.product_assem_id]
        return [self.product_assem_id, self.leaving_assem_id]

    def to_rich_reaction(
            self, id_to_assembly: Mapping[int, Assembly]
            ) -> IntraReactionRich:
        return IntraReactionRich.from_reaction(self, id_to_assembly)
