# Test Logs Directory

This directory contains pytest log files generated during test execution.

## Log Files

- `pytest.log`: Detailed DEBUG-level logs from all test runs
- Log files are automatically created by pytest based on `pytest.ini` configuration

## Configuration

Log settings are defined in `pytest.ini`:
- Log level: DEBUG
- Format: Timestamp, level, logger name, and message
- Rotation: Logs are appended to existing files

## Viewing Logs

```bash
# View recent logs
tail -f tests/logs/pytest.log

# Search logs for specific test
grep "test_function_name" tests/logs/pytest.log

# View errors only
grep "ERROR" tests/logs/pytest.log
```

## Cleanup

Log files can grow large over time. Clean them periodically:

```bash
# Remove old logs
rm tests/logs/*.log

# Keep only recent logs
find tests/logs -name "*.log" -mtime +7 -delete
```

## Git Ignore

Log files are git-ignored by default. Only the directory structure is tracked.
