"""
Telegraph API Utility Functions
"""

import re
from typing import List, Union
from .types import Node, NodeElement, ALLOWED_TAGS


def html_to_nodes(html: str) -> List[Node]:
    """
    Convert HTML string to Telegraph Node array.

    Supports all Telegraph-allowed HTML tags:
    p, b, i, strong, em, a, br, h3, h4, blockquote, code, pre,
    ul, ol, li, figure, figcaption, img, video, iframe, hr, aside, s, u

    Args:
        html: HTML string to convert

    Returns:
        List of Node objects (strings or NodeElements)

    Example:
        >>> html_to_nodes("<p>Hello <b>world</b></p>")
        [NodeElement(tag='p', children=['Hello ', NodeElement(tag='b', children=['world'])])]
    """
    nodes: List[Node] = []

    # Simple regex-based parser for basic HTML
    # This handles common cases but is not a full HTML parser
    tag_regex = re.compile(r'<(/?)(\w+)([^>]*)>|([^<]+)')
    stack: List[dict] = []
    current: List[Node] = nodes

    for match in tag_regex.finditer(html):
        closing, tag_name, attr_string, text = match.groups()

        if text:
            # Text node - preserve all text including whitespace
            if text:
                current.append(text)
        elif tag_name:
            tag = tag_name.lower()

            if closing:
                # Closing tag
                if stack:
                    completed = stack.pop()
                    current = stack[-1]['children'] if stack else nodes

                    element = NodeElement(tag=completed['tag'])
                    if completed.get('attrs'):
                        element.attrs = completed['attrs']
                    if completed.get('children'):
                        element.children = completed['children']
                    current.append(element)
            else:
                # Opening tag
                attrs = {}

                # Parse attributes
                attr_regex = re.compile(r'(\w+)=["\']([^"\']*)["\']')
                for attr_match in attr_regex.finditer(attr_string):
                    attr_name, attr_value = attr_match.groups()
                    attrs[attr_name] = attr_value

                # Self-closing tags
                if tag in ['br', 'hr', 'img'] or attr_string.strip().endswith('/'):
                    element = NodeElement(tag=tag)
                    if attrs:
                        element.attrs = attrs
                    current.append(element)
                else:
                    # Regular tag - push to stack
                    new_element = {
                        'tag': tag,
                        'attrs': attrs if attrs else None,
                        'children': []
                    }
                    stack.append(new_element)
                    current = new_element['children']

    # Handle any unclosed tags
    while stack:
        completed = stack.pop()
        parent = stack[-1]['children'] if stack else nodes

        element = NodeElement(tag=completed['tag'])
        if completed.get('attrs'):
            element.attrs = completed['attrs']
        if completed.get('children'):
            element.children = completed['children']
        parent.append(element)

    return nodes


