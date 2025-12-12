import pytest
import os
import yaml
from cuepy.config import load_and_validate

def test_load_valid_config(temp_config_file):
    """Test loading a perfectly valid YAML."""
    data, path = load_and_validate(temp_config_file)
    assert data['experiments'][0]['name'] == 'test_exp'
    assert len(data['experiments'][0]['runs']) == 1

def test_missing_experiments_key(tmp_path):
    """Test config that is valid YAML but missing 'experiments' key."""
    p = tmp_path / "bad.yaml"
    p.write_text("config: {log_dir: 'logs'}") # No experiments list
    
    with pytest.raises(ValueError, match="missing required 'experiments' list"):
        load_and_validate(str(p))

def test_empty_experiments_list(tmp_path):
    """Test config with empty experiments list."""
    data = {"experiments": []}
    p = tmp_path / "empty.yaml"
    with open(p, 'w') as f:
        yaml.dump(data, f)
        
    with pytest.raises(ValueError, match="list cannot be empty"):
        load_and_validate(str(p))

def test_missing_script_field(tmp_path):
    """Test experiment missing the 'script' field."""
    data = {
        "experiments": [{
            "name": "bad_exp",
            # "script": "missing", <--- Intentionally removed
            "runs": [{"args": ""}]
        }]
    }
    p = tmp_path / "no_script.yaml"
    with open(p, 'w') as f:
        yaml.dump(data, f)
        
    with pytest.raises(ValueError, match="missing the 'script' field"):
        load_and_validate(str(p))