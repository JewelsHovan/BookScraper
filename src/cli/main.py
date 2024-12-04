import click
from rich.console import Console

from src.cli.commands.search import search
from src.cli.commands.download import download
from src.cli.commands.hot import hot
from src.cli.commands.list import list_books
from src.cli.commands.config import config

@click.group()
def cli():
    """BookScraper CLI - Download and manage web novels."""
    pass

# Add commands
cli.add_command(search)
cli.add_command(download)
cli.add_command(hot)
cli.add_command(list_books, name='list')
cli.add_command(config)

if __name__ == '__main__':
    cli()
