from collections.abc import Iterable
from typing import cast

import yaml

from ..aux_edge import AuxEdge
from ..validations import validate_name_of_binding_site
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['Component']


class Component(yaml.YAMLObject):
    """A component of an assembly. (Immutable)"""
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.Dumper
    yaml_tag = '!Component'
    yaml_flow_style = None

    def __init__(
            self,
            binding_sites: Iterable[str],
            aux_edges: (
                Iterable[AuxEdge] 
                | Iterable[tuple[str, str, str]] | None
                ) = None):
        """
        Parameters
        ----------
        component_kind : str
            The component type, e.g., 'M', 'L', 'L1', 'X', etc.
        binding_sites : Iterable[str]
            The binding sites. Each binding site should be a string.
        aux_edges : Mapping[tuple[str, str], str], optional
            Mapping of auxiliary edges. The keys are tuples of two binding
            sites, and the values are the auxiliary kinds. The binding sites
            should be in the binding_sites.
            Duplicate pairs of binding sites raise an error regardless of the
            order of the binding sites.
        """
        for binding_site in binding_sites:
            validate_name_of_binding_site(binding_site)
        self._binding_sites = frozenset(binding_sites)

        if aux_edges is None:
            self._aux_edges = frozenset[AuxEdge]()
        elif all(isinstance(edge, AuxEdge) for edge in aux_edges):
            aux_edges = cast(Iterable[AuxEdge], aux_edges)
            self._aux_edges = frozenset(aux_edges)
        else:
            aux_edges = cast(Iterable[tuple[str, str, str]], aux_edges)
            self._aux_edges = frozenset(
                {AuxEdge(*edge) for edge in aux_edges})

        check_bindsites_of_aux_edges_exists(
            self._aux_edges, self._binding_sites)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Component):
            return False
        return (
            self.binding_sites == value.binding_sites
            and self.aux_edges == value.aux_edges)
    
    def __repr__(self) -> str:
        if not self.aux_edges:
            return f'Component({sorted(self.binding_sites)!r})'
        return (
            f'Component({sorted(self.binding_sites)!r}, '
            f'{sorted(self.aux_edges)!r})'
            )
    
    @property
    def binding_sites(self) -> set[str]:
        return set(self._binding_sites)

    @property
    def aux_edges(self) -> set[AuxEdge]:
        return set(self._aux_edges)
    
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        binding_sites = data['binding_sites']
        aux_edges = data.get('aux_edges', None)
        return cls(binding_sites, aux_edges)

    @classmethod
    def to_yaml(cls, dumper, data):
        data_dict = {'binding_sites': sorted(data.binding_sites)}
        if data.aux_edges:
            data_dict['aux_edges'] = sorted(
                data.aux_edges,
                key=lambda edge: sorted(edge.binding_sites))
        return dumper.represent_mapping(
            cls.yaml_tag, data_dict,
            flow_style=cls.yaml_flow_style)
