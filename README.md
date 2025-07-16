# HF Transformers

A comprehensive Python project template for transformers with common utilities, base classes, and best practices for building scalable applications.

## Features

- **Base Classes**: Abstract base classes with common functionality
- **Configuration Management**: Flexible configuration handling with environment variables and JSON files
- **Logging**: Centralized logging with configurable levels and outputs
- **Data Processing**: Utilities for reading/writing JSON, CSV, and text files
- **API Client**: HTTP client with retry logic and error handling
- **Utility Classes**: String, file, and date utilities
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Black formatting, flake8 linting, and mypy type checking

## Project Structure

```
hf-transformers/
├── src/
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging utilities
│   │   ├── base_class.py      # Abstract base class
│   │   ├── data_processor.py  # Data processing utilities
│   │   └── api_client.py      # HTTP API client
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py      # File operations
│       ├── string_utils.py    # String manipulation
│       └── date_utils.py      # Date/time utilities
├── tests/
│   ├── __init__.py
│   └── test_base_classes.py   # Unit tests
├── main.py                    # Example application
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
├── pyproject.toml            # Modern Python project config
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hf-transformers
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Usage

### Basic Example

```python
from src.base import Config, Logger, BaseClass, DataProcessor

# Create a custom class that inherits from BaseClass
class MyApp(BaseClass):
    def __init__(self):
        super().__init__(name="MyApp")
        self.data_processor = DataProcessor()
    
    def initialize(self):
        self.log_info("Initializing MyApp...")
        return self.data_processor.initialize()
    
    def cleanup(self):
        self.data_processor.cleanup()
        self.log_info("MyApp cleanup completed")

# Usage
app = MyApp()
if app.initialize():
    app.log_info("Application is running!")
    app.cleanup()
```

### Configuration Management

```python
from src.base import Config

# Create configuration
config = Config()

# Set values
config.set("database_url", "postgresql://localhost/mydb")
config.set("api_key", "your-api-key")
config.set("debug", True)

# Get values
db_url = config.get("database_url")
api_key = config.get("api_key")
debug = config.get("debug", False)  # with default

# Save to file
config.save_to_file("config.json")
```

### Logging

```python
from src.base import Logger

# Create logger
logger = Logger(
    name="MyApp",
    level=logging.INFO,
    log_file="app.log"
)

# Log messages
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### Data Processing

```python
from src.base import DataProcessor

processor = DataProcessor()

# JSON operations
data = {"name": "John", "age": 30}
processor.write_json(data, "user.json")
loaded_data = processor.read_json("user.json")

# CSV operations
csv_data = [
    {"name": "John", "age": "30"},
    {"name": "Jane", "age": "25"}
]
processor.write_csv(csv_data, "users.csv")
loaded_csv = processor.read_csv("users.csv")
```

### API Client

```python
from src.base import APIClient

# Create API client
client = APIClient(
    base_url="https://api.example.com",
    api_key="your-api-key",
    timeout=30,
    max_retries=3
)

# Make requests
response = client.get("/users")
users = client.get_json("/users")
new_user = client.post_json("/users", {"name": "John", "email": "john@example.com"})
```

### Utility Classes

```python
from src.utils import StringUtils, FileUtils, DateUtils

# String utilities
text = "  Hello, World!  "
normalized = StringUtils.normalize_whitespace(text)
slug = StringUtils.slugify(text)
word_count = StringUtils.count_words(text)

# File utilities
file_utils = FileUtils()
exists = file_utils.file_exists("file.txt")
file_info = file_utils.get_file_info("file.txt")
file_hash = file_utils.calculate_file_hash("file.txt", "md5")

# Date utilities
now = DateUtils.now()
today = DateUtils.today()
tomorrow = DateUtils.add_days(today, 1)
is_weekend = DateUtils.is_weekend(today)
```

## Running the Example

The project includes a comprehensive example in `main.py`:

```bash
python main.py
```

This will demonstrate all the base classes and utilities in action.

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_base_classes.py

# Run with verbose output
pytest -v
```

## Code Quality

### Formatting

Format code with Black:

```bash
black src/ tests/ main.py
```

### Linting

Check code with flake8:

```bash
flake8 src/ tests/ main.py
```

### Type Checking

Run mypy for type checking:

```bash
mypy src/
```

## Development

### Adding New Base Classes

1. Create a new file in `src/base/`
2. Inherit from `BaseClass` or create a standalone class
3. Add comprehensive docstrings
4. Write unit tests in `tests/`
5. Update `src/base/__init__.py` to export the new class

### Adding New Utilities

1. Create a new file in `src/utils/`
2. Implement utility functions or classes
3. Add comprehensive docstrings
4. Write unit tests
5. Update `src/utils/__init__.py` to export the new utilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Format and lint your code
7. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- Built with modern Python best practices
- Inspired by various open-source projects
- Uses industry-standard tools and libraries