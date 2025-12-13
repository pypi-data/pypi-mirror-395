from nasap_net.binding_site_equivalence import \
    group_equivalent_binding_site_combs
from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component


def test_single_binding_site():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX2 = Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
    )

    expected = {
        frozenset({(BindingSite('M0', 0),), (BindingSite('M0', 1),)}),
        frozenset({(BindingSite('X0', 0),), (BindingSite('X1', 0),)}),
    }

    result = group_equivalent_binding_site_combs(
        node_combs=[(BindingSite('M0', 0),), (BindingSite('M0', 1),),
                    (BindingSite('X0', 0),), (BindingSite('X1', 0),)],
        assembly=MX2,
    )

    assert result == expected


def test_binding_site_pairs():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX2 = Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
    )

    expected = {
        frozenset({
            (BindingSite('M0', 0), BindingSite('X0', 0)),
            (BindingSite('M0', 1), BindingSite('X1', 0)),
        }),
        frozenset({
            (BindingSite('M0', 0), BindingSite('X1', 0)),
            (BindingSite('M0', 1), BindingSite('X0', 0)),
        }),
    }

    result = group_equivalent_binding_site_combs(
        node_combs=[(BindingSite('M0', 0), BindingSite('X0', 0)),
                    (BindingSite('M0', 0), BindingSite('X1', 0)),
                    (BindingSite('M0', 1), BindingSite('X0', 0)),
                    (BindingSite('M0', 1), BindingSite('X1', 0))],
        assembly=MX2,
    )

    assert result == expected


def test_aux_edges():
    M = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)]
    )
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    ML2X2_cis = Assembly(
        components={'M0': M, 'L0': L, 'L1': L, 'X0': X, 'X1': X},
        bonds=[
            Bond('M0', 0, 'X0', 0),
            Bond('M0', 1, 'X1', 0),
            Bond('M0', 2, 'L0', 0),
            Bond('M0', 3, 'L1', 0),
        ]
    )

    expected = {
        frozenset({
            (BindingSite('X0', 0), BindingSite('L0', 0)),
            (BindingSite('X1', 0), BindingSite('L1', 0)),
        }),
        frozenset({
            (BindingSite('X0', 0), BindingSite('L1', 0)),
            (BindingSite('X1', 0), BindingSite('L0', 0)),
        }),
    }

    result = group_equivalent_binding_site_combs(
        node_combs=[
            (BindingSite('X0', 0), BindingSite('L0', 0)),  # trans
            (BindingSite('X0', 0), BindingSite('L1', 0)),  # cis
            (BindingSite('X1', 0), BindingSite('L0', 0)),  # cis
            (BindingSite('X1', 0), BindingSite('L1', 0)),  # trans
        ],
        assembly=ML2X2_cis,
    )

    assert result == expected
