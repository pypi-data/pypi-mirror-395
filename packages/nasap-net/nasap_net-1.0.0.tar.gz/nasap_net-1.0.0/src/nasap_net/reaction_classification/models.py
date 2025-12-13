from functools import cached_property
from typing import Self

from nasap_net.models import Assembly, Reaction
from nasap_net.reaction_pairing import generate_sample_rev_reaction
from .connection_count import get_connection_count_of_kind
from .ring_breaking_size import get_min_breaking_ring_size
from .ring_formation_size import get_min_forming_ring_size
from .temp_ring_formation import get_min_forming_ring_size_including_temporary


class ReactionToClassify(Reaction):
    """Dataclass representing a reaction to classify."""

    _is_sample_rev: bool

    def __init__(
            self,
            init_assem,
            entering_assem,
            product_assem,
            leaving_assem,
            metal_bs,
            leaving_bs,
            entering_bs,
            duplicate_count=None,
            id_=None,
            _is_sample_rev=False,
    ):
        super().__init__(
            init_assem=init_assem,
            entering_assem=entering_assem,
            product_assem=product_assem,
            leaving_assem=leaving_assem,
            metal_bs=metal_bs,
            leaving_bs=leaving_bs,
            entering_bs=entering_bs,
            duplicate_count=duplicate_count,
            id_=id_,
        )
        object.__setattr__(self, '_is_sample_rev', _is_sample_rev)

    @property
    def metal_kind(self) -> str:
        """Return the kind of the metal binding site."""
        return self.init_assem.get_component_kind_of_site(self.metal_bs)

    @property
    def leaving_kind(self) -> str:
        """Return the kind of the leaving binding site."""
        return self.init_assem.get_component_kind_of_site(self.leaving_bs)

    @property
    def entering_kind(self) -> str:
        """Return the kind of the entering binding site."""
        return self.assem_with_entering_bs.get_component_kind_of_site(self.entering_bs)

    def forms_ring(self) -> bool:
        """Whether this reaction forms any rings."""
        return self.forming_ring_size is not None

    def breaks_ring(self) -> bool:
        """Whether this reaction breaks any rings."""
        return self.breaking_ring_size is not None

    @cached_property
    def forming_ring_size(self) -> int | None:
        """The minimum size of rings formed in this reaction,
        or None if no rings are formed.
        """
        return get_min_forming_ring_size(self)

    @cached_property
    def breaking_ring_size(self) -> int | None:
        """The minimum size of rings broken in this reaction,
        or None if no rings are broken.
        """
        return get_min_breaking_ring_size(self)

    @cached_property
    def forming_ring_size_including_temporary(self) -> int | None:
        """The minimum size of rings formed in this reaction,
        including temporary rings, or None if no rings are formed.

        Notes
        -----
        "Temporary ring" includes rings that may be broken later in the reaction.
        Example:
        X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
        metal_bs = M0(1), leaving_bs = L0(0), entering_bs = L1(1)
        This reaction temporarily forms a ring of size 2, even though the ring is broken
        when L0 leaves.
        """
        return get_min_forming_ring_size_including_temporary(self)

    @cached_property
    def init_ligand_count_on_metal(self) -> int:
        """Return the number of ligands bound to the metal before reaction."""
        return get_connection_count_of_kind(
            assembly=self.init_assem,
            source_component_id=self.metal_bs.component_id,
            target_kind=self.entering_kind,
        )

    @cached_property
    def init_metal_count_on_ligand(self) -> int:
        """Return the number of metals bound to the entering ligand before reaction."""
        return get_connection_count_of_kind(
            assembly=self.assem_with_entering_bs,
            source_component_id=self.entering_bs.component_id,
            target_kind=self.metal_kind,
        )

    @cached_property
    def sample_rev(self) -> 'ReactionToClassify | None':
        """Return the reverse reaction.

        Returns None if this reaction is already a sample reverse reaction,
        to prevent infinite recursion.
        """
        if self._is_sample_rev:
            return None
        reverse_reaction = generate_sample_rev_reaction(self)
        # Create reverse reaction with _is_sample_rev=True
        result = ReactionToClassify.from_reaction(reverse_reaction)
        object.__setattr__(result, '_is_sample_rev', True)
        return result

    @property
    def assem_with_entering_bs(self) -> Assembly:
        """Return the assembly that contains the entering binding site."""
        if self.is_inter():
            return self.entering_assem_strict
        return self.init_assem

    @classmethod
    def from_reaction(cls, reaction: Reaction) -> Self:
        """Create a ReactionToClassify from a Reaction."""
        return cls(
            init_assem=reaction.init_assem,
            entering_assem=reaction.entering_assem,
            product_assem=reaction.product_assem,
            leaving_assem=reaction.leaving_assem,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
            _is_sample_rev=False,
        )
