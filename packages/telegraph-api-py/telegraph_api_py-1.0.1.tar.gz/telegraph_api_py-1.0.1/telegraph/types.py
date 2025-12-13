"""
Telegraph API Type Definitions
Based on https://telegra.ph/api
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Literal, Dict, Any


# Allowed HTML tags in Telegraph content
ALLOWED_TAGS = [
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption',
    'figure', 'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p',
    'pre', 's', 'strong', 'u', 'ul', 'video'
]

# Account fields that can be requested
AccountField = Literal['short_name', 'author_name', 'author_url', 'auth_url', 'page_count']


@dataclass
class NodeElement:
    """
    Telegraph NodeElement - represents a DOM element.

    Attributes:
        tag: Name of the DOM element tag
        attrs: Attributes of the DOM element (href for <a>, src for <img>, <video>, <iframe>)
        children: List of child nodes for the DOM element
    """
    tag: str
    attrs: Optional[Dict[str, str]] = None
    children: Optional[List['Node']] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert NodeElement to dictionary for JSON serialization."""
        result: Dict[str, Any] = {'tag': self.tag}
        if self.attrs:
            result['attrs'] = self.attrs
        if self.children:
            result['children'] = [
                child if isinstance(child, str) else child.to_dict()
                for child in self.children
            ]
        return result


# Telegraph Node - can be either a string (text content) or a NodeElement
Node = Union[str, NodeElement]


@dataclass
class Account:
    """
    Telegraph Account object.

    Attributes:
        short_name: Account name, helps users with several accounts remember which they are currently using
        author_name: Default author name used when creating new articles
        author_url: Profile link, opened when users click on the author's name below the title
        access_token: Access token of the Telegraph account (only returned by createAccount and revokeAccessToken)
        auth_url: URL to authorize a browser on telegra.ph (only returned by revokeAccessToken)
        page_count: Number of pages belonging to the Telegraph account (only returned when requested)
    """
    short_name: str
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    access_token: Optional[str] = None
    auth_url: Optional[str] = None
    page_count: Optional[int] = None


@dataclass
class Page:
    """
    Telegraph Page object.

    Attributes:
        path: Path to the page
        url: URL of the page
        title: Title of the page
        description: Description of the page
        views: Number of page views for the page
        author_name: Name of the author, displayed below the title
        author_url: Profile link, opened when users click on the author's name below the title
        image_url: Image URL of the page
        content: Content of the page (array of Node objects, only returned if return_content is true)
        can_edit: True if the target Telegraph account can edit the page
    """
    path: str
    url: str
    title: str
    description: str
    views: int
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[List[Node]] = None
    can_edit: Optional[bool] = None


@dataclass
class PageList:
    """
    Telegraph PageList object.

    Attributes:
        total_count: Total number of pages belonging to the target Telegraph account
        pages: Requested pages of the target Telegraph account
    """
    total_count: int
    pages: List[Page] = field(default_factory=list)


@dataclass
class PageViews:
    """
    Telegraph PageViews object.

    Attributes:
        views: Number of page views for the target page
    """
    views: int


@dataclass
class ApiResponse:
    """
    Telegraph API Response wrapper.

    Attributes:
        ok: True if the request was successful
        result: Result of the request (only present if ok is true)
        error: Error message (only present if ok is false)
    """
    ok: bool
    result: Optional[Any] = None
    error: Optional[str] = None
