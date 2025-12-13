import pytest

from nasap_net.models import Assembly, Bond, Component
from nasap_net.reaction_classification import get_connection_count_of_kind


@pytest.fixture
def M() -> Component:
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])


def test_basic(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    M2L2X = Assembly(
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ],
    )
    assert get_connection_count_of_kind(
        assembly=M2L2X,
        source_component_id='M0',
        target_kind='L',
    ) == 1
    assert get_connection_count_of_kind(
        assembly=M2L2X,
        source_component_id='M1',
        target_kind='L',
    ) == 2
    assert get_connection_count_of_kind(
        assembly=M2L2X,
        source_component_id='L0',
        target_kind='X',
    ) == 0
