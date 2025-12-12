"""Constants for aserpc protocol and configuration.

Configuration priority (highest to lowest):
1. Environment variables (ASERPC_*)
2. pyproject.toml [tool.aserpc] section
3. Default values

IPC directory defaults to .aserpc in the project root (where pyproject.toml is found),
or in the current working directory if no pyproject.toml is found.
"""

import os
import tomllib
from pathlib import Path
from typing import Any

# Protocol version (not configurable)
PROTOCOL_VERSION = 1

# Message types (single byte for efficiency, not configurable)
READY = b"\x01"  # Worker -> Broker: ready/heartbeat (also used for re-registration)
BUSY = b"\x03"  # Worker -> Broker: still alive (processing)
REQUEST = b"\x04"  # Client -> Broker: calculation request
RESPONSE = b"\x05"  # Broker -> Client: calculation response
LIST = b"\x06"  # Client -> Broker: list available calculators
STATUS = b"\x07"  # Client -> Broker: broker status query
SHUTDOWN = b"\x08"  # Broker -> Worker: shutdown command
WORKER_SHUTDOWN = b"\x09"  # Client -> Broker: shutdown workers
ERROR = b"\x0a"  # Broker -> Client: error response
DISCONNECT = b"\x0b"  # Worker -> Broker: worker disconnecting

# Manager-related message types
SPAWN_REQUEST = b"\x0c"  # Broker -> Manager: spawn a worker
SPAWN_RESPONSE = b"\x0d"  # Manager -> Broker: spawn result
MANAGER_READY = (
    b"\x0e"  # Manager -> Broker: ready/heartbeat (also used for re-registration)
)

# Message type names for logging
MESSAGE_NAMES = {
    READY: "READY",
    BUSY: "BUSY",
    REQUEST: "REQUEST",
    RESPONSE: "RESPONSE",
    LIST: "LIST",
    STATUS: "STATUS",
    SHUTDOWN: "SHUTDOWN",
    WORKER_SHUTDOWN: "WORKER_SHUTDOWN",
    ERROR: "ERROR",
    DISCONNECT: "DISCONNECT",
    SPAWN_REQUEST: "SPAWN_REQUEST",
    SPAWN_RESPONSE: "SPAWN_RESPONSE",
    MANAGER_READY: "MANAGER_READY",
}


# =============================================================================
# Configuration loading
# =============================================================================


def _find_project_root() -> Path | None:
    """Find project root by searching for pyproject.toml.

    Returns the directory containing pyproject.toml, or None if not found.
    """
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return None


def _load_pyproject_config() -> dict[str, Any]:
    """Load configuration from pyproject.toml [tool.aserpc] section."""
    project_root = _find_project_root()
    if project_root is None:
        return {}

    pyproject = project_root / "pyproject.toml"
    try:
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
        return data.get("tool", {}).get("aserpc", {})
    except Exception:
        return {}


# Cache for config to avoid repeated file reads
_config_cache: dict[str, Any] | None = None


def _get_cached_config() -> dict[str, Any]:
    """Get cached pyproject.toml config."""
    global _config_cache
    if _config_cache is None:
        _config_cache = _load_pyproject_config()
    return _config_cache


def _get_config(key: str, default: Any, cast: type = str) -> Any:
    """Get configuration value with priority: env var > pyproject.toml > default.

    Environment variables are prefixed with ASERPC_ and uppercased.
    Example: ipc_dir -> ASERPC_IPC_DIR
    """
    # 1. Check environment variable
    env_key = f"ASERPC_{key.upper()}"
    env_val = os.environ.get(env_key)
    if env_val is not None:
        if cast is bool:
            return env_val.lower() in ("true", "1", "yes")
        return cast(env_val)

    # 2. Check pyproject.toml
    config = _get_cached_config()
    if key in config:
        return cast(config[key])

    # 3. Return default
    return default


def _get_default_ipc_dir() -> str:
    """Get default IPC directory.

    Returns .aserpc in the project root (if pyproject.toml found),
    otherwise .aserpc in the current working directory.
    """
    project_root = _find_project_root()
    base_dir = project_root if project_root is not None else Path.cwd()
    return str(base_dir / ".aserpc")


# =============================================================================
# Configurable values
# =============================================================================

# IPC directory - defaults to .aserpc in project root or CWD
# Can also be set to absolute path like /tmp/aserpc
IPC_DIR = Path(_get_config("ipc_dir", _get_default_ipc_dir(), str))

# IPC socket addresses (derived from IPC_DIR if not explicitly set)
IPC_FRONTEND = _get_config("ipc_frontend", f"ipc://{IPC_DIR}/frontend.ipc", str)
IPC_BACKEND = _get_config("ipc_backend", f"ipc://{IPC_DIR}/backend.ipc", str)

# Timeouts (seconds)
WORKER_TIMEOUT = _get_config("worker_timeout", 30.0, float)
HEARTBEAT_INTERVAL = _get_config("heartbeat_interval", 5.0, float)
IDLE_TIMEOUT = _get_config("idle_timeout", 300.0, float)
REQUEST_QUEUE_TIMEOUT = _get_config("request_queue_timeout", 60.0, float)

# Client defaults
CLIENT_TIMEOUT_MS = _get_config("client_timeout_ms", 60000, int)
