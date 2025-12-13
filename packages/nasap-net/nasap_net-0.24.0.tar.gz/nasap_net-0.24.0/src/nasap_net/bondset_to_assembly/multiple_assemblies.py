from collections.abc import Iterable, Iterator, Mapping

from nasap_net import Assembly

from .single_assembly import convert_bondset_to_assembly

__all__ = ['convert_bondsets_to_assemblies']


def convert_bondsets_to_assemblies(
        bondsets: Iterable[frozenset[str]],
        components: Mapping[str, str],
        bond_id_to_bindsites: dict[str, frozenset[str]]
        ) -> Iterator[Assembly]:
    """Converts the connected bonds to graphs."""

    for bondset in bondsets:
        yield convert_bondset_to_assembly(
            set(bondset), components, bond_id_to_bindsites)