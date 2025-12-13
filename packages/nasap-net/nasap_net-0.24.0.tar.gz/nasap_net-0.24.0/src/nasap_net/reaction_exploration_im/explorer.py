import itertools
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from nasap_net.binding_site_equivalence import \
    extract_unique_binding_site_combs
from nasap_net.models import Assembly, BindingSite, MLE, MLEKind, \
    Reaction
from nasap_net.reaction_performance import perform_inter_reaction, \
    perform_intra_reaction, reindex_components_for_inter_reaction


class ReactionExplorer(ABC):
    def explore(self) -> Iterator[Reaction]:
        mles = self._iter_mles()
        unique_mles = self._get_unique_mles(mles)
        for mle in unique_mles:
            yield self._perform_reaction(mle)

    @abstractmethod
    def _iter_mles(self) -> Iterator[MLE]:
        pass

    @abstractmethod
    def _get_unique_mles(self, mles: Iterable[MLE]) -> Iterator[MLE]:
        pass

    @abstractmethod
    def _perform_reaction(self, mle: MLE) -> Reaction:
        pass


@dataclass(frozen=True)
class IntraReactionExplorer(ReactionExplorer):
    """Class to explore intra-molecular reactions within an assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly in which intra-molecular reactions are to be explored.
    mle_kind : MLEKind
        The kinds of components involved in the reaction:
            - `mle_kind.metal`: The component kind of the metal binding site.
            - `mle_kind.leaving`: The component kind of the leaving binding site.
            - `mle_kind.entering`: The component kind of the entering binding site.

    Methods
    -------
    explore() -> Iterator[Reaction]
        Explore and yield all possible intra-molecular reactions within the
        assembly based on the specified MLE kind.
    """
    assembly: Assembly
    mle_kind: MLEKind

    def _iter_mles(self) -> Iterator[MLE]:
        """Get all possible MLEs for intra-molecular reactions in an assembly.

        This function generates all MLEs (combinations of metal binding sites,
        leaving binding sites, and entering binding sites) for intra-molecular
        reactions within a given assembly based on the specified component kinds.

        Returned MLEs meet the following conditions:
          - The metal binding site and leaving binding site are connected to each other.
          - The component kind of the metal binding site is `mle_kind.metal`.
          - The component kind of the leaving binding site is `mle_kind.leaving`.
          - The entering binding site is free and has the component kind `mle_kind.entering`.
        """
        ml_pairs = _enum_ml_pair(
            self.assembly,
            metal_kind=self.mle_kind.metal, leaving_kind=self.mle_kind.leaving)

        entering_sites = self.assembly.find_sites(
            has_bond=False, component_kind=self.mle_kind.entering)

        for (metal, leaving), entering in itertools.product(
                ml_pairs, entering_sites):

            if forms_parallel_bond(self.assembly, entering, leaving, metal):
                # Parallel bond formation is not allowed
                continue

            yield MLE(metal, leaving, entering)

    def _get_unique_mles(self, mles: Iterable[MLE]) -> Iterator[MLE]:
        unique_mle_trios = extract_unique_binding_site_combs(
            [(mle.metal, mle.leaving, mle.entering) for mle in mles],
             self.assembly)
        for unique_mle in unique_mle_trios:
            metal, leaving, entering = unique_mle.site_comb
            yield MLE(
                metal, leaving, entering,
                duplication=unique_mle.duplication)

    def _perform_reaction(self, mle: MLE) -> Reaction:
        product, leaving = perform_intra_reaction(
            assembly=self.assembly,
            mle=mle
        )
        return Reaction(
            init_assem=self.assembly,
            entering_assem=None,
            product_assem=product,
            leaving_assem=leaving,
            metal_bs=mle.metal,
            leaving_bs=mle.leaving,
            entering_bs=mle.entering,
            duplicate_count=mle.duplication
        )


