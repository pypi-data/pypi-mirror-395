from dataclasses import dataclass
from functools import total_ordering
from typing import Self, TYPE_CHECKING

from nasap_net.exceptions import IDNotSetError, NasapNetError
from nasap_net.models import Assembly, BindingSite, MLE
from nasap_net.types import ID
from nasap_net.utils.default import MISSING, Missing, default_if_missing

if TYPE_CHECKING:
    from nasap_net.reaction_classification import ReactionToClassify


class DuplicateCountNotSetError(NasapNetError):
    """Raised when the duplicate count of a reaction is not set."""
    def __init__(self):
        super().__init__("Duplicate count is not set.")


@total_ordering
@dataclass(frozen=True, init=False)
class Reaction:
    init_assem: Assembly
    entering_assem: Assembly | None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: BindingSite
    leaving_bs: BindingSite
    entering_bs: BindingSite
    _duplicate_count: int | None
    _id: ID | None

    def __init__(
            self,
            init_assem: Assembly,
            entering_assem: Assembly | None,
            product_assem: Assembly,
            leaving_assem: Assembly | None,
            metal_bs: BindingSite,
            leaving_bs: BindingSite,
            entering_bs: BindingSite,
            duplicate_count: int | None = None,
            id_: ID | None = None,
    ):
        if init_assem is None:
            raise TypeError("init_assem cannot be None")
        if product_assem is None:
            raise TypeError("product_assem cannot be None")
        if metal_bs is None:
            raise TypeError("metal_bs cannot be None")
        if leaving_bs is None:
            raise TypeError("leaving_bs cannot be None")
        if entering_bs is None:
            raise TypeError("entering_bs cannot be None")
        if duplicate_count is not None and duplicate_count <= 0:
            raise ValueError("duplicate_count must be a positive integer")

        object.__setattr__(self, 'init_assem', init_assem)
        object.__setattr__(self, 'entering_assem', entering_assem)
        object.__setattr__(self, 'product_assem', product_assem)
        object.__setattr__(self, 'leaving_assem', leaving_assem)
        object.__setattr__(self, 'metal_bs', metal_bs)
        object.__setattr__(self, 'leaving_bs', leaving_bs)
        object.__setattr__(self, 'entering_bs', entering_bs)
        object.__setattr__(self, '_duplicate_count', duplicate_count)
        object.__setattr__(self, '_id', id_)

    def __lt__(self, other):
        if not isinstance(other, Reaction):
            return NotImplemented
        def key(reaction: Reaction) -> tuple:
            return (
                reaction.init_assem_id,
                reaction.entering_assem_id,
                reaction.product_assem_id,
                reaction.leaving_assem_id,
                reaction.metal_bs,
                reaction.leaving_bs,
                reaction.entering_bs,
                reaction.duplicate_count_or_none,
                reaction.id_or_none,
            )
        return key(self) < key(other)

    def __str__(self):
        equation = self.equation_str
        dup = self.duplicate_count
        return f'{equation} (x{dup})'

    def __repr__(self):
        equation = self.equation_str
        if self._id is None:
            return f'<{self.__class__.__name__} {equation}>'
        return f'<{self.__class__.__name__} ID={self._id} {equation}>'

    @property
    def id_(self) -> ID:
        """Return the ID of the reaction."""
        if self._id is None:
            raise IDNotSetError("Reaction ID is not set.")
        return self._id

    @property
    def id_or_none(self) -> ID | None:
        """Return the ID of the reaction, or None if not set."""
        return self._id

    @property
    def duplicate_count(self) -> int:
        """Return the duplicate count of the reaction."""
        if self._duplicate_count is None:
            raise DuplicateCountNotSetError()
        return self._duplicate_count

    @property
    def duplicate_count_or_none(self) -> int | None:
        """Return the duplicate count of the reaction, or None if not set."""
        return self._duplicate_count

    @property
    def equation_str(self) -> str:
        """Return a string representation of the reaction equation.

        If an assembly ID is not set, '??' is used in its place.
        """
        init = _assembly_to_id(self.init_assem)
        entering = _assembly_to_id(self.entering_assem)
        product = _assembly_to_id(self.product_assem)
        leaving = _assembly_to_id(self.leaving_assem)

        left = f'{init}' if entering is None else f'{init} + {entering}'
        right = f'{product}' if leaving is None else f'{product} + {leaving}'

        return f'{left} -> {right}'

    @property
    def entering_assem_strict(self) -> Assembly:
        """Return the entering assembly.

        Errors if there is no entering assembly.
        """
        if self.entering_assem is None:
            raise ValueError("No entering assembly in this reaction.")
        return self.entering_assem

    @property
    def leaving_assem_strict(self) -> Assembly:
        """Return the leaving assembly.

        Errors if there is no leaving assembly.
        """
        if self.leaving_assem is None:
            raise ValueError("No leaving assembly in this reaction.")
        return self.leaving_assem

    @property
    def init_assem_id(self) -> ID:
        """Return the ID of the initial assembly.

        Errors if the ID is not set.
        """
        return self.init_assem.id_

    @property
    def entering_assem_id(self) -> ID | None:
        """Return the ID of the entering assembly, or None if there is none.

        Errors if the ID is not set.
        """
        if self.entering_assem is None:
            return None
        return self.entering_assem.id_

    @property
    def product_assem_id(self) -> ID:
        """Return the ID of the product assembly.

        Errors if the ID is not set.
        """
        return self.product_assem.id_

    @property
    def leaving_assem_id(self) -> ID | None:
        """Return the ID of the leaving assembly, or None if there is none.

        Errors if the ID is not set.
        """
        if self.leaving_assem is None:
            return None
        return self.leaving_assem.id_

    @property
    def mle(self) -> MLE:
        """Return the MLE (metal, leaving, entering binding sites) of the reaction."""
        return MLE(
            metal=self.metal_bs,
            leaving=self.leaving_bs,
            entering=self.entering_bs,
        )

    def is_inter(self) -> bool:
        """Return True if the reaction is an inter-molecular reaction."""
        return self.entering_assem is not None

    def is_intra(self) -> bool:
        """Return True if the reaction is an intra-molecular reaction."""
        return self.entering_assem is None

    @property
    def metal_kind(self) -> str:
        """Return the kind of the metal binding site."""
        return self.init_assem.get_component_kind_of_site(self.metal_bs)

    def copy_with(
            self,
            *,
            init_assem: Assembly | Missing = MISSING,
            entering_assem: Assembly | None | Missing = MISSING,
            product_assem: Assembly | Missing = MISSING,
            leaving_assem: Assembly | None | Missing = MISSING,
            metal_bs: BindingSite | Missing = MISSING,
            leaving_bs: BindingSite | Missing = MISSING,
            entering_bs: BindingSite | Missing = MISSING,
            duplicate_count: int | Missing = MISSING,
            id_: ID | None | Missing = MISSING,
            ) -> Self:
        """Return a copy of the reaction with optional modifications.

        - Fields not provided will default to the current values,
            except for the ID, which will be set to None if not provided.
        - Fields explicitly set to None will overwrite with None.
            (only applies to fields that can be None)

        If you want to copy the current ID, specify it explicitly,
        e.g., `copied = reaction.copy_with(id_=reaction.id_or_none)`.
        """
        return self.__class__(
            init_assem=default_if_missing(init_assem, self.init_assem),
            entering_assem=default_if_missing(entering_assem, self.entering_assem),
            product_assem=default_if_missing(product_assem, self.product_assem),
            leaving_assem=default_if_missing(leaving_assem, self.leaving_assem),
            metal_bs=default_if_missing(metal_bs, self.metal_bs),
            leaving_bs=default_if_missing(leaving_bs, self.leaving_bs),
            entering_bs=default_if_missing(entering_bs, self.entering_bs),
            duplicate_count=default_if_missing(duplicate_count, self.duplicate_count),
            id_=default_if_missing(id_, None),
        )

    def as_reaction_to_classify(self) -> 'ReactionToClassify':
        """Return a ReactionToClassify version of this reaction."""
        from nasap_net.reaction_classification import ReactionToClassify
        return ReactionToClassify.from_reaction(self)


def _assembly_to_id(assembly: Assembly | None) -> ID | None:
    """Return the ID of the assembly, or '??' if not set, or None if assembly
    is None.
    """
    if assembly is None:
        return None
    if assembly.id_or_none is None:
        # ID not set
        return '??'
    return assembly.id_or_none
