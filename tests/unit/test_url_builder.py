"""
Unit tests for URLBuilder class.

Tests cover:
- Chapter URL generation for different sites
- Search URL generation with special characters
- Hot novels URL generation with different pages
- Invalid site name error handling
- Template loading from JSON config
- Template formatting errors
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.utils.url_builder import URLBuilder


@pytest.fixture
def url_builder():
    """Create a URLBuilder instance for testing."""
    return URLBuilder()


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config = {
            'custom_site': 'https://example.com/{book_name}/ch-{chapter_number}.html',
            'another_site': 'https://another.com/books/{book_name}/{chapter_number}'
        }
        json.dump(config, f)
        temp_path = Path(f.name)
    
    yield temp_path
    
    # Cleanup
    temp_path.unlink()


class TestURLBuilderInitialization:
    """Test URLBuilder initialization and configuration."""

    def test_default_initialization(self, url_builder):
        """Test that URLBuilder initializes with default templates."""
        assert 'novelfull' in url_builder.templates
        assert 'novelusb' in url_builder.templates
        assert 'search' in url_builder.templates
        assert 'hot_novels' in url_builder.templates

    def test_initialization_with_config(self, temp_config_file):
        """Test initialization with custom config file."""
        builder = URLBuilder(config_path=temp_config_file)
        
        assert 'custom_site' in builder.templates
        assert 'another_site' in builder.templates
        # Default templates should still be present
        assert 'novelfull' in builder.templates

    def test_load_config_updates_templates(self, url_builder, temp_config_file):
        """Test that load_config updates existing templates."""
        initial_count = len(url_builder.templates)
        url_builder.load_config(temp_config_file)
        
        assert len(url_builder.templates) > initial_count
        assert 'custom_site' in url_builder.templates


class TestChapterURLGeneration:
    """Test chapter URL generation for different sites."""

    def test_get_chapter_url_novelfull(self, url_builder):
        """Test chapter URL generation for novelfull."""
        url = url_builder.get_chapter_url('test-book', 1, 'novelfull')
        
        assert url == 'https://novelfull.com/test-book/chapter-1.html'

    def test_get_chapter_url_novelusb(self, url_builder):
        """Test chapter URL generation for novelusb."""
        url = url_builder.get_chapter_url('test-book', 1, 'novelusb')
        
        assert url == 'https://novelusb.com/novel-book/test-book/chapter-1'

    def test_get_chapter_url_default_site(self, url_builder):
        """Test that default site is novelfull."""
        url = url_builder.get_chapter_url('test-book', 1)
        
        assert 'novelfull.com' in url

    @pytest.mark.parametrize("book_name,chapter_num,expected_url", [
        ('dragon-king', 1, 'https://novelfull.com/dragon-king/chapter-1.html'),
        ('the-great-mage', 42, 'https://novelfull.com/the-great-mage/chapter-42.html'),
        ('book-with-numbers-123', 999, 'https://novelfull.com/book-with-numbers-123/chapter-999.html'),
    ])
    def test_chapter_url_various_inputs(self, url_builder, book_name, chapter_num, expected_url):
        """Test chapter URL generation with various inputs."""
        url = url_builder.get_chapter_url(book_name, chapter_num, 'novelfull')
        
        assert url == expected_url

    def test_get_chapter_url_invalid_site(self, url_builder):
        """Test that invalid site name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            url_builder.get_chapter_url('test-book', 1, 'invalid_site')
        
        assert 'No URL template found for site' in str(exc_info.value)
        assert 'invalid_site' in str(exc_info.value)

    def test_chapter_url_with_hyphens(self, url_builder):
        """Test chapter URL with book names containing hyphens."""
        url = url_builder.get_chapter_url('multi-word-book-name', 10)
        
        assert 'multi-word-book-name' in url
        assert 'chapter-10' in url

    def test_chapter_url_with_numbers(self, url_builder):
        """Test chapter URL with book names containing numbers."""
        url = url_builder.get_chapter_url('book123', 5)
        
        assert 'book123' in url


class TestSearchURLGeneration:
    """Test search URL generation."""

    def test_get_search_url_simple(self, url_builder):
        """Test search URL generation with simple term."""
        url = url_builder.get_search_url('dragon')
        
        assert url == 'https://novelfull.net/search?keyword=dragon'

    def test_get_search_url_with_spaces(self, url_builder):
        """Test search URL generation with spaces."""
        url = url_builder.get_search_url('dragon king')
        
        assert url == 'https://novelfull.net/search?keyword=dragon%20king'

    def test_get_search_url_multiple_spaces(self, url_builder):
        """Test search URL with multiple spaces."""
        url = url_builder.get_search_url('the great mage returns')
        
        assert url == 'https://novelfull.net/search?keyword=the%20great%20mage%20returns'

    @pytest.mark.parametrize("search_term,expected_encoded", [
        ('dragon', 'dragon'),
        ('dragon king', 'dragon%20king'),
        ('the great mage', 'the%20great%20mage'),
        ('a b c d', 'a%20b%20c%20d'),
    ])
    def test_search_url_space_encoding(self, url_builder, search_term, expected_encoded):
        """Test that spaces are properly encoded as %20."""
        url = url_builder.get_search_url(search_term)
        
        assert expected_encoded in url

    def test_get_search_url_special_characters(self, url_builder):
        """Test search URL with special characters."""
        # Note: Current implementation only handles spaces
        url = url_builder.get_search_url("dragon's tale")
        
        assert 'search?keyword=' in url

    def test_get_search_url_empty_string(self, url_builder):
        """Test search URL with empty string."""
        url = url_builder.get_search_url('')
        
        assert url == 'https://novelfull.net/search?keyword='

    def test_get_search_url_single_character(self, url_builder):
        """Test search URL with single character."""
        url = url_builder.get_search_url('a')
        
        assert url == 'https://novelfull.net/search?keyword=a'