def markdown_to_html(markdown: str) -> str:
    """
    Convert Markdown to Telegraph-compatible HTML.

    Supports basic Markdown syntax:
    - Headers (# ## ### ####) -> h3, h4
    - Bold (**text** or __text__) -> <b>
    - Italic (*text* or _text_) -> <i>
    - Links [text](url) -> <a href="url">
    - Images ![alt](src) -> <figure><img src="..."><figcaption>alt</figcaption></figure>
    - Code blocks (```code```) -> <pre>
    - Inline code (`code`) -> <code>
    - Blockquotes (> text) -> <blockquote>
    - Lists (- or * or 1.) -> <ul>/<ol>
    - Horizontal rules (---) -> <hr>

    Args:
        markdown: Markdown string to convert

    Returns:
        HTML string
    """
    html = markdown

    # Escape special HTML characters in code blocks first to preserve them
    code_blocks: List[str] = []
    html = re.sub(r'```([\s\S]*?)```', lambda m: (
        code_blocks.append(m.group(1).strip()),
        f'__CODEBLOCK_{len(code_blocks) - 1}__'
    )[1], html)

    inline_codes: List[str] = []
    html = re.sub(r'`([^`]+)`', lambda m: (
        inline_codes.append(m.group(1)),
        f'__INLINECODE_{len(inline_codes) - 1}__'
    )[1], html)

    # Convert headers (Telegraph only supports h3 and h4)
    html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Convert horizontal rules
    html = re.sub(r'^---+$', '<hr/>', html, flags=re.MULTILINE)

    # Convert images with caption ![alt](src)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<figure><img src="\2"/><figcaption>\1</figcaption></figure>', html)

    # Convert links [text](url)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Convert bold **text** or __text__
    html = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', html)
    html = re.sub(r'__([^_]+)__', r'<b>\1</b>', html)

    # Convert italic *text* or _text_ (but not in middle of words)
    html = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'<i>\1</i>', html)
    html = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'<i>\1</i>', html)

    # Convert blockquotes
    html = re.sub(r'^>\s+(.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Convert unordered lists
    ul_lines: List[str] = []
    in_ul = False
    lines = html.split('\n')
    processed_lines: List[str] = []

    for line in lines:
        ul_match = re.match(r'^[-*]\s+(.+)$', line)

        if ul_match:
            ul_lines.append(f'<li>{ul_match.group(1)}</li>')
            in_ul = True
        else:
            if in_ul:
                processed_lines.append(f'<ul>{"".join(ul_lines)}</ul>')
                ul_lines = []
                in_ul = False
            processed_lines.append(line)

    if in_ul:
        processed_lines.append(f'<ul>{"".join(ul_lines)}</ul>')
    html = '\n'.join(processed_lines)

    # Convert ordered lists
    ol_lines: List[str] = []
    in_ol = False
    lines2 = html.split('\n')
    processed_lines2: List[str] = []

    for line in lines2:
        ol_match = re.match(r'^\d+\.\s+(.+)$', line)

        if ol_match:
            ol_lines.append(f'<li>{ol_match.group(1)}</li>')
            in_ol = True
        else:
            if in_ol:
                processed_lines2.append(f'<ol>{"".join(ol_lines)}</ol>')
                ol_lines = []
                in_ol = False
            processed_lines2.append(line)

    if in_ol:
        processed_lines2.append(f'<ol>{"".join(ol_lines)}</ol>')
    html = '\n'.join(processed_lines2)

    # Restore code blocks
    html = re.sub(r'__CODEBLOCK_(\d+)__', lambda m: f'<pre>{code_blocks[int(m.group(1))]}</pre>', html)

    # Restore inline code
    html = re.sub(r'__INLINECODE_(\d+)__', lambda m: f'<code>{inline_codes[int(m.group(1))]}</code>', html)

    # Convert paragraphs (lines separated by blank lines)
    paragraphs = re.split(r'\n\n+', html)
    html = '\n'.join(
        para.strip() if (para.strip().startswith('<') and para.strip().endswith('>')) or not para.strip()
        else f'<p>{para.strip()}</p>'
        for para in paragraphs
        if para.strip()
    )

    return html


def parse_content(content: Union[str, List[Node]], format: str = 'html') -> List[Node]:
    """
    Parse content input - accepts either HTML string, Markdown string, or Node array.

    Args:
        content: Content to parse (HTML string, Markdown string, or Node array)
        format: Content format ('html' or 'markdown'). Default is 'html'

    Returns:
        List of Node objects

    Example:
        >>> parse_content("<p>Hello</p>")
        [NodeElement(tag='p', children=['Hello'])]
        >>> parse_content("# Hello", format='markdown')
        [NodeElement(tag='h3', children=['Hello'])]
    """
    # If already a list of nodes, return as-is
    if isinstance(content, list):
        return content

    # Convert markdown to HTML if format is markdown
    html_content = content
    if format == 'markdown':
        html_content = markdown_to_html(content)

    # Convert HTML to nodes
    return html_to_nodes(html_content)


def nodes_to_json(nodes: List[Node]) -> List[Union[str, dict]]:
    """
    Convert Node list to JSON-serializable format.

    Args:
        nodes: List of Node objects

    Returns:
        List of strings and dictionaries that can be JSON serialized
    """
    result = []
    for node in nodes:
        if isinstance(node, str):
            result.append(node)
        elif isinstance(node, NodeElement):
            result.append(node.to_dict())
    return result


def _node_element_to_markdown(node: NodeElement) -> str:
    """
    Convert a single NodeElement to Markdown string.

    Args:
        node: NodeElement to convert

    Returns:
        Markdown string
    """
    children = nodes_to_markdown(node.children) if node.children else ""
    tag = node.tag

    if tag == 'h3':
        return f"\n# {children}\n"
    if tag == 'h4':
        return f"\n## {children}\n"
    if tag == 'p':
        return f"\n{children}\n"
    if tag in ('b', 'strong'):
        return f"**{children}**"
    if tag in ('i', 'em'):
        return f"*{children}*"
    if tag == 'a':
        href = node.attrs.get('href', '') if node.attrs else ''
        return f"[{children}]({href})"
    if tag == 'img':
        src = node.attrs.get('src', '') if node.attrs else ''
        return f"![image]({src})"
    if tag in ('ul', 'ol'):
        return f"\n{children}"
    if tag == 'li':
        return f"- {children}\n"
    if tag == 'blockquote':
        return f"\n> {children}\n"
    if tag == 'code':
        return f"`{children}`"
    if tag == 'pre':
        return f"\n```\n{children}\n```\n"
    if tag == 'br':
        return "\n"
    if tag == 'hr':
        return "\n---\n"
    if tag == 's':
        return f"~~{children}~~"
    if tag == 'u':
        return f"__{children}__"
    if tag == 'aside':
        return f"\n> {children}\n"
    if tag == 'figure':
        # Handle figure with possible img and figcaption
        return children
    if tag == 'figcaption':
        return f"\n*{children}*\n"
    if tag == 'video':
        src = node.attrs.get('src', '') if node.attrs else ''
        return f"\n[Video]({src})\n"
    if tag == 'iframe':
        src = node.attrs.get('src', '') if node.attrs else ''
        return f"\n[Embed]({src})\n"

    # Default: just return children
    return children


def nodes_to_markdown(nodes: List[Node]) -> str:
    """
    Convert Node array to Markdown string.

    Args:
        nodes: List of Node objects (strings or NodeElements)

    Returns:
        Markdown string

    Example:
        >>> nodes = [NodeElement(tag='p', children=['Hello ', NodeElement(tag='b', children=['world'])])]
        >>> nodes_to_markdown(nodes)
        '\\nHello **world**\\n'
    """
    markdown = ""
    for node in nodes:
        if isinstance(node, str):
            markdown += node
        else:
            markdown += _node_element_to_markdown(node)
    return markdown


def _node_element_to_html(node: NodeElement) -> str:
    """
    Convert a single NodeElement to HTML string.

    Args:
        node: NodeElement to convert

    Returns:
        HTML string
    """
    tag = node.tag
    attrs_str = ""

    if node.attrs:
        attrs_str = " " + " ".join(
            f'{key}="{value}"' for key, value in node.attrs.items()
        )

    children = nodes_to_html(node.children) if node.children else ""

    # Self-closing tags
    if tag in ('br', 'hr', 'img'):
        return f"<{tag}{attrs_str}/>"

    return f"<{tag}{attrs_str}>{children}</{tag}>"


def nodes_to_html(nodes: List[Node]) -> str:
    """
    Convert Node array to HTML string.

    Args:
        nodes: List of Node objects (strings or NodeElements)

    Returns:
        HTML string

    Example:
        >>> nodes = [NodeElement(tag='p', children=['Hello ', NodeElement(tag='b', children=['world'])])]
        >>> nodes_to_html(nodes)
        '<p>Hello <b>world</b></p>'
    """
    html = ""
    for node in nodes:
        if isinstance(node, str):
            html += node
        else:
            html += _node_element_to_html(node)
    return html
