# BookScraper CLI Documentation

## Overview

BookScraper CLI is a command-line interface for downloading and managing web novels. It provides an intuitive interface for searching, downloading, and managing your novel collection.

## Command Structure

The CLI follows this general structure:
```bash
bookscraper <command> [subcommand] [options]
```

## Current Commands

### 1. Search
Search for novels by title or keywords.

```bash
bookscraper search <query> [options]
```

Options:
- `--limit, -l`: Maximum number of results (default: 10)
- `--detailed, -d`: Show detailed descriptions
- `--cache-ttl`: Cache duration in seconds (default: 3600)

Example:
```bash
bookscraper search "dragon cultivation" --limit 5
```

### 2. Hot
List trending/hot novels.

```bash
bookscraper hot [options]
```

Options:
- `--limit, -l`: Maximum number of results (default: 10)
- `--page, -p`: Page number (default: 1)
- `--cache-ttl`: Cache duration in seconds (default: 3600)

Example:
```bash
bookscraper hot --limit 20
```

### 3. Download
Download chapters from a novel.

```bash
bookscraper download <novel-name> [options]
```

Options:
- `--start, -s`: Starting chapter (default: 1)
- `--end, -e`: Ending chapter (default: 50)
- `--workers, -w`: Number of concurrent downloads (default: 5)
- `--output, -o`: Output directory (default: ./novels)
- `--format, -f`: Output format [html|txt] (default: html)

Example:
```bash
bookscraper download "martial-peak" -s 1 -e 10 -w 3
```

### 4. List
List downloaded novels.

```bash
bookscraper list [options]
```

Options:
- `--detailed, -d`: Show chapter information
- `--sort`: Sort by [name|date|chapters] (default: name)

Example:
```bash
bookscraper list --detailed --sort date
```

### 5. Config
Manage configuration settings.

```bash
bookscraper config [get|set|list]
```

Example:
```bash
bookscraper config set output_dir ~/novels
bookscraper config set max_workers 3
```

## Planned Features

### 1. Library Management
```bash
# Add tags to novels
bookscraper tag <novel-name> add|remove <tags...>

# Create reading lists
bookscraper list create|delete|add|remove <list-name> [novels...]

# Mark reading progress
bookscraper mark <novel-name> --chapter <number>
```

### 2. Content Management
```bash
# Convert between formats
bookscraper convert <novel-name> --to [epub|pdf|mobi]

# Update existing novels
bookscraper update <novel-name> [--check-only]

# Validate downloaded content
bookscraper validate <novel-name> [--fix]
```

### 3. Advanced Search
```bash
# Search with filters
bookscraper search "dragon" --genre fantasy --status complete

# Search local library
bookscraper search --local "cultivation" --tags [action,completed]
```

### 4. Statistics and Reports
```bash
# View reading statistics
bookscraper stats [novel-name]

# Generate library report
bookscraper report [--format pdf]
```

## Configuration

The CLI uses a configuration file located at `~/.config/bookscraper/config.yaml`:

```yaml
# Default settings
output_dir: ~/novels
max_workers: 5
default_format: html
cache_ttl: 3600

# Site-specific settings
sites:
  novelfull:
    enabled: true
    rate_limit: 1  # requests per second
  novelusb:
    enabled: true
    rate_limit: 2

# Display settings
progress_bar: true
color_output: true
verbose: false
```

## Error Handling

The CLI provides clear error messages and suggestions:

```bash
$ bookscraper download "invalid-novel"
Error: Novel "invalid-novel" not found
Suggestions:
1. Check the spelling
2. Use 'bookscraper search' to find the correct name
3. Use quotes if the name contains spaces
```

## Development Guidelines

### Adding New Commands

1. Create a new command module in `src/cli/commands/`
2. Implement the command class with `@click.command()` decorator
3. Add command to the main CLI group
4. Update documentation

Example:
```python
@click.command()
@click.argument('novel_name')
@click.option('--format', '-f', default='html')
def convert(novel_name: str, format: str):
    """Convert novel to different format."""
    pass
```

### Command Structure Guidelines

1. Use verb-based command names
2. Provide short and long option names
3. Include help text for all commands
4. Implement --help for all commands
5. Follow consistent naming conventions

## Testing

Run CLI tests:
```bash
pytest tests/cli/
```

## Contribution

When adding new commands:

1. Update CLI.md documentation
2. Add appropriate tests
3. Follow error handling guidelines
4. Update help messages
5. Consider backward compatibility
