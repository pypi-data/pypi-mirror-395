"""
Telegraph API Client - Synchronous Implementation
"""

import json
import logging
from typing import List, Optional, Union
from urllib.parse import urlencode

import requests

from .types import Account, Page, PageList, PageViews, Node, AccountField
from .errors import (
    TelegraphError,
    TelegraphAPIError,
    TelegraphHTTPError,
    TelegraphConnectionError,
    TelegraphValidationError
)
from .utils import parse_content, nodes_to_json


logger = logging.getLogger(__name__)


class Telegraph:
    """
    Synchronous Telegraph API client.

    Provides methods to interact with all Telegraph API endpoints.

    Attributes:
        base_url: Base URL for Telegraph API (default: https://api.telegra.ph)
        access_token: Optional access token for authenticated requests
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> tg = Telegraph()
        >>> account = tg.create_account(short_name="MyBot")
        >>> page = tg.create_page(
        ...     access_token=account.access_token,
        ...     title="Hello World",
        ...     content="<p>This is my page</p>"
        ... )
        >>> print(page.url)
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        base_url: str = "https://api.telegra.ph",
        timeout: int = 30
    ) -> None:
        """
        Initialize Telegraph client.

        Args:
            access_token: Optional access token for authenticated requests
            base_url: Base URL for Telegraph API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.access_token = access_token
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'telegraph-py/1.0.0'
        })

    def _api_request(self, method: str, params: dict = None) -> dict:
        """
        Make a request to the Telegraph API.

        Args:
            method: API method name
            params: Request parameters

        Returns:
            API response result

        Raises:
            TelegraphAPIError: If the API returns an error
            TelegraphHTTPError: If an HTTP error occurs
            TelegraphConnectionError: If a connection error occurs
        """
        url = f"{self.base_url}/{method}"
        params = params or {}

        # Filter out None values and convert to strings
        filtered_params = {}
        for key, value in params.items():
            if value is not None:
                if isinstance(value, bool):
                    filtered_params[key] = str(value).lower()
                elif isinstance(value, list):
                    # Convert list to JSON string
                    filtered_params[key] = json.dumps(value)
                else:
                    filtered_params[key] = str(value)

        logger.debug(f"API request: {method} with params: {list(filtered_params.keys())}")

        try:
            response = self._session.post(
                url,
                data=urlencode(filtered_params),
                timeout=self.timeout
            )

            # Check HTTP status
            if not response.ok:
                raise TelegraphHTTPError(
                    f"HTTP error: {response.status_code} {response.reason}",
                    status_code=response.status_code,
                    response_text=response.text
                )

            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                raise TelegraphAPIError(f"Invalid JSON response: {str(e)}")

            # Check API response status
            if not data.get('ok', False):
                error_msg = data.get('error', 'Unknown Telegraph API error')
                raise TelegraphAPIError(error_msg)

            return data.get('result', {})

        except requests.exceptions.Timeout:
            raise TelegraphConnectionError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise TelegraphConnectionError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TelegraphError(f"Request error: {str(e)}")

    def create_account(
        self,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None
    ) -> Account:
        """
        Create a new Telegraph account.

        Args:
            short_name: Account name (1-32 characters)
            author_name: Default author name (0-128 characters)
            author_url: Default profile link (0-512 characters)

        Returns:
            Account object with access_token

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        if not short_name or len(short_name) > 32:
            raise TelegraphValidationError("short_name must be 1-32 characters", field="short_name")

        if author_name and len(author_name) > 128:
            raise TelegraphValidationError("author_name must be 0-128 characters", field="author_name")

        if author_url and len(author_url) > 512:
            raise TelegraphValidationError("author_url must be 0-512 characters", field="author_url")

        result = self._api_request('createAccount', {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        })

        account = Account(**result)
        # Store access token for subsequent requests
        if account.access_token:
            self.access_token = account.access_token
        return account

    def edit_account_info(
        self,
        access_token: Optional[str] = None,
        short_name: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None
    ) -> Account:
        """
        Update information about a Telegraph account.

        Args:
            access_token: Access token of the Telegraph account (uses instance token if not provided)
            short_name: New account name (1-32 characters)
            author_name: New default author name (0-128 characters)
            author_url: New default profile link (0-512 characters)

        Returns:
            Updated Account object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        if short_name and len(short_name) > 32:
            raise TelegraphValidationError("short_name must be 1-32 characters", field="short_name")

        if author_name and len(author_name) > 128:
            raise TelegraphValidationError("author_name must be 0-128 characters", field="author_name")

        if author_url and len(author_url) > 512:
            raise TelegraphValidationError("author_url must be 0-512 characters", field="author_url")

        result = self._api_request('editAccountInfo', {
            'access_token': token,
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        })

        return Account(**result)

    def get_account_info(
        self,
        access_token: Optional[str] = None,
        fields: Optional[List[AccountField]] = None
    ) -> Account:
        """
        Get information about a Telegraph account.

        Args:
            access_token: Access token of the Telegraph account (uses instance token if not provided)
            fields: List of account fields to return
                   Available fields: short_name, author_name, author_url, auth_url, page_count

        Returns:
            Account object with requested fields

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        result = self._api_request('getAccountInfo', {
            'access_token': token,
            'fields': fields
        })

        return Account(**result)

    def revoke_access_token(self, access_token: Optional[str] = None) -> Account:
        """
        Revoke access_token and generate a new one.

        Args:
            access_token: Access token of the Telegraph account (uses instance token if not provided)

        Returns:
            Account object with new access_token and auth_url

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        result = self._api_request('revokeAccessToken', {
            'access_token': token
        })

        account = Account(**result)
        # Update instance token with new one
        if account.access_token:
            self.access_token = account.access_token
        return account

    def create_page(
        self,
        title: str,
        content: Union[str, List[Node]],
        access_token: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
        content_format: str = 'html'
    ) -> Page:
        """
        Create a new Telegraph page.

        Args:
            title: Page title (1-256 characters)
            content: Content of the page (HTML string, Markdown string, or Node array)
            access_token: Access token of the Telegraph account (uses instance token if not provided)
            author_name: Author name (0-128 characters)
            author_url: Profile link (0-512 characters)
            return_content: If True, content field will be returned
            content_format: Content format ('html' or 'markdown'). Default is 'html'

        Returns:
            Page object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        if not title or len(title) > 256:
            raise TelegraphValidationError("title must be 1-256 characters", field="title")

        if author_name and len(author_name) > 128:
            raise TelegraphValidationError("author_name must be 0-128 characters", field="author_name")

        if author_url and len(author_url) > 512:
            raise TelegraphValidationError("author_url must be 0-512 characters", field="author_url")

        # Parse content to Node array
        nodes = parse_content(content, format=content_format)
        content_json = nodes_to_json(nodes)

        result = self._api_request('createPage', {
            'access_token': token,
            'title': title,
            'content': content_json,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        })

        return Page(**result)

    def edit_page(
        self,
        path: str,
        title: str,
        content: Union[str, List[Node]],
        access_token: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
        content_format: str = 'html'
    ) -> Page:
        """
        Edit an existing Telegraph page.

        Args:
            path: Path to the page
            title: Page title (1-256 characters)
            content: Content of the page (HTML string, Markdown string, or Node array)
            access_token: Access token of the Telegraph account (uses instance token if not provided)
            author_name: Author name (0-128 characters)
            author_url: Profile link (0-512 characters)
            return_content: If True, content field will be returned
            content_format: Content format ('html' or 'markdown'). Default is 'html'

        Returns:
            Updated Page object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        if not path:
            raise TelegraphValidationError("path is required", field="path")

        if not title or len(title) > 256:
            raise TelegraphValidationError("title must be 1-256 characters", field="title")

        if author_name and len(author_name) > 128:
            raise TelegraphValidationError("author_name must be 0-128 characters", field="author_name")

        if author_url and len(author_url) > 512:
            raise TelegraphValidationError("author_url must be 0-512 characters", field="author_url")

        # Parse content to Node array
        nodes = parse_content(content, format=content_format)
        content_json = nodes_to_json(nodes)

        result = self._api_request('editPage', {
            'access_token': token,
            'path': path,
            'title': title,
            'content': content_json,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        })

        return Page(**result)

    def get_page(self, path: str, return_content: bool = False) -> Page:
        """
        Get a Telegraph page.

        Args:
            path: Path to the Telegraph page
            return_content: If True, content field will be returned

        Returns:
            Page object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        if not path:
            raise TelegraphValidationError("path is required", field="path")

        result = self._api_request('getPage', {
            'path': path,
            'return_content': return_content
        })

        return Page(**result)

    def get_page_list(
        self,
        access_token: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> PageList:
        """
        Get a list of pages belonging to a Telegraph account.

        Args:
            access_token: Access token of the Telegraph account (uses instance token if not provided)
            offset: Sequential number of the first page (default: 0)
            limit: Number of pages to be returned (0-200, default: 50)

        Returns:
            PageList object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        token = access_token or self.access_token
        if not token:
            raise TelegraphValidationError("access_token is required", field="access_token")

        if limit < 0 or limit > 200:
            raise TelegraphValidationError("limit must be 0-200", field="limit")

        result = self._api_request('getPageList', {
            'access_token': token,
            'offset': offset,
            'limit': limit
        })

        # Convert pages to Page objects
        pages = [Page(**page) for page in result.get('pages', [])]
        return PageList(total_count=result.get('total_count', 0), pages=pages)

    def get_views(
        self,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None
    ) -> PageViews:
        """
        Get the number of views for a Telegraph page.

        Args:
            path: Path to the Telegraph page
            year: Required if month is passed (2000-2100)
            month: Required if day is passed (1-12)
            day: Required if hour is passed (1-31)
            hour: Pass to get views for a specific hour (0-24)

        Returns:
            PageViews object

        Raises:
            TelegraphValidationError: If validation fails
            TelegraphAPIError: If the API returns an error
        """
        if not path:
            raise TelegraphValidationError("path is required", field="path")

        if month and not year:
            raise TelegraphValidationError("year is required when month is specified", field="year")

        if day and not month:
            raise TelegraphValidationError("month is required when day is specified", field="month")

        if hour is not None and not day:
            raise TelegraphValidationError("day is required when hour is specified", field="day")

        if year and (year < 2000 or year > 2100):
            raise TelegraphValidationError("year must be 2000-2100", field="year")

        if month and (month < 1 or month > 12):
            raise TelegraphValidationError("month must be 1-12", field="month")

        if day and (day < 1 or day > 31):
            raise TelegraphValidationError("day must be 1-31", field="day")

        if hour is not None and (hour < 0 or hour > 24):
            raise TelegraphValidationError("hour must be 0-24", field="hour")

        result = self._api_request('getViews', {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        })

        return PageViews(**result)

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self) -> 'Telegraph':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
