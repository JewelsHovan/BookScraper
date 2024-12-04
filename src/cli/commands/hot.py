import click
from rich.console import Console
from rich.table import Table

from src.core.scraper import BookScraper
from src.cli.config import Config

@click.command()
@click.option('--limit', '-l', default=10, help='Maximum number of results')
@click.option('--page', '-p', default=1, help='Page number')
def hot(limit: int, page: int):
    """List trending/hot novels."""
    config = Config()
    scraper = BookScraper(config.get_output_dir())
    console = Console()
    
    with console.status("Fetching hot novels..."):
        novels = scraper.get_hot_novels()
    
    if not novels:
        console.print("[yellow]No hot novels found.[/yellow]")
        return
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="dim")
    
    # Calculate slice based on page and limit
    start = (page - 1) * limit
    end = start + limit
    
    # Add novels to table
    for i, novel in enumerate(novels[start:end], start=start+1):
        table.add_row(str(i), novel.title)
    
    console.print(table)
