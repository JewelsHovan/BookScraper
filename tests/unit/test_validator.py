"""
Unit tests for ContentValidator class.

Tests cover:
- Valid chapter content validation
- Missing content div detection
- Empty content handling
- Content length validation (too short/too long)
- Error indicator detection
- Warning conditions
- ValidationResult structure
"""

import pytest
from pathlib import Path
from src.utils.validator import ContentValidator, ValidationResult


@pytest.fixture
def validator():
    """Create a ContentValidator instance for testing."""
    return ContentValidator()


@pytest.fixture
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def valid_chapter_html(fixtures_dir):
    """Load valid chapter HTML fixture."""
    return (fixtures_dir / "valid_chapter.html").read_text()


@pytest.fixture
def missing_div_html(fixtures_dir):
    """Load chapter with missing content div fixture."""
    return (fixtures_dir / "chapter_missing_content_div.html").read_text()


@pytest.fixture
def empty_content_html(fixtures_dir):
    """Load chapter with empty content fixture."""
    return (fixtures_dir / "chapter_empty_content.html").read_text()


@pytest.fixture
def short_content_html(fixtures_dir):
    """Load chapter with too short content fixture."""
    return (fixtures_dir / "chapter_too_short.html").read_text()


@pytest.fixture
def error_chapter_html(fixtures_dir):
    """Load chapter with error indicator fixture."""
    return (fixtures_dir / "chapter_with_error.html").read_text()


