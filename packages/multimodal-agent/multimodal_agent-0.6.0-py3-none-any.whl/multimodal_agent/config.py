from functools import lru_cache
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "local_learning": True,
    "project_paths": [],
    "preferred_architecture": None,
    "include_analysis_options": True,
    "max_learn_files": 500,
    "embedding_model": "text-embedding-004",
}

CONFIG_PATH = Path.home() / ".multimodal_agent" / "config.yaml"


def ensure_config_file():
    """Create default config file if missing."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)


@lru_cache
def get_config():
    ensure_config_file()

    try:
        with open(CONFIG_PATH, "r") as f:
            user_cfg = yaml.safe_load(f) or {}
    except Exception:
        user_cfg = {}

    merged = DEFAULT_CONFIG.copy()
    merged.update(user_cfg)

    return merged
