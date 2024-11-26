# BookScraper

A Python-based web scraper for downloading novels from various online sources. This project demonstrates modern Python practices with proper error handling, type hints, and modular design.

## Features

- Search for novels by title
- Get list of hot/trending novels
- Download complete novels chapter by chapter
- Combine chapters into a single HTML file
- Support for multiple novel websites (extensible)
- Robust error handling and retry logic
- Clean and modular code structure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BookScraper.git
cd BookScraper
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from pathlib import Path
from src.core.scraper import BookScraper

# Initialize the scraper with output directory
scraper = BookScraper(Path("./novels"))

# Search for novels
results = scraper.search_novels("dragon")
for title, url, description in results:
    print(f"{title}: {description}")

# Get hot novels
hot_novels = scraper.get_hot_novels()
for novel in hot_novels:
    print(novel.title)

# Download a book
output_file = scraper.download_book("some-novel-name", start_chapter=1, end_chapter=10)
if output_file:
    print(f"Book downloaded to: {output_file}")
```

## Project Structure

```
BookScraper/
├── src/
│   ├── core/
│   │   ├── scraper.py     # Main scraper class
│   │   └── parser.py      # HTML parsing logic
│   ├── models/
│   │   └── book.py        # Book data model
│   └── utils/
│       ├── url_builder.py # URL generation
│       ├── file_handler.py# File operations
│       └── html_fetcher.py# HTTP requests
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
