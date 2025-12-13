"""
ADEMA CLI - Command Line Interface
==================================

Entry point for the django-adema command.
Provides commands for project/app scaffolding and the Web Wizard launcher.

Commands:
    - startproject: Create a new ADEMA Django project (headless)
    - startapp: Create a new ADEMA app module (headless)
    - launch: Start the interactive Web Wizard UI
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize Typer app and Rich console
app = typer.Typer(
    name="django-adema",
    help="🏭 ADEMA Framework - Django Project Generator for ERP/CRM Applications",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()


def get_package_path() -> Path:
    """Get the path to the installed adema package."""
    return Path(__file__).parent


def get_template_path(template_name: str) -> Path:
    """
    Get the absolute path to a template directory.
    
    Uses importlib.resources for reliable path resolution
    even when the package is installed as a zip/wheel.
    """
    from importlib import resources
    
    try:
        # Python 3.9+ approach
        template_files = resources.files('adema.templates')
        template_path = template_files.joinpath(template_name)
        
        # Convert to actual filesystem path
        with resources.as_file(template_path) as path:
            return Path(path)
    except Exception:
        # Fallback to __file__ based resolution
        return get_package_path() / 'templates' / template_name


def print_banner():
    """Display the ADEMA banner."""
    banner = """
[bold green]    _    ____  _____ __  __    _    [/bold green]
[bold green]   / \\  |  _ \\| ____|  \\/  |  / \\   [/bold green]
[bold green]  / _ \\ | | | |  _| | |\\/| | / _ \\  [/bold green]
[bold green] / ___ \\| |_| | |___| |  | |/ ___ \\ [/bold green]
[bold green]/_/   \\_\\____/|_____|_|  |_/_/   \\_\\[/bold green]

