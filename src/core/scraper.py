from typing import List, Optional
from pathlib import Path

from src.models.book import Book
from src.utils.url_builder import URLBuilder
from src.utils.html_fetcher import HTMLFetcher
from src.utils.file_handler import FileHandler
from src.core.parser import HTMLParser, ParsedChapter

class BookScraper:
    """Main scraper class that coordinates all components."""
    
    def __init__(self, output_dir: Path):
        self.file_handler = FileHandler(output_dir)
        self.url_builder = URLBuilder()
        self.parser = HTMLParser()
        self.novels: List[Book] = self.file_handler.load_books()
    
    def search_novels(self, query: str) -> List[tuple[str, str, str]]:
        """Search for novels matching the query."""
        url = self.url_builder.get_search_url(query)
        with HTMLFetcher() as fetcher:
            if html := fetcher.fetch(url):
                return self.parser.parse_search_results(html)
        return []
    
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
        
        # Create a new book or get existing one
        book = next((b for b in self.novels if b.formatted_title == book_name), None)
        if not book:
            book = Book(
                title=book_name,
                folder_path=self.file_handler.base_path / book_name
            )
            self.novels.append(book)
        
        successful_chapters = []
        with HTMLFetcher() as fetcher:
            for chapter_num in range(start_chapter, end_chapter + 1):
                url = self.url_builder.get_chapter_url(book_name, chapter_num)
                if html := fetcher.fetch(url):
                    if chapter := self.parser.parse_chapter(html, chapter_num):
                        if self.file_handler.save_chapter(book, chapter_num, chapter.content):
                            successful_chapters.append(chapter_num)
                            print(f"Downloaded chapter {chapter_num}")
        
        if successful_chapters:
            book.chapters = successful_chapters
            self.file_handler.save_books(self.novels)
            return self.file_handler.combine_chapters(book, min(successful_chapters), max(successful_chapters))
        
        return None
    
    def get_downloaded_books(self) -> List[Book]:
        """Get list of all downloaded books."""
        return self.novels
