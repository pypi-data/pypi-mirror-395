import pytest

from nasap_net.bondset_enumeration import normalize_bondset_under_sym_ops


def test_1():
    BONDSET = {1}
    SYM_OPS = {'foo': {1: 2, 2: 1}}
    result = normalize_bondset_under_sym_ops(BONDSET, SYM_OPS)
    assert result == {1}


def test_2():
    BONDSET = {2}
    SYM_OPS = {'foo': {1: 2, 2: 1}}
    result = normalize_bondset_under_sym_ops(BONDSET, SYM_OPS)
    assert result == {1}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
