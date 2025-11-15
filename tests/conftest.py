"""
Common pytest fixtures for BookScraper tests.

This module provides reusable fixtures for testing the BookScraper application,
including mock objects, sample data, and temporary directories.

Note: Some fixtures require BookScraper dependencies to be installed.
Install with: pip install -r requirements.txt
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import Mock, MagicMock
from typing import List, Optional
import tempfile
import shutil

# Try to import BookScraper modules (may fail if dependencies not installed)
try:
    from src.models.book import Book
    from src.core.parser import ParsedChapter
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    # Create dummy classes for when dependencies aren't installed
    from dataclasses import dataclass
    from typing import Optional, List
    
    @dataclass
    class Book:
        title: str
        folder_path: Path
        chapters: Optional[List[int]] = None
        description: Optional[str] = None
        author: Optional[str] = None
        
        @property
        def formatted_title(self) -> str:
            return self.title.lower().replace(' ', '-')
        
        @property
        def html_path(self) -> Path:
            return self.folder_path / f"{self.formatted_title}.html"
    
    @dataclass
    class ParsedChapter:
        title: str
        content: str
        chapter_number: int

try:
    from src.utils.html_fetcher import HTMLFetcher
    from src.utils.file_handler import FileHandler
    from src.core.parser import HTMLParser
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    # Create dummy classes
    HTMLFetcher = object
    FileHandler = object
    HTMLParser = object


# ============================================================================
# Directory and Path Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_book():
    """Create a sample Book instance for testing."""
    return Book(
        title="The Great Adventure",
        folder_path=Path("/tmp/books/the-great-adventure"),
        chapters=[1, 2, 3, 4, 5],
        description="An epic tale of adventure and discovery.",
        author="John Doe"
    )


@pytest.fixture
def sample_book_list():
    """Create a list of sample Book instances."""
    return [
        Book(
            title="The Great Adventure",
            folder_path=Path("/tmp/books/the-great-adventure"),
            chapters=[1, 2, 3],
            description="An epic tale",
            author="John Doe"
        ),
        Book(
            title="Mystery Manor",
            folder_path=Path("/tmp/books/mystery-manor"),
            chapters=[1, 2],
            description="A thrilling mystery",
            author="Jane Smith"
        ),
        Book(
            title="Space Odyssey",
            folder_path=Path("/tmp/books/space-odyssey"),
            chapters=[1, 2, 3, 4],
            description="Journey through the stars",
            author="Bob Wilson"
        )
    ]


@pytest.fixture
def sample_parsed_chapter():
    """Create a sample ParsedChapter instance."""
    return ParsedChapter(
        title="Chapter 1: The Beginning",
        content="<h1>Chapter 1: The Beginning</h1>\n<p>This is the first paragraph.</p>\n<p>This is the second paragraph.</p>",
        chapter_number=1
    )


# ============================================================================
# HTML Content Fixtures
# ============================================================================

@pytest.fixture
def sample_chapter_html(fixtures_dir):
    """Load sample chapter HTML from fixtures."""
    html_file = fixtures_dir / "sample_chapter.html"
    if html_file.exists():
        return html_file.read_text()
    # Fallback if file doesn't exist yet
    return """
<!DOCTYPE html>
<html>
<head><title>Chapter 1</title></head>
<body>
    <div id="chapter-content">
        <h2>Chapter 1: The Beginning</h2>
        <p>This is the first paragraph of the chapter.</p>
        <p>This is the second paragraph with more content.</p>
        <p>And here's a third paragraph to make it interesting.</p>
    </div>
</body>
</html>
"""


@pytest.fixture
def sample_search_html(fixtures_dir):
    """Load sample search results HTML from fixtures."""
    html_file = fixtures_dir / "sample_search.html"
    if html_file.exists():
        return html_file.read_text()
    # Fallback
    return """
<!DOCTYPE html>
<html>
<body>
    <div class="col-truyen-main">
        <div class="row">
            <h3 class="truyen-title">
                <a href="/the-great-adventure">The Great Adventure</a>
            </h3>
            <div class="excerpt">An epic tale of adventure and discovery.</div>
            <span class="author">John Doe</span>
        </div>
        <div class="row">
            <h3 class="truyen-title">
                <a href="/mystery-manor">Mystery Manor</a>
            </h3>
            <div class="excerpt">A thrilling mystery in an old mansion.</div>
            <span class="author">Jane Smith</span>
        </div>
    </div>
</body>
</html>
"""


@pytest.fixture
def sample_hot_novels_html(fixtures_dir):
    """Load sample hot novels HTML from fixtures."""
    html_file = fixtures_dir / "sample_hot_novels.html"
    if html_file.exists():
        return html_file.read_text()
    # Fallback
    return """
