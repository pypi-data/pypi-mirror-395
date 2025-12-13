# MarqetiveLib

[![CI](https://github.com/yourusername/marqetive-lib/workflows/CI/badge.svg)](https://github.com/yourusername/marqetive-lib/actions)
[![codecov](https://codecov.io/gh/yourusername/marqetive-lib/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/marqetive-lib)
[![PyPI version](https://badge.fury.io/py/marqetive-lib.svg)](https://badge.fury.io/py/marqetive-lib)
[![Python versions](https://img.shields.io/pypi/pyversions/marqetive-lib.svg)](https://pypi.org/project/marqetive-lib/)
[![License](https://img.shields.io/github/license/yourusername/marqetive-lib.svg)](https://github.com/yourusername/marqetive-lib/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://marqetive-lib.readthedocs.io)

Modern Python utilities for web APIs - Simple, type-safe, and async-ready.

## Features

- **🚀 Fast and Lightweight**: Built on httpx with minimal dependencies
- **🔒 Type-Safe**: Full type hints and Pyright compliance for better IDE support
- **📦 Zero Learning Curve**: Intuitive API design that feels natural
- **🧪 Well Tested**: Comprehensive test coverage (>90%)
- **📚 Excellent Documentation**: Clear examples and detailed API reference
- **🔄 Async/Await Support**: Built for modern async Python applications
- **✨ Developer Friendly**: Great error messages and helpful utilities

## Installation

```bash
pip install marqetive-lib
```

Or with Poetry:

```bash
poetry add marqetive-lib
```

## Quick Start

```python
import asyncio
from marqetive_lib import APIClient

async def main():
    async with APIClient(base_url="https://api.example.com") as client:
        # Make a GET request
        response = await client.get("/users/1")
        print(f"User: {response.data['name']}")

        # Make a POST request
        new_user = {"name": "John Doe", "email": "john@example.com"}
        response = await client.post("/users", data=new_user)
        print(f"Created user ID: {response.data['id']}")

asyncio.run(main())
```

## Core Features

### Simple HTTP Client

```python
from marqetive_lib import APIClient

async with APIClient(base_url="https://api.example.com") as client:
    # GET request with query parameters
    response = await client.get("/search", params={"q": "python"})

    # POST request with JSON body
    response = await client.post("/users", data={"name": "Alice"})

    # Access response details
    print(response.status_code)  # 200
    print(response.data)         # Parsed JSON response
    print(response.headers)      # Response headers
```

### Utility Functions

```python
from marqetive_lib.utils import (
    format_response,
    parse_query_params,
    build_query_string,
    merge_headers
)

# Format JSON responses beautifully
data = {"users": [{"id": 1, "name": "Alice"}]}
print(format_response(data, pretty=True, indent=2))

# Parse URL query parameters
params = parse_query_params("https://api.com/search?q=python&page=1")
# {'q': ['python'], 'page': ['1']}

# Build query strings
query = build_query_string({"search": "api", "limit": 10})
# "search=api&limit=10"

# Merge HTTP headers
headers = merge_headers(
    {"Content-Type": "application/json"},
    {"Authorization": "Bearer token"}
)
```

### Type-Safe Responses

```python
from marqetive_lib import APIClient
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

async with APIClient(base_url="https://api.example.com") as client:
    response = await client.get("/users/1")
    user = User(**response.data)  # Automatic validation
    print(user.name)
```

## Documentation

Full documentation is available at [marqetive-lib.readthedocs.io](https://marqetive-lib.readthedocs.io)

- [Getting Started Guide](https://marqetive-lib.readthedocs.io/getting-started/)
- [API Reference](https://marqetive-lib.readthedocs.io/api/core/)
- [Examples](https://marqetive-lib.readthedocs.io/examples/basic/)
- [Contributing Guide](https://marqetive-lib.readthedocs.io/contributing/)

## Requirements

- Python 3.9+
- httpx >= 0.27.0
- pydantic >= 2.0.0

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/marqetive-lib.git
cd marqetive-lib

# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --with dev,docs

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/marqetive_lib --cov-report=term-missing

# Run tests for specific Python versions
poetry run tox
```

### Code Quality

```bash
# Lint code with Ruff
poetry run ruff check .

# Format code with Ruff
poetry run ruff format .

# Type check with Pyright
poetry run pyright src/
```

### Building Documentation

```bash
# Serve documentation locally with live reload
poetry run mkdocs serve

# Build static documentation
poetry run mkdocs build
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development workflow
- Code style guidelines
- Testing requirements
- Pull request process

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [httpx](https://www.python-httpx.org/) for HTTP requests
- Uses [Pydantic](https://docs.pydantic.dev/) for data validation
- Tested with [pytest](https://pytest.org/)
- Documentation powered by [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

## Support

- **Documentation**: [marqetive-lib.readthedocs.io](https://marqetive-lib.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/yourusername/marqetive-lib/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/marqetive-lib/discussions)

## Links

- **PyPI**: [pypi.org/project/marqetive-lib](https://pypi.org/project/marqetive-lib/)
- **Source Code**: [github.com/yourusername/marqetive-lib](https://github.com/yourusername/marqetive-lib)
- **Documentation**: [marqetive-lib.readthedocs.io](https://marqetive-lib.readthedocs.io)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
