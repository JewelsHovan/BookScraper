from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

@dataclass
class Book:
    """Represents a book with its metadata and content information."""
    title: str
    folder_path: Path
    chapters: Optional[List[int]] = None
    description: Optional[str] = None
    author: Optional[str] = None
    
    @property
    def formatted_title(self) -> str:
        """Returns the title formatted for URL usage."""
        return self.title.lower().replace(' ', '-')
    
    @property
    def html_path(self) -> Path:
        """Returns the path to the combined HTML file."""
        return self.folder_path / f"{self.formatted_title}.html"
