import pytest
import yaml

from nasap_net import Assembly
from nasap_net.pipelines import concatenate_assemblies_without_isom_checks


def test_basic(tmp_path):
    assemblies_paths = [
        tmp_path / 'assemblies-0.yaml',
        tmp_path / 'assemblies-1.yaml']
    
    ASSEMBLIES = [
        {0: Assembly({'L0': 'L'}), 1: Assembly({'M0': 'M'})},
        {0: Assembly({'L1': 'L'}), 1: Assembly({'M1': 'M'})}]
    
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=assemblies_paths,
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == {
        0: Assembly({'L0': 'L'}), 1: Assembly({'M0': 'M'}),
        2: Assembly({'L1': 'L'}), 3: Assembly({'M1': 'M'})}


def test_paths_order_preservation(tmp_path):
    """Test that the order of the paths is preserved
    regardless of their alphabetical order.
    """
    # The order of the paths is different from their alphabetical order.
    assemblies_paths = [tmp_path / 'B.yaml', tmp_path / 'A.yaml']
    
    with open(tmp_path / 'B.yaml', 'w') as f:
        yaml.dump({0: Assembly({'first': 'first'})}, f)
    with open(tmp_path / 'A.yaml', 'w') as f:
        yaml.dump({0: Assembly({'second': 'second'})}, f)
    
    output_path = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=assemblies_paths,
        resulting_assems_path=str(output_path),
        start=0, overwrite=True, verbose=False)

    with open(output_path, 'r') as f:
        output_data = yaml.safe_load(f)

    # The order of the paths should be preserved.
    assert output_data == {
        0: Assembly({'first': 'first'}), 1: Assembly({'second': 'second'})}


def test_assembly_order_preservation(tmp_path):
    """Test that the order of the assemblies in each file is preserved
    regardless of the alphabetical order of the IDs.
    """
    assemblies_paths = [tmp_path / 'assemblies-0.yaml']
    
    # The order is different from their alphabetical order.
    ASSEMBLIES = [{
        'B': Assembly({'first': 'L'}), 
        'A': Assembly({'second': 'L'}),
        }]
    
    # Save the assemblies preserving the order
    for path, assems in zip(assemblies_paths, ASSEMBLIES):
        with open(path, 'w') as f:
            yaml.dump(assems, f, sort_keys=False)  # keep the order

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=assemblies_paths,
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    # The order of the assemblies should be preserved
    assert output_data == {
        0: Assembly({'first': 'L'}), 1: Assembly({'second': 'L'})}


def test_start(tmp_path):
    ASSEMBLIES = {
        0: Assembly({'L0': 'L'}),
        1: Assembly({'M0': 'M'}),
    }

    filepath = tmp_path / 'assemblies.yaml'
    with open(filepath, 'w') as f:
        yaml.dump(ASSEMBLIES, f)

    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=[filepath],
        resulting_assems_path=str(OUTPUT_PATH),
        start=10, overwrite=True, verbose=False)

    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == {
        10: Assembly({'L0': 'L'}),
        11: Assembly({'M0': 'M'})}


def test_overwrite_true(tmp_path):
    ASSEMBLIES = {0: Assembly({'L0': 'L'})}
    filepath = tmp_path / 'assemblies.yaml'
    with open(filepath, 'w') as f:
        yaml.dump(ASSEMBLIES, f)
    
    OUTPUT_PATH = tmp_path / 'concatenated.yaml'
    with open(OUTPUT_PATH, 'w') as f:
        yaml.dump('previous data', f)

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=[filepath],
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)
    
    with open(OUTPUT_PATH, 'r') as f:
        output_data = yaml.safe_load(f)

    assert output_data == {0: Assembly({'L0': 'L'})}


def test_overwrite_false(tmp_path):
    ASSEMBLIES = {0: Assembly({'L0': 'L'})}
    filepath = tmp_path / 'assemblies.yaml'
    with open(filepath, 'w') as f:
        yaml.dump(ASSEMBLIES, f)
    
    OUTPUT_PATH = tmp_path / 'concatenated.yaml'
    with open(OUTPUT_PATH, 'w') as f:
        yaml.dump('previous data', f)

    with pytest.raises(FileExistsError):
         concatenate_assemblies_without_isom_checks(
            assemblies_path_list=[filepath],
            resulting_assems_path=str(OUTPUT_PATH),
            start=0, overwrite=False, verbose=False)


def test_verbose_true(tmp_path, capsys):
    ASSEMBLIES = {0: Assembly({'L0': 'L'})}
    filepath = tmp_path / 'assemblies.yaml'
    with open(filepath, 'w') as f:
        yaml.dump(ASSEMBLIES, f)
    
    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=[filepath],
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=True)

    captured = capsys.readouterr()
    assert f'Finished reading from "{filepath}"' in captured.out
    assert 'Concatenating assembly lists...' in captured.out
    assert 'Concatenation completed.' in captured.out
    assert f'Successfully saved to "{OUTPUT_PATH}".' in captured.out


def test_verbose_false(tmp_path, capsys):
    ASSEMBLIES = {0: Assembly({'L0': 'L'})}
    filepath = tmp_path / 'assemblies.yaml'
    with open(filepath, 'w') as f:
        yaml.dump(ASSEMBLIES, f)
    
    OUTPUT_PATH = tmp_path / 'concatenated.yaml'

    concatenate_assemblies_without_isom_checks(
        assemblies_path_list=[filepath],
        resulting_assems_path=str(OUTPUT_PATH),
        start=0, overwrite=True, verbose=False)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
