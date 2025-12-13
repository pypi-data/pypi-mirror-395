from dataclasses import FrozenInstanceError

import pytest

from nasap_net.models import Component


def test_component():
    M = Component(kind='M', sites=['a', 'b'])
    assert M.kind == 'M'
    assert M.site_ids == frozenset({'a', 'b'})


def test_component_immutability():
    M = Component(kind='M', sites=['a', 'b'])
    with pytest.raises(FrozenInstanceError):
        M.kind = 'M2'  # type: ignore[attr-defined, misc]
    with pytest.raises(FrozenInstanceError):
        M.site_ids = frozenset({'c'})  # type: ignore[attr-defined, misc]


def test___repr__():
    M = Component(kind='M', sites=[0, 1])
    assert repr(M) == "<Component kind='M', site_ids=[0, 1]>"


def test___repr___with_aux_edges():
    from nasap_net.models import AuxEdge

    M = Component(
        kind='M',
        sites=[0, 1, 2],
        aux_edges=[AuxEdge(0, 1, 'cis'), AuxEdge(1, 2)],
    )
    assert repr(M) == (
        "<Component kind='M', site_ids=[0, 1, 2], "
        "aux_edges=[(0, 1, 'cis'), (1, 2)]>"
    )
