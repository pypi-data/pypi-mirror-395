import pytest

from nasap_net.utils import resolve_chain_map


def test_basic():
    input1 = {1: 10, 2: 20}
    input2 = {10: 100, 20: 200}
    input3 = {100: 1000, 200: 2000}

    output = resolve_chain_map(input1, input2, input3)
    assert output == {1: 1000, 2: 2000}


def test_empty():
    output = resolve_chain_map()
    assert output == {}


def test_single_input():
    input1 = {1: 10}
    output = resolve_chain_map(input1)
    assert output == {1: 10}


if __name__ == '__main__':
    pytest.main(['-v', __file__])
