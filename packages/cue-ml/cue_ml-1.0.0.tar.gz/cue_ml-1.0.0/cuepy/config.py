# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import os
import yaml 

def load_and_validate(config_path):
    """Loads a YAML/JSON config file, validates its schema, and returns the data."""
    abs_path = os.path.abspath(config_path)
    
    if not os.path.exists(abs_path): 
        raise FileNotFoundError(f"Config file not found at {abs_path}")

    # Detect format by extension (mostly for error context, as safe_load handles JSON too)
    ext = os.path.splitext(abs_path)[1].lower()
    
    try:
        with open(abs_path, 'r') as f:
            # yaml.safe_load parses both standard YAML and JSON (since JSON is valid YAML)
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Parsing error in {ext} file: {e}")
                    
    except Exception as e: 
        raise ValueError(f"Error reading {ext} file: {e}")

    if not data: 
        raise ValueError("Config file is empty.")

    # perform deep structure validation before returning
    _validate_structure(data)

    return data, abs_path

def resolve_script_path(config_path_abs, script_relative):
    """Resolves the script path relative to the location of the config file."""
    config_dir = os.path.dirname(config_path_abs)
    return os.path.normpath(os.path.join(config_dir, script_relative))

def _validate_structure(data):
    """Deep validation to ensure all required keys exist before execution starts."""
    
    # 1. Top-level validation
    if 'experiments' not in data: 
        raise ValueError("Config missing required 'experiments' list.")
    
    if not isinstance(data['experiments'], list): 
        raise ValueError("'experiments' must be a list.")

    if not data['experiments']:
        raise ValueError("'experiments' list cannot be empty.")

    # 2. Iterate through every experiment to check required fields
    for idx, exp in enumerate(data['experiments']):
        # Check Script path presence
        if 'script' not in exp:
            raise ValueError(f"Experiment #{idx+1} is missing the 'script' field.")
        
        # Check Runs list presence
        if 'runs' not in exp:
            name = exp.get('name', 'unnamed')
            raise ValueError(f"Experiment #{idx+1} ({name}) is missing 'runs' list.")
            
        if not isinstance(exp['runs'], list):
            raise ValueError(f"Experiment #{idx+1} 'runs' must be a list.")

        # 3. Validate individual Run arguments
        for r_idx, run in enumerate(exp['runs']):
            if 'args' not in run:
                raise ValueError(f"Run #{r_idx+1} in Experiment #{idx+1} is missing 'args'.")
            
            # Optional: Validate GPU request if present
            if 'gpus' in run:
                if not isinstance(run['gpus'], int) or run['gpus'] < 1:
                    raise ValueError(f"Run #{r_idx+1}: 'gpus' must be a positive integer.")