@dataclass(frozen=True)
class InterReactionExplorer(ReactionExplorer):
    """Class to explore inter-molecular reactions between two assemblies.

    Parameters
    ----------
    init_assembly : Assembly
        The initial assembly. This assembly contains the metal and leaving
        binding sites.
    entering_assembly : Assembly
        The entering assembly. This assembly contains the entering binding site.
    mle_kind : MLEKind
        The kinds of components involved in the reaction:
            - `mle_kind.metal`: The component kind of the metal binding site.
            - `mle_kind.leaving`: The component kind of the leaving binding site.
            - `mle_kind.entering`: The component kind of the entering binding site.

    Methods
    -------
    explore() -> Iterator[Reaction]
        Explore and yield all possible inter-molecular reactions between the
        two assemblies based on the specified MLE kind.
    """
    init_assembly: Assembly
    entering_assembly: Assembly
    mle_kind: MLEKind

    def _iter_mles(self) -> Iterator[MLE]:
        """Get all possible MLEs for inter-molecular reactions between two assemblies.

        This function generates all MLEs (combinations of metal binding sites,
        leaving binding sites, and entering binding sites) for inter-molecular
        reactions between an initial assembly and an entering assembly
        based on the specified component kinds.

        Returned MLEs meet the following conditions:
          - The metal binding site and leaving binding site are connected to each other.
          - The component kind of the metal binding site is `mle_kind.metal`.
          - The component kind of the leaving binding site is `mle_kind.leaving`.
          - The entering binding site is free and has the component kind `mle_kind.entering`.
        """
        ml_pair = _enum_ml_pair(
            self.init_assembly,
            metal_kind=self.mle_kind.metal, leaving_kind=self.mle_kind.leaving)

        entering_sites = self.entering_assembly.find_sites(
            has_bond=False, component_kind=self.mle_kind.entering)

        for (metal, leaving), entering in itertools.product(
                ml_pair, entering_sites):
            yield MLE(metal, leaving, entering)

    def _get_unique_mles(self, mles: Iterable[MLE]) -> Iterator[MLE]:
        mles1, mles2 = itertools.tee(mles)
        unique_ml_pairs = extract_unique_binding_site_combs(
            [(mle.metal, mle.leaving) for mle in mles1], self.init_assembly)
        unique_entering_sites = extract_unique_binding_site_combs(
            [(mle.entering,) for mle in mles2], self.entering_assembly)
        for unique_ml, unique_e in itertools.product(
                unique_ml_pairs, unique_entering_sites):
            metal, leaving = unique_ml.site_comb
            (entering,) = unique_e.site_comb
            yield MLE(
                metal, leaving, entering,
                duplication=unique_ml.duplication * unique_e.duplication)

    def _perform_reaction(self, mle: MLE) -> Reaction:
        renamed = reindex_components_for_inter_reaction(
            self.init_assembly, self.entering_assembly, mle
        )

        product, leaving = perform_inter_reaction(
            init_assem=renamed.init_assembly,
            entering_assem=renamed.entering_assembly,
            mle=renamed.mle,
        )

        # Double the duplication count if both assemblies are the same.
        # This is because the frequency of "A + A" is twice that of "A + B".
        if self.init_assembly == self.entering_assembly:
            dup = mle.duplication * 2
        else:
            dup = mle.duplication

        return Reaction(
            init_assem=self.init_assembly,
            entering_assem=self.entering_assembly,
            product_assem=product,
            leaving_assem=leaving,
            metal_bs=mle.metal,
            leaving_bs=mle.leaving,
            entering_bs=mle.entering,
            duplicate_count=dup
        )


def _enum_ml_pair(
        assem: Assembly, metal_kind: str, leaving_kind: str
        ) -> set[tuple[BindingSite, BindingSite]]:
    ml_pair: set[tuple[BindingSite, BindingSite]] = set()
    for bond in assem.bonds:
        site1, site2 = bond.sites
        kind1 = assem.get_component_kind_of_site(site1)
        kind2 = assem.get_component_kind_of_site(site2)
        if (kind1, kind2) == (metal_kind, leaving_kind):
            ml_pair.add((site1, site2))
        elif (kind1, kind2) == (leaving_kind, metal_kind):
            ml_pair.add((site2, site1))
    return ml_pair


def forms_parallel_bond(
        assembly: Assembly,
        entering: BindingSite,
        leaving: BindingSite,
        metal: BindingSite
) -> bool:
    """Return True if the reaction would form a parallel bond."""
    if not assembly.has_bond_between_components(
            metal.component_id, entering.component_id
    ):
        return False
    if leaving.component_id == entering.component_id:
        return False
    return True
