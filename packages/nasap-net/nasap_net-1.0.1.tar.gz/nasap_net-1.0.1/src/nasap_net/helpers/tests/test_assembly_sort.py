from nasap_net.helpers import sort_assemblies_by_component_kind_counts
from nasap_net.models import Assembly, Component


def test_typical_use():
    M = Component(kind='M', sites=[])
    L = Component(kind='L', sites=[])
    X = Component(kind='X', sites=[])

    free_L = Assembly(components={'L0': L}, bonds=[])
    free_X = Assembly(components={'X0': X}, bonds=[])
    MX2 = Assembly(components={'M0': M, 'X0': X, 'X1': X}, bonds=[])
    MLX = Assembly(components={'M0': M, 'L0': L, 'X0': X}, bonds=[])
    ML2 = Assembly(components={'M0': M, 'L0': L, 'L1': L}, bonds=[])
    M2LX2 = Assembly(
        components={'M0': M, 'M1': M, 'L0': L, 'X0': X, 'X1': X},
        bonds=[],
    )
    M2L2X = Assembly(
        components={'M0': M, 'M1': M, 'L0': L, 'L1': L, 'X0': X},
        bonds=[],
    )
    M2L3 = Assembly(
        components={'M0': M, 'M1': M, 'L0': L, 'L1': L, 'L2': L},
        bonds=[],
    )

    assemblies = [
        free_L,  # 0, 1, 0
        free_X,  # 0, 0, 1
        MX2,     # 1, 0, 2
        MLX,     # 1, 1, 1
        ML2,     # 1, 2, 0
        M2LX2,   # 2, 1, 2
        M2L2X,   # 2, 2, 1
        M2L3,    # 2, 3, 0
    ]
    expected = [
        free_X,  # 0, 0, 1
        free_L,  # 0, 1, 0
        MX2,     # 1, 0, 2
        MLX,     # 1, 1, 1
        ML2,     # 1, 2, 0
        M2LX2,   # 2, 1, 2
        M2L2X,   # 2, 2, 1
        M2L3,    # 2, 3, 0
    ]

    actual = sort_assemblies_by_component_kind_counts(
        assemblies,
        kinds=['M', 'L', 'X'],
    )
    assert actual == expected


def test_basic():
    A = Component(kind='A', sites=[])
    B = Component(kind='B', sites=[])

    A_free = Assembly(components={'A0': A}, bonds=[])
    B_free = Assembly(components={'B0': B}, bonds=[])
    AB = Assembly(components={'A0': A, 'B0': B}, bonds=[])
    A2 = Assembly(components={'A0': A, 'A1': A}, bonds=[])
    B2 = Assembly(components={'B0': B, 'B1': B}, bonds=[])
    A2B = Assembly(components={'A0': A, 'A1': A, 'B0': B}, bonds=[])
    AB2 = Assembly(components={'A0': A, 'B0': B, 'B1': B}, bonds=[])
    A2B2 = Assembly(components={'A0': A, 'A1': A, 'B0': B, 'B1': B}, bonds=[])

    assemblies = [
        A_free,  # 1, 0
        B_free,  # 0, 1
        AB,      # 1, 1
        A2,      # 2, 0
        B2,      # 0, 2
        A2B,     # 2, 1
        AB2,     # 1, 2
        A2B2,    # 2, 2
    ]
    expected = [
        B_free,  # 0, 1
        B2,      # 0, 2
        A_free,  # 1, 0
        AB,      # 1, 1
        AB2,     # 1, 2
        A2,      # 2, 0
        A2B,     # 2, 1
        A2B2,    # 2, 2
    ]

    actual = sort_assemblies_by_component_kind_counts(
        assemblies,
        kinds=['A', 'B'],
    )
    assert actual == expected


def test_unspecified_kind():
    """Test that unspecified kinds are ignored in sorting."""
    A = Component(kind='A', sites=[])
    B = Component(kind='B', sites=[])

    AB = Assembly(components={'A0': A, 'B0': B}, bonds=[])
    A2B = Assembly(components={'A0': A, 'A1': A, 'B0': B}, bonds=[])
    AB2 = Assembly(components={'A0': A, 'B0': B, 'B1': B}, bonds=[])
    A2B2 = Assembly(components={'A0': A, 'A1': A, 'B0': B, 'B1': B}, bonds=[])

    assemblies = [
        A2B2,  # 2, 2 (before 2, 1)
        AB2,   # 1, 2 (before 1, 1)
        A2B,   # 2, 1
        AB,    # 1, 1
    ]
    # Number of 'B's should be ignored,
    # and the order of assemblies with same number of 'A's should be preserved.
    expected = [
        AB2,   # 1, 2 (before 1, 1)
        AB,    # 1, 1
        A2B2,  # 2, 2 (before 2, 1)
        A2B,   # 2, 1
    ]

    actual = sort_assemblies_by_component_kind_counts(
        assemblies,
        kinds=['A'],  # 'B' is not specified
    )
    assert actual == expected
