"""
Telegraph API Python Library

A complete Python wrapper for the Telegraph API.

Example:
    >>> from telegraph import Telegraph
    >>> tg = Telegraph()
    >>> account = tg.create_account(short_name="MyBot")
    >>> page = tg.create_page(
    ...     access_token=account.access_token,
    ...     title="Hello World",
    ...     content="<p>This is my page</p>"
    ... )
    >>> print(page.url)
"""

__version__ = "1.0.0"
__author__ = "Telegraph Python Contributors"
__license__ = "MIT"

from .client import Telegraph

# Optional async support - only import if aiohttp is available
try:
    from .async_client import AsyncTelegraph
    _has_async = True
except ImportError:
    AsyncTelegraph = None  # type: ignore
    _has_async = False

from .types import (
    Account,
    Page,
    PageList,
    PageViews,
    Node,
    NodeElement,
    AccountField,
    ALLOWED_TAGS
)
from .errors import (
    TelegraphError,
    TelegraphAPIError,
    TelegraphHTTPError,
    TelegraphConnectionError,
    TelegraphValidationError
)
from .utils import (
    html_to_nodes,
    markdown_to_html,
    parse_content,
    nodes_to_json
)

__all__ = [
    # Version
    '__version__',

    # Clients
    'Telegraph',
    'AsyncTelegraph',

    # Types
    'Account',
    'Page',
    'PageList',
    'PageViews',
    'Node',
    'NodeElement',
    'AccountField',
    'ALLOWED_TAGS',

    # Errors
    'TelegraphError',
    'TelegraphAPIError',
    'TelegraphHTTPError',
    'TelegraphConnectionError',
    'TelegraphValidationError',

    # Utils
    'html_to_nodes',
    'markdown_to_html',
    'parse_content',
    'nodes_to_json',
]
