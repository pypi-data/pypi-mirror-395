"""
Dev loop commands (dev, serve, test, run).
"""

import os
import sys
import json
import click
import subprocess
import uuid
from pathlib import Path
from datetime import datetime, UTC

from rich.panel import Panel

from ..testing import ModuleTester
from ..client import APIClient
from ..config import Config
from ..auth import Auth
from .utils import console, verbose_option, ensure_docker_available, _ensure_verbose
from .module import build, _write_container_serve_script

@click.group()
def dev_group():
    pass

def _build_default_payload(manifest):
    inputs = manifest.get("inputs", {})
    defaults = {}
    # Simplified defaults
    if isinstance(inputs, dict):
        for k, v in inputs.items():
            if isinstance(v, dict) and "default" in v:
                defaults[k] = v["default"]
    return defaults

def _build_runtime_context(manifest, mode="interactive"):
    return {
        "run_id": f"local-{uuid.uuid4().hex[:8]}",
        "job_id": "local",
        "module_id": manifest.get("name", "dev"),
        "environment": Config.get_environment(),
        "mode": mode,
        "requested_at": datetime.now(UTC).isoformat()
    }

def _run_module_container(
    image=None,
    manifest_path=None,
    payload_path=None,
    context_path=None,
    output_dir=None,
    *,
    image_tag=None,
):
    manifest_path = Path(manifest_path) if manifest_path is not None else None
    payload_path = Path(payload_path) if payload_path is not None else None
    context_path = Path(context_path) if context_path is not None else None
    output_dir = Path(output_dir) if output_dir is not None else None

    if not all([manifest_path, payload_path, context_path, output_dir]):
        raise ValueError(
            "manifest_path, payload_path, context_path, and output_dir are required"
        )

    selected_image = image_tag or image
    if not selected_image:
        raise ValueError("image or image_tag is required")

    if output_dir and output_dir.exists():
        for f in output_dir.iterdir():
            f.unlink()

    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{payload_path.resolve()}:/var/input.json:ro",
        "-v",
        f"{context_path.resolve()}:/var/context.json:ro",
        "-v",
        f"{output_dir.resolve()}:/var/dev-out",
        "-v",
        f"{manifest_path.resolve()}:/app/manifest.json:ro",
        "-e",
        "HLA_COMPASS_OUTPUT=/var/dev-out/output.json",
    ]

    api_key = Auth().get_api_key()
    if api_key:
        cmd.extend(["-e", f"HLA_API_KEY={api_key}"])

    cmd.append(selected_image)

    return subprocess.run(cmd).returncode

@click.command()
@verbose_option
@click.option("--mode", default="interactive")
@click.option("--image-tag")
@click.option("--payload", type=click.Path(path_type=Path))
@click.pass_context
def dev(ctx, mode, image_tag, payload):
    """Run module in dev loop"""
    _ensure_verbose(ctx)
    ensure_docker_available()
    
    manifest_path = Path("manifest.json")
    if not manifest_path.exists():
        console.print("[red]manifest.json missing[/red]")
        return
        
    manifest = json.loads(manifest_path.read_text())
    
    # Build image first
    report = ctx.invoke(build, tag=image_tag, push=False)
    image = report.get("image_tag")
    
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    payload_path = payload or dist_dir / "dev-input.json"
    if not payload:
        payload_path.write_text(json.dumps(_build_default_payload(manifest)), encoding="utf-8")
        
    context_path = dist_dir / "dev-context.json"
    context_path.write_text(json.dumps(_build_runtime_context(manifest, mode)), encoding="utf-8")
    
    output_dir = dist_dir / "dev-output"
    output_dir.mkdir(exist_ok=True)
    
    console.print(f"[cyan]Running {image}...[/cyan]")
    try:
        while True:
            rc = _run_module_container(image, manifest_path, payload_path, context_path, output_dir)
            if (output_dir / "output.json").exists():
                console.print((output_dir / "output.json").read_text())
            input("\nPress Enter to re-run...")
    except KeyboardInterrupt:
        pass

@click.command()
@verbose_option
@click.option("--port", default=8080)
@click.pass_context
def serve(ctx, port):
    """Serve module UI locally"""
    _ensure_verbose(ctx)
    ensure_docker_available()
    
    report = ctx.invoke(build, push=False)
    image = report.get("image_tag")
    
    cmd = ["docker", "run", "--rm", "-p", f"{port}:8080", "--entrypoint", "python", image, "/app/container-serve.py"]
    subprocess.run(cmd)

@click.command()
@verbose_option
@click.option("--docker", is_flag=True)
@click.option("--input", type=click.Path(path_type=Path))
@click.option("--output", type=click.Path(path_type=Path))
@click.option("--json", "json_format", is_flag=True)
@click.pass_context
def test(ctx, docker, input, output, json_format):
    """Run tests"""
    if docker:
        ctx.invoke(dev, mode="test", payload=input) 
    else:
        tester = ModuleTester()
        input_data = {}
        if input and input.exists():
            input_data = json.loads(input.read_text())
            
        try:
            result = tester.test_local("backend/main.py", input_data)
            
            if output:
                output.write_text(json.dumps(result, indent=2))
                
            console.print("[green]✓ Test passed[/green]")
        except Exception as e:
            console.print(f"[red]Test failed: {e}[/red]")
            sys.exit(1)

@click.command()
@verbose_option
@click.argument("module_id")
def run(module_id):
    """Run remote module"""
    client = APIClient()
    res = client.start_module_run(module_id)
    console.print(f"Run started: {res['runId']}")
