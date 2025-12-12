"""
Authentication commands for HLA-Compass CLI.
"""
import click
import sys
from typing import Optional
from ..config import Config
from ..auth import Auth
from .utils import console

@click.group()
def auth():
    """Authentication and credential management
    
    Manage your HLA-Compass platform credentials for publishing modules.
    """
    pass

@auth.command("login")
@click.option("--env", 
              type=click.Choice(["dev", "staging", "prod"]), 
              default="dev",
              help="Target environment")
@click.option("--email", 
              required=False,
              help="Your email address (for non-browser login)")
@click.option("--password", 
              required=False,
              help="Your password (for non-browser login)")
# @click.option("--browser/--no-browser", 
#               default=True, 
#               help="Use browser-based SSO login (default)")
# @click.option("--interactive", 
#               is_flag=True, 
#               help="Force interactive prompt login (disable browser)")
def auth_login(env: str, email: Optional[str], password: Optional[str]):
    """Login to HLA-Compass platform
    
    Authenticate with the platform and store credentials securely.
    Defaults to opening a browser for Single Sign-On (SSO).
    
    Use --email/--password for non-browser login.
    """
    Config.set_environment(env)

    try:
        auth_client = Auth()

        # 1. Explicit credentials provided via flags
        if email and password:
            auth_client.login(email=email, password=password, environment=env)
        
        # 2. Partial credentials - require both
        elif email or password:
            raise click.UsageError("Both --email and --password are required for non-browser login.")

        # 3. Default: Browser SSO
        else:
            console.print(f"[bold cyan]Opening browser for SSO login to {env}...[/bold cyan]")
            auth_client.login_browser(environment=env)

        console.print(f"[green]✓[/green] Successfully logged in to {env} environment")
        console.print(f"[dim]Credentials stored in: {Config.get_credentials_path()}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Login failed: {e}[/red]")
        sys.exit(1)

@auth.command("logout")
def auth_logout():
    """Logout and clear stored credentials"""
    try:
        auth_client = Auth()
        auth_client.logout()
        console.print("[green]✓[/green] Successfully logged out")
    except Exception as e:
        console.print(f"[red]Logout failed: {e}[/red]")
        sys.exit(1)

@auth.command("status")
def auth_status():
    """Show current authentication status"""
    try:
        auth_client = Auth()
        status = auth_client.get_status()
        
        from rich.table import Table
        table = Table(title="Authentication Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in status.items():
            table.add_row(key, str(value))
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Failed to check status: {e}[/red]")
        sys.exit(1)

@auth.command("use-org")
@click.argument("org_id")
def auth_use_org(org_id: str):
    """Select a default organization for operations"""
    console.print(f"Selected organization: {org_id}")
