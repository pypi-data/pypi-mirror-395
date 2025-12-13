from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping
from copy import copy, deepcopy
from dataclasses import dataclass
from functools import wraps
from itertools import chain
from types import MappingProxyType
from typing import (Concatenate, Literal, ParamSpec, TypeVar, TypedDict,
                    overload)

import networkx as nx
import yaml

from .bindsite_id_converter import BindsiteIdConverter
from .component import Component

__all__ = ['Assembly', 'assembly_to_graph', 'assembly_to_rough_graph', 'find_free_bindsites']


# For type hint of the decorator
P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class AbsAuxEdge:
    """An auxiliary edge specified by absolute binding sites."""
    bindsite1: str
    bindsite2: str
    aux_type: str


class Assembly(yaml.YAMLObject):
    """A class to represent an assembly.
    
    An assembly is a group of components connected by bonds.
    """
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.Dumper
    yaml_tag = '!Assembly'
    yaml_flow_style = None
    
    def __init__(
            self, 
            comp_id_to_kind: Mapping[str, str] | None = None,
            bonds: (
                Iterable[tuple[str, str]] | Iterable[Iterable[str]] | None
                ) = None,
            name: str | None = None
            ) -> None:
        self._comp_id_to_kind = dict[str, str]()
        self._bonds = set[frozenset[str]]()
        self.name = name

        if comp_id_to_kind is not None:
            for component_id, component_kind in comp_id_to_kind.items():
                self.add_component(component_id, component_kind)
        if bonds is not None:
            for bindsite1, bindsite2 in bonds:
                self.add_bond(bindsite1, bindsite2)
            
        self._rough_g_cache: nx.Graph | None = None
        self._bindsite_to_connected_cache: dict[str, str] | None = None
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Assembly):
            return False
        return self.comp_id_to_kind == other.comp_id_to_kind and\
            self.bonds == other.bonds and self.name == other.name

    # Decorator
    # For type hint of the decorator, see the following link:
    # https://github.com/microsoft/pyright/issues/6472
    @staticmethod
    def _clear_g_caches(func: Callable[Concatenate[Assembly, P], R]
            ) -> Callable[Concatenate[Assembly, P], R]:
        """Decorator to clear the cache of the graph snapshot before
        calling the method."""
        @wraps(func)
        def wrapper(self: Assembly, *args: P.args, **kwargs: P.kwargs):
            self._rough_g_cache = None
            self._bindsite_to_connected_cache = None
            return func(self, *args, **kwargs)
        return wrapper

    # ============================================================
    # Properties (read-only)
    # ============================================================

    @property
    def comp_id_to_kind(self) -> MappingProxyType[str, str]:
        """Return a read-only view of the components.
        
        The returned object can be used like a dictionary, but it is
        read-only. Changes to the original assembly will be reflected
        in the returned object.
        """
        return MappingProxyType(self._comp_id_to_kind)
    
    @property
    def component_ids(self) -> set[str]:
        return set(self._comp_id_to_kind.keys())

    @property
    def component_kinds(self) -> set[str]:
        return set(self._comp_id_to_kind.values())
    
    @property
    def bonds(self) -> set[frozenset[str]]:
        return self._bonds.copy()
    
    @property
    def bindsite_to_connected(self) -> dict[str, str]:
        if getattr(self, '_bindsite_to_connected', None) is None:
            self._bindsite_to_connected_cache =\
                self.create_bindsite_to_connected()
        assert self._bindsite_to_connected_cache is not None
        return copy(self._bindsite_to_connected_cache)
    
    def create_bindsite_to_connected(self) -> dict[str, str]:
        d = {}
        for bond in self._bonds:
            bindsite1, bindsite2 = bond
            d[bindsite1] = bindsite2
            d[bindsite2] = bindsite1
        return d
    
    def g_snapshot(
            self, component_structures: Mapping[str, Component]
            ) -> nx.Graph:
        """Returns a snapshot of the assembly graph.
        
        The snapshot is a deep copy of the assembly graph. Therefore,
        any modification to the snapshot will not affect the assembly.
        """
        # Prevent the user from modifying the assembly.
        return self._to_graph(component_structures)
    
    @property
    def rough_g_snapshot(self) -> nx.Graph:
        """Returns a rough graph of the assembly."""
        if getattr(self, '_rough_g_cache', None) is None:
            self._rough_g_cache = self._to_rough_graph()
        return deepcopy(self._rough_g_cache)
    
    # ============================================================
    # Methods to modify the assembly (using relative names)
    # ============================================================
    
    @_clear_g_caches
    def add_component(
            self, component_id: str, component_kind: str) -> None:
        """Add a component to the assembly.
        
        Note: No bond is added between the component and the assembly.
        The user should add bonds between the component and the assembly
        if necessary.
        """
        self._comp_id_to_kind[component_id] = component_kind

    @_clear_g_caches
    def remove_component(self, component_id: str) -> None:
        del self._comp_id_to_kind[component_id]
    
    @_clear_g_caches
    def add_bond(self, bindsite1: str, bindsite2: str) -> None:
        """Add a bond to the assembly."""
        id_converter = BindsiteIdConverter()
        comp1, rel1 = id_converter.global_to_local(bindsite1)
        comp2, rel2 = id_converter.global_to_local(bindsite2)
        for comp in [comp1, comp2]:
            if comp not in self._comp_id_to_kind:
                raise ValueError(
                    f'The component "{comp}" does not exist in the assembly.')
        self._bonds.add(frozenset([bindsite1, bindsite2]))

    @_clear_g_caches
    def remove_bond(
            self, bindsite1: str, bindsite2: str) -> None:
        """Remove a bond from the assembly."""
        self._bonds.remove(frozenset([bindsite1, bindsite2]))

    # ============================================================
    # Methods to make multiple modifications at once
    # ============================================================

    def add_components(self, components: Iterable[tuple[str, str]]) -> None:
        for component_id, component_kind in components:
            self.add_component(component_id, component_kind)

    def remove_components(self, component_ids: Iterable[str]) -> None:
        for component_id in component_ids:
            self.remove_component(component_id)

    def add_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> None:
        for bindsite1, bindsite2 in bonds:
            self.add_bond(bindsite1, bindsite2)

    def remove_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> None:
        for bindsite1, bindsite2 in bonds:
            self.remove_bond(bindsite1, bindsite2)
    
    # ============================================================
    # Methods to relabel the assembly
    # ============================================================
    
    # `@overload` decorator is just for type hinting;
    # it does not affect the behavior of the method.
    @overload
    @_clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: Literal[True] = True) -> Assembly:
        ...
    @overload
    @_clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: Literal[False]) -> None:
        ...
    @_clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: bool = True) -> Assembly | None:
        if copy:
            assem = deepcopy(self)
        else:
            assem = self

        id_converter = BindsiteIdConverter()

        new_components = {}
        for old_id, component in assem._comp_id_to_kind.items():
            new_id = mapping.get(old_id, old_id)
            new_components[new_id] = component
        
        new_bonds = set()
        for bindsite1, bindsite2 in assem._bonds:
            comp1, rel1 = id_converter.global_to_local(bindsite1)
            comp2, rel2 = id_converter.global_to_local(bindsite2)
            new_bindsite1 = id_converter.local_to_global(
                mapping.get(comp1, comp1), rel1)
            new_bindsite2 = id_converter.local_to_global(
                mapping.get(comp2, comp2), rel2)
            new_bonds.add(frozenset([new_bindsite1, new_bindsite2]))

        assem._comp_id_to_kind = new_components
        assem._bonds = new_bonds
        assem._rough_g_cache = None

        # TODO: Check if the new component IDs are valid.
        
        return assem

    # ============================================================
    # Helper methods
    # ============================================================

    @overload
    def get_connected_bindsite(
            self, bindsite: str, error_if_free: Literal[False] = False
            ) -> str | None: ...
    @overload
    def get_connected_bindsite(
            self, bindsite: str, error_if_free: Literal[True]
            ) -> str: ...
    def get_connected_bindsite(
            self, bindsite, error_if_free=False):
        """Get the connected binding site of the binding site.
        
        Parameters
        ----------
        bindsite : str
            The binding site.
        error_if_free : bool, optional
            If True, raise an error if the binding site is free.
            It is useful when the user expects the binding site to be
            connected.

        Returns
        -------
        str | None
            The connected binding site. If the binding site is free,
            and `error_if_free` is False, return None.
        """
        connected = self.bindsite_to_connected.get(bindsite)
        if connected is None and error_if_free:
            raise ValueError(
                f'The binding site "{bindsite}" is free.')
        return connected
    
    def is_free_bindsite(self, bindsite: str) -> bool:
        return self.get_connected_bindsite(bindsite) is None
    
    def get_component_kind(self, component_id: str) -> str:
        return self._comp_id_to_kind[component_id]
    
    def get_component_kind_of_core(self, core: str) -> str:
        id_converter = BindsiteIdConverter()
        comp_id, rel = id_converter.global_to_local(core)
        return self.get_component_kind(comp_id)
    
    def get_component_kind_of_bindsite(self, bindsite: str) -> str:
        id_converter = BindsiteIdConverter()
        comp_id, rel = id_converter.global_to_local(bindsite)
        return self.get_component_kind(comp_id)
    
    def deepcopy(self) -> Assembly:
        return deepcopy(self)
    
    def get_core_of_the_component(self, component_id: str) -> str:
        id_converter = BindsiteIdConverter()
        return id_converter.local_to_global(component_id, 'core')

    def iter_all_cores(self) -> Iterator[str]:
        id_converter = BindsiteIdConverter()
        for comp_id, comp_kind in self.comp_id_to_kind.items():
            yield id_converter.local_to_global(comp_id, 'core')
    
    def get_all_bindsites(
            self, component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Get all the binding sites in the assembly."""
        # TODO: Consider yielding the binding sites instead of returning a set.
        id_converter = BindsiteIdConverter()
        all_bindsites = set()
        for comp_id, comp_kind in self.comp_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for bindsite in comp_struct.binding_sites:
                all_bindsites.add(id_converter.local_to_global(comp_id, bindsite))
        return all_bindsites

    def iter_aux_edges(
            self, component_structures: Mapping[str, Component]
            ) -> Iterator[AbsAuxEdge]:
        id_converter = BindsiteIdConverter()
        for comp_id, comp_kind in self.comp_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for rel_aux_edge in comp_struct.aux_edges:
                yield AbsAuxEdge(
                    id_converter.local_to_global(
                        comp_id, rel_aux_edge.local_binding_site1),
                    id_converter.local_to_global(
                        comp_id, rel_aux_edge.local_binding_site2),
                    rel_aux_edge.aux_kind)

    def get_bindsites_of_component(
            self, component_id: str, 
            component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Get the binding sites of the component."""
        id_converter = BindsiteIdConverter()
        comp_kind = self.get_component_kind(component_id)
        comp_struct = component_structures[comp_kind]
        return {
            id_converter.local_to_global(component_id, bindsite)
            for bindsite in comp_struct.binding_sites}
    
    def get_all_bindsites_of_kind(
            self, component_kind: str,
            component_structures: Mapping[str, Component],
            ) -> Iterator[str]:
        for comp_id, comp in self.comp_id_to_kind.items():
            if comp == component_kind:
                yield from self.get_bindsites_of_component(
                    comp_id, component_structures)

    def find_free_bindsites(
            self, component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Find free bindsites."""
        id_converter = BindsiteIdConverter()
        all_bindsites = {
            id_converter.local_to_global(comp_id, bindsite)
            for comp_id, comp_kind in self.comp_id_to_kind.items()
            for bindsite in component_structures[comp_kind].binding_sites
        }
        connected_bindsites = chain(*self.bonds)
        free_bindsites = all_bindsites - set(connected_bindsites)
        return free_bindsites

    # ============================================================
    # Methods to convert the assembly to graphs
    # ============================================================

    def _to_graph(
            self, component_kinds: Mapping[str, Component]
            ) -> nx.Graph:
        return assembly_to_graph(self, component_kinds)

    def _to_rough_graph(self) -> nx.Graph:
        id_converter = BindsiteIdConverter()
        G = nx.MultiGraph()
        for comp_id, comp_kind in self.comp_id_to_kind.items():
            G.add_node(comp_id, component_kind=comp_kind)
        for bindsite1, bindsite2 in self.bonds:
            comp1, rel1 = id_converter.global_to_local(bindsite1)
            comp2, rel2 = id_converter.global_to_local(bindsite2)
            G.add_edge(comp1, comp2, bindsites={comp1: rel1, comp2: rel2})
        return G

    @classmethod
    def bond_to_rough_bond(
            cls, bond: Iterable[str]) -> list[str]:
        # TODO: Move this method to a separate module.
        id_converter = BindsiteIdConverter()
        bindsites = list(bond)
        comp1, rel1 = id_converter.global_to_local(bindsites[0])
        comp2, rel2 = id_converter.global_to_local(bindsites[1])
        return [comp1, comp2]
    
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return cls(
            data.get('comp_id_to_kind', None),
            data.get('bonds', None),
            data.get('name', None))
    
    @classmethod
    def to_yaml(cls, dumper, data: Assembly):
        DataDict = TypedDict(
            'DataDict', {
                'comp_id_to_kind': dict[str, str],
                'bonds': list[list[str]],
                'name': str},
            total=False)
        data_dict: DataDict = {}
        if data.comp_id_to_kind:
            data_dict['comp_id_to_kind'] = dict(data.comp_id_to_kind)
        if data.bonds:
            data_dict['bonds'] = sorted(sorted(bond) for bond in data.bonds)
        if data.name:
            data_dict['name'] = data.name
        return dumper.represent_mapping(
            cls.yaml_tag, data_dict, flow_style=cls.yaml_flow_style)


def assembly_to_graph(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        ) -> nx.Graph:
    G = nx.Graph()
    for comp_id, comp_kind in assembly.comp_id_to_kind.items():
        comp_structure = component_structures[comp_kind]
        add_component_to_graph(G, comp_id, comp_kind, comp_structure)
    for bond in assembly.bonds:
        G.add_edge(*bond)
    return G


def add_component_to_graph(
        g: nx.Graph,
        component_id: str, component_kind: str,
        component_structure: Component,
        ) -> None:
    # Add the core node
    id_converter = BindsiteIdConverter()
    core_abs = id_converter.local_to_global(component_id, 'core')
    g.add_node(
        core_abs, core_or_bindsite='core', component_kind=component_kind)
    
    # Add the binding sites
    for bindsite in component_structure.binding_sites:
        bindsite_abs = id_converter.local_to_global(component_id, bindsite)
        g.add_node(bindsite_abs, core_or_bindsite='bindsite')
        g.add_edge(core_abs, bindsite_abs)
    
    # Add the auxiliary edges
    for aux_edge in component_structure.aux_edges:
        bs1_abs = id_converter.local_to_global(component_id, aux_edge.local_binding_site1)
        bs2_abs = id_converter.local_to_global(component_id, aux_edge.local_binding_site2)
        g.add_edge(bs1_abs, bs2_abs, aux_type=aux_edge.aux_kind)
