from pathlib import Path

import numpy as np
import toml
from numpy import genfromtxt
from scipy.interpolate import interp1d


def prepare_config_for_toml(config):
    """Prepare configuration data for TOML export by converting unsupported types"""
    if isinstance(config, dict):
        result = {}
        for key, value in config.items():
            result[key] = prepare_config_for_toml(value)
        return result
    elif isinstance(config, list):
        return [prepare_config_for_toml(item) for item in config]
    elif isinstance(config, complex):
        return {"__complex__": True, "real": float(config.real), "imag": float(config.imag)}
    elif isinstance(config, np.ndarray):
        return config.tolist()
    elif isinstance(config, (np.integer, np.int32, np.int64)):
        return int(config)
    elif isinstance(config, (np.floating, np.float32, np.float64)):
        return float(config)
    elif isinstance(config, (np.complex128, np.complex64)):
        return {"__complex__": True, "real": float(config.real), "imag": float(config.imag)}
    else:
        return config


def restore_config_from_toml(config):
    """Restore configuration data from TOML by converting back to original types"""
    if isinstance(config, dict):
        # Check if this is a complex number representation
        if "__complex__" in config and config.get("__complex__") is True:
            return complex(config["real"], config["imag"])
        else:
            result = {}
            for key, value in config.items():
                result[key] = restore_config_from_toml(value)
            return result
    elif isinstance(config, list):
        return [restore_config_from_toml(item) for item in config]
    else:
        return config


def load_config_from_toml(filename, load_csv=False):
    """
    Load configuration from a TOML file and restore original data types

    Args:
        filename (str): Path to the TOML file

    Returns:
        dict: Configuration dictionary with restored data types

    Raises:
        FileNotFoundError: If the file doesn't exist
        toml.TomlDecodeError: If the file is not valid TOML
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            toml_data = toml.load(f)

        # Restore the config from a toml file
        config = restore_config_from_toml(toml_data)

        if load_csv:
            for layer in config['mut']:
                if isinstance(layer['epsilon_r'], str):
                    path = layer['epsilon_r']
                    if path.startswith('./'):
                        path = path.replace('./', str(Path(filename).parent) + '/')

                    skip_header = 1
                    # check if thickness is stored in the file
                    with open(path, 'r') as f:
                        f.readline()
                        second_line = f.readline().strip()
                        if second_line.startswith('#') and 'Thickness_mm' in second_line:
                            # Extract thickness in mm and store it in meter
                            skip_header = 2
                            thickness_mm = float(second_line.split()[1])
                            layer['thickness'] = thickness_mm * .001

                    data = genfromtxt(path, delimiter=',', skip_header=skip_header)
                    layer['epsilon_r'] = interp1d(data[:, 0], data[:, 1] + data[:, 2] * 1j, fill_value='extrapolate')

        return config

    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{filename}' not found")
    except toml.TomlDecodeError as e:
        raise toml.TomlDecodeError(f"Invalid TOML format in '{filename}': {str(e)}")


def save_config_to_toml(config, filename, header_comment=None):
    """
    Save configuration to a TOML file with proper type conversion

    Args:
        config (dict): Configuration dictionary to save
        filename (str): Path where to save the TOML file
        header_comment (str, optional): Optional header comment to add to the file

    Raises:
        IOError: If the file cannot be written
    """
    try:
        # Prepare config for TOML
        toml_config = prepare_config_for_toml(config)

        with open(filename, 'w', encoding='utf-8') as f:
            # Add header comment if provided
            if header_comment:
                f.write(f"# {header_comment}\n")
                f.write(f"# Generated automatically\n\n")

            # Write TOML format
            toml.dump(toml_config, f)

    except IOError as e:
        raise IOError(f"Cannot write to file '{filename}': {str(e)}")


# Utility functions for validation and inspection
def validate_toml_file(filename):
    """
    Validate if a file is a valid TOML file

    Args:
        filename (str): Path to the file to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            toml.load(f)
        return True, None
    except FileNotFoundError:
        return False, f"File '{filename}' not found"
    except toml.TomlDecodeError as e:
        return False, f"Invalid TOML format: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def inspect_config_types(config, path=""):
    """
    Inspect the types in a configuration dictionary (useful for debugging)

    Args:
        config: Configuration data to inspect
        path (str): Current path in the nested structure

    Returns:
        list: List of (path, type, value_preview) tuples
    """
    results = []

    if isinstance(config, dict):
        if "__complex__" in config and config.get("__complex__") is True:
            complex_val = complex(config["real"], config["imag"])
            results.append((path, "complex", str(complex_val)))
        else:
            for key, value in config.items():
                new_path = f"{path}.{key}" if path else key
                results.extend(inspect_config_types(value, new_path))
    elif isinstance(config, list):
        for i, item in enumerate(config):
            new_path = f"{path}[{i}]"
            results.extend(inspect_config_types(item, new_path))
    else:
        value_preview = str(config)
        if len(value_preview) > 50:
            value_preview = value_preview[:47] + "..."
        results.append((path, type(config).__name__, value_preview))

    return results
