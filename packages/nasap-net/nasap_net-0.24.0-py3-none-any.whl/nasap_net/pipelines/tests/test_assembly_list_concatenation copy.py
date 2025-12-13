import pytest
import yaml

from nasap_net import Assembly
from nasap_net.pipelines import concatenate_assemblies_pipeline


def test_basic(tmp_path):
    assemblies_paths = [
        tmp_path / 'first.yaml',
        tmp_path / 'second.yaml']
    
    ASSEMBLIES = [
        {0: Assembly({'first': 'L'}), 1: Assembly({'first': 'M'})},
        {0: Assembly({'second': 'L'}), 1: Assembly({'second': 'M'})}]
    
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f)

    components_path = tmp_path / 'components.yaml'
    with open(components_path, 'w') as f:
        yaml.dump({'component_kinds': {}}, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_pipeline(
        assemblies_path_list=assemblies_paths,
        components_path=components_path,
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == {
        0: Assembly({'first': 'L'}), 1: Assembly({'first': 'M'})}
    # The second assemblies are not included because they are isomorphic
    # to the first ones.


def test_duplicates_within_files(tmp_path):
    assemblies_paths = [tmp_path / 'first.yaml']
    
    ASSEMBLIES = [
        {0: Assembly({'first': 'L'}), 1: Assembly({'second': 'L'})}]
    
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f)

    components_path = tmp_path / 'components.yaml'
    with open(components_path, 'w') as f:
        yaml.dump({'component_kinds': {}}, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_pipeline(
        assemblies_path_list=assemblies_paths,
        components_path=components_path,
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    # The second assembly is not included because it is isomorphic to 
    # the first one.
    assert output_data == {0: Assembly({'first': 'L'})}


def test_already_unique_within_files(tmp_path):
    assemblies_paths = [tmp_path / 'first.yaml']
    
    ASSEMBLIES = [
        {0: Assembly({'first': 'L'}), 1: Assembly({'second': 'L'})}]
    
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f)

    components_path = tmp_path / 'components.yaml'
    with open(components_path, 'w') as f:
        yaml.dump({'component_kinds': {}}, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_pipeline(
        assemblies_path_list=assemblies_paths,
        components_path=components_path,
        resulting_assems_path=str(OUTPUT_PATH),
        already_unique_within_files=True,  # This is the only difference
        start=0, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    # The second assembly is included even though it is isomorphic to
    # the first one. This is because the parameter 
    # `already_unique_within_files` is set to True, which means that
    # the isomorphism check is skipped for the assemblies within the
    # same file.
    assert output_data == {
        0: Assembly({'first': 'L'}), 1: Assembly({'second': 'L'})}


def test_skip_isomorphism_checks(tmp_path):
    assemblies_paths = [
        tmp_path / 'first.yaml',
        tmp_path / 'second.yaml']
    
    ASSEMBLIES = [
        {0: Assembly({'first': 'L'})},
        {0: Assembly({'second': 'L'})}]  # isomorphic to the first one
    
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f)

    components_path = tmp_path / 'components.yaml'
    with open(components_path, 'w') as f:
        yaml.dump({'component_kinds': {}}, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_pipeline(
        assemblies_path_list=assemblies_paths,
        components_path=components_path,
        resulting_assems_path=str(OUTPUT_PATH),
        skip_isomorphism_checks=True,  # This is the only difference
        start=0, overwrite=True, verbose=False)
    
    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    # The second assembly is included even though it is isomorphic to
    # the first one. This is because the parameter `skip_isomorphism_checks`
    # is set to True, which means that the isomorphism check is skipped
    # for all assemblies.

    assert output_data == {
        0: Assembly({'first': 'L'}), 1: Assembly({'second': 'L'})}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
