from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from .assembly import Assembly


class RichReactionBase(ABC):
    @property
    @abstractmethod
    def metal_kind(self) -> str:
        """Kind of the metal component."""
        pass

    @property
    @abstractmethod
    def leaving_kind(self) -> str:
        """Kind of the leaving component."""
        pass

    @property
    @abstractmethod
    def entering_kind(self) -> str:
        """Kind of the entering component."""
        pass

    @classmethod
    @abstractmethod
    def from_reaction(cls, reaction, id_to_assembly: Mapping[int, Assembly]):
        """Create a RichReaction from a Reaction and a mapping from assembly
        IDs to assemblies."""
        pass


@dataclass(frozen=True)
class InterReactionRich(RichReactionBase):
    init_assem: Assembly
    entering_assem: Assembly
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @cached_property
    def metal_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.metal_bs)

    @cached_property
    def leaving_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.leaving_bs)

    @cached_property
    def entering_kind(self) -> str:
        return self.entering_assem.get_component_kind_of_bindsite(
            self.entering_bs)

    @classmethod
    def from_reaction(cls, reaction, id_to_assembly: Mapping[int, Assembly]):
        init_assem = id_to_assembly[reaction.init_assem_id]
        entering_assem = id_to_assembly[reaction.entering_assem_id]
        product_assem = id_to_assembly[reaction.product_assem_id]
        if reaction.leaving_assem_id is None:
            leaving_assem = None
        else:
            leaving_assem = id_to_assembly[reaction.leaving_assem_id]
        return cls(
            init_assem=init_assem,
            entering_assem=entering_assem,
            product_assem=product_assem,
            leaving_assem=leaving_assem,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
            duplicate_count=reaction.duplicate_count
        )


@dataclass(frozen=True)
class IntraReactionRich(RichReactionBase):
    init_assem: Assembly
    entering_assem: ClassVar[None] = None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @cached_property
    def metal_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.metal_bs)

    @cached_property
    def leaving_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.leaving_bs)

    @cached_property
    def entering_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.entering_bs)

    @classmethod
    def from_reaction(cls, reaction, id_to_assembly: Mapping[int, Assembly]):
        init_assem = id_to_assembly[reaction.init_assem_id]
        product_assem = id_to_assembly[reaction.product_assem_id]
        if reaction.leaving_assem_id is None:
            leaving_assem = None
        else:
            leaving_assem = id_to_assembly[reaction.leaving_assem_id]
        return cls(
            init_assem=init_assem,
            product_assem=product_assem,
            leaving_assem=leaving_assem,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
            duplicate_count=reaction.duplicate_count
        )
