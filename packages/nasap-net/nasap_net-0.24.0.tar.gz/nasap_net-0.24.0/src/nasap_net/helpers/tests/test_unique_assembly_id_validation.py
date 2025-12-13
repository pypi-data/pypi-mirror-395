import pytest

from nasap_net.exceptions import DuplicateIDError, IDNotSetError
from nasap_net.helpers import validate_unique_ids
from nasap_net.models import Assembly


def test_valid():
    assemblies = [
        Assembly(id_='A1', components={}, bonds=[]),
        Assembly(id_='A2', components={}, bonds=[]),
        Assembly(id_='A3', components={}, bonds=[]),
    ]
    validate_unique_ids(assemblies)


def test_missing_id():
    assemblies = [
        Assembly(id_='A1', components={}, bonds=[]),
        Assembly(components={}, bonds=[]),  # Missing ID
        Assembly(id_='A3', components={}, bonds=[]),
    ]
    with pytest.raises(IDNotSetError):
        validate_unique_ids(assemblies)


def test_duplicate_id():
    assemblies = [
        Assembly(id_='A1', components={}, bonds=[]),
        Assembly(id_='A2', components={}, bonds=[]),
        Assembly(id_='A1', components={}, bonds=[]),  # Duplicate ID
    ]
    with pytest.raises(DuplicateIDError):
        validate_unique_ids(assemblies)
