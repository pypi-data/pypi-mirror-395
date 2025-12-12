# TidyLog

Clean, colorized structured logging for Python with JSON extra fields.

## Installation

```bash
pip install tidylog
```

## Usage

### Console Logging

```python
from tidylog import get_logger

logger = get_logger(__name__)
logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
```

Output:
```
2024-01-15 10:30:00 - myapp - INFO - User logged in - {"user_id": 123, "ip": "192.168.1.1"}
```

### File Logging

```python
from tidylog import setup_file_logging

handler = setup_file_logging(
    "logs/app.log",
    level="DEBUG",
    logger_names=["myapp", "myapp.api"],
)
```

## Examples

```bash
# Install in development mode
poetry install

# Run examples
poetry run python examples/console_logging.py
poetry run python examples/file_logging.py
poetry run python examples/custom_formatter.py
```

## Build & Deploy

```bash
pip install build twine
python -m build
twine upload dist/*
```
