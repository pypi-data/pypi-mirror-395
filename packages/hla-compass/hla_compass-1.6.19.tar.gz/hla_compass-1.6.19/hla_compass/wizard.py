"""
Interactive wizard for HLA-Compass module creation

Guides users through module setup with intelligent questions and code generation.
"""

import re
import shutil
import subprocess
import sys
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .generators import CodeGenerator

console = Console()

# Custom style for the wizard
WIZARD_STYLE = Style([
    ('qmark', 'fg:#667eea bold'),       # Purple question mark
    ('question', 'bold'),                # Bold questions
    ('answer', 'fg:#10b981 bold'),      # Green answers
    ('pointer', 'fg:#667eea bold'),     # Purple pointer
    ('highlighted', 'fg:#667eea bold'), # Purple highlights
    ('selected', 'fg:#10b981'),         # Green selected
    ('separator', 'fg:#6b7280'),        # Gray separator
    ('instruction', 'fg:#6b7280'),      # Gray instructions
    ('text', ''),
    ('disabled', 'fg:#6b7280 italic'),
])


class ModuleWizard:
    """Interactive wizard for module creation"""
    
    def __init__(self):
        self.generator = CodeGenerator()
        self.config = {}
        
    def run(self) -> Dict[str, Any]:
        """Run the interactive wizard and return configuration"""

        # Welcome message
        self._show_welcome()

        # Step 1: Module name
        self.config.update(self._ask_basic_info())

        # Step 2: UI choice (critical architectural decision)
        self.config.update(self._ask_module_type())

        # Step 3: Optional dependencies
        self.config['dependencies'] = self._ask_dependencies()

        # Set sensible defaults for everything else
        self._set_defaults()

        # Step 4: Confirm and generate
        if self._confirm_configuration():
            return self.config
        else:
            console.print("\n[yellow]Module creation cancelled[/yellow]")
            return None
    
    def _show_welcome(self):
        """Display welcome message"""
        console.print(Panel.fit(
            "[bold bright_magenta]🧬 HLA-Compass Module Creation Wizard[/bold bright_magenta]\n\n"
            "Quick setup to get you started:\n"
            "• Choose module name\n"
            "• Pick UI or backend-only\n"
            "• Select common dependencies (optional)\n\n"
            "The wizard generates a working template with sensible defaults.\n"
            "You can customize everything after generation.\n\n"
            "[dim]Press Ctrl+C at any time to cancel[/dim]",
            title="Welcome",
            border_style="bright_magenta"
        ))
        console.print()
    
    def _ask_basic_info(self) -> Dict[str, Any]:
        """Ask for basic module information"""
        console.print("[bold cyan]📝 Module Setup[/bold cyan]\n")

        # Load author info from SDK config
        from .cli import load_sdk_config
        import os

        sdk_config = load_sdk_config()
        author_info = sdk_config.get("author", {}) if sdk_config else {}

        default_author = (
            author_info.get("name") or
            os.environ.get("HLA_AUTHOR_NAME") or
            os.environ.get("USER", "Developer")
        )
        default_email = (
            author_info.get("email") or
            os.environ.get("HLA_AUTHOR_EMAIL", "developer@example.com")
        )

        # Ask name, then validate/normalize to a slug
        while True:
            name = questionary.text(
                "Module name:",
                default="my-module",
                style=WIZARD_STYLE,
                validate=lambda x: len(x) > 0
            ).ask()

            slug = self._slugify(name)
            if slug != name:
                accept = questionary.confirm(
                    f"Use normalized name '{slug}'?",
                    default=True,
                    style=WIZARD_STYLE
                ).ask()
                if accept:
                    name = slug
                elif not self._is_valid_module_name(name):
                    console.print("[yellow]Name must contain only letters, numbers, hyphens, or underscores and start with a letter.[/yellow]")
                    continue

            target = Path(name)
            if target.exists() and any(target.iterdir()):
                choice = questionary.select(
                    f"Directory '{name}' already exists and is not empty. What would you like to do?",
                    choices=[
                        "Choose a different name",
                        "Continue and overwrite (may replace files)",
                        "Cancel"
                    ],
                    style=WIZARD_STYLE
                ).ask()
                if choice == "Choose a different name":
                    continue
                if choice == "Cancel":
                    return None
            break

        # Ask for description
        description = questionary.text(
            "Brief description (used in UI and MCP tooling):",
            default=f"HLA-Compass analysis module",
            style=WIZARD_STYLE
        ).ask()

        return {
            'name': name,
            'description': description,
            'author': {'name': default_author, 'email': default_email}
        }
    
    def _ask_module_type(self) -> Dict[str, Any]:
        """Ask about module type"""
        console.print("\n[bold cyan]🎨 Module Type[/bold cyan]\n")

        has_ui = questionary.confirm(
            "Include UI? (React/TypeScript frontend)",
            default=False,
            style=WIZARD_STYLE
        ).ask()

        result = {'has_ui': has_ui}

        if has_ui:
            # Environment check for Node/npm
            node_ok, node_ver, npm_ok, npm_ver, notes = self._check_node_tools()
            if not node_ok or not npm_ok:
                console.print("[yellow]⚠️  Node.js and npm not detected. You'll need Node.js (>=18) and npm to build the frontend.[/yellow]")
            else:
                console.print(f"[dim]✓ Node.js {node_ver}, npm {npm_ver}[/dim]")
                for w in notes:
                    console.print(f"[yellow]  • {w}[/yellow]")

        return result

    def _ask_dependencies(self) -> List[str]:
        """Ask about required dependencies"""
        console.print("\n[bold cyan]📦 Dependencies[/bold cyan]\n")
        console.print("[dim]Select common packages (optional - you can add more later)[/dim]\n")

        # Simplified list of most common packages
        deps = questionary.checkbox(
            "Common packages:",
            choices=[
                "pandas - Data manipulation and analysis",
                "numpy - Numerical computing",
                "requests - HTTP requests and API calls",
                "biopython - Bioinformatics utilities",
            ],
            style=WIZARD_STYLE
        ).ask()

        # Clean up dependency names
        clean_deps = [dep.split(' - ')[0] for dep in deps]

        return clean_deps

    def _set_defaults(self):
        """Set sensible defaults for all configuration not explicitly asked"""
        # Default input schema - simple and flexible
        if 'inputs' not in self.config:
            self.config['inputs'] = {
                'param1': {
                    'type': 'string',
                    'description': 'Primary input parameter',
                    'required': True
                },
                'param2': {
                    'type': 'string',
                    'description': 'Optional parameter',
                    'required': False,
                    'default': 'default_value'
                }
            }

        # Default output schema - flexible structure
        if 'outputs' not in self.config:
            self.config['outputs'] = {
                'results': {
                    'type': 'array',
                    'description': 'Processed results'
                },
                'summary': {
                    'type': 'object',
                    'description': 'Summary statistics'
                },
                'status': {
                    'type': 'string',
                    'description': 'Execution status'
                },
                'metadata': {
                    'type': 'object',
                    'description': 'Execution metadata'
                }
            }

        # Default processing type
        if 'processing_type' not in self.config:
            self.config['processing_type'] = 'Data transformation'
            self.config['features'] = []

    def _confirm_configuration(self) -> bool:
        """Show configuration summary and confirm"""
        console.print("\n[bold cyan]📋 Configuration Summary[/bold cyan]\n")

        # Create summary table
        table = Table(show_header=True, header_style="bold cyan", box=None)
        table.add_column("Setting", style="dim")
        table.add_column("Value", style="bright_white")

        table.add_row("Module Name", self.config['name'])
        table.add_row("Description", self.config['description'])
        table.add_row("Type", "With UI" if self.config.get('has_ui') else "Backend-only")
        table.add_row("Author", f"{self.config['author']['name']} <{self.config['author']['email']}>")

        deps = self.config.get('dependencies', [])
        if deps:
            table.add_row("Dependencies", ", ".join(deps))
        else:
            table.add_row("Dependencies", "[dim]none selected[/dim]")

        console.print(table)
        console.print()

        # Run preflight checks
        ok, warnings, errors = self._preflight_checks()
        self._display_preflight(ok, warnings, errors)

        if errors:
            console.print("\n[red]Cannot proceed with errors. Please fix issues and try again.[/red]")
            return False

        console.print()
        return questionary.confirm(
            "Create module?",
            default=True,
            style=WIZARD_STYLE
        ).ask()
    
    # --- Validation helpers and preflight ---
    def _slugify(self, name: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip())
        if not re.match(r"^[A-Za-z]", slug):
            slug = f"m-{slug}"
        return slug[:64]

    def _is_valid_module_name(self, name: str) -> bool:
        return bool(re.match(r"^[A-Za-z][A-Za-z0-9_-]{1,63}$", name))

    def _is_valid_email(self, email: str) -> bool:
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def _check_node_tools(self) -> Tuple[bool, str, bool, str, List[str]]:
        warnings: List[str] = []
        node_ok = False
        npm_ok = False
        node_ver = ""
        npm_ver = ""
        try:
            node_out = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if node_out.returncode == 0:
                node_ver = node_out.stdout.strip().lstrip('v')
                node_ok = True
                try:
                    major = int(node_ver.split(".")[0])
                    if major < 18:
                        warnings.append(f"Node.js {node_ver} detected; version 18+ is recommended.")
                except Exception:
                    pass
        except Exception:
            pass
        try:
            npm_out = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if npm_out.returncode == 0:
                npm_ver = npm_out.stdout.strip()
                npm_ok = True
        except Exception:
            pass
        return node_ok, node_ver, npm_ok, npm_ver, warnings

    def _preflight_checks(self) -> Tuple[bool, List[str], List[str]]:
        warnings: List[str] = []
        errors: List[str] = []

        # Python version
        py_major, py_minor = sys.version_info[:2]
        if py_major < 3 or (py_major == 3 and py_minor < 8):
            errors.append("Python >= 3.8 required")
        elif py_major == 3 and py_minor < 10:
            warnings.append("Python 3.10+ recommended for best experience")

        # Directory writability
        try:
            test_dir = Path.cwd() / ".wizard_write_test"
            test_dir.mkdir(exist_ok=True)
            (test_dir / "_touch").write_text("ok")
            shutil.rmtree(test_dir)
        except Exception as e:
            errors.append(f"No write permission in current directory: {e}")

        # Module name validity
        name = self.config.get('name', '')
        if not self._is_valid_module_name(name):
            errors.append("Invalid module name format")

        # Email validity
        email = self.config.get('author', {}).get('email', '')
        if not self._is_valid_email(email):
            errors.append("Invalid author email format")

        # Duplicate input names and parameter names format
        inputs = self.config.get('inputs', {})
        if len(inputs) != len(set(inputs.keys())):
            errors.append("Duplicate input parameter names")
        for k in inputs.keys():
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", k):
                errors.append(f"Invalid input parameter name: {k}")

        # Dependencies sanity
        deps = self.config.get('dependencies', []) or []
        if len(deps) != len(set(deps)):
            warnings.append("Duplicate dependencies were specified; duplicates will be ignored")

        # UI environment
        if self.config.get('has_ui'):
            node_ok, node_ver, npm_ok, npm_ver, tool_warnings = self._check_node_tools()
            warnings.extend(tool_warnings)
            if not node_ok:
                warnings.append("Node.js not found; frontend dev/build will not work until installed")
            if not npm_ok:
                warnings.append("npm not found; frontend dev/build will not work until installed")

        return (len(errors) == 0), warnings, errors

    def _display_preflight(self, ok: bool, warnings: List[str], errors: List[str]) -> None:
        console.print("\n[bold cyan]🧪 Preflight Checks[/bold cyan]")
        status = "[green]OK[/green]" if ok and not errors else "[red]Issues detected[/red]"
        console.print(f"Status: {status}")
        if warnings:
            console.print("[yellow]Warnings:[/yellow]")
            for w in warnings:
                console.print(f"  • {w}")
        if errors:
            console.print("[red]Errors:[/red]")
            for e in errors:
                console.print(f"  • {e}")


def run_wizard() -> Optional[Dict[str, Any]]:
    """Run the module creation wizard"""
    try:
        wizard = ModuleWizard()
        config = wizard.run()
        
        if config:
            console.print("\n[green]✓ Configuration complete![/green]")
            console.print("[dim]Generating module files...[/dim]\n")
            return config
        else:
            console.print("\n[yellow]Module creation cancelled or needs revision[/yellow]")
            return None
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Wizard interrupted[/yellow]")
        return None
    except Exception as e:
        console.print(f"\n[red]Wizard error: {e}[/red]")
        return None