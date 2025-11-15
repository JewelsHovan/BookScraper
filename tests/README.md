# BookScraper Test Suite

## Overview
This directory contains the comprehensive test suite for the BookScraper project.

## Test Structure
```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared pytest fixtures and configuration
├── fixtures/                # HTML and data fixtures for testing
│   ├── valid_chapter.html
│   ├── chapter_missing_content_div.html
│   ├── chapter_empty_content.html
│   ├── chapter_too_short.html
│   ├── chapter_with_error.html
│   ├── search_results.html
│   └── hot_novels.html
├── unit/                    # Unit tests for individual components
│   ├── __init__.py
│   ├── test_validator.py    # ContentValidator tests (24 tests)
│   ├── test_url_builder.py  # URLBuilder tests (45 tests)
│   └── test_parser.py       # HTMLParser tests (46 tests)
└── integration/             # Integration tests (future)
```

## Test Coverage

### Current Coverage (100% for tested modules)
- **src/utils/validator.py**: 100% coverage (41/41 statements)
- **src/utils/url_builder.py**: 100% coverage (21/21 statements)
- **src/core/parser.py**: 100% coverage (71/71 statements)

### Total Tests: 115 tests, all passing

## Running Tests

### Run all tests
```bash
python -m pytest tests/unit/ -v
```

### Run specific test file
```bash
python -m pytest tests/unit/test_validator.py -v
python -m pytest tests/unit/test_url_builder.py -v
python -m pytest tests/unit/test_parser.py -v
```

### Run with coverage report
```bash
python -m pytest tests/unit/ --cov=src/utils/validator --cov=src/utils/url_builder --cov=src/core/parser --cov-report=term-missing
```

### Run specific test class or method
```bash
python -m pytest tests/unit/test_validator.py::TestContentValidator -v
python -m pytest tests/unit/test_validator.py::TestContentValidator::test_valid_chapter_content -v
```

## Test Details

### test_validator.py (24 tests)
Tests for the `ContentValidator` class that validates chapter content.

**Test Classes:**
- `TestContentValidator`: Main validation logic tests

**Key Test Scenarios:**
- Valid chapter content validation
- Missing content div detection
- Empty content handling
- Content length validation (too short/too long)
- Error indicator detection (404, page not found, etc.)
- Warning conditions (chapter number mismatch, short content)
- ValidationResult structure validation
- Exception handling
- Malformed HTML handling
- Unicode and special character handling

### test_url_builder.py (45 tests)
Tests for the `URLBuilder` class that generates URLs for different sites.

**Test Classes:**
- `TestURLBuilderInitialization`: Initialization and config loading
- `TestChapterURLGeneration`: Chapter URL generation
- `TestSearchURLGeneration`: Search URL generation
- `TestHotNovelsURLGeneration`: Hot novels URL generation
- `TestTemplateLoading`: Template configuration
- `TestTemplateFormatting`: Template formatting and errors
- `TestEdgeCases`: Edge cases and boundary conditions

**Key Test Scenarios:**
- Default and custom initialization
- URL generation for different sites (novelfull, novelusb)
- Search URL generation with special characters and spaces
- Hot novels URL generation with pagination
- Template loading from JSON config
- Invalid site name error handling
- Template formatting errors
- Unicode and edge cases

### test_parser.py (46 tests)
Tests for the `HTMLParser` class that parses HTML content.

**Test Classes:**
- `TestHTMLParserInitialization`: Parser initialization
- `TestParseChapter`: Chapter parsing functionality
- `TestParseHotNovels`: Hot novels list parsing
- `TestParseSearchResults`: Search results parsing
- `TestErrorHandling`: Error handling and edge cases
- `TestMockedBeautifulSoup`: Tests with mocked BeautifulSoup

**Key Test Scenarios:**
- Valid chapter parsing
- Title and paragraph extraction
- Missing content div handling
- Custom content ID support
- Default title fallback
- Empty paragraph filtering
- Whitespace stripping
- Hot novels list parsing
- Search results parsing with author information
- Relative URL to absolute URL conversion
- Malformed HTML handling
- Exception handling
- Unicode support

## Test Fixtures

The `fixtures/` directory contains HTML samples used for testing:
- **valid_chapter.html**: Complete valid chapter with all elements
- **chapter_missing_content_div.html**: Chapter without content div
- **chapter_empty_content.html**: Chapter with empty content
- **chapter_too_short.html**: Chapter with insufficient content
- **chapter_with_error.html**: Chapter containing error indicators
- **search_results.html**: Valid search results page
- **hot_novels.html**: Valid hot novels list page

## Best Practices

### Writing New Tests
1. Use descriptive test names that explain what is being tested
2. Include docstrings for each test method
3. Use pytest fixtures for common setup
4. Group related tests in classes
5. Use `@pytest.mark.parametrize` for testing multiple inputs
6. Include edge cases and error conditions
7. Aim for >90% code coverage

### Test Organization
- Put unit tests in `tests/unit/`
- Put integration tests in `tests/integration/`
- Store test data in `tests/fixtures/`
- Use `conftest.py` for shared fixtures
- Keep test files organized by module

### Assertions
```python
# Good - descriptive assertion messages
assert result.is_valid is True, "Valid content should pass validation"

# Good - specific assertions
assert len(result.errors) == 0
assert "404" in error_message.lower()

# Good - type checking
assert isinstance(result, ValidationResult)
```

## Dependencies
- pytest>=7.4.0
- pytest-cov>=4.1.0
- pytest-mock>=3.11.1
- responses>=0.23.0
- beautifulsoup4>=4.12.2
- lxml>=4.9.3

## Contributing
When adding new functionality:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain >90% code coverage
4. Add docstrings to test methods
5. Update this README if adding new test files

## Continuous Integration
Tests are automatically run on:
- Every commit
- Pull requests
- Before merging to main branch

## Future Test Coverage
Modules to be tested in future iterations:
- src/core/scraper.py
- src/core/downloader.py
- src/utils/html_fetcher.py
- src/utils/file_handler.py
- src/utils/cache.py
- src/cli/commands/*.py
