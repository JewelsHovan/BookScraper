"""
Unit tests for HTMLParser class.

Tests cover:
- Parsing chapters with valid HTML
- Parsing chapters with missing elements
- Parsing search results with valid HTML
- Parsing hot novels with valid HTML
- Error handling for malformed HTML
- Mocked BeautifulSoup responses
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from src.core.parser import HTMLParser, ParsedChapter


@pytest.fixture
def parser():
    """Create an HTMLParser instance for testing."""
    return HTMLParser()


@pytest.fixture
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def valid_chapter_html(fixtures_dir):
    """Load valid chapter HTML fixture."""
    return (fixtures_dir / "valid_chapter.html").read_text()


@pytest.fixture
def empty_chapter_html(fixtures_dir):
    """Load empty chapter HTML fixture."""
    return (fixtures_dir / "chapter_empty_content.html").read_text()


@pytest.fixture
def search_results_html(fixtures_dir):
    """Load search results HTML fixture."""
    return (fixtures_dir / "search_results.html").read_text()


@pytest.fixture
def hot_novels_html(fixtures_dir):
    """Load hot novels HTML fixture."""
    return (fixtures_dir / "hot_novels.html").read_text()


class TestHTMLParserInitialization:
    """Test HTMLParser initialization."""

    def test_default_initialization(self, parser):
        """Test that parser initializes with default content_id."""
        assert parser.content_id == 'chapter-content'

    def test_custom_content_id(self):
        """Test initialization with custom content_id."""
        custom_parser = HTMLParser(content_id='custom-id')
        
        assert custom_parser.content_id == 'custom-id'


class TestParseChapter:
    """Test chapter parsing functionality."""

    def test_parse_valid_chapter(self, parser, valid_chapter_html):
        """Test parsing a valid chapter."""
        result = parser.parse_chapter(valid_chapter_html, 1)
        
        assert result is not None
        assert isinstance(result, ParsedChapter)
        assert result.chapter_number == 1
        assert len(result.title) > 0
        assert len(result.content) > 0

    def test_parsed_chapter_structure(self, parser, valid_chapter_html):
        """Test that ParsedChapter has correct structure."""
        result = parser.parse_chapter(valid_chapter_html, 1)
        
        assert hasattr(result, 'title')
        assert hasattr(result, 'content')
        assert hasattr(result, 'chapter_number')
        assert isinstance(result.title, str)
        assert isinstance(result.content, str)
        assert isinstance(result.chapter_number, int)

    def test_parse_chapter_extracts_title(self, parser, valid_chapter_html):
        """Test that chapter title is properly extracted."""
        result = parser.parse_chapter(valid_chapter_html, 1)
        
        assert 'Chapter 1' in result.title or 'The Beginning' in result.title

    def test_parse_chapter_extracts_paragraphs(self, parser, valid_chapter_html):
        """Test that chapter paragraphs are extracted."""
        result = parser.parse_chapter(valid_chapter_html, 1)
        
        # Should contain paragraph tags
        assert '<p>' in result.content
        assert '</p>' in result.content

    def test_parse_chapter_missing_content_div(self, parser):
        """Test parsing chapter when content div is missing."""
        html = """
        <html>
        <body>
            <div id="wrong-id">
                <p>This is in the wrong div.</p>
            </div>
        </body>
        </html>
        """
        
        result = parser.parse_chapter(html, 1)
        
        assert result is None

    def test_parse_chapter_with_custom_content_id(self):
        """Test parsing with custom content_id."""
        custom_parser = HTMLParser(content_id='custom-content')
        html = """
        <html>
        <body>
            <div id="custom-content">
                <h2>Chapter Title</h2>
                <p>Chapter content here.</p>
            </div>
        </body>
        </html>
        """
        
        result = custom_parser.parse_chapter(html, 1)
        
        assert result is not None
        assert 'Chapter Title' in result.title

    def test_parse_chapter_no_title_uses_default(self, parser):
        """Test that default title is used when no title tag found."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <p>Content without a title.</p>
            </div>
        </body>
        </html>
        """
        
        result = parser.parse_chapter(html, 42)
        
        assert result is not None
        assert result.title == 'Chapter 42'

    def test_parse_chapter_filters_empty_paragraphs(self, parser):
        """Test that empty paragraphs are filtered out."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>Valid content.</p>
                <p>   </p>
                <p></p>
                <p>More valid content.</p>
            </div>
        </body>
        </html>
        """
        
        result = parser.parse_chapter(html, 1)
        
        # Should only have the two non-empty paragraphs
        assert result is not None
        assert result.content.count('<p>') == 2

    def test_parse_chapter_strips_whitespace(self, parser):
        """Test that paragraph whitespace is stripped."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>  Content with spaces  </p>
            </div>
        </body>
        </html>
        """
        
        result = parser.parse_chapter(html, 1)
        
        assert result is not None
        assert '<p>Content with spaces</p>' in result.content

    def test_parse_chapter_includes_h1_title(self, parser, valid_chapter_html):
        """Test that parsed content includes h1 title."""
        result = parser.parse_chapter(valid_chapter_html, 1)
        
        assert '<h1>' in result.content
        assert '</h1>' in result.content

    @pytest.mark.parametrize("chapter_num", [1, 10, 100, 999])
    def test_parse_chapter_various_numbers(self, parser, valid_chapter_html, chapter_num):
        """Test parsing chapters with various chapter numbers."""
        result = parser.parse_chapter(valid_chapter_html, chapter_num)
        
        assert result is not None
        assert result.chapter_number == chapter_num

    def test_parse_malformed_html(self, parser):
        """Test parsing malformed HTML."""
        malformed = "<html><body><div id='chapter-content'><p>Unclosed paragraph</body>"
        
        # BeautifulSoup handles malformed HTML gracefully
        result = parser.parse_chapter(malformed, 1)
        
        # Should still parse something
        assert result is not None

    def test_parse_chapter_with_nested_elements(self, parser):
        """Test parsing chapter with nested HTML elements."""
        html = """
        <html>
        <body>
            <div id="chapter-content">
                <h2>Chapter 1</h2>
                <p>Text with <strong>bold</strong> and <em>italic</em>.</p>
            </div>
        </body>
        </html>
        """
        
        result = parser.parse_chapter(html, 1)
        
        assert result is not None
        # Should extract the full text including nested elements
        assert 'bold' in result.content
        assert 'italic' in result.content


class TestParseHotNovels:
    """Test hot novels parsing functionality."""

    def test_parse_hot_novels_valid_html(self, parser, hot_novels_html):
        """Test parsing valid hot novels HTML."""
        results = parser.parse_hot_novels(hot_novels_html)
        
        assert isinstance(results, list)
        assert len(results) > 0

    def test_parse_hot_novels_returns_tuples(self, parser, hot_novels_html):
        """Test that hot novels returns list of tuples."""
        results = parser.parse_hot_novels(hot_novels_html)
        
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2
            title, url = item
            assert isinstance(title, str)
            assert isinstance(url, str)

    def test_parse_hot_novels_extracts_titles(self, parser, hot_novels_html):
        """Test that novel titles are extracted."""
        results = parser.parse_hot_novels(hot_novels_html)
        
        titles = [title for title, _ in results]
        assert len(titles) > 0
        assert all(len(title) > 0 for title in titles)

    def test_parse_hot_novels_extracts_urls(self, parser, hot_novels_html):
        """Test that novel URLs are extracted."""
        results = parser.parse_hot_novels(hot_novels_html)
        
        urls = [url for _, url in results]
        assert len(urls) > 0
        assert all(len(url) > 0 for url in urls)

    def test_parse_hot_novels_empty_html(self, parser):
        """Test parsing hot novels with empty HTML."""
        results = parser.parse_hot_novels("")
        
        assert isinstance(results, list)
        assert len(results) == 0

    def test_parse_hot_novels_no_novels(self, parser):
        """Test parsing HTML with no novel elements."""
        html = "<html><body><div>No novels here</div></body></html>"
        
        results = parser.parse_hot_novels(html)
        
        assert isinstance(results, list)
        assert len(results) == 0

    def test_parse_hot_novels_missing_link(self, parser):
        """Test parsing hot novels when link is missing."""
        html = """
        <html>
        <body>
            <h3 class="truyen-title">
                Novel without link
            </h3>
        </body>
        </html>
        """
        
        results = parser.parse_hot_novels(html)
        
        # Should skip entries without links
        assert len(results) == 0

    def test_parse_hot_novels_malformed_html(self, parser):
        """Test that malformed HTML doesn't crash parser."""
        malformed = "<h3 class='truyen-title'><a href='url'>Title"
        
        results = parser.parse_hot_novels(malformed)
        
        # Should handle gracefully
        assert isinstance(results, list)

    def test_parse_hot_novels_exception_handling(self, parser):
        """Test exception handling in parse_hot_novels."""
        # Pass None to trigger exception
        results = parser.parse_hot_novels(None)
        
        # Should return empty list on error
        assert isinstance(results, list)
        assert len(results) == 0


