import click
from rich.console import Console
from rich.table import Table

from src.cli.config import Config

@click.group()
def config():
    """Manage configuration settings."""
    pass

@config.command()
@click.argument('key')
def get(key: str):
    """Get configuration value."""
    config = Config()
    console = Console()
    
    value = config.get(key)
    if value is None:
        console.print(f"[yellow]No configuration found for '{key}'[/yellow]")
    else:
        console.print(f"{key} = {value}")

@config.command()
@click.argument('key')
@click.argument('value')
def set(key: str, value: str):
    """Set configuration value."""
    config = Config()
    console = Console()
    
    # Convert string value to appropriate type
    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    elif value.isdigit():
        value = int(value)
    
    config.set(key, value)
    console.print(f"[green]Set {key} = {value}[/green]")

@config.command()
def list():
    """List all configuration settings."""
    config = Config()
    console = Console()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Key", style="dim")
    table.add_column("Value")
    
    for key, value in config.config.items():
        if isinstance(value, dict):
            table.add_row(key, "[cyan]<nested>[/cyan]")
            for sub_key, sub_value in value.items():
                table.add_row(f"  {key}.{sub_key}", str(sub_value))
        else:
            table.add_row(key, str(value))
    
    console.print(table)
