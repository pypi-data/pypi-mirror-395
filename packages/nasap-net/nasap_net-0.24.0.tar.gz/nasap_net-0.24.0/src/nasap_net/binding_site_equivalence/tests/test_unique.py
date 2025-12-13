import pytest

from nasap_net.binding_site_equivalence import UniqueComb, \
    extract_unique_binding_site_combs
from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component


@pytest.fixture
def MX2():
    """X0(0)-(0)M0(1)-(0)X1"""
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    return Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )


def test_single_site(MX2):
    binding_site_combs = [
        (BindingSite('M0', 0),),
        (BindingSite('M0', 1),),
        (BindingSite('X0', 0),),
        (BindingSite('X1', 0),),
    ]

    result = extract_unique_binding_site_combs(binding_site_combs, MX2)

    assert result == {
        UniqueComb(site_comb=(BindingSite('M0', 0),), duplication=2),
        UniqueComb(site_comb=(BindingSite('X0', 0),), duplication=2),
    }


def test_site_pairs(MX2):
    binding_site_combs = [
        (BindingSite('M0', 0), BindingSite('X0', 0)),
        (BindingSite('M0', 0), BindingSite('X1', 0)),
        (BindingSite('M0', 1), BindingSite('X0', 0)),
        (BindingSite('M0', 1), BindingSite('X1', 0)),
    ]

    result = extract_unique_binding_site_combs(binding_site_combs, MX2)

    assert result == {
        UniqueComb(
            site_comb=(BindingSite('M0', 0), BindingSite('X0', 0)),
            duplication=2),
        UniqueComb(
            site_comb=(BindingSite('M0', 0), BindingSite('X1', 0)),
            duplication=2),
    }


def test_site_triplets():
    #          X1
    #         (0)
    #          |
    #         (1)
    # X0(0)-(0)M0(2)-(0)L0(1)
    #         (3)
    #          |
    #         (0)
    #          L1
    #         (1)
    M = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    cis_ML2X2 = Assembly(
        {'M0': M, 'L0': L, 'L1': L, 'X0': X, 'X1': X},
        [Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
         Bond('M0', 2, 'L0', 0), Bond('M0', 3, 'L1', 0)]
    )
    binding_site_combs = [
        (BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 1)),  # trans
        (BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L1', 1)),  # cis
        (BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L0', 1)),  # trans
        (BindingSite('M0', 1), BindingSite('X1', 0), BindingSite('L1', 1)),  # cis
    ]

    result = extract_unique_binding_site_combs(binding_site_combs, cis_ML2X2)

    assert result == {
        UniqueComb(
            (BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L0', 1)),
            duplication=2),
        UniqueComb(
            (BindingSite('M0', 0), BindingSite('X0', 0), BindingSite('L1', 1)),
            duplication=2),
    }
