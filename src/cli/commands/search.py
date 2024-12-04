import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

from src.core.scraper import BookScraper
from src.cli.config import Config

@click.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed descriptions')
@click.option('--cache-ttl', default=3600, help='Cache duration in seconds')
def search(query: str, limit: int, detailed: bool, cache_ttl: int):
    """Search for novels by title or keywords."""
    config = Config()
    scraper = BookScraper(config.get_output_dir())
    
    console = Console()
    
    with console.status(f"Searching for '{query}'..."):
        results = scraper.search_novels(query)
    
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return
    
    # Create results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title", style="dim")
    if detailed:
        table.add_column("Description")
    
    # Add results to table
    for title, url, description in results[:limit]:
        if detailed:
            table.add_row(title, description)
        else:
            table.add_row(title)
    
    console.print(table)
