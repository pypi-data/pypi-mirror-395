# src/zipbundler/constants.py
"""Central constants used across the project."""

RUNTIME_MODES = {
    "standalone",  # single stitched file
    "installed",  # poetry-installed / pip-installed / importable
    "zipapp",  # .pyz bundle
}

# --- env keys ---
DEFAULT_ENV_LOG_LEVEL: str = "LOG_LEVEL"
DEFAULT_ENV_RESPECT_GITIGNORE: str = "RESPECT_GITIGNORE"
DEFAULT_ENV_WATCH_INTERVAL: str = "WATCH_INTERVAL"

# --- program defaults ---
DEFAULT_LOG_LEVEL: str = "detail"
DEFAULT_WATCH_INTERVAL: float = 1.0  # seconds

# --- config defaults ---
DEFAULT_STRICT_CONFIG: bool = True
DEFAULT_DRY_RUN: bool = False
