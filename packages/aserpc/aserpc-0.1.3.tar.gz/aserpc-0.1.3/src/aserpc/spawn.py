"""Spawn configuration for scale-to-zero worker management.

This module provides:
- SpawnConfig: Configuration for spawning calculator workers
- discover_spawn_configs: Discovery via entry points (aserpc.spawn group)
- load_spawn_registry: Load configs from a Python module

Example registry:
    # myproject/aserpc.py
    from aserpc.spawn import SpawnConfig

    def get_spawn_configs() -> dict[str, SpawnConfig]:
        return {
            "mace_mp": SpawnConfig(
                name="mace_mp",
                command=["uvx", "--with", "mace-torch", "aserpc", "worker", "mace_mp"],
            ),
        }

Register via entry points in pyproject.toml:
    [project.entry-points."aserpc.spawn"]
    myproject = "myproject.aserpc:get_spawn_configs"
"""

from __future__ import annotations

import importlib
import logging
from dataclasses import dataclass
from importlib.metadata import entry_points

from aserpc.constants import IPC_BACKEND, IDLE_TIMEOUT

log = logging.getLogger(__name__)


@dataclass
class SpawnConfig:
    """Configuration for spawning a calculator worker.

    Attributes:
        name: Calculator name (must match what workers register with)
        command: Command to spawn the worker. Can include template variables:
            - {name}: Calculator name
            - {broker}: Broker backend address
            - {idle_timeout}: Idle timeout in seconds
        env: Additional environment variables for the subprocess
        cwd: Working directory for the subprocess
        idle_timeout: Worker idle timeout in seconds (passed to worker)
    """

    name: str
    command: list[str]
    env: dict[str, str] | None = None
    cwd: str | None = None
    idle_timeout: float = IDLE_TIMEOUT

    def render_command(self, broker: str = IPC_BACKEND) -> list[str]:
        """Render command with template variables substituted.

        Args:
            broker: Broker backend address

        Returns:
            Command list with variables substituted
        """
        variables = {
            "name": self.name,
            "broker": broker,
            "idle_timeout": str(self.idle_timeout),
        }
        return [arg.format(**variables) for arg in self.command]


def discover_spawn_configs() -> dict[str, SpawnConfig]:
    """Discover spawn configs from entry points.

    Entry points are registered in the 'aserpc.spawn' group.
    Each entry point should be a callable that returns dict[str, SpawnConfig].

    Returns:
        Dictionary mapping calculator names to spawn configs
    """
    configs: dict[str, SpawnConfig] = {}
    eps = entry_points(group="aserpc.spawn")

    for ep in eps:
        try:
            provider = ep.load()
            provider_configs = provider()
            if isinstance(provider_configs, dict):
                for name, config in provider_configs.items():
                    if isinstance(config, SpawnConfig):
                        configs[name] = config
                    else:
                        log.warning(
                            f"Entry point {ep.name}: config for '{name}' is not a SpawnConfig"
                        )
            else:
                log.warning(f"Entry point {ep.name}: provider did not return a dict")
        except Exception as e:
            log.warning(f"Failed to load spawn config from entry point {ep.name}: {e}")

    return configs


def load_spawn_registry(path: str) -> dict[str, SpawnConfig]:
    """Load spawn configs from a Python module path.

    Args:
        path: Module path in format 'module:variable' or 'module:function'
              e.g., 'myproject.aserpc:SPAWN_CONFIGS'
              e.g., 'myproject.aserpc:get_spawn_configs'

    Returns:
        Dictionary mapping calculator names to spawn configs

    Raises:
        ValueError: If path format is invalid
        ImportError: If module cannot be imported
        AttributeError: If variable/function not found in module
    """
    if ":" not in path:
        raise ValueError(f"Invalid registry path '{path}': expected 'module:variable'")

    module_path, attr_name = path.rsplit(":", 1)
    module = importlib.import_module(module_path)
    obj = getattr(module, attr_name)

    # If it's callable, call it to get the configs
    if callable(obj):
        obj = obj()

    if not isinstance(obj, dict):
        raise TypeError(f"Registry '{path}' must be or return a dict, got {type(obj)}")

    # Validate configs
    configs: dict[str, SpawnConfig] = {}
    for name, config in obj.items():
        if isinstance(config, SpawnConfig):
            configs[name] = config
        elif isinstance(config, dict):
            # Allow dict-based configs for convenience
            configs[name] = SpawnConfig(name=name, **config)
        else:
            raise TypeError(
                f"Config for '{name}' must be SpawnConfig or dict, got {type(config)}"
            )

    return configs


def get_spawn_configs(registry_path: str | None = None) -> dict[str, SpawnConfig]:
    """Get spawn configs from registry or entry points.

    Args:
        registry_path: Optional path to registry module (module:variable format).
                      If None, discovers from entry points.

    Returns:
        Dictionary mapping calculator names to spawn configs
    """
    if registry_path:
        return load_spawn_registry(registry_path)
    return discover_spawn_configs()
