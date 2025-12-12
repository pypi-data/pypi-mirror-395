import pytest
import os
from utils import load_config, save_config, update_config

def test_save_and_load_config(tmp_path):
    path = tmp_path / "config.json"
    config = {"env": "dev", "debug": True}
    save_config(config, path)
    loaded = load_config(path)
    assert loaded == config

def test_update_config(tmp_path):
    path = tmp_path / "config.json"
    save_config({"env": "dev"}, path)
    updated = update_config(path, {"debug": True})
    assert updated["debug"] is True
    assert updated["env"] == "dev"