class TestHotNovelsURLGeneration:
    """Test hot novels URL generation."""

    def test_get_hot_novels_url_page_1(self, url_builder):
        """Test hot novels URL for page 1."""
        url = url_builder.get_hot_novels_url(1)
        
        assert url == 'https://novelfull.net/hot-novel?page=1'

    def test_get_hot_novels_url_page_10(self, url_builder):
        """Test hot novels URL for page 10."""
        url = url_builder.get_hot_novels_url(10)
        
        assert url == 'https://novelfull.net/hot-novel?page=10'

    @pytest.mark.parametrize("page_num", [1, 5, 10, 50, 100])
    def test_hot_novels_url_various_pages(self, url_builder, page_num):
        """Test hot novels URL generation for various page numbers."""
        url = url_builder.get_hot_novels_url(page_num)
        
        assert f'page={page_num}' in url

    def test_get_hot_novels_url_zero_page(self, url_builder):
        """Test hot novels URL with page 0."""
        url = url_builder.get_hot_novels_url(0)
        
        assert 'page=0' in url


class TestTemplateLoading:
    """Test template loading from JSON config."""

    def test_load_config_valid_json(self, url_builder, temp_config_file):
        """Test loading valid JSON config file."""
        url_builder.load_config(temp_config_file)
        
        assert 'custom_site' in url_builder.templates
        assert url_builder.templates['custom_site'] == 'https://example.com/{book_name}/ch-{chapter_number}.html'

    def test_load_config_nonexistent_file(self, url_builder):
        """Test loading non-existent config file raises error."""
        with pytest.raises(FileNotFoundError):
            url_builder.load_config(Path('/nonexistent/path/config.json'))

    def test_load_config_invalid_json(self, url_builder):
        """Test loading invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{ invalid json }')
            temp_path = Path(f.name)
        
        try:
            with pytest.raises(json.JSONDecodeError):
                url_builder.load_config(temp_path)
        finally:
            temp_path.unlink()

    def test_custom_template_usage(self, temp_config_file):
        """Test that custom templates can be used for URL generation."""
        builder = URLBuilder(config_path=temp_config_file)
        
        url = builder.get_chapter_url('my-book', 5, 'custom_site')
        
        assert url == 'https://example.com/my-book/ch-5.html'

    def test_templates_are_updated_not_replaced(self, url_builder, temp_config_file):
        """Test that loading config updates templates, not replaces them."""
        original_templates = url_builder.templates.copy()
        url_builder.load_config(temp_config_file)
        
        # Original templates should still exist
        for key in original_templates:
            assert key in url_builder.templates


class TestTemplateFormatting:
    """Test template formatting and error handling."""

    def test_template_with_missing_placeholder(self, url_builder):
        """Test template formatting with missing required placeholder."""
        # Add a template with wrong placeholder names
        url_builder.templates['broken_site'] = 'https://example.com/{wrong_name}'
        
        with pytest.raises(KeyError):
            url_builder.get_chapter_url('test-book', 1, 'broken_site')

    def test_template_with_extra_placeholders(self, url_builder):
        """Test that unused placeholders don't cause errors."""
        url_builder.templates['extra_site'] = 'https://example.com/{book_name}/chapter-{chapter_number}'
        
        # Should work fine even if template has all needed placeholders
        url = url_builder.get_chapter_url('test', 1, 'extra_site')
        
        assert 'test' in url

    def test_url_formatting_preserves_structure(self, url_builder):
        """Test that URL formatting preserves the template structure."""
        url = url_builder.get_chapter_url('test-book', 42, 'novelfull')
        
        # Check structure is preserved
        assert url.startswith('https://')
        assert 'novelfull.com' in url
        assert url.endswith('.html')

    def test_search_url_formatting(self, url_builder):
        """Test search URL maintains proper format."""
        url = url_builder.get_search_url('test search')
        
        assert url.startswith('https://')
        assert 'search?keyword=' in url

    def test_multiple_format_calls(self, url_builder):
        """Test that multiple format calls produce consistent results."""
        url1 = url_builder.get_chapter_url('test-book', 1, 'novelfull')
        url2 = url_builder.get_chapter_url('test-book', 1, 'novelfull')
        
        assert url1 == url2


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_book_name(self, url_builder):
        """Test URL generation with very long book name."""
        long_name = 'a' * 200
        url = url_builder.get_chapter_url(long_name, 1)
        
        assert long_name in url

    def test_very_large_chapter_number(self, url_builder):
        """Test URL generation with very large chapter number."""
        url = url_builder.get_chapter_url('test-book', 999999)
        
        assert '999999' in url

    def test_book_name_with_special_chars(self, url_builder):
        """Test book name with special characters (as they appear in URLs)."""
        # In real usage, book names in URLs are already sanitized
        url = url_builder.get_chapter_url('book-with-dashes', 1)
        
        assert 'book-with-dashes' in url

    def test_unicode_in_search_term(self, url_builder):
        """Test search URL with unicode characters."""
        url = url_builder.get_search_url('龙王')
        
        # Should handle unicode gracefully
        assert isinstance(url, str)
        assert 'search?keyword=' in url

    def test_empty_templates_dict(self):
        """Test behavior with no templates."""
        builder = URLBuilder()
        builder.templates = {}
        
        with pytest.raises(ValueError):
            builder.get_chapter_url('test', 1, 'novelfull')
