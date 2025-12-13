import pytest

from nasap_net.pipelines.bondset_to_assembly import validate_bond_id_to_bindsites


def test_validate_bond_id_to_bindsites_valid():
    bond_id_to_bindsites = {
        1: ['L1.b', 'M1.a'],
        2: ['M1.b', 'L2.a'],
        3: ['L2.b', 'M2.a'],
        4: ['M2.b', 'L3.a']
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    # Should not raise any exception
    validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


def test_validate_bond_id_to_bindsites_invalid_string():
    bond_id_to_bindsites = {
        1: ['L1.b', 123],  # Invalid: second value is not a string
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    with pytest.raises(
            ValueError, 
            match='Values in "bonds_and_their_binding_sites" must be '
            'strings.'):
        validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


def test_validate_bond_id_to_bindsites_same_values():
    bond_id_to_bindsites = {
        1: ['L1.b', 'L1.b'],  # Invalid: both values are the same
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    with pytest.raises(
            ValueError, 
            match='Values in "bonds_and_their_binding_sites" must be '
            'different.'):
        validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


def test_validate_bond_id_to_bindsites_invalid_format():
    bond_id_to_bindsites = {
        1: ['L1b', 'M1.a'],  # Invalid: first value does not have a dot
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    with pytest.raises(
            ValueError,
            match='must be in the form of "comp_id.local_bindsite_id"'):
        validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


def test_validate_bond_id_to_bindsites_unknown_component():
    bond_id_to_bindsites = {
        1: ['L1.b', 'X1.a'],  # Invalid: 'X1' is not in comp_ids
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    with pytest.raises(
            ValueError, 
            match='Unknown component ID "X1" in '
            '"bonds_and_their_binding_sites".'):
        validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


def test_validate_bond_id_to_bindsites_same_component():
    bond_id_to_bindsites = {
        1: ['M1.a', 'M1.b'],  # Invalid: both components are the same
    }
    comp_ids = ['M1', 'M2', 'L1', 'L2', 'L3']
    with pytest.raises(
            ValueError, 
            match='The two components in a bond must be different.'):
        validate_bond_id_to_bindsites(bond_id_to_bindsites, comp_ids)


if __name__ == "__main__":
    pytest.main(['-v', __file__])
