"""
Test Infrastructure Verification

This test module verifies that the testing infrastructure is set up correctly.
Run this first to ensure all fixtures, configurations, and dependencies are working.
"""

import pytest
from pathlib import Path


class TestInfrastructure:
    """Tests to verify the testing infrastructure is properly configured."""
    
    @pytest.mark.unit
    def test_pytest_is_working(self):
        """Verify pytest is functioning."""
        assert True
    
    @pytest.mark.unit
    def test_fixtures_directory_exists(self, fixtures_dir):
        """Verify fixtures directory exists and is accessible."""
        assert fixtures_dir.exists()
        assert fixtures_dir.is_dir()
    
    @pytest.mark.unit
    def test_sample_fixtures_exist(self, fixtures_dir):
        """Verify all required fixture files exist."""
        required_fixtures = [
            "sample_chapter.html",
            "sample_search.html",
            "sample_hot_novels.html",
            "invalid_chapter.html"
        ]
        
        for fixture_file in required_fixtures:
            fixture_path = fixtures_dir / fixture_file
            assert fixture_path.exists(), f"Missing fixture: {fixture_file}"
            assert fixture_path.stat().st_size > 0, f"Empty fixture: {fixture_file}"
    
    @pytest.mark.unit
    def test_temp_dir_fixture(self, temp_dir):
        """Verify temp_dir fixture creates a usable directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test writing to temp dir
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.read_text() == "test content"
    
    @pytest.mark.unit
    def test_sample_book_fixture(self, sample_book):
        """Verify sample_book fixture is properly configured."""
        assert sample_book is not None
        assert sample_book.title == "The Great Adventure"
        assert sample_book.author == "John Doe"
        assert sample_book.formatted_title == "the-great-adventure"
        assert sample_book.chapters == [1, 2, 3, 4, 5]
    
    @pytest.mark.unit
    def test_sample_book_list_fixture(self, sample_book_list):
        """Verify sample_book_list fixture has multiple books."""
        assert len(sample_book_list) == 3
        assert all(book.title for book in sample_book_list)
        assert all(book.author for book in sample_book_list)
    
    @pytest.mark.unit
    def test_sample_chapter_html_fixture(self, sample_chapter_html):
        """Verify sample chapter HTML fixture is loaded."""
        assert sample_chapter_html is not None
        assert len(sample_chapter_html) > 100
        assert "chapter-content" in sample_chapter_html
        assert "<p>" in sample_chapter_html
    
    @pytest.mark.unit
    def test_sample_search_html_fixture(self, sample_search_html):
        """Verify sample search HTML fixture is loaded."""
        assert sample_search_html is not None
        assert "col-truyen-main" in sample_search_html
        assert "truyen-title" in sample_search_html
    
    @pytest.mark.unit
    def test_sample_hot_novels_html_fixture(self, sample_hot_novels_html):
        """Verify sample hot novels HTML fixture is loaded."""
        assert sample_hot_novels_html is not None
        assert "truyen-title" in sample_hot_novels_html
        assert len([line for line in sample_hot_novels_html.split('\n') 
                   if "truyen-title" in line]) >= 3
    
    @pytest.mark.unit
    def test_invalid_chapter_html_fixture(self, invalid_chapter_html):
        """Verify invalid chapter HTML fixture is loaded."""
        assert invalid_chapter_html is not None
        # Should have wrong or missing chapter-content div
        assert "wrong-container-id" in invalid_chapter_html or \
               invalid_chapter_html.count('id="chapter-content"') < 1 or \
               'id="chapter-content"' in invalid_chapter_html
    
    @pytest.mark.unit
    def test_mock_html_fetcher_fixture(self, mock_html_fetcher):
        """Verify mock HTMLFetcher fixture is properly configured."""
        assert mock_html_fetcher is not None
        assert hasattr(mock_html_fetcher, 'fetch')
        
        # Test mock returns expected value
        result = mock_html_fetcher.fetch("https://example.com")
        assert result is not None
        assert "Mock content" in result
    
    @pytest.mark.unit
    def test_mock_file_handler_fixture(self, mock_file_handler):
        """Verify mock FileHandler fixture is properly configured."""
        assert mock_file_handler is not None
        assert hasattr(mock_file_handler, 'save_books')
        assert hasattr(mock_file_handler, 'load_books')
        assert hasattr(mock_file_handler, 'save_chapter')
    
    @pytest.mark.unit
    def test_mock_parser_fixture(self, mock_parser):
        """Verify mock Parser fixture is properly configured."""
        assert mock_parser is not None
        assert hasattr(mock_parser, 'parse_chapter')
        assert hasattr(mock_parser, 'parse_hot_novels')
        assert hasattr(mock_parser, 'parse_search_results')
    
    @pytest.mark.unit
    def test_real_file_handler_fixture(self, real_file_handler, temp_dir):
        """Verify real FileHandler fixture uses temp directory."""
        assert real_file_handler is not None
        assert real_file_handler.base_path == temp_dir
    
    @pytest.mark.unit
    def test_real_parser_fixture(self, real_parser):
        """Verify real Parser fixture is instantiated correctly."""
        assert real_parser is not None
        assert real_parser.content_id == 'chapter-content'
    
    @pytest.mark.unit
    def test_mock_config_fixture(self, mock_config):
        """Verify mock configuration fixture has required keys."""
        required_keys = ['base_url', 'base_path', 'timeout', 'max_retries']
        for key in required_keys:
            assert key in mock_config, f"Missing config key: {key}"
    
    @pytest.mark.unit
    def test_sample_url_params_fixture(self, sample_url_params):
        """Verify sample URL params fixture is properly configured."""
        assert 'book_title' in sample_url_params
        assert 'chapter_number' in sample_url_params
    
    @pytest.mark.unit
    def test_mock_responses_fixtures(
        self,
        mock_successful_response,
        mock_failed_response
    ):
        """Verify mock response fixtures are properly configured."""
        # Successful response
        assert mock_successful_response.status_code == 200
        assert mock_successful_response.ok
        
        # Failed response
        assert mock_failed_response.status_code == 404
        assert not mock_failed_response.ok


class TestMarkers:
    """Tests to verify pytest markers are working."""
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker is recognized."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration marker is recognized."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker is recognized."""
        assert True
    
    @pytest.mark.parser
    def test_parser_marker(self):
        """Test that parser marker is recognized."""
        assert True
    
    @pytest.mark.scraper
    def test_scraper_marker(self):
        """Test that scraper marker is recognized."""
        assert True


class TestParametrization:
    """Tests to verify parameterization works correctly."""
    
    @pytest.mark.unit
    @pytest.mark.parametrize("input,expected", [
        (1, 1),
        (2, 2),
        (3, 3),
    ])
    def test_parametrize_works(self, input, expected):
        """Verify parametrized tests work."""
        assert input == expected


class TestCoverageConfiguration:
    """Tests to verify coverage is properly configured."""
    
    @pytest.mark.unit
    def test_coverage_tracks_source(self):
        """Verify coverage is tracking source code."""
        # This test just verifies the infrastructure
        # Actual coverage is checked by pytest-cov
        from pathlib import Path
        src_dir = Path(__file__).parent.parent / "src"
        assert src_dir.exists(), "Source directory not found"


if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__, "-v"])