[dim]Arquitectura Django para Emprendedores con Módulos Acoplables[/dim]
    """
    console.print(Panel(banner, border_style="green", padding=(0, 2)))


@app.command()
def startproject(
    name: str = typer.Argument(..., help="Name of the project to create"),
    directory: Optional[str] = typer.Option(
        None, "--directory", "-d",
        help="Directory where the project will be created (default: current directory)"
    ),
    database: str = typer.Option(
        "sqlite", "--database", "-db",
        help="Database backend: sqlite, postgres"
    ),
):
    """
    🚀 Create a new ADEMA Django project.
    
    Creates a complete Django project with the ADEMA architecture:
    modular settings, vertical slicing structure, and pre-configured
    base models and services.
    
    Example:
        django-adema startproject mi_erp
        django-adema startproject mi_erp --database postgres
    """
    print_banner()
    
    console.print(f"\n[bold blue]Creating project:[/bold blue] {name}")
    console.print(f"[dim]Database:[/dim] {database}")
    
    # Get the project template path
    template_path = get_template_path('project_template')
    
    if not template_path.exists():
        console.print(f"[red]Error:[/red] Template not found at {template_path}")
        raise typer.Exit(code=1)
    
    # Determine output directory
    output_dir = Path(directory) if directory else Path.cwd()
    project_dir = output_dir / name
    
    if project_dir.exists():
        console.print(f"[red]Error:[/red] Directory '{project_dir}' already exists")
        raise typer.Exit(code=1)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating project structure...", total=None)
        
        try:
            # Use the generator module to create the project
            from adema.generator.project_builder import ProjectBuilder
            
            config = {
                'name': name,
                'database': {
                    'engine': database
                },
                'output_dir': str(output_dir),
            }
            
            builder = ProjectBuilder(config)
            builder.build()
            
            progress.update(task, description="[green]✓[/green] Project created successfully!")
            
        except ImportError:
            # Fallback: Use django-admin startproject
            progress.update(task, description="Using django-admin startproject...")
            
            cmd = [
                sys.executable, '-m', 'django',
                'startproject',
                '--template', str(template_path),
                '--extension', 'py,txt,env,md,jinja2',
                name,
            ]
            
            if directory:
                cmd.append(directory)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                progress.update(task, description="[red]✗[/red] Error creating project")
                console.print(f"[red]{result.stderr}[/red]")
                raise typer.Exit(code=1)
            
            progress.update(task, description="[green]✓[/green] Project created successfully!")
    
    # Post-creation instructions
    console.print("\n[bold green]🎉 Project created successfully![/bold green]\n")
    console.print("Next steps:")
    console.print(f"  [cyan]cd {name}[/cyan]")
    console.print(f"  [cyan]python -m venv venv[/cyan]")
    console.print(f"  [cyan]pip install -r requirements.txt[/cyan]")
    console.print(f"  [cyan]python manage.py migrate[/cyan]")
    console.print(f"  [cyan]python manage.py runserver[/cyan]")


@app.command()
def startapp(
    name: str = typer.Argument(..., help="Name of the app to create"),
    directory: Optional[str] = typer.Option(
        None, "--directory", "-d",
        help="Directory where the app will be created (default: apps/)"
    ),
):
    """
    📦 Create a new ADEMA app module.
    
    Creates a vertical slice app with the ADEMA structure:
    views/, components/, services/, admin/.
    
    Example:
        django-adema startapp ventas
        django-adema startapp inventario --directory modules/
    """
    print_banner()
    
    console.print(f"\n[bold blue]Creating app:[/bold blue] {name}")
    
    # Get the app template path
    template_path = get_template_path('app_template')
    
    if not template_path.exists():
        console.print(f"[red]Error:[/red] Template not found at {template_path}")
        raise typer.Exit(code=1)
    
    # Determine output directory
    output_dir = Path(directory) if directory else Path.cwd() / 'apps'
    app_dir = output_dir / name
    
    if app_dir.exists():
        console.print(f"[red]Error:[/red] Directory '{app_dir}' already exists")
        raise typer.Exit(code=1)
    
    # Create the apps directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating app structure...", total=None)
        
        try:
            # Use the generator module
            from adema.generator.project_builder import AppBuilder
            
            config = {
                'name': name,
                'output_dir': str(output_dir),
            }
            
            builder = AppBuilder(config)
            builder.build()
            
            progress.update(task, description="[green]✓[/green] App created successfully!")
            
        except ImportError:
            # Fallback: Use django-admin startapp
            progress.update(task, description="Using django-admin startapp...")
            
            cmd = [
                sys.executable, '-m', 'django',
                'startapp',
                '--template', str(template_path),
                '--extension', 'py,txt,tpl',
                name,
                str(output_dir / name),
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                progress.update(task, description="[red]✗[/red] Error creating app")
                console.print(f"[red]{result.stderr}[/red]")
                raise typer.Exit(code=1)
            
            progress.update(task, description="[green]✓[/green] App created successfully!")
    
    console.print("\n[bold green]🎉 App created successfully![/bold green]\n")
    console.print("Don't forget to add it to INSTALLED_APPS:")
    console.print(f"  [cyan]'apps.{name}'[/cyan]")


@app.command()
def launch(
    port: int = typer.Option(8765, "--port", "-p", help="Port for the Web Wizard UI"),
    no_browser: bool = typer.Option(False, "--no-browser", help="Don't open browser automatically"),
):
    """
    🌐 Launch the interactive Web Wizard UI.
    
    Opens a local web server with a visual interface for configuring
    and generating ADEMA projects.
    
    Example:
        django-adema launch
        django-adema launch --port 9000
    """
    print_banner()
    
    console.print("\n[bold blue]🚀 Launching ADEMA Web Wizard...[/bold blue]\n")
    
    url = f"http://localhost:{port}"
    
    console.print(f"[green]Server starting at:[/green] {url}")
    console.print("[dim]Press Ctrl+C to stop the server[/dim]\n")
    
    # Open browser if requested
    if not no_browser:
        webbrowser.open(url)
    
    try:
        # Start the FastAPI server
        from adema.ui.server import start_server
        start_server(port=port)
    except ImportError as e:
        console.print(f"[red]Error:[/red] UI module not available: {e}")
        console.print("[yellow]Tip:[/yellow] Make sure fastapi and uvicorn are installed")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped.[/yellow]")


@app.command()
def version():
    """Show the ADEMA version."""
    from adema import __version__
    console.print(f"[bold]django-adema[/bold] version [green]{__version__}[/green]")


@app.command()
def info():
    """Show information about the ADEMA installation."""
    from adema import __version__
    
    print_banner()
    
    package_path = get_package_path()
    templates_path = package_path / 'templates'
    
    console.print("\n[bold]Installation Info:[/bold]")
    console.print(f"  Version: [green]{__version__}[/green]")
    console.print(f"  Package Path: [cyan]{package_path}[/cyan]")
    console.print(f"  Templates: [cyan]{templates_path}[/cyan]")
    
    # Check templates availability
    project_tpl = templates_path / 'project_template'
    app_tpl = templates_path / 'app_template'
    
    console.print("\n[bold]Templates Status:[/bold]")
    console.print(f"  project_template: {'[green]✓[/green]' if project_tpl.exists() else '[red]✗[/red]'}")
    console.print(f"  app_template: {'[green]✓[/green]' if app_tpl.exists() else '[red]✗[/red]'}")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
