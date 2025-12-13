import pytest

from nasap_net.assembly_enumeration.lib.fragment_enumeration import \
    enumerate_fragments
from nasap_net.models import Assembly, AuxEdge, Bond, Component


@pytest.fixture
def M() -> Component:
    return Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X) -> Assembly:
    return Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)])


def test(MX2, M, X):
    frags = enumerate_fragments(MX2)
    assert frags == {
        Assembly(
            {'M0': M, 'X0': X, 'X1': X},
            [Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
        ),
        Assembly({'M0': M, 'X0': X}, [Bond('M0', 0, 'X0', 0)]),
        Assembly({'M0': M, 'X1': X}, [Bond('M0', 1, 'X1', 0)]),
        Assembly({'M0': M}, []),
        Assembly({'X0': X}, []),
        Assembly({'X1': X}, []),
    }


def test_symmetry_operations(MX2, M, X):
    symmetry_operations = [
        {
            'M0': 'M0',
            'X0': 'X1',
            'X1': 'X0',
        }
    ]
    frags = enumerate_fragments(MX2, symmetry_operations)
    assert frags == {
        Assembly(
            {'M0': M, 'X0': X, 'X1': X},
            [Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
        ),
        Assembly({'M0': M, 'X0': X}, [Bond('M0', 0, 'X0', 0)]),
        Assembly({'M0': M}, []),
        Assembly({'X0': X}, []),
    }


def test_M4L4(M4L4, M4L4_symmetry_operations):
    frags = enumerate_fragments(
        M4L4,
        list(M4L4_symmetry_operations.values())
    )
    assert len(frags) == 13


def test_M2L4(M2L4, M2L4_symmetry_operations):
    frags = enumerate_fragments(
        M2L4,
        list(M2L4_symmetry_operations.values())
    )
    assert len(frags) == 28


def test_M9L6(M9L6, M9L6_symmetry_operations):
    frags = enumerate_fragments(
        M9L6,
        list(M9L6_symmetry_operations.values())
    )
    assert len(frags) == 1480
