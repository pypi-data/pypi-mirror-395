from nasap_net.helpers import assign_composition_formula_ids
from nasap_net.models import Assembly, Component


def test():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )
    MX2_2 = Assembly(
        components={'X0_2': X, 'M0_2': M, 'X1_2': X},
        bonds=[],
    )

    assert assign_composition_formula_ids([MX2, MX2_2]) == [
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[],
        ),
        Assembly(
            id_='MX2_2',
            components={'X0_2': X, 'M0_2': M, 'X1_2': X},
            bonds=[],
        ),
    ]


def test_order():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )

    assert assign_composition_formula_ids(
        [MX2], order=['X', 'M']) == [
        Assembly(
            id_='X2M',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[],
        ),
    ]
