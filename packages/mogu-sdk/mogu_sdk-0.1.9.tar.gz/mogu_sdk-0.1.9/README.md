# Mogu SDK

Official Python SDK for the [Mogu Workflow Management Platform](https://github.com/yourusername/mogu).

[![PyPI version](https://badge.fury.io/py/mogu-sdk.svg)](https://badge.fury.io/py/mogu-sdk)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- 🔐 **OAuth2 Authentication** - Secure token-based authentication
- 📝 **Wiki Management** - Create, update, search wiki pages in Git repositories
- ⚡ **Async-First** - Built on httpx for high-performance async operations
- 🎯 **Type-Safe** - Full type hints with Pydantic models
- 🧪 **Well-Tested** - Comprehensive test coverage
- 📚 **Great Documentation** - Detailed API docs and examples

## Installation

```bash
pip install mogu-sdk
```

Or with Poetry:

```bash
poetry add mogu-sdk
```

## Quick Start

### Environment Configuration

The SDK automatically reads configuration from environment variables or a `.env` file:

```bash
# Create a .env file
MOGU_BASE_URL=http://localhost:8000
MOGU_TOKEN=your-oauth-token
MOGU_WORKSPACE_ID=your-workspace-id
```

### Basic Usage

```python
import asyncio
from mogu_sdk import MoguClient

async def main():
    # Initialize client - automatically reads from environment variables
    client = MoguClient()
    
    # Or override specific values
    client = MoguClient(
        base_url="https://api.mogu.example.com",
        token="your-oauth-token"
    )
    
    # Access wiki client
    wiki = client.wiki
    
    # Create or update a wiki page
    result = await wiki.create_or_update_page(
        workspace_id="ws-123",
        path="docs/getting-started.md",
        content="# Getting Started\n\nWelcome to our wiki!",
        commit_message="Add getting started guide"
    )
    print(f"Committed: {result.commit_id}")
    
    # Search wiki with context
    results = await wiki.search(
        workspace_id="ws-123",
        query="authentication",
        max_results=10,
        context_lines=3
    )
    
    for result in results:
        print(f"\nFound in: {result.path}")
        for match in result.matches:
            print(f"  Line {match.line_number}: {match.line_content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Wiki Client

### Create or Update Wiki Page

Smart method that automatically detects if a file exists and creates or updates accordingly:

```python
result = await wiki.create_or_update_page(
    workspace_id="ws-123",
    path="docs/api-reference.md",
    content="# API Reference\n\n## Authentication\n...",
    commit_message="Update API reference"
)

print(f"Success: {result.success}")
print(f"Commit ID: {result.commit_id}")
print(f"Message: {result.message}")
```

### Search Wiki with Context

Search across all wiki files with configurable context extraction:

```python
results = await wiki.search(
    workspace_id="ws-123",
    query="deployment kubernetes",
    max_results=20,
    context_lines=5  # Get 5 lines before/after each match
)

for result in results:
    print(f"\n📄 {result.path} (score: {result.score})")
    
    for match in result.matches:
        print(f"\n  Line {match.line_number}:")
        
        # Context before match
        if match.context_before:
            for line in match.context_before:
                print(f"    {line}")
        
        # The matched line (highlighted)
        print(f"  ➤ {match.line_content}")
        
        # Context after match
        if match.context_after:
            for line in match.context_after:
                print(f"    {line}")
```

### Search with Character-Based Snippets (NEW!)

Extract text snippets of specific character length around matches - perfect for displaying search results in UIs:

```python
results = await wiki.search(
    workspace_id="ws-123",
    query="authentication",
    max_results=10,
    snippet_chars=1000  # Extract ~1000 character snippet around each match
)

for result in results:
    for match in result.matches:
        if match.text_snippet:
            # Get the snippet with match position
            snippet = match.text_snippet
            start = match.snippet_match_start
            end = match.snippet_match_end
            
            # Highlight the match within snippet
            before = snippet[:start]
            matched = snippet[start:end]
            after = snippet[end:]
            
            print(f"{before}**{matched}**{after}")
```

**Features:**
- Character-based extraction (e.g., 1000 chars) for consistent UI display
- Smart word boundaries - avoids cutting words mid-character
- Automatic ellipsis (...) for truncated text
- Exact match position within snippet for highlighting
- Works alongside line-based context (use both together!)

**Combined context example:**
```python
# Get both line-based and character-based context
results = await wiki.search(
    workspace_id="ws-123",
    query="configuration",
    context_lines=2,      # 2 lines before/after (for code structure)
    snippet_chars=800     # 800 char snippet (for prose context)
)

# Now you have:
# - match.context_before / context_after (lines)
# - match.text_snippet (character-based snippet)
```

### Search with Character-Based Snippets (NEW!)

Extract text snippets of specific character length around matches - perfect for displaying search results in UIs:

```python
results = await wiki.search(
    workspace_id="ws-123",
    query="authentication",
    max_results=10,
    snippet_chars=1000  # Extract ~1000 character snippet around each match
)

for result in results:
    for match in result.matches:
        if match.text_snippet:
            # Get the snippet with match position
            snippet = match.text_snippet
            start = match.snippet_match_start
            end = match.snippet_match_end
            
            # Highlight the match within snippet
            before = snippet[:start]
            matched = snippet[start:end]
            after = snippet[end:]
            
            print(f"{before}**{matched}**{after}")
```

**Features:**
- Character-based extraction (e.g., 1000 chars) for consistent UI display
- Smart word boundaries - avoids cutting words mid-character
- Automatic ellipsis (...) for truncated text
- Exact match position within snippet for highlighting
- Works alongside line-based context (use both together!)

**Combined context example:**
```python
# Get both line-based and character-based context
results = await wiki.search(
    workspace_id="ws-123",
    query="configuration",
    context_lines=2,      # 2 lines before/after (for code structure)
    snippet_chars=800     # 800 char snippet (for prose context)
)

# Now you have:
# - match.context_before / context_after (lines)
# - match.text_snippet (character-based snippet)
```

### List Wiki Files

```python
files = await wiki.list_files(
    workspace_id="ws-123",
    folder_path="docs",  # Optional: filter by folder
    recursive=True
)

for file in files:
    icon = "📁" if file.is_folder else "📄"
    print(f"{icon} {file.path}")
```

### Get File Content

```python
content = await wiki.get_content(
    workspace_id="ws-123",
    path="docs/README.md"
)

print(f"Path: {content.path}")
print(f"Content:\n{content.content}")
```

### Delete File

```python
result = await wiki.delete_file(
    workspace_id="ws-123",
    path="docs/old-guide.md",
    commit_message="Remove outdated guide"
)

print(f"Deleted: {result.success}")
```

## Configuration

The SDK supports multiple configuration methods with automatic environment variable loading.

### Method 1: .env File (Recommended)

Create a `.env` file in your project root:

```bash
# .env
MOGU_BASE_URL=http://localhost:8000
MOGU_TOKEN=your-oauth-token
MOGU_WORKSPACE_ID=your-workspace-id
MOGU_TIMEOUT=30.0
MOGU_MAX_RETRIES=3
MOGU_VERIFY_SSL=true
```

Then simply initialize the client:

```python
from mogu_sdk import MoguClient

# Automatically reads from .env file
client = MoguClient()

# Access default workspace_id
print(client.workspace_id)  # your-workspace-id
```

### Method 2: Environment Variables

Set environment variables directly:

```bash
export MOGU_BASE_URL="https://api.mogu.example.com"
export MOGU_TOKEN="your-oauth-token"
export MOGU_WORKSPACE_ID="your-workspace-id"
```

```python
from mogu_sdk import MoguClient

client = MoguClient()  # Reads from environment
```

### Method 3: Direct Parameters

Override environment variables by passing parameters:

```python
from mogu_sdk import MoguClient

client = MoguClient(
    base_url="https://api.mogu.example.com",
    token="your-oauth-token",
    workspace_id="your-workspace-id",
    timeout=30.0,  # Request timeout in seconds
    max_retries=3,  # Number of retry attempts
    verify_ssl=True  # SSL certificate verification
)
```

## Error Handling

The SDK provides specific exceptions for different error scenarios:

```python
from mogu_sdk.exceptions import (
    MoguAPIError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError
)

try:
    result = await wiki.create_or_update_page(
        workspace_id="ws-123",
        path="docs/guide.md",
        content="# Guide",
        commit_message="Update guide"
    )
except AuthenticationError:
    print("Invalid or expired token")
except PermissionDeniedError:
    print("No permission to edit wiki")
except NotFoundError:
    print("Workspace not found")
except ValidationError as e:
    print(f"Invalid input: {e}")
except MoguAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Advanced Usage

### Context Manager

```python
async with MoguClient(base_url="...", token="...") as client:
    result = await client.wiki.search(
        workspace_id="ws-123",
        query="deployment"
    )
    # Client automatically closed after context
```

### Async Iteration

```python
# Process search results as they arrive
async for result in wiki.search_stream(
    workspace_id="ws-123",
    query="api"
):
    print(f"Found: {result.path}")
```

### Custom Headers

```python
client = MoguClient(
    base_url="...",
    token="...",
    headers={
        "X-Custom-Header": "value",
        "User-Agent": "MyApp/1.0"
    }
)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/mogu-sdk.git
cd mogu-sdk

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linters
poetry run black mogu_sdk tests
poetry run ruff mogu_sdk tests
poetry run mypy mogu_sdk
```

### Run Examples

```bash
# Set environment variables
export MOGU_BASE_URL="http://localhost:8000"
export MOGU_TOKEN="your-token"

# Run examples
poetry run python examples/wiki_basic.py
poetry run python examples/wiki_search.py
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Documentation**: https://mogu-sdk.readthedocs.io
- **Source Code**: https://github.com/yourusername/mogu-sdk
- **Issue Tracker**: https://github.com/yourusername/mogu-sdk/issues
- **PyPI**: https://pypi.org/project/mogu-sdk/
- **Mogu Platform**: https://github.com/yourusername/mogu

## Support

- 📧 Email: support@mogu.example.com
- 💬 Discord: https://discord.gg/mogu
- 📖 Documentation: https://docs.mogu.example.com
- 🐛 Issues: https://github.com/yourusername/mogu-sdk/issues
