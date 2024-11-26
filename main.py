from pathlib import Path
from src.core.scraper import BookScraper

scraper = BookScraper(Path("./novels"))
scraper.download_book("Hidden Marriage", 1, 100)