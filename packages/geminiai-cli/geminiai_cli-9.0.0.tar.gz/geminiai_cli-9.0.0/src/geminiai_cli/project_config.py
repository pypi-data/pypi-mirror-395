import os
import sys

# Standard library TOML support in 3.11+, fallback to tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        # If tomli is missing on old python, we just won't load toml config
        tomllib = None

def load_project_config():
    """
    Load configuration from pyproject.toml or geminiai.toml in the current directory.
    Returns a dictionary of {arg_name: value}.
    
    Priority:
    1. geminiai.toml ([tool.geminiai] or root)
    2. pyproject.toml ([tool.geminiai])
    """
    if not tomllib:
        return {}

    # 1. geminiai.toml
    if os.path.exists("geminiai.toml"):
        try:
            with open("geminiai.toml", "rb") as f:
                data = tomllib.load(f)
                # Check if it has [tool.geminiai] or just keys
                if "tool" in data and "geminiai" in data["tool"]:
                    return data["tool"]["geminiai"]
                return data # Assume root keys if no [tool.geminiai]
        except Exception:
            pass

    # 2. pyproject.toml
    if os.path.exists("pyproject.toml"):
        try:
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
                if "tool" in data and "geminiai" in data["tool"]:
                    return data["tool"]["geminiai"]
        except Exception:
            pass
            
    return {}

def normalize_config_keys(config):
    """
    Normalize config keys to match argparse dest names.
    TOML uses 'backup-dir', argparse uses 'backup_dir' (or we map it).
    """
    normalized = {}
    for k, v in config.items():
        # Convert kebab-case to snake_case
        key = k.replace("-", "_")
        normalized[key] = v
    return normalized