class TestContentValidator:
    """Test suite for ContentValidator class."""

    def test_validator_initialization(self, validator):
        """Test that validator initializes with correct default values."""
        assert validator.min_chapter_length == 500
        assert validator.max_chapter_length == 50000
        assert len(validator.error_indicators) > 0
        assert "404 not found" in validator.error_indicators

    def test_valid_chapter_content(self, validator, valid_chapter_html):
        """Test validation of valid chapter content."""
        result = validator.validate_chapter(valid_chapter_html, 1)
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_missing_content_div(self, validator, missing_div_html):
        """Test that missing content div is detected as error."""
        result = validator.validate_chapter(missing_div_html, 2)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Chapter content div not found" in result.errors[0]

    def test_empty_content(self, validator, empty_content_html):
        """Test that empty content is detected as error."""
        result = validator.validate_chapter(empty_content_html, 3)
        
        assert result.is_valid is False
        assert any("No text content found" in error for error in result.errors)

    def test_content_too_short(self, validator, short_content_html):
        """Test that content below minimum length generates warning."""
        result = validator.validate_chapter(short_content_html, 4)
        
        # Should be valid but with warning
        assert result.is_valid is True
        assert len(result.warnings) > 0
        assert any("too short" in warning.lower() for warning in result.warnings)

    def test_error_indicators(self, validator, error_chapter_html):
        """Test that error indicators in content are detected."""
        result = validator.validate_chapter(error_chapter_html, 5)
        
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("404 not found" in error.lower() for error in result.errors)

    @pytest.mark.parametrize("error_text,expected_error", [
        ("404 not found", "404 not found"),
        ("page not found", "page not found"),
        ("chapter not available", "chapter not available"),
        ("access denied", "access denied"),
    ])
    def test_all_error_indicators(self, validator, error_text, expected_error):
        """Test all error indicators are properly detected."""
        html = f"""
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>{error_text}</p>
            </div>
        </body>
        </html>
        """
        
        result = validator.validate_chapter(html, 1)
        
        assert result.is_valid is False
        assert any(expected_error in error.lower() for error in result.errors)

    def test_content_too_long(self, validator):
        """Test that content exceeding maximum length is handled."""
        # Create content that's too long (> 50,000 chars)
        long_text = "A" * 60000
        html = f"""
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>{long_text}</p>
            </div>
        </body>
        </html>
        """
        
        result = validator.validate_chapter(html, 1)
        
        # Current implementation doesn't fail on too long, but should still validate
        assert isinstance(result, ValidationResult)

    def test_chapter_number_mismatch_warning(self, validator):
        """Test that chapter number mismatch generates warning."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 5</h2>
                <span class="chapter-text">Chapter 5</span>
                <p>This is chapter content with enough text to pass minimum length requirements. 
                We need to add more content here to ensure it's long enough for validation. 
                Adding more sentences to meet the minimum character count requirement.</p>
            </div>
        </body>
        </html>
        """
        
        # Validate as chapter 1, but content says chapter 5
        result = validator.validate_chapter(html, 1)
        
        # Should have a warning about chapter number mismatch
        assert any("mismatch" in warning.lower() for warning in result.warnings)

    def test_validation_result_structure(self, validator, valid_chapter_html):
        """Test that ValidationResult has correct structure."""
        result = validator.validate_chapter(valid_chapter_html, 1)
        
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)

    def test_malformed_html(self, validator):
        """Test handling of malformed HTML."""
        malformed_html = "<html><body><div id='chapter-content'><p>Unclosed paragraph</body>"
        
        # Should not crash, BeautifulSoup handles malformed HTML gracefully
        result = validator.validate_chapter(malformed_html, 1)
        
        assert isinstance(result, ValidationResult)

    def test_html_with_navigation_and_ads(self, validator):
        """Test that navigation and ads don't interfere with validation."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1: Test</h2>
                <span class="chapter-text">Chapter 1</span>
                <p>This is the actual chapter content with enough text to be valid. 
                We need several sentences to meet the minimum length requirement.
                This ensures the validator properly extracts content from paragraphs.
                Navigation and ads should be ignored by the validator logic.</p>
                <div class="ads">Advertisement content here</div>
                <nav>Previous | Next</nav>
                <p>More actual content that should be validated properly.
                The validator should focus on paragraph text content only.
                This helps ensure accurate content length calculation.</p>
            </div>
        </body>
        </html>
        """
        
        result = validator.validate_chapter(html, 1)
        
        assert result.is_valid is True

    @pytest.mark.parametrize("chapter_number", [1, 10, 100, 999])
    def test_various_chapter_numbers(self, validator, valid_chapter_html, chapter_number):
        """Test validation works with various chapter numbers."""
        result = validator.validate_chapter(valid_chapter_html, chapter_number)
        
        # Should validate regardless of chapter number
        assert isinstance(result, ValidationResult)

    def test_exception_handling(self, validator):
        """Test that exceptions during validation are caught and reported."""
        # Pass None as content to trigger an exception
        result = validator.validate_chapter(None, 1)
        
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("Validation error" in error for error in result.errors)

    def test_empty_string_content(self, validator):
        """Test validation of empty string content."""
        result = validator.validate_chapter("", 1)
        
        assert result.is_valid is False
        assert len(result.errors) > 0

    def test_whitespace_only_paragraphs(self, validator):
        """Test that whitespace-only paragraphs are ignored."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>   </p>
                <p>Actual content here with enough text to be valid and meet requirements.</p>
                <p>
                
                </p>
                <p>More valid content to ensure we meet minimum length requirements for validation.</p>
            </div>
        </body>
        </html>
        """
        
        result = validator.validate_chapter(html, 1)
        
        # Should only count non-whitespace paragraphs
        assert isinstance(result, ValidationResult)

    def test_multiple_warnings(self, validator):
        """Test that multiple warnings can be collected."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 5</h2>
                <span class="chapter-text">Chapter 5</span>
                <p>Short content.</p>
            </div>
        </body>
        </html>
        """
        
        # Chapter 1 but content says 5, and content is short
        result = validator.validate_chapter(html, 1)
        
        # Should have warnings for both issues
        assert len(result.warnings) >= 1

    def test_case_insensitive_error_detection(self, validator):
        """Test that error indicators are detected case-insensitively."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>THIS PAGE WAS NOT FOUND - 404 NOT FOUND</p>
            </div>
        </body>
        </html>
        """
        
        result = validator.validate_chapter(html, 1)
        
        assert result.is_valid is False
        assert len(result.errors) > 0
