from pathlib import Path
from src.core.scraper import BookScraper
from src.utils.html_fetcher import HTMLFetcher
from src.utils.url_builder import URLBuilder
from bs4 import BeautifulSoup

def analyze_html(content):
    """Analyze HTML content for debugging"""
    soup = BeautifulSoup(content, 'lxml')
    
    print("\nHTML Structure Analysis:")
    
    # 1. Find main content container
    main_content = soup.find("div", class_="col-truyen-main")
    if main_content:
        print(" Found main content container")
        
        # 2. Look at the first search result's structure
        first_row = main_content.find("div", class_="row")
        if first_row:
            print("\nFirst search result's HTML structure:")
            print("-" * 50)
            print(first_row.prettify())
            print("-" * 50)
        else:
            print(" No search result rows found in main content")
    else:
        print(" Main content container not found")

def test_search():
    # Initialize components
    print("\n=== Testing Search Functionality ===")
    
    # 1. Test URL generation
    print("\n1. Testing URL Builder:")
    url_builder = URLBuilder()
    search_term = "dragon"
    search_url = url_builder.get_search_url(search_term)
    print(f"Search Term: {search_term}")
    print(f"Generated URL: {search_url}")
    
    # 2. Test HTML fetching
    print("\n2. Testing HTML Fetching:")
    with HTMLFetcher() as fetcher:
        print("Fetching content...")
        content = fetcher.fetch(search_url)
        if content:
            print(f"Content length: {len(content)} characters")
            print("\nFirst 500 characters of response:")
            print("-" * 50)
            print(content[:500])
            print("-" * 50)
            analyze_html(content)
        else:
            print("No content received!")
    
    # 3. Test full search through scraper
    print("\n3. Testing Full Search:")
    scraper = BookScraper(Path("./novels"))
    results = scraper.search_novels(search_term)
    
    print(f"\nFound {len(results)} results")
    if results:
        print("\nFirst 3 results:")
        for i, (title, url, desc) in enumerate(results[:3], 1):
            print(f"\nResult {i}:")
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Description: {desc[:100]}...")
    else:
        print("No results found!")

if __name__ == "__main__":
    test_search()
