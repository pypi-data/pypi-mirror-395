# telegraph-api

[![PyPI version](https://badge.fury.io/py/telegraph-api.svg)](https://badge.fury.io/py/telegraph-api)
[![Python versions](https://img.shields.io/pypi/pyversions/telegraph-api.svg)](https://pypi.org/project/telegraph-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete Python wrapper for the [Telegraph API](https://telegra.ph/api).

## Features

- Full support for all 9 Telegraph API methods
- Both synchronous and asynchronous clients
- Type hints for better IDE support and type checking
- HTML and Markdown content support
- Automatic content parsing and validation
- Comprehensive error handling
- Context manager support
- Zero dependencies for sync client (only `requests`)
- Optional async support with `aiohttp`

## Installation

### Basic installation (synchronous client only)

```bash
pip install telegraph-api-py
```

### With async support

```bash
pip install telegraph-api-py[async]
```

### For development

```bash
pip install telegraph-api-py[dev]
```

## Quick Start

### Synchronous Usage

```python
from telegraph import Telegraph

# Create a Telegraph client
tg = Telegraph()

# Create an account
account = tg.create_account(
    short_name="MyBot",
    author_name="John Doe",
    author_url="https://example.com"
)

print(f"Access token: {account.access_token}")

# Create a page with HTML content
page = tg.create_page(
    title="Hello World",
    content="<p>This is my <b>first</b> Telegraph page!</p>",
    author_name="John Doe"
)

print(f"Page URL: {page.url}")
print(f"Page views: {page.views}")
```

### Asynchronous Usage

```python
import asyncio
from telegraph import AsyncTelegraph

async def main():
    async with AsyncTelegraph() as tg:
        # Create an account
        account = await tg.create_account(
            short_name="MyAsyncBot",
            author_name="Jane Doe"
        )

        # Create a page
        page = await tg.create_page(
            title="Async Hello World",
            content="<p>This page was created asynchronously!</p>"
        )

        print(f"Page URL: {page.url}")

asyncio.run(main())
```

## API Methods

### Account Methods

#### Create Account

```python
account = tg.create_account(
    short_name="MyBot",           # Required: 1-32 characters
    author_name="John Doe",       # Optional: 0-128 characters
    author_url="https://example.com"  # Optional: 0-512 characters
)

# Returns Account object with access_token
print(account.access_token)
```

#### Edit Account Info

```python
account = tg.edit_account_info(
    short_name="NewName",
    author_name="New Author",
    author_url="https://newurl.com"
)
```

#### Get Account Info

```python
account = tg.get_account_info(
    fields=["short_name", "author_name", "page_count"]
)

print(f"Pages created: {account.page_count}")
```

#### Revoke Access Token

```python
account = tg.revoke_access_token()
print(f"New access token: {account.access_token}")
print(f"Auth URL: {account.auth_url}")
```

### Page Methods

#### Create Page

```python
# With HTML content
page = tg.create_page(
    title="My Page",
    content="<p>Hello <b>world</b>!</p>",
    author_name="John Doe",
    author_url="https://example.com",
    return_content=False
)

# With Markdown content
page = tg.create_page(
    title="My Markdown Page",
    content="# Hello\n\nThis is **bold** and this is *italic*.",
    content_format="markdown"
)

# With Node array
from telegraph import NodeElement

nodes = [
    NodeElement(tag='p', children=['Hello ', NodeElement(tag='b', children=['world'])])
]
page = tg.create_page(
    title="My Node Page",
    content=nodes
)
```

#### Edit Page

```python
page = tg.edit_page(
    path="My-Page-12-15",
    title="Updated Title",
    content="<p>Updated content</p>",
    return_content=True
)
```

#### Get Page

```python
page = tg.get_page(
    path="My-Page-12-15",
    return_content=True
)

print(f"Title: {page.title}")
print(f"Views: {page.views}")
print(f"Content: {page.content}")
```

#### Get Page List

```python
page_list = tg.get_page_list(
    offset=0,
    limit=50
)

print(f"Total pages: {page_list.total_count}")
for page in page_list.pages:
    print(f"- {page.title}: {page.url}")
```

#### Get Page Views

```python
# Get total views
views = tg.get_views(path="My-Page-12-15")
print(f"Total views: {views.views}")

# Get views for specific date
views = tg.get_views(
    path="My-Page-12-15",
    year=2025,
    month=12,
    day=7,
    hour=12  # Optional
)
print(f"Views: {views.views}")
```

## Content Formats

### HTML Content

Telegraph supports the following HTML tags:

- `<a>` - links (requires `href` attribute)
- `<aside>` - aside block
- `<b>`, `<strong>` - bold text
- `<blockquote>` - blockquote
- `<br>` - line break
- `<code>` - inline code
- `<em>`, `<i>` - italic text
- `<figcaption>` - figure caption
- `<figure>` - figure
- `<h3>`, `<h4>` - headers
- `<hr>` - horizontal rule
- `<iframe>` - iframe (requires `src` attribute)
- `<img>` - image (requires `src` attribute)
- `<li>` - list item
- `<ol>` - ordered list
- `<p>` - paragraph
- `<pre>` - preformatted text
- `<s>` - strikethrough
- `<u>` - underline
- `<ul>` - unordered list
- `<video>` - video (requires `src` attribute)

Example:

```python
content = """
<h3>Article Title</h3>
<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>
<blockquote>This is a quote</blockquote>
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
<a href="https://example.com">Link</a>
<img src="https://example.com/image.jpg"/>
"""

page = tg.create_page(title="My Article", content=content)
```

### Markdown Content

The library includes a Markdown to HTML converter:

```python
markdown = """
# Main Title

This is a paragraph with **bold** and *italic* text.

## Subheading

> This is a blockquote

### Features

- Item 1
- Item 2
- Item 3

1. First
2. Second
3. Third

[Link text](https://example.com)

![Image caption](https://example.com/image.jpg)

`inline code`

```
code block
```
"""

page = tg.create_page(
    title="Markdown Example",
    content=markdown,
    content_format="markdown"
)
```

### Node Array Content

For maximum control, use Node arrays:

```python
from telegraph import NodeElement

content = [
    NodeElement(tag='h3', children=['Title']),
    NodeElement(tag='p', children=[
        'This is ',
        NodeElement(tag='b', children=['bold']),
        ' text.'
    ]),
    NodeElement(tag='img', attrs={'src': 'https://example.com/image.jpg'})
]

page = tg.create_page(title="Node Example", content=content)
```

## Error Handling

The library provides specific exception types:

```python
from telegraph import Telegraph, TelegraphError, TelegraphValidationError, TelegraphAPIError

tg = Telegraph()

try:
    page = tg.create_page(
        title="Test",
        content="<p>Test</p>"
    )
except TelegraphValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Field: {e.field}")
except TelegraphAPIError as e:
    print(f"API error: {e.message}")
except TelegraphError as e:
    print(f"General error: {e.message}")
```

Exception hierarchy:

- `TelegraphError` - Base exception
  - `TelegraphAPIError` - API returned an error
  - `TelegraphHTTPError` - HTTP error occurred
  - `TelegraphConnectionError` - Connection error
  - `TelegraphValidationError` - Input validation failed

## Context Manager

Both clients support context managers for automatic cleanup:

```python
# Synchronous
with Telegraph() as tg:
    account = tg.create_account(short_name="MyBot")
    page = tg.create_page(title="Test", content="<p>Test</p>")
# Session automatically closed

# Asynchronous
async with AsyncTelegraph() as tg:
    account = await tg.create_account(short_name="MyBot")
    page = await tg.create_page(title="Test", content="<p>Test</p>")
# Session automatically closed
```

## Using Access Tokens

You can store the access token and reuse it:

```python
# Create account and get token
tg = Telegraph()
account = tg.create_account(short_name="MyBot")
token = account.access_token

# Save token to database/file...

# Later, reuse the token
tg = Telegraph(access_token=token)
page = tg.create_page(title="Test", content="<p>Test</p>")

# Or pass explicitly
page = tg.create_page(
    access_token="different_token",
    title="Test",
    content="<p>Test</p>"
)
```

## Utility Functions

The library provides utility functions for content manipulation:

```python
from telegraph import html_to_nodes, markdown_to_html, parse_content, nodes_to_json

# Convert HTML to Node array
nodes = html_to_nodes("<p>Hello <b>world</b></p>")

# Convert Markdown to HTML
html = markdown_to_html("# Title\n\nThis is **bold**")

# Parse content (auto-detect format)
nodes = parse_content("<p>HTML content</p>", format='html')
nodes = parse_content("# Markdown content", format='markdown')

# Convert nodes to JSON-serializable format
json_nodes = nodes_to_json(nodes)
```

## Advanced Usage

### Custom Timeout

```python
# Synchronous client with custom timeout
tg = Telegraph(timeout=60)  # 60 seconds

# Asynchronous client with custom timeout
tg = AsyncTelegraph(timeout=60)
```

### Custom Base URL

```python
# Use custom Telegraph API endpoint
tg = Telegraph(base_url="https://custom-api.example.com")
```

## Type Hints

The library is fully typed. Use with mypy or other type checkers:

```python
from telegraph import Telegraph, Account, Page

tg: Telegraph = Telegraph()
account: Account = tg.create_account(short_name="MyBot")
page: Page = tg.create_page(title="Test", content="<p>Test</p>")
```

## Testing

Run tests:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=telegraph --cov-report=html
```

## Requirements

- Python 3.9+
- `requests` (for synchronous client)
- `aiohttp` (optional, for asynchronous client)

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Links

- [Telegraph API Documentation](https://telegra.ph/api)
- [PyPI Package](https://pypi.org/project/telegraph-api/)
- [GitHub Repository](https://github.com/telegraph-py/telegraph-api)
- [Issue Tracker](https://github.com/telegraph-py/telegraph-api/issues)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### Version 1.0.0 (2025-12-07)

- Initial release
- Full support for all 9 Telegraph API methods
- Synchronous and asynchronous clients
- HTML and Markdown content support
- Comprehensive error handling
- Type hints
- Full test coverage
