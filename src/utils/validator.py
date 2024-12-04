from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ContentValidator:
    """Validates chapter content with appropriate rules for the website structure."""
    
    def __init__(self):
        self.min_chapter_length = 500  # Reduced minimum length
        self.max_chapter_length = 50000  # Increased maximum length
        
        # Common error messages that indicate failed scraping
        self.error_indicators = [
            "404 not found",
            "page not found",
            "chapter not available",
            "access denied"
        ]

    def validate_chapter(self, content: str, chapter_number: int) -> ValidationResult:
        """
        Validate chapter content with focus on essential elements.
        
        Args:
            content: Raw HTML content
            chapter_number: Chapter number for reference
        """
        errors = []
        warnings = []
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # 1. Check for chapter content div
            chapter_content = soup.find('div', id='chapter-content')
            if not chapter_content:
                errors.append("Chapter content div not found")
                return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
            
            # 2. Extract actual text content (excluding navigation and ads)
            paragraphs = chapter_content.find_all('p')
            text_content = ' '.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            
            # 3. Basic content checks
            if not text_content:
                errors.append("No text content found in chapter")
            elif len(text_content) < self.min_chapter_length:
                warnings.append(f"Chapter content might be too short ({len(text_content)} chars)")
            
            # 4. Check for error indicators in the text
            content_lower = text_content.lower()
            for indicator in self.error_indicators:
                if indicator in content_lower:
                    errors.append(f"Error indicator found: {indicator}")
            
            # 5. Verify chapter number presence (optional)
            chapter_title = soup.find('span', class_='chapter-text')
            if chapter_title and str(chapter_number) not in chapter_title.get_text():
                warnings.append("Chapter number mismatch in title")
            
            # Consider valid if we have content and no critical errors
            is_valid = len(text_content) > 0 and len(errors) == 0
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
