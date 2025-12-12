"""aserpc - RPC framework for ASE calculators over ZeroMQ."""

try:
    from aserpc._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0.dev0"
    __version_tuple__ = (0, 0, 0, "dev0")

from aserpc.broker import Broker
from aserpc.client import (
    RemoteCalculator,
    broker_status,
    list_calculators,
    shutdown_workers,
)
from aserpc.manager import Manager
from aserpc.spawn import SpawnConfig
from aserpc.worker import Worker

__all__ = [
    "Broker",
    "Manager",
    "SpawnConfig",
    "Worker",
    "RemoteCalculator",
    "list_calculators",
    "broker_status",
    "shutdown_workers",
]
