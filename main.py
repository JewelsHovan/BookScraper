from pathlib import Path
from src.core.scraper import BookScraper

def main():
    # Initialize the scraper with an output directory
    scraper = BookScraper(Path("./novels"))
    
    # Example 1: Search for novels
    print("Searching for novels containing 'dragon'...")
    results = scraper.search_novels("dragon")
    for title, url, description in results[:3]:  # Show first 3 results
        print(f"\nTitle: {title}")
        print(f"Description: {description}")
    
    # Example 2: Get hot novels
    print("\nFetching hot novels...")
    hot_novels = scraper.get_hot_novels()
    print("\nTop 5 Hot Novels:")
    for novel in hot_novels[:5]:
        print(f"- {novel.title}")
    
    # Example 3: Download a specific book
    book_name = "martial-peak"  # Example book
    print(f"\nDownloading {book_name} (chapters 1-5)...")
    output_file = scraper.download_book(book_name, start_chapter=1, end_chapter=5)
    
    if output_file:
        print(f"Book downloaded successfully to: {output_file}")
    else:
        print("Failed to download book")

if __name__ == "__main__":
    main()