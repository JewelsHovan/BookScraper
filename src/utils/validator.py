from typing import Optional, Dict, Any
from dataclasses import dataclass
import re

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]
    warnings: list[str]

class ContentValidator:
    """Validates downloaded content for integrity and quality."""
    
    def __init__(self):
        self.min_chapter_length = 100  # characters
        self.max_chapter_length = 50000  # characters
        self.suspicious_patterns = [
            r'404 not found',
            r'error',
            r'page not found',
            r'access denied',
            r'please try again',
        ]
    
    def validate_chapter(self, content: str, chapter_number: int) -> ValidationResult:
        """
        Validate chapter content.
        
        Checks:
        1. Content length
        2. Error messages
        3. HTML structure
        4. Content quality indicators
        """
        errors = []
        warnings = []
        
        # Check content length
        if len(content) < self.min_chapter_length:
            errors.append(f"Chapter {chapter_number} content too short ({len(content)} chars)")
        elif len(content) > self.max_chapter_length:
            warnings.append(f"Chapter {chapter_number} content unusually long ({len(content)} chars)")
        
        # Check for error messages
        content_lower = content.lower()
        for pattern in self.suspicious_patterns:
            if re.search(pattern, content_lower):
                errors.append(f"Chapter {chapter_number} contains error indicator: {pattern}")
        
        # Check HTML structure
        if not self._validate_html_structure(content):
            errors.append(f"Chapter {chapter_number} has invalid HTML structure")
        
        # Check content quality
        quality_issues = self._check_content_quality(content)
        warnings.extend(quality_issues)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_html_structure(self, content: str) -> bool:
        """Check if HTML has basic required structure."""
        has_paragraph = bool(re.search(r'<p>.*?</p>', content))
        has_title = bool(re.search(r'<h[1-6]>.*?</h[1-6]>', content))
        return has_paragraph and has_title
    
    def _check_content_quality(self, content: str) -> list[str]:
        """Check for potential content quality issues."""
        warnings = []
        
        # Check for repeated content
        if self._has_repeated_paragraphs(content):
            warnings.append("Contains repeated paragraphs")
        
        # Check for missing punctuation
        if not re.search(r'[.!?]', content):
            warnings.append("No sentence-ending punctuation found")
        
        # Check for unusually short paragraphs
        if self._has_short_paragraphs(content):
            warnings.append("Contains very short paragraphs")
        
        return warnings
    
    def _has_repeated_paragraphs(self, content: str) -> bool:
        """Check if content has repeated paragraphs."""
        paragraphs = re.findall(r'<p>(.*?)</p>', content)
        seen = set()
        for p in paragraphs:
            if p in seen and len(p) > 20:  # Only check substantial paragraphs
                return True
            seen.add(p)
        return False
    
    def _has_short_paragraphs(self, content: str) -> bool:
        """Check if content has very short paragraphs."""
        paragraphs = re.findall(r'<p>(.*?)</p>', content)
        short_count = sum(1 for p in paragraphs if len(p) < 20)
        return short_count > len(paragraphs) / 2  # More than half are short
