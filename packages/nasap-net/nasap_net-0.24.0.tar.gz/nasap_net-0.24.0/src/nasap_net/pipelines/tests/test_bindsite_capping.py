import pytest
import yaml

from nasap_net import Assembly, Component, is_isomorphic
from nasap_net.pipelines import cap_bindsites_pipeline


@pytest.fixture
def assemblies_data():
    return {
        0: Assembly({'M1': 'M'}),  # M1
        1: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),  # L1--M1
        2: Assembly(  # M1--L1--M2
            {'M1': 'M', 'L1': 'L', 'M2': 'M'},
            [('M1.b', 'L1.a'), ('L1.b', 'M2.a')]),
    }


@pytest.fixture
def components_data():
    return {'component_kinds': {
        'L': Component(['a', 'b']),
        'M': Component(['a', 'b']),
        'X': Component(['a']),
    }}


def test_add_X_on_M(
        tmp_path, assemblies_data, components_data):
    assemblies_path = tmp_path / 'assemblies.yaml'
    components_path = tmp_path / 'components.yaml'
    config_path = tmp_path / 'config.yaml'
    output_path = tmp_path / 'output.yaml'

    CONFIG_DATA = {'capping_config': {
        'target_component_kind': 'M',
        'capping_component_kind': 'X',
        'capping_binding_site': 'a'
    }}

    EXPECTED_CAPPED_ASSEMBLIES = {
        0: Assembly(  # X1--M1--X2
            {'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('X1.a', 'M1.a'), ('X2.a', 'M1.b')]),
        1: Assembly(  # L1--M1--X1
            {'L1': 'L', 'M1': 'M', 'X1': 'X'}, 
            [('L1.b', 'M1.a'), ('X1.a', 'M1.b')]),
        2: Assembly(  # X1--M1--L1--M2--X2
            {'M1': 'M', 'L1': 'L', 'M2': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('X1.a', 'M1.a'), ('M1.b', 'L1.a'), ('L1.b', 'M2.a'), 
             ('M2.b', 'X2.a')]),
        }

    with open(assemblies_path, 'w') as f:
        yaml.dump(assemblies_data, f)
    
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)
    
    with open(config_path, 'w') as f:
        yaml.dump(CONFIG_DATA, f)

    # Run the pipeline
    cap_bindsites_pipeline(
        assemblies_path=str(assemblies_path),
        components_path=str(components_path),
        config_path=str(config_path),
        output_path=str(output_path),
    )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data.keys() == EXPECTED_CAPPED_ASSEMBLIES.keys()
    for assembly_id, expected_assembly in EXPECTED_CAPPED_ASSEMBLIES.items():
        assert is_isomorphic(
            output_data[assembly_id], expected_assembly,
            components_data['component_kinds'])


def test_add_L_on_M(
        tmp_path, assemblies_data, components_data):
    assemblies_path = tmp_path / 'assemblies.yaml'
    components_path = tmp_path / 'components.yaml'
    config_path = tmp_path / 'config.yaml'
    output_path = tmp_path / 'output.yaml'

    CONFIG_DATA = {
        'capping_config': {
        'target_component_kind': 'M',
        'capping_component_kind': 'L',
        'capping_binding_site': 'a'
    }}

    EXPECTED_CAPPED_ASSEMBLIES = {
        0: Assembly(  # L1--M1--L2
            {'M1': 'M', 'L1': 'L', 'L2': 'L'}, 
            [('L1.a', 'M1.a'), ('L2.a', 'M1.b')]),
        1: Assembly(  # L1--M1--L2
            {'L1': 'L', 'M1': 'M', 'L2': 'L'}, 
            [('L1.b', 'M1.a'), ('L2.a', 'M1.b')]),
        2: Assembly(  # L1--M1--L2--M2--L3
            {'M1': 'M', 'L1': 'L', 'L2': 'L', 'M2': 'M', 'L3': 'L'},
            [('L1.a', 'M1.a'), ('L2.a', 'M1.b'), ('L2.b', 'M2.a'),
             ('L3.a', 'M2.b')]),
        }

    with open(assemblies_path, 'w') as f:
        yaml.dump(assemblies_data, f)
    
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)
    
    with open(config_path, 'w') as f:
        yaml.dump(CONFIG_DATA, f)

    # Run the pipeline
    cap_bindsites_pipeline(
        assemblies_path=str(assemblies_path),
        components_path=str(components_path),
        config_path=str(config_path),
        output_path=str(output_path),
    )

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data.keys() == EXPECTED_CAPPED_ASSEMBLIES.keys()
    for assembly_id, expected_assembly in EXPECTED_CAPPED_ASSEMBLIES.items():
        assert is_isomorphic(
            output_data[assembly_id], expected_assembly,
            components_data['component_kinds'])
        

if __name__ == '__main__':
    pytest.main(['-v', __file__])
