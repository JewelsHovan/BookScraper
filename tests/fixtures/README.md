# Test Fixtures

This directory contains sample HTML files and data used for testing the BookScraper application.

## HTML Fixtures

### sample_chapter.html
A valid, well-formed chapter HTML page containing:
- Proper HTML5 structure
- A div with id="chapter-content"
- Chapter title in an h2 tag
- Multiple paragraphs of content
- Navigation links
- Realistic novel chapter content

**Use for:**
- Testing successful chapter parsing
- Validating content extraction
- Testing paragraph extraction
- Verifying title extraction

### sample_search.html
A valid search results page containing:
- Multiple novel results (3 novels)
- Each result has title, author, description
- Proper class structure (col-truyen-main, truyen-title, etc.)
- Additional metadata (genre, status, chapters, rating)
- Pagination controls

**Use for:**
- Testing search result parsing
- Validating multiple result extraction
- Testing metadata extraction
- Verifying URL construction

### sample_hot_novels.html
A valid hot/trending novels page containing:
- 10 popular novels in ranked order
- Each novel has title, author, views
- Rank badges
- Proper link structure
- Pagination

**Use for:**
- Testing hot novels parsing
- Validating ranking order
- Testing bulk novel extraction
- Verifying popularity data extraction

### invalid_chapter.html
A malformed/invalid chapter page containing:
- Wrong container IDs (not "chapter-content")
- Broken HTML structure
- Unclosed tags
- Empty content areas
- Nested malformed elements

**Use for:**
- Testing error handling
- Validating graceful failure
- Testing parser robustness
- Verifying validation logic

## Using Fixtures in Tests

### Loading Fixtures

Fixtures can be loaded using the pytest fixtures defined in `conftest.py`:

```python
def test_parse_chapter(sample_chapter_html):
    parser = HTMLParser()
    result = parser.parse_chapter(sample_chapter_html, 1)
    assert result is not None
    assert "Beginning" in result.title
```

### Direct File Access

You can also load fixtures directly:

```python
def test_with_fixture_file(fixtures_dir):
    html_file = fixtures_dir / "sample_chapter.html"
    html_content = html_file.read_text()
    # Use html_content in your test
```

### Creating Custom Fixtures

For specific test cases, you can create custom HTML inline:

```python
def test_custom_html():
    custom_html = """
    <div id="chapter-content">
        <h2>Custom Chapter</h2>
        <p>Custom content</p>
    </div>
    """
    # Test with custom_html
```

## Fixture Maintenance

When updating the BookScraper to handle new HTML structures:

1. Update existing fixtures to match new patterns
2. Add new fixtures for new page types
3. Keep invalid fixtures to test backward compatibility
4. Document changes in this README

## Coverage Matrix

| Fixture | Parser | Scraper | Validator | File Handler |
|---------|--------|---------|-----------|--------------|
| sample_chapter.html | ✓ | ✓ | ✓ | ✓ |
| sample_search.html | ✓ | ✓ | ✓ | - |
| sample_hot_novels.html | ✓ | ✓ | - | - |
| invalid_chapter.html | ✓ | ✓ | ✓ | - |

## Best Practices

1. **Realistic Data**: Fixtures should mirror real website HTML structure
2. **Self-Contained**: Each fixture should be usable independently
3. **Documented**: Add comments in HTML for complex structures
4. **Version Control**: Keep fixtures in git to track HTML structure changes
5. **Minimal Size**: Keep fixtures as small as possible while being realistic
6. **Valid HTML**: Use proper HTML5 structure unless testing error cases
