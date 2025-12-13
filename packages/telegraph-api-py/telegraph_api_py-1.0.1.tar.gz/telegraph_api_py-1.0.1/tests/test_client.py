"""
Basic tests for Telegraph API client
"""

import pytest
from telegraph import Telegraph, AsyncTelegraph
from telegraph.errors import TelegraphValidationError
from telegraph.utils import html_to_nodes, markdown_to_html, parse_content
from telegraph.types import NodeElement


class TestUtils:
    """Test utility functions"""

    def test_html_to_nodes_simple(self):
        """Test simple HTML to nodes conversion"""
        nodes = html_to_nodes("<p>Hello World</p>")
        assert len(nodes) == 1
        assert isinstance(nodes[0], NodeElement)
        assert nodes[0].tag == 'p'
        assert nodes[0].children == ['Hello World']

    def test_html_to_nodes_nested(self):
        """Test nested HTML to nodes conversion"""
        nodes = html_to_nodes("<p>Hello <b>World</b></p>")
        assert len(nodes) == 1
        assert isinstance(nodes[0], NodeElement)
        assert nodes[0].tag == 'p'
        assert len(nodes[0].children) == 2
        assert nodes[0].children[0] == 'Hello '
        assert isinstance(nodes[0].children[1], NodeElement)
        assert nodes[0].children[1].tag == 'b'

    def test_html_to_nodes_with_attrs(self):
        """Test HTML with attributes"""
        nodes = html_to_nodes('<a href="https://example.com">Link</a>')
        assert len(nodes) == 1
        assert isinstance(nodes[0], NodeElement)
        assert nodes[0].tag == 'a'
        assert nodes[0].attrs == {'href': 'https://example.com'}
        assert nodes[0].children == ['Link']

    def test_html_to_nodes_self_closing(self):
        """Test self-closing tags"""
        nodes = html_to_nodes('<p>Line 1<br/>Line 2</p>')
        assert len(nodes) == 1
        assert nodes[0].tag == 'p'
        assert len(nodes[0].children) == 3
        assert nodes[0].children[1].tag == 'br'

    def test_markdown_to_html_headers(self):
        """Test markdown headers conversion"""
        html = markdown_to_html("# Header 1\n## Header 2")
        assert '<h3>Header 1</h3>' in html
        assert '<h4>Header 2</h4>' in html

    def test_markdown_to_html_bold(self):
        """Test markdown bold conversion"""
        html = markdown_to_html("**bold text**")
        assert '<b>bold text</b>' in html

    def test_markdown_to_html_italic(self):
        """Test markdown italic conversion"""
        html = markdown_to_html("*italic text*")
        assert '<i>italic text</i>' in html

    def test_markdown_to_html_links(self):
        """Test markdown links conversion"""
        html = markdown_to_html("[Click here](https://example.com)")
        assert '<a href="https://example.com">Click here</a>' in html

    def test_markdown_to_html_code(self):
        """Test markdown code conversion"""
        html = markdown_to_html("`inline code`")
        assert '<code>inline code</code>' in html

    def test_markdown_to_html_code_block(self):
        """Test markdown code block conversion"""
        html = markdown_to_html("```\ncode block\n```")
        assert '<pre>code block</pre>' in html

    def test_parse_content_html(self):
        """Test parse_content with HTML"""
        nodes = parse_content("<p>Test</p>", format='html')
        assert len(nodes) == 1
        assert nodes[0].tag == 'p'

    def test_parse_content_markdown(self):
        """Test parse_content with Markdown"""
        nodes = parse_content("# Test", format='markdown')
        assert len(nodes) == 1
        assert nodes[0].tag == 'h3'

    def test_parse_content_nodes_list(self):
        """Test parse_content with node list"""
        input_nodes = [NodeElement(tag='p', children=['Test'])]
        nodes = parse_content(input_nodes)
        assert nodes == input_nodes


class TestTelegraphValidation:
    """Test Telegraph client validation"""

    def test_create_account_invalid_short_name(self):
        """Test create_account with invalid short_name"""
        tg = Telegraph()
        with pytest.raises(TelegraphValidationError) as exc_info:
            tg.create_account(short_name="")
        assert "short_name" in str(exc_info.value)

    def test_create_account_short_name_too_long(self):
        """Test create_account with too long short_name"""
        tg = Telegraph()
        with pytest.raises(TelegraphValidationError) as exc_info:
            tg.create_account(short_name="a" * 33)
        assert "short_name" in str(exc_info.value)

    def test_create_page_no_token(self):
        """Test create_page without access token"""
        tg = Telegraph()
        with pytest.raises(TelegraphValidationError) as exc_info:
            tg.create_page(title="Test", content="<p>Test</p>")
        assert "access_token" in str(exc_info.value)

    def test_create_page_invalid_title(self):
        """Test create_page with invalid title"""
        tg = Telegraph(access_token="test_token")
        with pytest.raises(TelegraphValidationError) as exc_info:
            tg.create_page(title="", content="<p>Test</p>")
        assert "title" in str(exc_info.value)

    def test_get_page_invalid_path(self):
        """Test get_page with empty path"""
        tg = Telegraph()
        with pytest.raises(TelegraphValidationError) as exc_info:
            tg.get_page(path="")
        assert "path" in str(exc_info.value)

    def test_get_views_validation(self):
        """Test get_views with invalid parameters"""
        tg = Telegraph()

        # Month without year
        with pytest.raises(TelegraphValidationError):
            tg.get_views(path="test", month=1)

        # Day without month
        with pytest.raises(TelegraphValidationError):
            tg.get_views(path="test", year=2025, day=1)

        # Invalid year range
        with pytest.raises(TelegraphValidationError):
            tg.get_views(path="test", year=1999)

        # Invalid month range
        with pytest.raises(TelegraphValidationError):
            tg.get_views(path="test", year=2025, month=13)

    def test_get_page_list_invalid_limit(self):
        """Test get_page_list with invalid limit"""
        tg = Telegraph(access_token="test_token")
        with pytest.raises(TelegraphValidationError):
            tg.get_page_list(limit=201)


class TestTelegraphClient:
    """Test Telegraph synchronous client"""

    def test_client_initialization(self):
        """Test Telegraph client initialization"""
        tg = Telegraph()
        assert tg.base_url == "https://api.telegra.ph"
        assert tg.timeout == 30
        assert tg.access_token is None

    def test_client_with_token(self):
        """Test Telegraph client with access token"""
        tg = Telegraph(access_token="test_token")
        assert tg.access_token == "test_token"

    def test_context_manager(self):
        """Test Telegraph client as context manager"""
        with Telegraph() as tg:
            assert tg is not None
            assert hasattr(tg, '_session')


class TestAsyncTelegraphClient:
    """Test AsyncTelegraph asynchronous client"""

    def test_async_client_initialization(self):
        """Test AsyncTelegraph client initialization"""
        tg = AsyncTelegraph()
        assert tg.base_url == "https://api.telegra.ph"
        assert tg.timeout == 30
        assert tg.access_token is None

    def test_async_client_with_token(self):
        """Test AsyncTelegraph client with access token"""
        tg = AsyncTelegraph(access_token="test_token")
        assert tg.access_token == "test_token"

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test AsyncTelegraph client as async context manager"""
        async with AsyncTelegraph() as tg:
            assert tg is not None


# Note: Integration tests that actually call the Telegraph API are not included
# as they would require network access and could be rate-limited.
# For production use, you would want to add integration tests with proper mocking
# or test against a local mock server.
