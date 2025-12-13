import os

import pytest
import yaml

from nasap_net.pipelines.bondset_enumeration import enum_bond_subsets_pipeline


def test_without_sym_ops(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        }
    }
    EXPECTED = {
        0: [1], 1: [2], 2: [3], 3: [4],
        4: [1, 2], 5: [2, 3], 6: [3, 4],
        7: [1, 2, 3], 8: [2, 3, 4],
        9: [1, 2, 3, 4]
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)

    output_path = tmp_path / "output.yaml"
    enum_bond_subsets_pipeline(input_path, output_path)

    with open(output_path, 'r') as f:
        actual_output = yaml.safe_load(f)

    assert actual_output == EXPECTED


def test_with_sym_ops(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        },
        'sym_ops': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        }
    }
    EXPECTED = {
        0: [1], 1: [2], 2: [1, 2], 3: [2, 3], 4: [1, 2, 3], 5: [1, 2, 3, 4]
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)
    
    output_path = tmp_path / "output.yaml"
    enum_bond_subsets_pipeline(input_path, output_path)

    with open(output_path, 'r') as f:
        actual_output = yaml.safe_load(f)

    assert actual_output == EXPECTED


def test_missing_input_key(tmp_path):
    INPUT_DATA = {
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        }
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)

    with pytest.raises(KeyError):
        enum_bond_subsets_pipeline(input_path, "output.yaml")


def test_verbose_false(tmp_path, capsys):
    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        }
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)

    output_path = tmp_path / "output.yaml"
    enum_bond_subsets_pipeline(input_path, output_path, verbose=False)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_verbose_true(tmp_path, capsys):
    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        }
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)

    output_path = tmp_path / "output.yaml"
    enum_bond_subsets_pipeline(input_path, output_path, verbose=True)

    captured = capsys.readouterr()
    assert f'Reading from "{input_path}"...' in captured.out
    assert f'Finished reading from "{input_path}".' in captured.out
    assert 'Enumerating bond subsets...' in captured.out
    assert f'Number of bond subsets: 10' in captured.out
    assert f'Saving the results to "{output_path}"...' in captured.out
    assert (
        f'Successfully saved to "{output_path}"' in captured.out)


def test_wip(tmp_path):
    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        },
        'sym_ops': {
            'C2': [[1, 4], [2, 3]]
        }
    }
    input_path = tmp_path / "input.yaml"
    with open(input_path, 'w') as f:
        yaml.safe_dump(INPUT_DATA, f)

    output_path = tmp_path / "output.yaml"
    wip_dir = tmp_path / "resolved_sym_ops.yaml"
    enum_bond_subsets_pipeline(input_path, output_path, path_to_output_resolved_sym_ops=wip_dir)

    assert os.path.exists(wip_dir)
    assert os.path.isfile(wip_dir)

    EXPECTED = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    with open(wip_dir, 'r') as f:
        actual_output = yaml.safe_load(f)
    
    assert actual_output == EXPECTED


if __name__ == "__main__":
    pytest.main(['-v', __file__])
