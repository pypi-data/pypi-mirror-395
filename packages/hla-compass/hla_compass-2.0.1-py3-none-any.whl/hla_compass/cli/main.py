import click
import logging
# from .. import __version__
from .._version import __version__
from .utils import console, verbose_option, _enable_verbose

from .auth import auth, auth_login, auth_logout, auth_status, auth_use_org
from .module import init, build, publish, validate, preflight
from .dev import dev, serve, test, run
# from .devkit import devkit, devkit_up, devkit_down, devkit_status

@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx, verbose):
    """HLA-Compass SDK"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    if verbose:
        _enable_verbose(ctx)
    else:
        logging.getLogger().setLevel(logging.INFO)

# Register Auth commands
cli.add_command(auth)
# Auth subcommands are already attached to auth group in auth.py,
# but we need to ensure the group is attached to root.

# Register Module commands
cli.add_command(init)
cli.add_command(build)
cli.add_command(publish)
cli.add_command(validate)
cli.add_command(validate, name="validate-module")
cli.add_command(preflight)

# Register Dev commands
cli.add_command(dev)
cli.add_command(serve)
cli.add_command(test)
cli.add_command(run)

# Register Devkit
# cli.add_command(devkit)

# Doctor command (simplified inline for now)
@cli.command()
def doctor():
    """Check environment configuration and dependencies."""
    import shutil
    import sys
    import subprocess
    
    console.print(f"[bold]HLA-Compass SDK v{__version__}[/bold]")
    
    checks = {
        "Python": sys.version.split()[0],
        "Node": bool(shutil.which("node")),
        "Git": bool(shutil.which("git"))
    }
    
    # Docker check
    docker_path = shutil.which("docker")
    docker_status = "Missing"
    if docker_path:
        docker_status = "Available"
        try:
            # Check daemon connectivity
            subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            docker_status += " (Daemon running)"
        except subprocess.CalledProcessError:
            docker_status += " (Daemon not running)"
            
    checks["Docker"] = docker_status
    
    for tool, val in checks.items():
        available = "Missing" not in str(val) and "not running" not in str(val)
        status = "[green]✓[/green]" if available else "[red]✗[/red]"
        console.print(f"{tool}: {status} {val}")
        
    console.print("\n[green]Doctor check complete[/green]")


@cli.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completions(shell):
    """
    Generate shell completion script.
    
    Install completions:
    
        # Bash
        hla-compass completions bash >> ~/.bashrc
        
        # Zsh  
        hla-compass completions zsh >> ~/.zshrc
        
        # Fish
        hla-compass completions fish > ~/.config/fish/completions/hla-compass.fish
    """
    import os
    
    if shell == "bash":
        script = f'eval "$(_HLA_COMPASS_COMPLETE=bash_source hla-compass)"'
    elif shell == "zsh":
        script = f'eval "$(_HLA_COMPASS_COMPLETE=zsh_source hla-compass)"'
    elif shell == "fish":
        script = f'eval (env _HLA_COMPASS_COMPLETE=fish_source hla-compass)'
    
    click.echo(script)


def main():
    cli()

if __name__ == "__main__":
    main()
