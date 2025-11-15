"""
Integration Tests for BookScraper

This package contains integration tests that verify the interaction between
multiple components of the BookScraper application.

Test Modules:
    - test_scraper_integration.py: Tests for scraper with parser and fetcher
    - test_download_flow.py: Tests for complete download workflow
    - test_cli_integration.py: Tests for CLI commands with real components
    - test_search_workflow.py: Tests for search functionality end-to-end
    - test_file_operations.py: Tests for file handling with real I/O

Guidelines for Integration Tests:
    - Test multiple components working together
    - May use real file I/O with temporary directories
    - May take longer than unit tests
    - Should still avoid actual network calls (use mocks or VCR)
    - Test realistic user workflows
    - Verify data flow between components

Example Integration Test:
    def test_download_chapter_workflow():
        # Arrange: Set up real components with mocked network
        fetcher = Mock(spec=HTMLFetcher)
        fetcher.fetch.return_value = sample_html
        parser = HTMLParser()
        file_handler = FileHandler(temp_dir)
        downloader = ChapterDownloader(fetcher, parser, file_handler)
        
        # Act: Execute the workflow
        success = downloader.download_chapter(book, chapter_num)
        
        # Assert: Verify end-to-end behavior
        assert success
        assert chapter_file.exists()
        assert "expected content" in chapter_file.read_text()
"""

__all__ = []
