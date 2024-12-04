import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

from src.core.scraper import BookScraper
from src.cli.config import Config

@click.command()
@click.option('--detailed', '-d', is_flag=True, help='Show chapter information')
@click.option('--sort', type=click.Choice(['name', 'date', 'chapters']), default='name', help='Sort order')
def list_books(detailed: bool, sort: str):
    """List downloaded novels."""
    config = Config()
    scraper = BookScraper(config.get_output_dir())
    console = Console()
    
    novels = scraper.get_downloaded_books()
    
    if not novels:
        console.print("[yellow]No downloaded novels found.[/yellow]")
        return
    
    # Sort novels
    if sort == 'name':
        novels.sort(key=lambda x: x.title)
    elif sort == 'chapters':
        novels.sort(key=lambda x: len(x.chapters) if x.chapters else 0, reverse=True)
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title", style="dim")
    if detailed:
        table.add_column("Chapters", justify="right")
        table.add_column("Path")
    
    # Add novels to table
    for novel in novels:
        if detailed:
            chapters = len(novel.chapters) if novel.chapters else 0
            table.add_row(
                novel.title,
                str(chapters),
                str(novel.folder_path)
            )
        else:
            table.add_row(novel.title)
    
    console.print(table)
