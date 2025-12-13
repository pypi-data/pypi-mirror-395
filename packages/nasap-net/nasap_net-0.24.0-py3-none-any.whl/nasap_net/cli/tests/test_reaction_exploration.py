import os

import pytest
import yaml
from click.testing import CliRunner

from nasap_net import Assembly, Component
from nasap_net.cli.commands import run_explore_reactions_pipeline


@pytest.fixture
def components_data():
    return {
        'component_kinds': {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
        }
    }


@pytest.fixture
def assemblies():
    return {
        # MX2: X0(a)-(a)M0(b)-(a)X1
        0: Assembly(
            {'M0': 'M', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'X1.a')]
        ),
        1: Assembly({'L0': 'L'}),  # L: (a)L0(b)
        2: Assembly({'X0': 'X'}),  # X: (a)X0
        # MLX: (a)L0(b)-(a)M0(b)-(a)X0
        3: Assembly(
            {'M0': 'M', 'L0': 'L', 'X0': 'X'},
            [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
        ),
        # ML2: (a)L0(b)-(a)M0(b)-(a)L1(b)
        4: Assembly(
            {'M0': 'M', 'L0': 'L', 'L1': 'L'},
            [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
        ),
        # M2L2X: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)
        5: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'X0': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'L1.a')]
        ),
        # M2LX2: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)X1
        6: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'X1.a')]
        ),
        # M2L2-ring: //-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)-//
        7: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L'},
            [('M0.b', 'L0.a'), ('L0.b', 'M1.a'), ('M1.b', 'L1.a'),
             ('L1.b', 'M0.a')]
        ),
    }


@pytest.fixture
def config():
    return {
        'mle_kinds': {
            'metal': 'M',
            'leaving': 'X',
            'entering': 'L',
        }
    }


@pytest.fixture
def expected_csv():
    return """\
init_assem_id,entering_assem_id,product_assem_id,leaving_assem_id,metal_bs,leaving_bs,entering_bs,duplicate_count
5,,7,2,M0.a,X0.a,L1.b,1
0,1,3,2,M0.a,X0.a,L0.a,4
0,3,6,2,M0.a,X0.a,L0.a,2
0,4,5,2,M0.a,X0.a,L0.a,4
3,1,4,2,M0.b,X0.a,L0.a,2
3,3,5,2,M0.b,X0.a,L0.a,2
6,1,5,2,M0.a,X0.a,L0.a,4
"""


def test_run_enum_assemblies_pipeline(
        tmp_path, assemblies, components_data, config, expected_csv):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        assemblies_path = os.path.join(td, 'assemblies.yaml')
        components_path = os.path.join(td, 'components.yaml')
        config_path = os.path.join(td, 'config.yaml')
        output_path = os.path.join(td, 'output.csv')

        with open(assemblies_path, 'w') as f:
            yaml.dump(assemblies, f)
        with open(components_path, 'w') as f:
            yaml.dump(components_data, f)
        with open(config_path, 'w') as f:
            yaml.dump(config, f)

        result = runner.invoke(
            run_explore_reactions_pipeline, [
                str(assemblies_path), str(components_path),
                str(config_path), str(output_path),
                '--overwrite', '--verbose'])

        assert result.exit_code == 0

        with open(output_path, 'r') as f:
            output_data = f.read()
        assert output_data == expected_csv


if __name__ == '__main__':
    pytest.main(['-v', __file__])
