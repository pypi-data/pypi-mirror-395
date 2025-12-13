import pytest

from nasap_net.pipelines.bondset_enumeration import validate_sym_ops


def test_valid():
    bonds = [1, 2, 3]
    sym_ops = {
        'C3': {1: 2, 2: 3, 3: 1},
        'C3^2': {1: 3, 2: 1, 3: 2}
    }
    validate_sym_ops(sym_ops, bonds)


def test_invalid_keys():
    bonds = [1, 2, 3]
    sym_ops = {
        'C3': {1: 2, 2: 3, 4: 1},  # Missing key 3
    }
    with pytest.raises(
            ValueError, 
            match='Keys in the operation mapping must contain all bonds'):
        validate_sym_ops(sym_ops, bonds)


def test_invalid_values():
    bonds = [1, 2, 3]
    sym_ops = {
        'C3': {1: 2, 2: 3, 3: 2},  # Missing value 1
    }
    with pytest.raises(
            ValueError, 
            match='Values in the operation mapping must contain all bonds'):
        validate_sym_ops(sym_ops, bonds)


if __name__ == '__main__':
    pytest.main(['-v', __file__])
