import json
import os
import logging

logging.basicConfig(level=logging.INFO)

def load_config(path: str) -> dict:
    """Load configuration from a JSON file."""
    if not os.path.exists(path):
        logging.error(f"Config file not found: {path}")
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, 'r') as f:
        config = json.load(f)
    logging.info(f"Loaded config from {path}")
    return config

def save_config(config: dict, path: str) -> None:
    """Save configuration to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(config, f, indent=4)
    logging.info(f"Saved config to {path}")

def update_config(path: str, updates: dict) -> dict:
    """Update existing config file with new values."""
    config = load_config(path)
    config.update(updates)
    save_config(config, path)
    logging.info(f"Updated config at {path}")
    return config