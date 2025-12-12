"""
Shared CLI utilities, console, and common options.
"""

import logging
import subprocess
import sys
import click
from rich.console import Console

console = Console()
# class DummyConsole:
#     def print(self, *args, **kwargs):
#         import sys
#         sys.stderr.write(f"{args}\n")
#     def log(self, *args, **kwargs):
#         pass
# console = DummyConsole()

VERBOSE_MODE = False
_VERBOSE_INITIALIZED = False

def _enable_verbose(ctx: click.Context | None = None):
    """Turn on verbose logging globally and remember the state."""
    global VERBOSE_MODE, _VERBOSE_INITIALIZED
    VERBOSE_MODE = True
    if ctx is not None:
        ctx.ensure_object(dict)
        ctx.obj["verbose"] = True

    if not _VERBOSE_INITIALIZED:
        logging.basicConfig(level=logging.DEBUG)
        _VERBOSE_INITIALIZED = True
        console.log("Verbose mode enabled")

    logging.getLogger().setLevel(logging.DEBUG)

def _ensure_verbose(ctx: click.Context | None = None):
    """Apply verbose mode when previously enabled on the parent context."""
    if ctx is None:
        return
    ctx.ensure_object(dict)
    if ctx.obj.get("verbose"):
        _enable_verbose(ctx)

def _handle_command_verbose(ctx: click.Context, _param: click.Option, value: bool):
    if value:
        _enable_verbose(ctx)
    return value

def verbose_option(command):
    """Decorator to add --verbose flag to commands."""
    return click.option(
        "--verbose",
        is_flag=True,
        expose_value=False,
        is_eager=True,
        help="Enable verbose logging output for troubleshooting",
        callback=_handle_command_verbose,
    )(command)

def ensure_docker_available() -> None:
    try:
        subprocess.run(
            ["docker", "version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError:
        console.print("[red]Docker CLI not found. Install Docker to continue.[/red]")
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        console.print("[red]Docker is not available:[/red]")
        console.print(exc.stderr.decode("utf-8") if exc.stderr else "")
        sys.exit(exc.returncode)
