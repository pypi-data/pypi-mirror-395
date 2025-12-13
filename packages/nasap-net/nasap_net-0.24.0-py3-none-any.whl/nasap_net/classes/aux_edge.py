from typing import Any

import yaml

import nasap_net as rx
from nasap_net.utils import FrozenUnorderedPair

from .validations import (validate_name_of_aux_type,
                          validate_name_of_binding_site)

__all__ = ['AuxEdge']


class AuxEdge(yaml.YAMLObject):
    """An auxiliary edge between two binding sites. (Immutable)"""
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.Dumper
    yaml_tag = '!AuxEdge'
    yaml_flow_style = None

    def __init__(
            self, local_binding_site1: str, local_binding_site2: str, 
            aux_kind: str):
        """Initialize an auxiliary edge.

        Note that the order of the binding sites does not matter,
        i.e., AuxEdge('a', 'b', 'cis') is the same as AuxEdge('b', 'a', 'cis').

        Parameters
        ----------
        local_binding_site1 : str
            The local id of the first binding site.
        local_binding_site2 : str
            The local id of the second binding site.
        aux_kind : str
            The auxiliary type.

        Note
        ----
        The order of the binding sites does not matter.

        Raises
        ------
        ValueError
            If the two binding sites are the same.
        """
        validate_name_of_binding_site(local_binding_site1)
        validate_name_of_binding_site(local_binding_site2)
        if local_binding_site1 == local_binding_site2:
            raise ValueError(
                'The two binding sites should be different.')
        self._binding_sites = FrozenUnorderedPair[str](
            local_binding_site1, local_binding_site2)

        validate_name_of_aux_type(aux_kind)
        self._aux_kind = aux_kind
    
    @property
    def local_binding_site1(self) -> str:
        return self._binding_sites.first
    
    @property
    def local_binding_site2(self) -> str:
        return self._binding_sites.second
    
    @property
    def binding_sites(self) -> FrozenUnorderedPair[str]:
        return self._binding_sites

    @property
    def aux_kind(self) -> str:
        return self._aux_kind

    def __hash__(self) -> int:
        return hash((self.binding_sites, self.aux_kind))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AuxEdge):
            return False
        return (
            self.binding_sites == other.binding_sites and
            self.aux_kind == other.aux_kind)
    
    def __lt__(self, other: 'AuxEdge') -> bool:
        return (sorted(self.binding_sites), self.aux_kind) < (
            sorted(other.binding_sites), other.aux_kind)

    def __repr__(self) -> str:
        return f'AuxEdge({self.local_binding_site1!r}, {self.local_binding_site2!r}, {self.aux_kind!r})'
    
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return AuxEdge(
            data['binding_sites'][0], data['binding_sites'][1], data['aux_kind'])

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(
            cls.yaml_tag, {
            'binding_sites': sorted(data.binding_sites),
            'aux_kind': data.aux_kind},
            flow_style=cls.yaml_flow_style)
