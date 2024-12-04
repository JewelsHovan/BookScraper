import click
from rich.console import Console
from pathlib import Path

from src.core.scraper import BookScraper
from src.cli.config import Config

@click.command()
@click.argument('novel_name')
@click.option('--start', '-s', default=1, help='Starting chapter')
@click.option('--end', '-e', default=50, help='Ending chapter')
@click.option('--workers', '-w', default=5, help='Number of concurrent downloads')
@click.option('--output', '-o', help='Output directory')
@click.option('--format', '-f', default='html', type=click.Choice(['html', 'txt']), help='Output format')
def download(novel_name: str, start: int, end: int, workers: int, output: str, format: str):
    """Download chapters from a novel."""
    config = Config()
    output_dir = Path(output) if output else config.get_output_dir()
    
    console = Console()
    scraper = BookScraper(output_dir, max_workers=workers)
    
    console.print(f"[green]Downloading {novel_name} chapters {start}-{end}[/green]")
    
    output_file = scraper.download_book(novel_name, start, end)
    print(output_file)
    
    if output_file:
        console.print(f"[green]Successfully downloaded to: {output_file}[/green]")
    else:
        console.print("[red]Failed to download novel.[/red]")
