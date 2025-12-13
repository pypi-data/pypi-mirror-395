from nasap_net.io.assemblies import dump_assemblies_to_str, load_assemblies_from_str
from nasap_net.models import Assembly, AuxEdge, Bond, Component


def test_round_trip():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M_aux = Component(
        kind='M(aux)', sites=[0, 1, 2],
        aux_edges=[AuxEdge(0, 1), AuxEdge(0, 2, kind='cis')])

    assemblies = [
        Assembly(components={'X0': X}, bonds=[]),
        # MX2: X0(0)-(0)M0(1)-(0)X1
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        Assembly(
            components={'M0': M_aux, 'X0': X, 'X1': X, 'X2': X},
            bonds=[
                Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
                Bond('M0', 2, 'X2', 0)
            ]
        ),
    ]

    dumped = dump_assemblies_to_str(assemblies)
    loaded = load_assemblies_from_str(dumped)
    assert loaded == assemblies
