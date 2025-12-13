from nasap_net.models import BindingSite


def test_binding_site():
    site = BindingSite(component_id="M1", site_id="a")
    assert site.component_id == "M1"
    assert site.site_id == "a"


def test_binding_site_ordering():
    site1 = BindingSite(component_id="M1", site_id="a")
    site2 = BindingSite(component_id="M1", site_id="b")
    site3 = BindingSite(component_id="M2", site_id="a")
    assert site1 < site2
    assert site1 < site3
    assert site2 < site3


def test_binding_site_equality():
    site1 = BindingSite(component_id="M1", site_id="a")
    site2 = BindingSite(component_id="M1", site_id="a")
    site3 = BindingSite(component_id="M1", site_id="b")
    assert site1 == site2
    assert site1 != site3


def test___repr__():
    site = BindingSite(component_id="M1", site_id="a")
    assert repr(site) == "BindingSite('M1', 'a')"
