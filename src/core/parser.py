from typing import Optional, List, Tuple
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class ParsedChapter:
    """Represents a parsed chapter with its content."""
    title: str
    content: str
    chapter_number: int

class HTMLParser:
    """Handles HTML parsing with BeautifulSoup."""
    
    def __init__(self, content_id: str = 'chapter-content'):
        self.content_id = content_id
    
    def parse_chapter(self, html: str, chapter_number: int) -> Optional[ParsedChapter]:
        """Parse chapter content from HTML."""
        try:
            soup = BeautifulSoup(html, 'lxml')
            content_div = soup.find('div', id=self.content_id)
            
            if not content_div:
                print(f"Could not find content div for chapter {chapter_number}")
                return None
            
            # Extract title
            title_tag = content_div.find(['h2', 'h3'])
            title = title_tag.text if title_tag else f"Chapter {chapter_number}"
            
            # Extract paragraphs
            paragraphs = []
            for p in content_div.find_all('p'):
                text = p.text.strip()
                if text:
                    paragraphs.append(f"<p>{text}</p>")
            
            content = f"<h1>{title}</h1>\n" + "\n".join(paragraphs)
            return ParsedChapter(title=title, content=content, chapter_number=chapter_number)
            
        except Exception as e:
            print(f"Error parsing chapter {chapter_number}: {str(e)}")
            return None
    
    def parse_hot_novels(self, html: str) -> List[Tuple[str, str]]:
        """Parse hot novels list from HTML."""
        novels = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            for novel in soup.find_all('h3', class_='truyen-title'):
                link = novel.find('a')
                if link:
                    title = link.text.strip()
                    url = link.get('href', '')
                    novels.append((title, url))
        except Exception as e:
            print(f"Error parsing hot novels list: {str(e)}")
        
        return novels
    
    def parse_search_results(self, html: str) -> List[Tuple[str, str, str]]:
        """Parse search results from HTML."""
        results = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            for item in soup.find_all('div', class_='row'):
                title_tag = item.find('h3', class_='truyen-title')
                desc_tag = item.find('div', class_='excerpt')
                
                if title_tag and desc_tag:
                    link = title_tag.find('a')
                    if link:
                        title = link.text.strip()
                        url = link.get('href', '')
                        description = desc_tag.text.strip()
                        results.append((title, url, description))
        except Exception as e:
            print(f"Error parsing search results: {str(e)}")
        
        return results
