from pathlib import Path
from typing import List, Optional
import pickle
from src.models.book import Book
import fickling

class FileHandler:
    """Handles file operations for the book scraper."""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.books_file = self.base_path / 'books.pkl'
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_books(self, books: List[Book]) -> None:
        """Save books list to pickle file."""
        with open(self.books_file, 'wb') as f:
            pickle.dump(books, f)
    
    def load_books(self) -> List[Book]:
        """Load books list from pickle file."""
        if not self.books_file.exists():
            return []
        
        try:
            with open(self.books_file, 'rb') as f:
                return fickling.load(f)
        except Exception as e:
            print(f"Error loading books: {str(e)}")
            return []
    
    def save_chapter(self, book: Book, chapter_number: int, content: str) -> bool:
        """Save chapter content to file."""
        chapter_dir = self.base_path / book.formatted_title
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            chapter_file = chapter_dir / f'chapter_{chapter_number}.html'
            chapter_file.write_text(content)
            return True
        except Exception as e:
            print(f"Error saving chapter {chapter_number}: {str(e)}")
            return False
    
    def combine_chapters(self, book: Book, start: int, end: int) -> Optional[Path]:
        """Combine chapter files into a single HTML file."""
        chapter_dir = self.base_path / book.formatted_title
        if not chapter_dir.exists():
            return None
        
        try:
            combined_content = ["<html>", "<body>"]
            
            for chapter_num in range(start, end + 1):
                chapter_file = chapter_dir / f'chapter_{chapter_num}.html'
                if chapter_file.exists():
                    content = chapter_file.read_text()
                    combined_content.append(content)
                    combined_content.append("<hr>")
            
            combined_content.extend(["</body>", "</html>"])
            
            output_file = book.html_path
            output_file.write_text("\n".join(combined_content))
            
            # Clean up individual chapter files
            for chapter_num in range(start, end + 1):
                chapter_file = chapter_dir / f'chapter_{chapter_num}.html'
                if chapter_file.exists():
                    chapter_file.unlink()
            
            return output_file
            
        except Exception as e:
            print(f"Error combining chapters: {str(e)}")
            return None
