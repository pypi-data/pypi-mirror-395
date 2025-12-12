"""
Devkit management commands.
"""

import click
import sys
from .utils import console, verbose_option, ensure_docker_available, _ensure_verbose
from ..devkit import (
    compose_up, compose_down, compose_ps, 
    compose_logs, find_devkit_dir, describe_paths
)

@click.group()
def devkit():
    """Manage local devkit stack"""
    pass

@devkit.command("up")
@verbose_option
@click.option("--build", is_flag=True)
def devkit_up(build):
    ensure_docker_available()
    d = find_devkit_dir()
    compose_up(d, build=build)
    console.print("[green]Devkit started[/green]")

@devkit.command("down")
def devkit_down():
    ensure_docker_available()
    compose_down(find_devkit_dir())

@devkit.command("status")
def devkit_status():
    ensure_docker_available()
    compose_ps(find_devkit_dir())
