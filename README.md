# BookScraper

A powerful command-line tool for downloading web novels with concurrent chapter downloading, caching, and comprehensive novel management.

## Features

- 🚀 Concurrent chapter downloads for faster retrieval
- 💾 File-based caching system
- 🔍 Advanced search functionality
- 📚 Novel library management
- 🔥 Hot novels tracking
- ⚙️ Configurable settings
- 🛡️ Built-in rate limiting and retry mechanisms

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BookScraper.git
cd BookScraper
```

2. Install dependencies:
```bash
pip install -e .
```

## CLI Commands

The BookScraper CLI provides several commands for managing and downloading web novels:

### Search Novels
Search for novels by title or keywords:
```bash
bookscraper search "dragon" --detailed
```
Options:
- `--detailed`: Show extended information including descriptions

### Download Novels
Download chapters from a novel:
```bash
bookscraper download "martial-peak" --start 1 --end 10
```
Options:
- `--start`: Starting chapter number (default: 1)
- `--end`: Ending chapter number
- `--workers`: Number of concurrent downloads (default: from config)

### Hot Novels
List trending/popular novels:
```bash
bookscraper hot --limit 20
```
Options:
- `--limit`: Maximum number of novels to show

### List Library
View your downloaded novels:
```bash
bookscraper list --detailed
```
Options:
- `--detailed`: Show additional information about each novel

### Configure Settings
Manage BookScraper settings:
```bash
bookscraper config set output_dir ~/my-novels
bookscraper config get output_dir
```
Available settings:
- `output_dir`: Novel download location
- `max_workers`: Concurrent download threads
- `cache_ttl`: Cache duration
- `sites`: Website-specific settings

## Configuration

The default configuration file is located at `~/.config/bookscraper/config.yaml`. You can modify these settings:

```yaml
output_dir: "~/novels"
max_workers: 5
cache_ttl: 3600
sites:
  novelfull:
    base_url: "https://novelfull.net"
    rate_limit: 1.0
```

## Project Structure

```
BookScraper/
├── src/
│   ├── cli/           # CLI implementation
│   ├── core/          # Core functionality
│   ├── utils/         # Utility functions
│   └── models/        # Data models
├── tests/             # Test suite
└── novels/            # Default download directory
```

## Development

- Python 3.9+ recommended
- Uses virtual environment
- Type hints throughout codebase
- Modular and extensible architecture

## Dependencies

- requests: HTTP requests
- beautifulsoup4: HTML parsing
- lxml: XML/HTML processing
- click: CLI framework
- rich: Terminal formatting
- tqdm: Progress bars
- PyYAML: Configuration management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
