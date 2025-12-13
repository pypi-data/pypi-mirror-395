import pytest

from nasap_net.classes.bindsite_id_converter import BindsiteIdConverter


def test_local_to_global():
    id_converter = BindsiteIdConverter()
    result = id_converter.local_to_global('M1', 'a')
    assert result == 'M1.a'


def test_global_to_local():
    id_converter = BindsiteIdConverter()
    result = id_converter.global_to_local('M1.a')
    assert result == ('M1', 'a')


def test_global_to_local_invalid_format():
    id_converter = BindsiteIdConverter()
    with pytest.raises(AssertionError):
        id_converter.global_to_local('invalid_format')


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
