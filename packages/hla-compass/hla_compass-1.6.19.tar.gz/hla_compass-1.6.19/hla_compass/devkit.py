"""Helpers for managing the local devkit docker-compose stack."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Sequence


class DevkitNotFoundError(RuntimeError):
    pass


def find_devkit_dir(start: Optional[Path] = None) -> Path:
    """Return the devkit directory by searching upwards from *start*."""

    origin = Path(start or Path.cwd()).resolve()
    for candidate in [origin, *origin.parents]:
        devkit_dir = candidate / "devkit"
        compose = devkit_dir / "docker-compose.yml"
        if compose.exists():
            return devkit_dir
    raise DevkitNotFoundError("devkit/docker-compose.yml not found. Run this command from the repo root or provide --path.")


def ensure_env_file(devkit_dir: Path) -> Path:
    env_path = devkit_dir / ".env.devkit"
    if env_path.exists():
        return env_path
    template = devkit_dir / ".env.example"
    if template.exists():
        shutil.copy(template, env_path)
    else:
        env_path.touch()
    return env_path


def _compose_base_args(devkit_dir: Path) -> list[str]:
    return ["docker", "compose", "-f", str(devkit_dir / "docker-compose.yml")]


def run_compose(devkit_dir: Path, compose_args: Sequence[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.setdefault("COMPOSE_PROJECT_NAME", "hla-devkit")
    ensure_env_file(devkit_dir)
    cmd = [*_compose_base_args(devkit_dir), *compose_args]
    return subprocess.run(cmd, cwd=devkit_dir, env=env)


def compose_ps(devkit_dir: Path) -> subprocess.CompletedProcess:
    return run_compose(devkit_dir, ["ps"])


def compose_up(devkit_dir: Path, *, build: bool = False) -> subprocess.CompletedProcess:
    args = ["up", "-d"]
    if build:
        args.append("--build")
    return run_compose(devkit_dir, args)


def compose_down(devkit_dir: Path) -> subprocess.CompletedProcess:
    return run_compose(devkit_dir, ["down"])


def compose_logs(devkit_dir: Path, services: Sequence[str] | None = None, follow: bool = False) -> subprocess.CompletedProcess:
    args = ["logs", "--tail", "100"]
    if follow:
        args.append("-f")
    if services:
        args.extend(services)
    return run_compose(devkit_dir, args)


def ready_script_path(devkit_dir: Path) -> Path:
    return devkit_dir / "checks" / "ready.py"


def run_ready_probe(devkit_dir: Path) -> subprocess.CompletedProcess:
    script = ready_script_path(devkit_dir)
    if not script.exists():
        raise FileNotFoundError(script)
    cmd = [sys.executable, str(script)]
    env = os.environ.copy()
    env.setdefault("HLA_DEVKIT_API_PORT", os.environ.get("HLA_DEVKIT_API_PORT", "4100"))
    return subprocess.run(cmd, cwd=devkit_dir, env=env)


def describe_paths(devkit_dir: Path) -> Dict[str, Path]:
    return {
        "devkit": devkit_dir,
        "compose": devkit_dir / "docker-compose.yml",
        "env": devkit_dir / ".env.devkit",
    }
