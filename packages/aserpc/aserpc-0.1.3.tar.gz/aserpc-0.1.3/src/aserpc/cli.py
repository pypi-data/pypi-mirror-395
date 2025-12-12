"""Command-line interface for aserpc."""

import functools
import importlib
import logging
from collections.abc import Callable
from importlib.metadata import entry_points
from typing import Annotated, Optional

import typer
import uvloop
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from aserpc.constants import (
    HEARTBEAT_INTERVAL,
    IDLE_TIMEOUT,
    IPC_BACKEND,
    IPC_FRONTEND,
    REQUEST_QUEUE_TIMEOUT,
    WORKER_TIMEOUT,
)

# Entry point group for calculator providers
ENTRY_POINT_GROUP = "aserpc.calculators"

# Type for calculator metadata
CalculatorInfo = dict  # {"factory": "module:callable", "args": [...], "kwargs": {...}}

app = typer.Typer(
    name="aserpc",
    help="RPC framework for ASE calculators over ZeroMQ",
    no_args_is_help=True,
)
console = Console()


def setup_logging(level: str) -> None:
    """Configure logging with rich handler."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


# =============================================================================
# broker command
# =============================================================================


@app.command()
def broker(
    frontend: Annotated[
        str,
        typer.Option(help="Frontend socket address for clients"),
    ] = IPC_FRONTEND,
    backend: Annotated[
        str,
        typer.Option(help="Backend socket address for workers"),
    ] = IPC_BACKEND,
    timeout: Annotated[
        float,
        typer.Option(help="Worker timeout in seconds"),
    ] = WORKER_TIMEOUT,
    queue_timeout: Annotated[
        float,
        typer.Option(help="Request queue timeout in seconds"),
    ] = REQUEST_QUEUE_TIMEOUT,
    log_level: Annotated[
        str,
        typer.Option(help="Logging level"),
    ] = "INFO",
) -> None:
    """Start the message broker."""
    setup_logging(log_level)

    from aserpc.broker import Broker

    b = Broker(
        frontend=frontend,
        backend=backend,
        worker_timeout=timeout,
        request_queue_timeout=queue_timeout,
    )

    console.print("[bold green]Starting broker[/bold green]")
    console.print(f"  Frontend: {frontend}")
    console.print(f"  Backend: {backend}")

    try:
        uvloop.run(b.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Broker stopped[/yellow]")


# =============================================================================
# worker command
# =============================================================================


@app.command()
def worker(
    calculator: Annotated[
        str,
        typer.Argument(
            help="Calculator name or module:callable (e.g., 'lj' or 'mace.calculators:mace_mp')"
        ),
    ],
    name: Annotated[
        Optional[str],
        typer.Option(
            "--name",
            "-n",
            help="Name to register with broker (default: extracted from calculator)",
        ),
    ] = None,
    kwargs: Annotated[
        Optional[str],
        typer.Option(
            help='JSON kwargs for calculator factory (e.g., \'{"model": "medium"}\')'
        ),
    ] = None,
    args: Annotated[
        Optional[str],
        typer.Option(help="JSON args for calculator factory (e.g., '[1, 2]')"),
    ] = None,
    registry: Annotated[
        Optional[str],
        typer.Option(help="Python path to registry (module:variable)"),
    ] = None,
    broker_addr: Annotated[
        str,
        typer.Option("--broker", help="Broker backend socket address"),
    ] = IPC_BACKEND,
    idle_timeout: Annotated[
        float,
        typer.Option("--idle-timeout", help="Idle timeout in seconds"),
    ] = IDLE_TIMEOUT,
    heartbeat: Annotated[
        float,
        typer.Option(help="Heartbeat interval in seconds"),
    ] = HEARTBEAT_INTERVAL,
    log_level: Annotated[
        str,
        typer.Option(help="Logging level"),
    ] = "INFO",
) -> None:
    """Start a worker process for a specific calculator.

    The calculator can be specified as:

    1. A name to lookup from entry points or registry:
       aserpc worker lj
       aserpc worker mace_mp --registry mymodule:CALCS

    2. A direct module:callable path:
       aserpc worker mace.calculators:mace_mp
       aserpc worker mace.calculators:mace_mp --kwargs '{"model": "medium"}'
       aserpc worker ase.calculators.lj:LennardJones --name lj

    Use --name to override the name registered with the broker.
    Use --args and --kwargs to pass arguments to the calculator factory.
    """
    import json

    setup_logging(log_level)

    # Parse args/kwargs if provided
    factory_args: list = []
    factory_kwargs: dict = {}

    if args:
        try:
            factory_args = json.loads(args)
            if not isinstance(factory_args, list):
                console.print("[bold red]--args must be a JSON array[/bold red]")
                raise typer.Exit(1)
        except json.JSONDecodeError as e:
            console.print(f"[bold red]Invalid JSON in --args:[/bold red] {e}")
            raise typer.Exit(1)

    if kwargs:
        try:
            factory_kwargs = json.loads(kwargs)
            if not isinstance(factory_kwargs, dict):
                console.print("[bold red]--kwargs must be a JSON object[/bold red]")
                raise typer.Exit(1)
        except json.JSONDecodeError as e:
            console.print(f"[bold red]Invalid JSON in --kwargs:[/bold red] {e}")
            raise typer.Exit(1)

    # Determine if calculator is a direct module:callable or a name to lookup
    is_direct_factory = ":" in calculator and "." in calculator.split(":")[0]

    if is_direct_factory:
        # Direct module:callable syntax
        try:
            base_factory = load_factory(calculator)
        except Exception as e:
            console.print(f"[bold red]Error loading factory:[/bold red] {e}")
            raise typer.Exit(1)

        # Extract name from callable if not provided
        calc_name = name or calculator.rsplit(":", 1)[1]

        # Wrap factory with args/kwargs if provided
        if factory_args or factory_kwargs:
            factory = functools.partial(base_factory, *factory_args, **factory_kwargs)
        else:
            factory = base_factory
    else:
        # Name-based lookup
        calc_name = name or calculator

        # args/kwargs not supported with name lookup (they're in the registry)
        if factory_args or factory_kwargs:
            console.print(
                "[bold yellow]Warning:[/bold yellow] --args/--kwargs ignored for name-based lookup. "
                "Use direct module:callable syntax or configure in registry."
            )

        try:
            factory = get_calculator_factory(calculator, registry)
        except ValueError as e:
            console.print(f"[bold red]{e}[/bold red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[bold red]Error loading calculator:[/bold red] {e}")
            raise typer.Exit(1)

    from aserpc.worker import Worker

    w = Worker(
        name=calc_name,
        calculator_factory=factory,
        broker=broker_addr,
        idle_timeout=idle_timeout,
        heartbeat_interval=heartbeat,
    )

    console.print("[bold green]Starting worker[/bold green]")
    console.print(f"  Calculator: {calc_name}")
    if is_direct_factory:
        console.print(f"  Factory: {calculator}")
        if factory_kwargs:
            console.print(f"  Kwargs: {factory_kwargs}")
        if factory_args:
            console.print(f"  Args: {factory_args}")
    console.print(f"  Broker: {broker_addr}")

    try:
        uvloop.run(w.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Worker stopped[/yellow]")


# =============================================================================
# status command
# =============================================================================


@app.command()
def status(
    broker_addr: Annotated[
        str,
        typer.Option("--broker", help="Broker frontend socket address"),
    ] = IPC_FRONTEND,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Output as JSON"),
    ] = False,
) -> None:
    """Query broker status."""
    from aserpc.client import broker_status as get_status

    try:
        data = get_status(broker_addr)
    except TimeoutError:
        console.print("[bold red]Timeout - broker not responding[/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

    if json_output:
        import json

        console.print(json.dumps(data, indent=2))
        return

    # Rich table output
    workers = data.get("workers", {})
    pending = data.get("pending_requests", {})

    if not workers:
        console.print("[yellow]No workers connected[/yellow]")
        return

    table = Table(title="Broker Status")
    table.add_column("Calculator", style="cyan")
    table.add_column("Total", justify="right")
    table.add_column("Idle", justify="right", style="green")
    table.add_column("Busy", justify="right", style="yellow")
    table.add_column("Pending", justify="right", style="red")

    for calc_name, info in workers.items():
        table.add_row(
            calc_name,
            str(info.get("total", 0)),
            str(info.get("idle", 0)),
            str(info.get("busy", 0)),
            str(pending.get(calc_name, 0)),
        )

    console.print(table)


# =============================================================================
# list command
# =============================================================================


@app.command("list")
def list_calcs(
    registry: Annotated[
        Optional[str],
        typer.Option(help="Python path to registry (module:variable)"),
    ] = None,
    broker_addr: Annotated[
        Optional[str],
        typer.Option("--broker", help="Broker frontend socket address"),
    ] = None,
) -> None:
    """List available calculators.

    With no options, lists calculators from entry points.
    """
    if registry:
        # List from registry (local)
        try:
            reg = load_registry(registry)
        except Exception as e:
            console.print(f"[bold red]Error loading registry:[/bold red] {e}")
            raise typer.Exit(1)

        table = Table(title="Registry Calculators")
        table.add_column("Name", style="cyan")
        table.add_column("Factory")

        for name, factory in reg.items():
            table.add_row(name, f"{factory.__module__}.{factory.__qualname__}")

        console.print(table)

    elif broker_addr:
        # List from broker (remote)
        from aserpc.client import list_calculators

        try:
            data = list_calculators(broker_addr)
        except TimeoutError:
            console.print("[bold red]Timeout - broker not responding[/bold red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(1)

        if not data:
            console.print("[yellow]No calculators available[/yellow]")
            return

        table = Table(title="Available Calculators")
        table.add_column("Name", style="cyan")
        table.add_column("Workers", justify="right")

        for name, count in data.items():
            table.add_row(name, str(count))

        console.print(table)

    else:
        # List from entry point providers
        calcs = discover_calculators()

        if not calcs:
            console.print("[yellow]No calculators registered via providers[/yellow]")
            console.print(
                "Use --registry to list from a file, or --broker to list from a running broker"
            )
            return

        table = Table(title="Available Calculators")
        table.add_column("Name", style="cyan")
        table.add_column("Factory")

        for name, info in sorted(calcs.items()):
            table.add_row(name, info["factory"])

        console.print(table)


# =============================================================================
# shutdown command
# =============================================================================


@app.command()
def shutdown(
    broker_addr: Annotated[
        str,
        typer.Option("--broker", help="Broker frontend socket address"),
    ] = IPC_FRONTEND,
    workers: Annotated[
        Optional[str],
        typer.Option(help="Calculator name to shutdown workers for"),
    ] = None,
    all_workers: Annotated[
        bool,
        typer.Option("--all", help="Shutdown all workers"),
    ] = False,
) -> None:
    """Shutdown workers or broker."""
    if workers:
        from aserpc.client import shutdown_workers

        try:
            count = shutdown_workers(workers, broker_addr)
            console.print(f"[green]Shutdown {count} workers for '{workers}'[/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(1)

    elif all_workers:
        console.print("[yellow]Full broker shutdown not yet implemented[/yellow]")
        # TODO: Implement broker shutdown

    else:
        console.print("[yellow]Specify --workers CALC_NAME or --all[/yellow]")
        raise typer.Exit(1)


# =============================================================================
# manager command
# =============================================================================


@app.command()
def manager(
    registry: Annotated[
        Optional[str],
        typer.Option(help="Python path to spawn config registry (module:variable)"),
    ] = None,
    broker_addr: Annotated[
        str,
        typer.Option("--broker", help="Broker backend socket address"),
    ] = IPC_BACKEND,
    heartbeat: Annotated[
        float,
        typer.Option(help="Heartbeat interval in seconds"),
    ] = HEARTBEAT_INTERVAL,
    log_level: Annotated[
        str,
        typer.Option(help="Logging level"),
    ] = "INFO",
) -> None:
    """Start the infrastructure manager for scale-to-zero workers.

    The manager spawns workers on demand when clients request calculators
    that have no available workers. Workers self-terminate after idle timeout.

    Spawn configurations are discovered from entry points (aserpc.spawn group)
    or loaded from a registry file.

    Example registry:

        from aserpc.spawn import SpawnConfig

        def get_spawn_configs():
            return {
                "mace_mp": SpawnConfig(
                    name="mace_mp",
                    command=["uvx", "--with", "mace-torch", "aserpc", "worker", "mace_mp"],
                ),
            }
    """
    setup_logging(log_level)

    from aserpc.manager import Manager
    from aserpc.spawn import get_spawn_configs

    # Load spawn configurations
    try:
        configs = get_spawn_configs(registry)
    except Exception as e:
        console.print(f"[bold red]Error loading spawn configs:[/bold red] {e}")
        raise typer.Exit(1)

    if not configs:
        console.print("[bold red]No spawn configs found[/bold red]")
        console.print(
            "Register spawn configs via entry points (aserpc.spawn) or --registry"
        )
        raise typer.Exit(1)

    m = Manager(
        configs=configs,
        broker=broker_addr,
        heartbeat_interval=heartbeat,
    )

    console.print("[bold green]Starting manager[/bold green]")
    console.print(f"  Broker: {broker_addr}")
    console.print("  Spawn configs:")
    for name, config in configs.items():
        console.print(f"    - {name}: {' '.join(config.command)}")

    try:
        uvloop.run(m.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Manager stopped[/yellow]")


# =============================================================================
# Helper functions
# =============================================================================


def load_registry(path: str) -> dict:
    """Load a calculator registry from a file path or module path.

    Args:
        path: Either "file.py:VARIABLE" or "module.path:variable"

    Returns:
        Registry dict mapping names to factory callables
    """
    if ":" not in path:
        raise ValueError(f"Invalid registry path '{path}', expected 'path:variable'")

    module_path, var_name = path.rsplit(":", 1)

    # Check if it's a file path (ends with .py or contains /)
    if module_path.endswith(".py") or "/" in module_path:
        import importlib.util
        from pathlib import Path

        file_path = Path(module_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"Registry file not found: {file_path}")

        spec = importlib.util.spec_from_file_location("_registry", file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        # Standard module import
        module = importlib.import_module(module_path)

    registry = getattr(module, var_name)

    if not isinstance(registry, dict):
        raise TypeError(f"Registry must be a dict, got {type(registry)}")

    return registry


def discover_calculators() -> dict[str, CalculatorInfo]:
    """Discover calculator metadata from entry point providers.

    Providers are functions that return dict[str, CalculatorInfo] where
    CalculatorInfo is:
        {
            "factory": "module.path:ClassName",  # Required
            "args": [...],                        # Optional
            "kwargs": {...},                      # Optional
        }

    Providers can use importlib.util.find_spec() to check package availability
    without importing heavy dependencies (like torch).

    Returns:
        Dict mapping calculator names to metadata dicts
    """
    eps = entry_points(group=ENTRY_POINT_GROUP)
    all_calcs: dict[str, CalculatorInfo] = {}

    for ep in eps:
        try:
            provider = ep.load()
        except ImportError:
            # Entry point's module not available, skip
            continue

        if not callable(provider):
            continue

        try:
            result = provider()
            if isinstance(result, dict):
                all_calcs.update(result)
        except Exception:
            # Provider function failed, skip
            continue

    return all_calcs


def load_factory(factory_path: str) -> Callable:
    """Load a factory callable from a module path.

    Args:
        factory_path: Path in format "module.path:ClassName"

    Returns:
        The loaded callable
    """
    if ":" not in factory_path:
        raise ValueError(
            f"Invalid factory path '{factory_path}', expected 'module:name'"
        )

    module_path, attr_name = factory_path.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def get_calculator_factory(name: str, registry_path: str | None = None) -> Callable:
    """Get a calculator factory by name.

    Searches in this order:
    1. Registry file (if provided)
    2. Entry point providers

    Args:
        name: Calculator name
        registry_path: Optional path to registry file

    Returns:
        Calculator factory callable (with args/kwargs pre-bound if specified)

    Raises:
        ValueError: If calculator not found
    """
    # Try registry first
    if registry_path:
        reg = load_registry(registry_path)
        if name in reg:
            return reg[name]

    # Try entry point providers
    calcs = discover_calculators()
    if name in calcs:
        info = calcs[name]
        factory = load_factory(info["factory"])

        # If args/kwargs specified, return a wrapped factory
        args = info.get("args", [])
        kwargs = info.get("kwargs", {})
        if args or kwargs:
            return lambda: factory(*args, **kwargs)
        return factory

    # Not found
    available = list(calcs.keys())
    if registry_path:
        try:
            reg = load_registry(registry_path)
            available.extend(reg.keys())
        except Exception:
            pass

    raise ValueError(
        f"Calculator '{name}' not found. Available: {sorted(set(available)) or 'none'}"
    )


def main() -> None:
    """Entry point."""
    app()


if __name__ == "__main__":
    main()
