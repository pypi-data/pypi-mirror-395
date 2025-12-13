from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypeVar

from nasap_net.io.assemblies.lib import dump_components, \
    dump_semi_light_assemblies
from nasap_net.io.assemblies.semi_light_assembly import \
    convert_assemblies_to_semi_light_ones
from nasap_net.models import Assembly
from nasap_net.types import ID

_T = TypeVar('_T', bound=ID)

def dump_assemblies_to_str(assemblies: Iterable[Assembly]) -> str:
    """Dump assemblies and components into a YAML string."""
    dumped = _dump_separately(assemblies)
    return '---\n'.join([dumped.components, dumped.assemblies])


@dataclass(frozen=True)
class _Dumped:
    assemblies: str
    components: str


def _dump_separately(
        assemblies: Iterable[Assembly],
        ) -> _Dumped:
    assembly_list = list(assemblies)
    assembly_map = dict(enumerate(assembly_list))
    res = convert_assemblies_to_semi_light_ones(assembly_map)

    res_assemblies = [
        res.semi_light_assemblies[id_]
        for id_ in sorted(res.semi_light_assemblies.keys())
    ]

    return _Dumped(
        assemblies=dump_semi_light_assemblies(
            res_assemblies
        ),
        components=dump_components(
            dict(sorted(res.components.items())),
        ),
    )
