import pytest

from nasap_net.pipelines.bondset_enumeration import parse_sym_ops


def test_with_sym_maps():
    input_data = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    expected = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_sym_perms():
    input_data = {
        'C3': [[1, 2, 3]]
    }
    expected = {
        'C3': {1: 2, 2: 3, 3: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_both_sym_maps_and_sym_perms():
    input_data = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1},
        'C3': [[1, 2, 3]]
    }
    # sym_maps should be prioritized
    expected = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1},
        'C3': {1: 2, 2: 3, 3: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_no_sym_ops():
    input_data = {}  # type: ignore
    assert parse_sym_ops(input_data) == {}


def test_op_chain():
    input_data = {
        'op1': {1: 2, 2: 3, 3: 1},
        'op2': {1: 1, 2: 3, 3: 2},
        'op3': ['op2', 'op1']  # op2(op1(x))
    }

    expected = {
        'op1': {1: 2, 2: 3, 3: 1},
        'op2': {1: 1, 2: 3, 3: 2},
        'op3': {1: 3, 2: 2, 3: 1},  # op2(op1(x))
    }
    assert parse_sym_ops(input_data) == expected


def test_chain_of_op_chain():
    input_data = {
        'op1': {1: 2, 2: 3, 3: 1},
        'op2': {1: 1, 2: 3, 3: 2},
        'op3': ['op2', 'op1'],
        'op4': ['op1', 'op3']  # op1(op3(x)) = op1(op2(op1(x)))
    }

    expected = {
        'op1': {1: 2, 2: 3, 3: 1},
        'op2': {1: 1, 2: 3, 3: 2},
        'op3': {1: 3, 2: 2, 3: 1},  # op2(op1(x))
        'op4': {1: 1, 2: 3, 3: 2},  # op1(op3(x))
    }
    assert parse_sym_ops(input_data) == expected



if __name__ == '__main__':
    pytest.main(['-vv', __file__])