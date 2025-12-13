import pytest

from nasap_net.io.assemblies.semi_light_assembly import SemiLightAssembly, \
    convert_assemblies_to_semi_light_ones
from nasap_net.models import Assembly, AuxEdge, Bond, Component
from nasap_net.models.component_consistency_check import \
    InconsistentComponentBetweenAssembliesError


def test():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M_square = Component(
        kind='M(sq)', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])

    assemblies = {
        # MX2: X0(0)-(0)M0(1)-(0)X1
        'MX2': Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        'free_X': Assembly(components={'X0': X}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        'MLX': Assembly(
            components={'L0': L, 'M0': M, 'X0': X},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        'M(sq)X4': Assembly(
            components={'M0': M_square, 'X0': X, 'X1': X, 'X2': X, 'X3': X},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
                   Bond('M0', 2, 'X2', 0), Bond('M0', 3, 'X3', 0)]),
        'M(sq)L2X2': Assembly(
            components={'M0': M_square, 'L0': L, 'L1': L, 'X0': X, 'X1': X},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('M0', 2, 'X1', 0), Bond('M0', 3, 'L1', 0)]),
    }

    conv_res = convert_assemblies_to_semi_light_ones(assemblies)

    assert conv_res.components == {
        'M': M,
        'L': L,
        'X': X,
        'M(sq)': M_square,
    }

    assert conv_res.semi_light_assemblies == {
        # MX2: X0(0)-(0)M0(1)-(0)X1
        'MX2': SemiLightAssembly(
            id_='MX2',
            components={'X0': 'X', 'M0': 'M', 'X1': 'X'},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        'free_X': SemiLightAssembly(components={'X0': 'X'}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        'MLX': SemiLightAssembly(
            components={'L0': 'L', 'M0': 'M', 'X0': 'X'},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        'M(sq)X4': SemiLightAssembly(
            components={'M0': 'M(sq)', 'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
                   Bond('M0', 2, 'X2', 0), Bond('M0', 3, 'X3', 0)]),
        'M(sq)L2X2': SemiLightAssembly(
            components={'M0': 'M(sq)', 'L0': 'L', 'L1': 'L', 'X0': 'X', 'X1': 'X'},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('M0', 2, 'X1', 0), Bond('M0', 3, 'L1', 0)]),
    }


def test_inconsistent_component_kind_error():
    X1 = Component(kind='X', sites=[0])
    X2 = Component(kind='X', sites=[1])  # Same kind but different sites

    assemblies = {
        'free_X1': Assembly(components={'X0': X1}, bonds=[]),
        'free_X2': Assembly(components={'X0': X2}, bonds=[]),
    }

    with pytest.raises(InconsistentComponentBetweenAssembliesError):
        convert_assemblies_to_semi_light_ones(assemblies)
