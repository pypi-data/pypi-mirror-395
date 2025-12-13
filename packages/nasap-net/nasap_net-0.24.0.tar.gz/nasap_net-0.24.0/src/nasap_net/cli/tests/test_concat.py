import os

import pytest
import yaml
from click.testing import CliRunner

from nasap_net import Assembly, Component
from nasap_net.cli.commands import run_concat_assembly_lists_pipeline


@pytest.fixture
def assemblies_data():
    return [
        {
            0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
            1: Assembly({'L2': 'L', 'M2': 'M'}, [('L2.b', 'M2.a')])
        },
        {
            2: Assembly({'L3': 'L', 'M3': 'M'}, [('L3.b', 'M3.a')]),
            3: Assembly({'L4': 'L', 'M4': 'M'}, [('L4.b', 'M4.a')])
        }
    ]


@pytest.fixture
def components_data():
    return {
        'component_kinds': {
            'L': Component({'a', 'b'}),
            'M': Component({'a', 'b'})
        }
    }


@pytest.fixture
def expected_concatenated_assemblies():
    return {
        0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
    }


def test_run_concat_assembly_lists_pipeline(tmp_path, assemblies_data, components_data, expected_concatenated_assemblies):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        assemblies_paths = []
        for i, data in enumerate(assemblies_data):
            path = os.path.join(td, f'assemblies_{i}.yaml')
            with open(path, 'w') as f:
                yaml.dump(data, f)
            assemblies_paths.append(path)

        components_path = os.path.join(td, 'components.yaml')
        with open(components_path, 'w') as f:
            yaml.dump(components_data, f)

        output_path = os.path.join(td, 'output.yaml')

        result = runner.invoke(
            run_concat_assembly_lists_pipeline,
            [*assemblies_paths, components_path, output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)

        assert actual_output == expected_concatenated_assemblies


if __name__ == '__main__':
    pytest.main(['-v', __file__])