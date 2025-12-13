import os

import pytest
import yaml

from nasap_net import Assembly
from nasap_net.pipelines.bondset_to_assembly import bondsets_to_assemblies_pipeline


@pytest.fixture
def bondsets_data():
    return {
        0: [1],
        1: [1, 2],
        2: [2, 3],
        3: [1, 2, 3],
        4: [1, 2, 3, 4]
    }


@pytest.fixture
def structure_data():
    return {
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
        }
    }


@pytest.fixture
def expected_assemblies():
    return {
        0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
        1: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        2: Assembly(
            {'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        3: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')])
    }


def test_bondsets_to_assemblies_pipeline(
        tmp_path, bondsets_data, structure_data, expected_assemblies):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    bondsets_path = tmp_path / 'bondsets.yaml'
    structure_data_path = tmp_path / 'structure_data.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(bondsets_path, 'w') as f:
        yaml.dump(bondsets_data, f)
    
    with open(structure_data_path, 'w') as f:
        yaml.dump(structure_data, f)

    # Run the pipeline
    bondsets_to_assemblies_pipeline(
        bondsets_path=str(bondsets_path),
        structure_data_path=str(structure_data_path),
        output_path=str(output_path),
    )

    with open(output_path, 'r') as f:
        output_txt = f.read()

    # Check the output file
    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == expected_assemblies


def test_bondsets_to_assemblies_pipeline_overwrite(
        tmp_path, bondsets_data, structure_data, expected_assemblies):
    bondsets_path = tmp_path / 'bondsets.yaml'
    structure_data_path = tmp_path / 'structure_data.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(bondsets_path, 'w') as f:
        yaml.dump(bondsets_data, f)
    
    with open(structure_data_path, 'w') as f:
        yaml.dump(structure_data, f)
    
    # Create an initial output file
    with open(output_path, 'w') as f:
        yaml.dump({'initial': 'data'}, f)

    # Run the pipeline with overwrite
    bondsets_to_assemblies_pipeline(
        bondsets_path=str(bondsets_path),
        structure_data_path=str(structure_data_path),
        output_path=str(output_path),
        overwrite=True
    )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)
    
    # Check that the initial data is gone
    assert 'initial' not in output_data

    assert output_data == expected_assemblies


def test_bondsets_to_assemblies_pipeline_no_overwrite(
        tmp_path, bondsets_data, structure_data):
    bondsets_path = tmp_path / 'bondsets.yaml'
    structure_data_path = tmp_path / 'structure_data.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(bondsets_path, 'w') as f:
        yaml.dump(bondsets_data, f)
    
    with open(structure_data_path, 'w') as f:
        yaml.dump(structure_data, f)

    # Create an initial output file
    with open(output_path, 'w') as f:
        yaml.dump({'initial': 'data'}, f)

    # Run the pipeline without overwrite
    with pytest.raises(FileExistsError):
        bondsets_to_assemblies_pipeline(
            bondsets_path=str(bondsets_path),
            structure_data_path=str(structure_data_path),
            output_path=str(output_path),
            overwrite=False
        )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    # Check that the initial data is still there
    assert 'initial' in output_data
    assert output_data['initial'] == 'data'


if __name__ == '__main__':
    pytest.main(['-v', __file__])
