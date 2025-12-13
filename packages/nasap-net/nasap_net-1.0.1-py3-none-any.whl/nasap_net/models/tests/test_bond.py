import pytest

from nasap_net.models import BindingSite, Bond


def test_bond():
    bond = Bond(comp_id1="L1", site1="a", comp_id2="M1", site2="b")
    assert bond.sites == frozenset({
        BindingSite(component_id="L1", site_id="a"),
        BindingSite(component_id="M1", site_id="b")
    })


def test_bond_same_site_error():
    with pytest.raises(ValueError):
        Bond(comp_id1="M1", site1="a", comp_id2="M1", site2="b")
    # Should not raise
    Bond(comp_id1="M1", site1="a", comp_id2="M2", site2="a")
