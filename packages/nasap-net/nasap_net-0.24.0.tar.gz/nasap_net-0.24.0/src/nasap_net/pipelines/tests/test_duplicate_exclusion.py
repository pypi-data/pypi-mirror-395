import os

import pytest
import yaml

from nasap_net import Assembly, Component
from nasap_net.pipelines import find_unique_assemblies_pipeline


@pytest.fixture
def assemblies_data():
    return {
        0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
        1: Assembly({'M1': 'M', 'L2': 'L'}, [('M1.b', 'L2.a')]),  # Duplicate
        2: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        3: Assembly(
            {'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        5: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')])
    }

@pytest.fixture
def components_data():
    return {
        'component_kinds': {
            'L': Component(['a', 'b']),
            'M': Component(['a', 'b'])
            }}

@pytest.fixture
def expected_unique_assemblies(assemblies_data):
    return {
        0: assemblies_data[0],
        2: assemblies_data[2],
        3: assemblies_data[3],
        4: assemblies_data[4],
        5: assemblies_data[5]
    }

def test_find_unique_assemblies_pipeline(
        tmp_path, assemblies_data, components_data, 
        expected_unique_assemblies):
    assemblies_path = tmp_path / 'assemblies.yaml'
    components_path = tmp_path / 'components.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(assemblies_path, 'w') as f:
        yaml.dump(assemblies_data, f)
    
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)

    # Run the pipeline
    find_unique_assemblies_pipeline(
        assemblies_path=str(assemblies_path),
        components_path=str(components_path),
        output_path=str(output_path),
    )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == expected_unique_assemblies


def test_find_unique_assemblies_pipeline_overwrite(
        tmp_path, assemblies_data, components_data, 
        expected_unique_assemblies):
    assemblies_path = tmp_path / 'assemblies.yaml'
    components_path = tmp_path / 'components.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(assemblies_path, 'w') as f:
        yaml.dump(assemblies_data, f)
    
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)
    
    # Create an initial output file
    with open(output_path, 'w') as f:
        yaml.dump({'initial': 'data'}, f)

    # Run the pipeline with overwrite
    find_unique_assemblies_pipeline(
        assemblies_path=str(assemblies_path),
        components_path=str(components_path),
        output_path=str(output_path),
        overwrite=True
    )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)
    
    # Check that the initial data is gone
    assert 'initial' not in output_data

    assert output_data == expected_unique_assemblies


def test_find_unique_assemblies_pipeline_no_overwrite(
        tmp_path, assemblies_data, components_data):
    assemblies_path = tmp_path / 'assemblies.yaml'
    components_path = tmp_path / 'components.yaml'
    output_path = tmp_path / 'output.yaml'

    with open(assemblies_path, 'w') as f:
        yaml.dump(assemblies_data, f)
    
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)

    # Create an initial output file
    with open(output_path, 'w') as f:
        yaml.dump({'initial': 'data'}, f)

    # Run the pipeline without overwrite
    with pytest.raises(FileExistsError):
        find_unique_assemblies_pipeline(
            assemblies_path=str(assemblies_path),
            components_path=str(components_path),
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
