import pytest
import yaml

from nasap_net.pipelines.lib import read_file


def test_basic(tmp_path):
    input_path = tmp_path / "input.yaml"
    data = {"key": "value"}
    with open(input_path, 'w') as f:
        yaml.dump(data, f)
    
    result = read_file(input_path)
    
    assert result == data


def test_nonexistent():
    input_path = "non_existent_file.yaml"
    with pytest.raises(FileNotFoundError):
        read_file(input_path)


def test_invalid_yaml(tmp_path):
    input_path = tmp_path / "invalid.yaml"
    with open(input_path, 'w') as f:
        f.write("key: value: bad_yaml")
    
    with pytest.raises(yaml.YAMLError):
        read_file(input_path)


if __name__ == '__main__':
    pytest.main(['-v', __file__])