class TestParseSearchResults:
    """Test search results parsing functionality."""

    def test_parse_search_results_valid_html(self, parser, search_results_html):
        """Test parsing valid search results HTML."""
        results = parser.parse_search_results(search_results_html)
        
        assert isinstance(results, list)
        assert len(results) > 0

    def test_parse_search_results_returns_tuples(self, parser, search_results_html):
        """Test that search results returns list of tuples."""
        results = parser.parse_search_results(search_results_html)
        
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 3
            title, url, description = item
            assert isinstance(title, str)
            assert isinstance(url, str)
            assert isinstance(description, str)

    def test_parse_search_results_extracts_titles(self, parser, search_results_html):
        """Test that titles are properly extracted."""
        results = parser.parse_search_results(search_results_html)
        
        titles = [title for title, _, _ in results]
        assert 'Dragon King' in titles
        assert 'Dragon Warrior' in titles

    def test_parse_search_results_extracts_urls(self, parser, search_results_html):
        """Test that URLs are properly extracted."""
        results = parser.parse_search_results(search_results_html)
        
        urls = [url for _, url, _ in results]
        assert any('dragon-king' in url for url in urls)

    def test_parse_search_results_adds_domain_to_relative_urls(self, parser):
        """Test that relative URLs get domain prepended."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        <a href="/novel/test-novel">Test Novel</a>
                    </h3>
                    <div class="excerpt">Description</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        assert len(results) == 1
        _, url, _ = results[0]
        assert url.startswith('https://novelfull.net')

    def test_parse_search_results_keeps_absolute_urls(self, parser):
        """Test that absolute URLs are kept as-is."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        <a href="https://example.com/novel">Test Novel</a>
                    </h3>
                    <div class="excerpt">Description</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        assert len(results) == 1
        _, url, _ = results[0]
        assert url.startswith('https://example.com')

    def test_parse_search_results_includes_author(self, parser, search_results_html):
        """Test that author is included in description."""
        results = parser.parse_search_results(search_results_html)
        
        descriptions = [desc for _, _, desc in results]
        assert any('Author:' in desc for desc in descriptions)

    def test_parse_search_results_default_description(self, parser):
        """Test that default description is used when missing."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        <a href="/novel/test">Test Novel</a>
                    </h3>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        assert len(results) == 1
        _, _, description = results[0]
        assert 'No description available' in description

    def test_parse_search_results_no_main_content(self, parser):
        """Test parsing when main content div is missing."""
        html = "<html><body><div>No main content</div></body></html>"
        
        results = parser.parse_search_results(html)
        
        assert len(results) == 0

    def test_parse_search_results_empty_html(self, parser):
        """Test parsing empty HTML."""
        results = parser.parse_search_results("")
        
        assert isinstance(results, list)
        assert len(results) == 0

    def test_parse_search_results_skips_invalid_entries(self, parser):
        """Test that entries without required elements are skipped."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        Title without link
                    </h3>
                </div>
                <div class="row">
                    <div class="excerpt">Description without title</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        # Should skip both invalid entries
        assert len(results) == 0

    def test_parse_search_results_strips_whitespace(self, parser):
        """Test that whitespace is stripped from extracted text."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        <a href="/novel/test">  Test Novel  </a>
                    </h3>
                    <div class="excerpt">  Description text  </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        title, _, description = results[0]
        assert title == 'Test Novel'
        assert description.strip() == description


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_parse_chapter_with_none(self, parser):
        """Test parsing None as HTML."""
        result = parser.parse_chapter(None, 1)
        
        # Should return None on error
        assert result is None

    def test_parse_chapter_with_invalid_type(self, parser):
        """Test parsing invalid type (not string)."""
        result = parser.parse_chapter(12345, 1)
        
        # Should handle gracefully
        assert result is None

    @patch('src.core.parser.BeautifulSoup')
    def test_parse_chapter_beautifulsoup_exception(self, mock_bs, parser):
        """Test handling of BeautifulSoup exceptions."""
        mock_bs.side_effect = Exception("Parse error")
        
        result = parser.parse_chapter("<html></html>", 1)
        
        assert result is None

    def test_parse_hot_novels_with_exception(self, parser):
        """Test that exceptions in parse_hot_novels are handled."""
        # Passing an integer should cause an error
        results = parser.parse_hot_novels(12345)
        
        assert results == []

    def test_parse_search_results_unicode(self, parser):
        """Test parsing search results with unicode characters."""
        html = """
        <html>
        <body>
            <div class="col-truyen-main">
                <div class="row">
                    <h3 class="truyen-title">
                        <a href="/novel/test">龙王传说</a>
                    </h3>
                    <div class="excerpt">中文描述</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        results = parser.parse_search_results(html)
        
        assert len(results) == 1
        title, _, description = results[0]
        assert '龙王传说' in title