<!DOCTYPE html>
<html>
<body>
    <div class="hot-novels">
        <h3 class="truyen-title">
            <a href="https://novelfull.net/novel/trending-novel-1">Trending Novel 1</a>
        </h3>
        <h3 class="truyen-title">
            <a href="https://novelfull.net/novel/trending-novel-2">Trending Novel 2</a>
        </h3>
        <h3 class="truyen-title">
            <a href="https://novelfull.net/novel/trending-novel-3">Trending Novel 3</a>
        </h3>
    </div>
</body>
</html>
"""


@pytest.fixture
def invalid_chapter_html(fixtures_dir):
    """Load invalid/malformed chapter HTML from fixtures."""
    html_file = fixtures_dir / "invalid_chapter.html"
    if html_file.exists():
        return html_file.read_text()
    # Fallback
    return """
<!DOCTYPE html>
<html>
<head><title>Broken Chapter</title></head>
<body>
    <div id="wrong-id">
        <p>Content is in the wrong container.</p>
    </div>
    <!-- Missing chapter-content div -->
</body>
</html>
"""


@pytest.fixture
def empty_search_html():
    """Return HTML with no search results."""
    return """
<!DOCTYPE html>
<html>
<body>
    <div class="col-truyen-main">
        <!-- No results -->
    </div>
</body>
</html>
"""


# ============================================================================
# Mock Component Fixtures
# ============================================================================

@pytest.fixture
def mock_html_fetcher():
    """Create a mock HTMLFetcher instance."""
    fetcher = Mock(spec=HTMLFetcher)
    fetcher.fetch = Mock(return_value="<html><body>Mock content</body></html>")
    fetcher.timeout = 10
    fetcher.session = Mock()
    return fetcher


@pytest.fixture
def mock_file_handler(temp_dir):
    """Create a mock FileHandler instance."""
    handler = Mock(spec=FileHandler)
    handler.base_path = temp_dir
    handler.books_file = temp_dir / 'books.pkl'
    handler.save_books = Mock(return_value=None)
    handler.load_books = Mock(return_value=[])
    handler.save_chapter = Mock(return_value=True)
    handler.combine_chapters = Mock(return_value=temp_dir / 'combined.html')
    return handler


@pytest.fixture
def mock_parser():
    """Create a mock HTMLParser instance."""
    parser = Mock(spec=HTMLParser)
    parser.content_id = 'chapter-content'
    parser.parse_chapter = Mock(return_value=ParsedChapter(
        title="Mock Chapter",
        content="<h1>Mock Chapter</h1><p>Mock content</p>",
        chapter_number=1
    ))
    parser.parse_hot_novels = Mock(return_value=[
        ("Novel 1", "https://example.com/novel-1"),
        ("Novel 2", "https://example.com/novel-2")
    ])
    parser.parse_search_results = Mock(return_value=[
        ("Novel 1", "https://example.com/novel-1", "Description 1"),
        ("Novel 2", "https://example.com/novel-2", "Description 2")
    ])
    return parser


@pytest.fixture
def real_file_handler(temp_dir):
    """Create a real FileHandler instance with a temporary directory."""
    if not UTILS_AVAILABLE:
        pytest.skip("FileHandler not available - install dependencies")
    return FileHandler(temp_dir)


@pytest.fixture
def real_parser():
    """Create a real HTMLParser instance."""
    if not UTILS_AVAILABLE:
        pytest.skip("HTMLParser not available - install dependencies")
    return HTMLParser(content_id='chapter-content')


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def mock_config():
    """Create a mock configuration dictionary."""
    return {
        'base_url': 'https://novelfull.net',
        'base_path': '/tmp/books',
        'timeout': 10,
        'max_retries': 3,
        'chunk_size': 10,
        'delay': 0.5,
        'user_agent': 'BookScraper/1.0'
    }


@pytest.fixture
def sample_url_params():
    """Sample URL parameters for testing."""
    return {
        'book_title': 'the-great-adventure',
        'chapter_number': 1,
        'page': 1,
        'search_term': 'adventure'
    }


# ============================================================================
# Response Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_successful_response(sample_chapter_html):
    """Create a mock successful HTTP response."""
    response = Mock()
    response.status_code = 200
    response.text = sample_chapter_html
    response.raise_for_status = Mock()
    response.ok = True
    return response


@pytest.fixture
def mock_failed_response():
    """Create a mock failed HTTP response."""
    response = Mock()
    response.status_code = 404
    response.text = "Not Found"
    response.ok = False
    response.raise_for_status = Mock(side_effect=Exception("404 Not Found"))
    return response


@pytest.fixture
def mock_timeout_response():
    """Create a mock timeout response."""
    response = Mock()
    response.side_effect = TimeoutError("Request timed out")
    return response


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("tests/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark tests based on their path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark slow tests (those with timeout or network operations)
        if "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
