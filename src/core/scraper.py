from typing import List, Optional, Tuple
from pathlib import Path
from tqdm import tqdm

from src.models.book import Book
from src.utils.url_builder import URLBuilder
from src.utils.html_fetcher import HTMLFetcher
from src.utils.file_handler import FileHandler
from src.core.parser import HTMLParser, ParsedChapter
from src.core.downloader import ChapterDownloader
from src.utils.cache import cached

class BookScraper:
    """Main scraper class that coordinates all components."""
    
    def __init__(self, output_dir: Path, max_workers: int = 5):
        self.file_handler = FileHandler(output_dir)
        self.url_builder = URLBuilder()
        self.parser = HTMLParser()
        self.downloader = ChapterDownloader(max_workers=max_workers)
        self.novels: List[Book] = self.file_handler.load_books()
    
    @cached(ttl=3600)  # Cache search results for 1 hour
    def search_novels(self, query: str) -> List[tuple[str, str, str]]:
        """Search for novels matching the query."""
        url = self.url_builder.get_search_url(query)
        with HTMLFetcher() as fetcher:
            if html := fetcher.fetch(url):
                return self.parser.parse_search_results(html)
        return []
    
    @cached(ttl=3600)  # Cache hot novels for 1 hour
    def get_hot_novels(self) -> List[Book]:
        """Fetch and update the list of hot novels."""
        page = 1
        new_novels = []
        
        with HTMLFetcher() as fetcher:
            while True:
                url = self.url_builder.get_hot_novels_url(page)
                if not (html := fetcher.fetch(url)):
                    break
                
                novels = self.parser.parse_hot_novels(html)
                if not novels or novels == new_novels:
                    break
                
                new_novels.extend(novels)
                page += 1
        
        # Convert to Book objects
        self.novels = [
            Book(title=title, folder_path=self.file_handler.base_path / title.lower().replace(' ', '-'))
            for title, _ in new_novels
        ]
        
        self.file_handler.save_books(self.novels)
        return self.novels
    
    def download_book(self, book_name: str, start_chapter: int = 1, end_chapter: int = 50) -> Optional[Path]:
        """Download a book's chapters and combine them into a single file."""
        book_name = book_name.lower().replace(' ', '-')
        
        # Create or get book
        book = next((b for b in self.novels if b.formatted_title == book_name), None)
        if not book:
            book = Book(
                title=book_name,
                folder_path=self.file_handler.base_path / book_name
            )
            self.novels.append(book)
        
        # Setup progress bar
        pbar = tqdm(total=(end_chapter - start_chapter + 1), desc=f"Downloading {book_name}")
        
        def update_progress(completed: int, total: int):
            pbar.n = completed
            pbar.refresh()
        
        # Download chapters
        results = self.downloader.download_chapters(
            book,
            self.url_builder.get_chapter_url(book_name, "{chapter_number}"),
            start_chapter,
            end_chapter,
            progress_callback=update_progress
        )
        
        pbar.close()
        
        # Process results
        successful_chapters = []
        for result in results:
            if result.content and result.validation and result.validation.is_valid:
                if self.file_handler.save_chapter(book, result.chapter_number, result.content):
                    successful_chapters.append(result.chapter_number)
            else:
                print(f"Chapter {result.chapter_number} failed: {result.error}")
                if result.validation and result.validation.warnings:
                    print(f"Warnings: {', '.join(result.validation.warnings)}")
        
        if successful_chapters:
            book.chapters = successful_chapters
            self.file_handler.save_books(self.novels)
            return self.file_handler.combine_chapters(book, min(successful_chapters), max(successful_chapters))
        
        return None
    
    def get_downloaded_books(self) -> List[Book]:
        """Get list of all downloaded books."""
        return self.novels
