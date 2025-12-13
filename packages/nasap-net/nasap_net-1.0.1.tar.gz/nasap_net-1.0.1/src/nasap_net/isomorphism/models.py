from dataclasses import dataclass
from typing import Mapping

from frozendict import frozendict

from nasap_net.models import BindingSite
from nasap_net.types import ID


@dataclass(frozen=True, init=False)
class Isomorphism:
    comp_id_mapping: frozendict[ID, ID]
    binding_site_mapping: frozendict[BindingSite, BindingSite]

    def __init__(
            self,
            comp_id_mapping: Mapping[ID, ID],
            binding_site_mapping: Mapping[BindingSite, BindingSite]
    ) -> None:
        object.__setattr__(
            self, 'comp_id_mapping', frozendict(comp_id_mapping))
        object.__setattr__(
            self, 'binding_site_mapping', frozendict(binding_site_mapping))
