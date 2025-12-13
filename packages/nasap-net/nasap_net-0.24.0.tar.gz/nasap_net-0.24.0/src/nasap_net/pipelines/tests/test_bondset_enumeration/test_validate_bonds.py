import pytest

from nasap_net.pipelines.bondset_enumeration import validate_bonds


def test_no_duplicates():
    bonds = [1, 2, 3, 4]
    validate_bonds(bonds)


def test_with_duplicates():
    bonds = [1, 2, 2, 4]
    with pytest.raises(
            ValueError, match='"bonds" must not contain duplicates.'):
        validate_bonds(bonds)


if __name__ == '__main__':
    pytest.main(['-v', __file__])