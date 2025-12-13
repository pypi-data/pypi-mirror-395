from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar, overload

import yaml

import nasap_net as rx

__all__ = ['FrozenUnorderedPair']


T = TypeVar('T', bound=Hashable)


class FrozenUnorderedPair(Generic[T], yaml.YAMLObject):
    """A frozen unordered pair of two hashable elements."""
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.Dumper
    yaml_tag = '!FrozenUnorderedPair'
    yaml_flow_style = None
    
    @overload
    def __init__(self, first: T, second: T) -> None: ...
    @overload
    def __init__(self, pair: Iterable[T]) -> None: ...
    def __init__(self, *args):
        # TODO: Add type validation.
        if len(args) == 1:
            pair = tuple(args[0])
            if len(pair) != 2:
                raise ValueError('The pair should have two elements.')
            self.__pair = pair
        elif len(args) == 2:
            self.__pair = tuple(args)
        else:
            raise ValueError('The pair should have two elements.')

    # TODO: Remove this property.
    @property
    def first(self) -> T:
        return self.__pair[0]
    
    # TODO: Remove this property.
    @property
    def second(self) -> T:
        return self.__pair[1]
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrozenUnorderedPair):
            return False
        return set(self.__pair) == set(other.__pair)
    
    def __hash__(self) -> int:
        return hash(frozenset(self.__pair))
    
    def __repr__(self) -> str:
        return f'FrozenUnorderedPair({self.first!r}, {self.second!r})'
    
    def __iter__(self):
        return iter(self.__pair)

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_sequence(node, deep=True)
        return FrozenUnorderedPair(data)
    
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_sequence(
            cls.yaml_tag, sorted(data), flow_style=cls.yaml_flow_style)
