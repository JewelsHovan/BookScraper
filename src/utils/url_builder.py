from typing import Dict
from pathlib import Path
import json

class URLBuilder:
    """Handles URL generation for different novel websites."""
    
    def __init__(self, config_path: Path = None):
        self.templates: Dict[str, str] = {
            'novelfull': "https://novelfull.com/{book_name}/chapter-{chapter_number}.html",
            'novelusb': "https://novelusb.com/novel-book/{book_name}/chapter-{chapter_number}",
            'search': "https://novelfull.net/search?keyword={search_term}",
            'hot_novels': "https://novelfull.net/hot-novel?page={page}"
        }
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: Path) -> None:
        """Load URL templates from a config file."""
        with open(config_path) as f:
            custom_templates = json.load(f)
            self.templates.update(custom_templates)
    
    def get_chapter_url(self, book_name: str, chapter_number: int, site: str = 'novelfull') -> str:
        """Generate URL for a specific chapter."""
        template = self.templates.get(site)
        if not template:
            raise ValueError(f"No URL template found for site: {site}")
        return template.format(book_name=book_name, chapter_number=chapter_number)
    
    def get_search_url(self, search_term: str) -> str:
        """Generate search URL."""
        return self.templates['search'].format(search_term=search_term.replace(' ', '%20'))
    
    def get_hot_novels_url(self, page: int) -> str:
        """Generate URL for hot novels page."""
        return self.templates['hot_novels'].format(page=page)
