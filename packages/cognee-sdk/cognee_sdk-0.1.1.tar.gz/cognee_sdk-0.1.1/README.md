# Cognee Python SDK

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Lightweight, type-safe, and fully asynchronous Python SDK for [Cognee](https://github.com/topoteretes/cognee) - an AI memory platform that transforms documents into persistent and dynamic knowledge graphs.

## Features

- 🚀 **Lightweight**: Only ~5-10MB (vs 500MB-2GB for full cognee library)
- 🔒 **Type Safe**: Full type hints with Pydantic validation
- ⚡ **Async First**: Fully asynchronous API with `httpx`
- 🛡️ **Error Handling**: Comprehensive error handling with retry mechanism
- 📁 **File Upload**: Support for multiple file formats and input types
- 🔌 **WebSocket**: Optional WebSocket support for real-time progress updates
- 🔄 **Retry Logic**: Automatic retry with exponential backoff
- 📊 **Batch Operations**: Support for batch data operations

## Installation

```bash
pip install cognee-sdk
```

### Optional Dependencies

For WebSocket support:

```bash
pip install cognee-sdk[websocket]
```

## Quick Start

```python
import asyncio
from cognee_sdk import CogneeClient, SearchType

async def main():
    # Initialize client
    client = CogneeClient(
        api_url="http://localhost:8000",
        api_token="your-token-here"  # Optional
    )
    
    try:
        # Add data
        result = await client.add(
            data="Cognee turns documents into AI memory.",
            dataset_name="my-dataset"
        )
        print(f"Added data: {result.data_id}")
        
        # Process data
        cognify_result = await client.cognify(datasets=["my-dataset"])
        print(f"Cognify status: {cognify_result.status}")
        
        # Search
        results = await client.search(
            query="What does Cognee do?",
            search_type=SearchType.GRAPH_COMPLETION
        )
        for result in results:
            print(result)
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## API Overview

### Core Operations

- **Data Management**: `add()`, `update()`, `delete()`
- **Processing**: `cognify()`, `memify()`
- **Search**: `search()` with 19 different search types
- **Datasets**: `list_datasets()`, `create_dataset()`, `delete_dataset()`
- **Authentication**: `login()`, `register()`, `get_current_user()`

### Advanced Features

- **WebSocket**: `subscribe_cognify_progress()` for real-time updates
- **Batch Operations**: `add_batch()` for bulk data operations
- **Visualization**: `visualize()` for graph visualization
- **Sync**: `sync_to_cloud()`, `get_sync_status()` for cloud synchronization

## Examples

See the [examples/](examples/) directory for more examples:

- [Basic Usage](examples/basic_usage.py) - Core functionality
- [File Upload](examples/file_upload.py) - Different file upload methods
- [Async Operations](examples/async_operations.py) - Concurrent operations
- [Search Types](examples/search_types.py) - All search types

## API Reference

### CogneeClient

Main client class for interacting with Cognee API.

```python
client = CogneeClient(
    api_url="http://localhost:8000",
    api_token="your-token",  # Optional
    timeout=300.0,           # Request timeout
    max_retries=3,           # Retry attempts
    retry_delay=1.0          # Initial retry delay
)
```

### Search Types

Available search types:

- `SearchType.GRAPH_COMPLETION` - Graph-based completion (default)
- `SearchType.RAG_COMPLETION` - RAG-based completion
- `SearchType.CHUNKS` - Chunk search
- `SearchType.SUMMARIES` - Summary search
- `SearchType.CODE` - Code search
- `SearchType.CYPHER` - Cypher query
- And 13 more types...

See [models.py](cognee_sdk/models.py) for the complete list.

## Error Handling

The SDK provides specific exception types:

```python
from cognee_sdk import CogneeClient
from cognee_sdk.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
)

try:
    await client.search("query")
except AuthenticationError:
    print("Authentication failed")
except NotFoundError:
    print("Resource not found")
except ValidationError:
    print("Invalid request")
except ServerError:
    print("Server error")
```

## Requirements

- Python 3.10+
- Cognee API server running (see [Cognee documentation](https://docs.cognee.ai))

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/cognee-sdk.git
cd cognee-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cognee_sdk --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Code Quality

```bash
# Format code
ruff format .

# Check code
ruff check .

# Type checking
mypy cognee_sdk/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Support

- [GitHub Issues](https://github.com/your-org/cognee-sdk/issues)
- [Documentation](https://github.com/your-org/cognee-sdk#readme)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