class TestMockedBeautifulSoup:
    """Test HTMLParser with mocked BeautifulSoup."""

    @patch('src.core.parser.BeautifulSoup')
    def test_parse_chapter_with_mock(self, mock_bs_class, parser):
        """Test parse_chapter with mocked BeautifulSoup."""
        # Setup mock
        mock_soup = Mock()
        mock_bs_class.return_value = mock_soup
        
        # Mock content div
        mock_content_div = Mock()
        mock_soup.find.return_value = mock_content_div
        
        # Mock title
        mock_title = Mock()
        mock_title.text = "Mocked Chapter Title"
        mock_content_div.find.return_value = mock_title
        
        # Mock paragraphs
        mock_p1 = Mock()
        mock_p1.text.strip.return_value = "Paragraph 1"
        mock_p2 = Mock()
        mock_p2.text.strip.return_value = "Paragraph 2"
        mock_content_div.find_all.return_value = [mock_p1, mock_p2]
        
        result = parser.parse_chapter("<html></html>", 1)
        
        # Verify BeautifulSoup was called
        mock_bs_class.assert_called_once()
        assert result is not None

    @patch('src.core.parser.BeautifulSoup')
    def test_parse_hot_novels_with_mock(self, mock_bs_class, parser):
        """Test parse_hot_novels with mocked BeautifulSoup."""
        mock_soup = Mock()
        mock_bs_class.return_value = mock_soup
        
        # Mock novel elements
        mock_novel1 = Mock()
        mock_link1 = Mock()
        mock_link1.text.strip.return_value = "Novel 1"
        mock_link1.get.return_value = "https://example.com/novel1"
        mock_novel1.find.return_value = mock_link1
        
        mock_soup.find_all.return_value = [mock_novel1]
        
        results = parser.parse_hot_novels("<html></html>")
        
        assert len(results) == 1
        assert results[0] == ("Novel 1", "https://example.com/novel1")
