"""
Telegraph Page Export and Backup Functions

Functions for exporting Telegraph pages to different formats and backing up accounts.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal, TYPE_CHECKING
from .types import Node
from .utils import nodes_to_markdown, nodes_to_html

if TYPE_CHECKING:
    from .client import Telegraph
    from .async_client import AsyncTelegraph


@dataclass
class ExportedPage:
    """
    Exported Telegraph page.

    Attributes:
        title: Page title
        path: Page path
        url: Page URL
        format: Export format (markdown or html)
        content: Exported content as string
    """
    title: str
    path: str
    url: str
    format: str
    content: str


@dataclass
class AccountBackup:
    """
    Backup of a Telegraph account.

    Attributes:
        total_count: Total number of pages in account
        exported_count: Number of pages exported
        format: Export format (markdown or html)
        pages: List of exported pages
    """
    total_count: int
    exported_count: int
    format: str
    pages: List[ExportedPage] = field(default_factory=list)


def export_page(
    path: str,
    format: Literal['markdown', 'html'] = 'markdown',
    telegraph_client: Optional['Telegraph'] = None
) -> ExportedPage:
    """
    Export a Telegraph page to Markdown or HTML format.

    Args:
        path: Path to the Telegraph page
        format: Export format ('markdown' or 'html'). Default is 'markdown'
        telegraph_client: Optional Telegraph client instance (creates new if not provided)

    Returns:
        ExportedPage object with exported content

    Raises:
        ValueError: If page has no content
        TelegraphAPIError: If API request fails

    Example:
        >>> from telegraph import Telegraph, export_page
        >>> exported = export_page('Sample-Page-12-15', format='markdown')
        >>> print(exported.content)
    """
    from .client import Telegraph

    client = telegraph_client or Telegraph()

    # Fetch page with content
    page = client.get_page(path, return_content=True)

    if not page.content:
        raise ValueError("Page has no content")

    # Convert content to requested format
    if format == 'markdown':
        content = nodes_to_markdown(page.content)
    else:
        content = nodes_to_html(page.content)

    return ExportedPage(
        title=page.title,
        path=page.path,
        url=page.url,
        format=format,
        content=content
    )


def backup_account(
    access_token: str,
    format: Literal['markdown', 'html'] = 'markdown',
    limit: int = 50,
    telegraph_client: Optional['Telegraph'] = None
) -> AccountBackup:
    """
    Backup all pages from a Telegraph account.

    Args:
        access_token: Telegraph account access token
        format: Export format ('markdown' or 'html'). Default is 'markdown'
        limit: Maximum number of pages to export (0-200). Default is 50
        telegraph_client: Optional Telegraph client instance (creates new if not provided)

    Returns:
        AccountBackup object with all exported pages

    Raises:
        TelegraphValidationError: If validation fails
        TelegraphAPIError: If API request fails

    Example:
        >>> from telegraph import backup_account
        >>> backup = backup_account(
        ...     access_token='your_token',
        ...     format='markdown',
        ...     limit=50
        ... )
        >>> print(f"Exported {backup.exported_count} pages")
    """
    from .client import Telegraph

    client = telegraph_client or Telegraph(access_token=access_token)

    # Get list of pages
    page_list = client.get_page_list(offset=0, limit=limit)
    exported_pages = []

    # Export each page
    for page in page_list.pages:
        # Fetch full page with content
        full_page = client.get_page(page.path, return_content=True)

        content = ""
        if full_page.content:
            # Convert content to requested format
            if format == 'markdown':
                content = nodes_to_markdown(full_page.content)
            else:
                content = nodes_to_html(full_page.content)

        exported_pages.append(ExportedPage(
            title=full_page.title,
            path=full_page.path,
            url=full_page.url,
            format=format,
            content=content
        ))

    return AccountBackup(
        total_count=page_list.total_count,
        exported_count=len(exported_pages),
        format=format,
        pages=exported_pages
    )


async def export_page_async(
    path: str,
    format: Literal['markdown', 'html'] = 'markdown',
    telegraph_client: Optional['AsyncTelegraph'] = None
) -> ExportedPage:
    """
    Export a Telegraph page to Markdown or HTML format (async version).

    Args:
        path: Path to the Telegraph page
        format: Export format ('markdown' or 'html'). Default is 'markdown'
        telegraph_client: Optional AsyncTelegraph client instance (creates new if not provided)

    Returns:
        ExportedPage object with exported content

    Raises:
        ValueError: If page has no content
        TelegraphAPIError: If API request fails

    Example:
        >>> from telegraph import AsyncTelegraph, export_page_async
        >>> async with AsyncTelegraph() as client:
        ...     exported = await export_page_async('Sample-Page-12-15', format='markdown')
        ...     print(exported.content)
    """
    from .async_client import AsyncTelegraph

    client = telegraph_client or AsyncTelegraph()
    created_client = client if telegraph_client else True

    try:
        # Fetch page with content
        page = await client.get_page(path, return_content=True)

        if not page.content:
            raise ValueError("Page has no content")

        # Convert content to requested format
        if format == 'markdown':
            content = nodes_to_markdown(page.content)
        else:
            content = nodes_to_html(page.content)

        return ExportedPage(
            title=page.title,
            path=page.path,
            url=page.url,
            format=format,
            content=content
        )

    finally:
        # Close client if we created it
        if created_client and not telegraph_client:
            await client.close()


async def backup_account_async(
    access_token: str,
    format: Literal['markdown', 'html'] = 'markdown',
    limit: int = 50,
    telegraph_client: Optional['AsyncTelegraph'] = None
) -> AccountBackup:
    """
    Backup all pages from a Telegraph account (async version).

    Args:
        access_token: Telegraph account access token
        format: Export format ('markdown' or 'html'). Default is 'markdown'
        limit: Maximum number of pages to export (0-200). Default is 50
        telegraph_client: Optional AsyncTelegraph client instance (creates new if not provided)

    Returns:
        AccountBackup object with all exported pages

    Raises:
        TelegraphValidationError: If validation fails
        TelegraphAPIError: If API request fails

    Example:
        >>> from telegraph import AsyncTelegraph, backup_account_async
        >>> async with AsyncTelegraph(access_token='your_token') as client:
        ...     backup = await backup_account_async(
        ...         access_token='your_token',
        ...         format='markdown',
        ...         limit=50
        ...     )
        ...     print(f"Exported {backup.exported_count} pages")
    """
    from .async_client import AsyncTelegraph

    client = telegraph_client or AsyncTelegraph(access_token=access_token)
    created_client = client if telegraph_client else True

    try:
        # Get list of pages
        page_list = await client.get_page_list(offset=0, limit=limit)
        exported_pages = []

        # Export each page
        for page in page_list.pages:
            # Fetch full page with content
            full_page = await client.get_page(page.path, return_content=True)

            content = ""
            if full_page.content:
                # Convert content to requested format
                if format == 'markdown':
                    content = nodes_to_markdown(full_page.content)
                else:
                    content = nodes_to_html(full_page.content)

            exported_pages.append(ExportedPage(
                title=full_page.title,
                path=full_page.path,
                url=full_page.url,
                format=format,
                content=content
            ))

        return AccountBackup(
            total_count=page_list.total_count,
            exported_count=len(exported_pages),
            format=format,
            pages=exported_pages
        )

    finally:
        # Close client if we created it
        if created_client and not telegraph_client:
            await client.close()
