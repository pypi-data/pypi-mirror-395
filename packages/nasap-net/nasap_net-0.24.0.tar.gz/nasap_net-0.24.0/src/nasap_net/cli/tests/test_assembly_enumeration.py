import os

import pytest
import yaml
from click.testing import CliRunner

from nasap_net import Assembly, Component, is_isomorphic
from nasap_net.cli.commands import run_enum_assemblies_pipeline


@pytest.fixture
def input_data():
    return {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3],
        },
        'sym_ops': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        },
        'component_kinds': {
            'L': Component(['a', 'b']),
            'M': Component(['a', 'b']),
            'X': Component(['a']),
        },
        'components_and_their_kinds': {
            'M1': 'M',
            'M2': 'M',
            'L1': 'L',
            'L2': 'L',
            'L3': 'L'
        },
        'bonds_and_their_binding_sites': {
            1: ['L1.b', 'M1.a'],
            2: ['M1.b', 'L2.a'],
            3: ['L2.b', 'M2.a'],
            4: ['M2.b', 'L3.a']
        },
        'capping_config': {
            'target_component_kind': 'M',
            'capping_component_kind': 'X',
            'capping_binding_site': 'a'
        }
    }


@pytest.fixture
def expected_output_data():
    return {
        # L1--M1--X1
        0: Assembly(
            {'L1': 'L', 'M1': 'M', 'X1': 'X'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'X1.a')]),
        # L1--M1--L2
        1: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        # X1--M1--L2--M2--X2
        2: Assembly(
            {'X1': 'X', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'X2': 'X'}, 
            [('X1.a', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'),
             ('M2.b', 'X2.a')]),
        # L1--M1--L2--M2--X1
        3: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'X1': 'X'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'),
             ('M2.b', 'X1.a')]),
        # L1--M1--L2--M2--L3
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')]),
        }


def test_run_enum_assemblies_pipeline(
        tmp_path, input_data, expected_output_data):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        input_path = os.path.join(td, 'input.yaml')
        output_path = os.path.join(td, 'output.yaml')
        wip_dir = os.path.join(td, 'tmp')

        with open(input_path, 'w') as f:
            yaml.dump(input_data, f)

        result = runner.invoke(
            run_enum_assemblies_pipeline, [
                str(input_path), str(output_path), 
                '--wip-dir', str(wip_dir), 
                '--overwrite', '--verbose'])

        assert result.exit_code == 0

        with open(output_path, 'r') as f:
            output_data = yaml.safe_load(f)

        for key, assembly in expected_output_data.items():
            assert is_isomorphic(
                output_data[key], assembly, input_data['component_kinds'])


if __name__ == '__main__':
    pytest.main(['-v', __file__])
