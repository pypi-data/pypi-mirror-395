import os

import pytest
import yaml

from nasap_net.pipelines.lib.saving import write_output


def test_creates_file(tmp_path):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data)
    
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == data


def test_overwrite_false(tmp_path):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data)
    
    with pytest.raises(FileExistsError):
        write_output(output_path, data, overwrite=False)


def test_overwrite_true(tmp_path):
    output_path = tmp_path / "output.yaml"
    data1 = {"key": "value1"}
    data2 = {"key": "value2"}
    
    write_output(output_path, data1)
    write_output(output_path, data2, overwrite=True)
    
    with open(output_path, 'r') as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == data2


def test_default_flow_style_true(tmp_path):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data, default_flow_style=True)
    
    with open(output_path, 'r') as f:
        content = f.read()
    assert "{key: value}" in content


def test_default_flow_style_false(tmp_path):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data, default_flow_style=False)
    
    with open(output_path, 'r') as f:
        content = f.read()
    assert "key: value" in content


def test_verbose_true(tmp_path, capsys):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data, verbose=True)
    
    captured = capsys.readouterr()
    assert f'Saving the results to "{output_path}"...' in captured.out


def test_verbose_false(tmp_path, capsys):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(output_path, data, verbose=False)
    
    captured = capsys.readouterr()
    assert f'Saving the results to "{output_path}"...' not in captured.out


def test_write_output_with_filename_only(tmp_path):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    
    write_output(str(output_path), data)
    
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == data


def test_header_with_verbose(tmp_path, capsys):
    output_path = tmp_path / "output.yaml"
    data = {"key": "value"}
    header = "Test Header"
    
    write_output(output_path, data, verbose=True, header=header)
    
    captured = capsys.readouterr()
    assert f'{header}: Successfully saved to "{output_path}".' in captured.out


if __name__ == '__main__':
    pytest.main(['-v', __file__])
