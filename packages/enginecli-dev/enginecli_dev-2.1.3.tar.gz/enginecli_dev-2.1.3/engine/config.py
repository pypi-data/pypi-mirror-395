"""
Configuration management for Engine CLI.
"""
import json
from pathlib import Path
from typing import Optional, Any


# Config directory
ENGINE_DIR = Path.home() / ".engine"
CONFIG_FILE = ENGINE_DIR / "config.json"

# Defaults
DEFAULT_CONFIG = {
    "api_url": "https://api.engine.dev",
    "index_file": ".engine/index.json",
    "max_context_tokens": 8000,
    "default_language": "python",
}


def ensure_engine_dir():
    """Create .engine directory if it doesn't exist."""
    ENGINE_DIR.mkdir(parents=True, exist_ok=True)


def get_config() -> dict:
    """Load configuration."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE) as f:
            user_config = json.load(f)
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG.copy()


def set_config(key: str, value: Any):
    """Set a configuration value."""
    ensure_engine_dir()
    
    config = get_config()
    config[key] = value
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific configuration value."""
    config = get_config()
    return config.get(key, default)


# Project-level config
def get_project_config(project_dir: Path = None) -> dict:
    """Get project-level configuration from engine.yaml or .engine/config.json."""
    if project_dir is None:
        project_dir = Path.cwd()
    
    # Try engine.yaml first
    yaml_file = project_dir / "engine.yaml"
    if yaml_file.exists():
        try:
            import yaml
            with open(yaml_file) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass  # yaml not installed
        except Exception:
            pass
    
    # Try .engine/config.json
    json_file = project_dir / ".engine" / "config.json"
    if json_file.exists():
        try:
            with open(json_file) as f:
                return json.load(f)
        except Exception:
            pass
    
    return {}


def get_api_url() -> str:
    """Get the API URL."""
    # Check environment variable first
    import os
    env_url = os.environ.get("ENGINE_API_URL")
    if env_url:
        return env_url
    
    return get_config_value("api_url", DEFAULT_CONFIG["api_url"])
