import pytest

from nasap_net.io.assemblies.lib import dump_components, load_components
from nasap_net.models import AuxEdge, Component


@pytest.fixture
def components():
    return {
        'X': Component(kind='X', sites=[0]),
        'M(aux)': Component(
            kind='M(aux)', sites=[0, 1, 2],
            aux_edges=[AuxEdge(0, 1), AuxEdge(0, 2, kind='cis')]
        ),
    }

@pytest.fixture
def dumped_components():
    return """X: !Component
  kind: X
  sites: [0]
M(aux): !Component
  kind: M(aux)
  sites: [0, 1, 2]
  aux_edges:
  - sites: [0, 1]
  - sites: [0, 2]
    kind: cis
"""


def test_dump_components(components, dumped_components):
    dumped = dump_components(components)
    assert dumped == dumped_components


def test_load_components(components, dumped_components):
    loaded = load_components(dumped_components)
    assert loaded == components


def test_round_trip(components, dumped_components):
    dumped = dump_components(components)
    loaded = load_components(dumped)
    assert loaded == components
