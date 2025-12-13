from nasap_net.models import Assembly, BindingSite, Bond, Component, MLEKind, \
    Reaction
from nasap_net.reaction_equivalence import compute_reaction_list_diff
from nasap_net.reaction_enumeration import enumerate_reactions


def test():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    assemblies = [
        # MX2: X0(0)-(0)M0(1)-(0)X1
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        Assembly(id_='free_L', components={'L0': L}, bonds=[]),
        Assembly(id_='free_X', components={'X0': X}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        Assembly(
            id_='MLX',
            components={'L0': L, 'M0': M, 'X0': X},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        # ML2: (0)L0(1)-(0)M0(1)-(0)L1(1)
        Assembly(
            id_='ML2',
            components={'L0': L, 'M0': M, 'L1': L},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'L1', 0)]),
        # M2L2X: X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
        Assembly(
            id_='M2L2X',
            components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0)]),
        # M2LX2: X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)X1
        Assembly(
            id_='M2LX2',
            components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'X1', 0)]),
        # M2L2-ring: //-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)-//
        Assembly(
            id_='M2L2-ring',
            components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
            bonds=[Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
                   Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M0', 0)]),
    ]
    result = set(enumerate_reactions(assemblies, [MLEKind('M', 'X', 'L')]))
    # TODO: add more detailed checks
    assert len(result) == 7


def test_temp_ring_size_limitation():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])

    # M2L3: (0)L0(1)-(0)M0(1)-(0)L1(1)-(0)M1(1)-(0)L2(1)
    M2L3 = Assembly(
        id_='M2L3',
        components={'L0': L, 'M0': M, 'L1': L, 'M1': M, 'L2': L},
        bonds=[
            Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'L1', 0),
            Bond('L1', 1, 'M1', 0), Bond('M1', 1, 'L2', 0),
        ]
    )
    free_L = Assembly(id_='free_L', components={'L0': L}, bonds=[])
    # M2L3: //-(0)L0(1)-(0)M0(1)-(0)L1(1)-(0)M1(1)-//
    M2L2_ring = Assembly(
        id_='M2L2-ring',
        components={'L0': L, 'M0': M, 'L1': L, 'M1': M},
        bonds=[
            Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'L1', 0),
            Bond('L1', 1, 'M1', 0), Bond('M1', 1, 'L0', 0),
        ]
    )

    # No limitation on ring size
    no_limit_actual = set(
        enumerate_reactions(
            assemblies=[M2L3, free_L, M2L2_ring],
            mle_kinds=[MLEKind('M', 'L', 'L')],
            min_temp_ring_size=None,
        )
    )

    no_limit_expected = {
        Reaction(
            init_assem=M2L3,
            entering_assem=None,
            product_assem=M2L3,
            leaving_assem=None,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('L0', 1),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
        Reaction(
            init_assem=M2L3,
            entering_assem=None,
            product_assem=M2L3,
            leaving_assem=None,
            metal_bs=BindingSite('M1', 0),
            leaving_bs=BindingSite('L1', 1),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
        Reaction(
            init_assem=M2L3,
            entering_assem=free_L,
            product_assem=M2L3,
            leaving_assem=free_L,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('L0', 1),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
        Reaction(
            init_assem=M2L3,
            entering_assem=None,
            product_assem=M2L2_ring,
            leaving_assem=free_L,
            metal_bs=BindingSite('M1', 1),
            leaving_bs=BindingSite('L2', 0),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
        Reaction(
            init_assem=M2L2_ring,
            entering_assem=free_L,
            product_assem=M2L3,
            leaving_assem=None,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('L0', 1),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
    }

    diff = compute_reaction_list_diff(no_limit_actual, no_limit_expected)
    assert diff.first_only == set()
    assert diff.second_only == set()

    # Limit to ring size 2 or larger
    limit_2_actual = set(
        enumerate_reactions(
            assemblies=[M2L3, free_L, M2L2_ring],
            mle_kinds=[MLEKind('M', 'L', 'L')],
            min_temp_ring_size=2,
        )
    )

    limit_2_expected = no_limit_expected - {
        # The following reaction forms a ring of size 1 during the process
        Reaction(
            init_assem=M2L3,
            entering_assem=None,
            product_assem=M2L3,
            leaving_assem=None,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('L0', 1),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=2,
        ),
    }

    diff = compute_reaction_list_diff(limit_2_actual, limit_2_expected)
    assert diff.first_only == set()
    assert diff.second_only == set()
