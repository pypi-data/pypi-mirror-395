"""
Telegraph Page Templates

Pre-defined templates for creating common types of Telegraph pages.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional
from .types import Node
from .utils import html_to_nodes


@dataclass
class TemplateField:
    """
    Field definition for a template.

    Attributes:
        name: Field identifier
        description: Human-readable description
        required: Whether the field is required
        type: Field type ('string' or 'string[]')
    """
    name: str
    description: str
    required: bool
    type: str  # 'string' or 'string[]'


@dataclass
class Template:
    """
    Telegraph page template.

    Attributes:
        name: Template identifier
        description: Template description
        fields: List of template fields
        generate: Function that generates HTML from data
    """
    name: str
    description: str
    fields: List[TemplateField]
    generate: Callable[[Dict[str, Any]], str]


def _generate_blog_post(data: Dict[str, Any]) -> str:
    """
    Generate HTML for a blog post.

    Required fields:
        - intro: Introduction paragraph

    Optional fields:
        - sections: List of {heading, content} objects
        - conclusion: Conclusion paragraph
    """
    html = f"<p>{data['intro']}</p>"

    for section in data.get('sections', []):
        html += f"<h3>{section['heading']}</h3><p>{section['content']}</p>"

    if data.get('conclusion'):
        html += f"<h4>Conclusion</h4><p>{data['conclusion']}</p>"

    return html


def _generate_documentation(data: Dict[str, Any]) -> str:
    """
    Generate HTML for documentation.

    Required fields:
        - overview: Overview section text

    Optional fields:
        - installation: Installation instructions (code)
        - usage: Usage examples (code)
        - api_reference: List of {name, description} objects
    """
    html = f"<h3>Overview</h3><p>{data['overview']}</p>"

    if data.get('installation'):
        html += f"<h3>Installation</h3><pre>{data['installation']}</pre>"

    if data.get('usage'):
        html += f"<h3>Usage</h3><pre>{data['usage']}</pre>"

    if data.get('api_reference'):
        html += "<h3>API Reference</h3>"
        for item in data['api_reference']:
            html += f"<h4>{item['name']}</h4><p>{item['description']}</p>"

    return html


def _generate_article(data: Dict[str, Any]) -> str:
    """
    Generate HTML for an article.

    Required fields:
        - body: List of paragraph strings

    Optional fields:
        - subtitle: Article subtitle
    """
    html = ""

    if data.get('subtitle'):
        html += f"<aside>{data['subtitle']}</aside>"

    for para in data.get('body', []):
        html += f"<p>{para}</p>"

    return html


def _generate_changelog(data: Dict[str, Any]) -> str:
    """
    Generate HTML for a changelog entry.

    Required fields:
        - version: Version number
        - date: Release date

    Optional fields:
        - added: List of added features
        - changed: List of changes
        - fixed: List of bug fixes
    """
    html = f"<h3>Version {data['version']} - {data['date']}</h3>"

    if data.get('added'):
        html += f"<h4>Added</h4><ul>{''.join(f'<li>{i}</li>' for i in data['added'])}</ul>"

    if data.get('changed'):
        html += f"<h4>Changed</h4><ul>{''.join(f'<li>{i}</li>' for i in data['changed'])}</ul>"

    if data.get('fixed'):
        html += f"<h4>Fixed</h4><ul>{''.join(f'<li>{i}</li>' for i in data['fixed'])}</ul>"

    return html


def _generate_tutorial(data: Dict[str, Any]) -> str:
    """
    Generate HTML for a tutorial.

    Required fields:
        - description: Tutorial description
        - steps: List of {title, content} objects

    Optional fields:
        - prerequisites: List of prerequisite strings
        - conclusion: Conclusion paragraph
    """
    html = f"<p>{data['description']}</p>"

    if data.get('prerequisites'):
        html += f"<h3>Prerequisites</h3><ul>{''.join(f'<li>{p}</li>' for p in data['prerequisites'])}</ul>"

    html += "<h3>Steps</h3><ol>"
    for step in data.get('steps', []):
        html += f"<li><b>{step['title']}</b><p>{step['content']}</p></li>"
    html += "</ol>"

    if data.get('conclusion'):
        html += f"<h3>Conclusion</h3><p>{data['conclusion']}</p>"

    return html


# Template definitions
TEMPLATES: Dict[str, Template] = {
    'blog_post': Template(
        name='blog_post',
        description='A blog post with introduction, sections, and optional conclusion',
        fields=[
            TemplateField(
                name='intro',
                description='Introduction paragraph',
                required=True,
                type='string'
            ),
            TemplateField(
                name='sections',
                description='Array of {heading, content} objects',
                required=False,
                type='string[]'
            ),
            TemplateField(
                name='conclusion',
                description='Conclusion paragraph',
                required=False,
                type='string'
            ),
        ],
        generate=_generate_blog_post
    ),

    'documentation': Template(
        name='documentation',
        description='Technical documentation with overview, installation, usage, and API reference',
        fields=[
            TemplateField(
                name='overview',
                description='Project overview text',
                required=True,
                type='string'
            ),
            TemplateField(
                name='installation',
                description='Installation instructions (code)',
                required=False,
                type='string'
            ),
            TemplateField(
                name='usage',
                description='Usage examples (code)',
                required=False,
                type='string'
            ),
            TemplateField(
                name='api_reference',
                description='Array of {name, description} objects',
                required=False,
                type='string[]'
            ),
        ],
        generate=_generate_documentation
    ),

    'article': Template(
        name='article',
        description='A simple article with optional subtitle and body paragraphs',
        fields=[
            TemplateField(
                name='body',
                description='Array of paragraph strings',
                required=True,
                type='string[]'
            ),
            TemplateField(
                name='subtitle',
                description='Article subtitle',
                required=False,
                type='string'
            ),
        ],
        generate=_generate_article
    ),

    'changelog': Template(
        name='changelog',
        description='A changelog entry for a software release',
        fields=[
            TemplateField(
                name='version',
                description='Version number',
                required=True,
                type='string'
            ),
            TemplateField(
                name='date',
                description='Release date',
                required=True,
                type='string'
            ),
            TemplateField(
                name='added',
                description='Array of added features',
                required=False,
                type='string[]'
            ),
            TemplateField(
                name='changed',
                description='Array of changes',
                required=False,
                type='string[]'
            ),
            TemplateField(
                name='fixed',
                description='Array of bug fixes',
                required=False,
                type='string[]'
            ),
        ],
        generate=_generate_changelog
    ),

    'tutorial': Template(
        name='tutorial',
        description='A step-by-step tutorial with prerequisites and conclusion',
        fields=[
            TemplateField(
                name='description',
                description='Tutorial description',
                required=True,
                type='string'
            ),
            TemplateField(
                name='steps',
                description='Array of {title, content} objects',
                required=True,
                type='string[]'
            ),
            TemplateField(
                name='prerequisites',
                description='Array of prerequisite strings',
                required=False,
                type='string[]'
            ),
            TemplateField(
                name='conclusion',
                description='Conclusion paragraph',
                required=False,
                type='string'
            ),
        ],
        generate=_generate_tutorial
    ),
}


def get_template(name: str) -> Optional[Template]:
    """
    Get a template by name.

    Args:
        name: Template identifier

    Returns:
        Template object or None if not found
    """
    return TEMPLATES.get(name)


def list_templates() -> List[Dict[str, Any]]:
    """
    List all available templates.

    Returns:
        List of template metadata dictionaries

    Example:
        >>> templates = list_templates()
        >>> for t in templates:
        ...     print(f"{t['name']}: {t['description']}")
    """
    return [
        {
            'name': t.name,
            'description': t.description,
            'fields': [
                {
                    'name': f.name,
                    'description': f.description,
                    'required': f.required,
                    'type': f.type
                }
                for f in t.fields
            ]
        }
        for t in TEMPLATES.values()
    ]


def create_from_template(template_name: str, data: Dict[str, Any]) -> List[Node]:
    """
    Create Telegraph content from a template.

    Args:
        template_name: Name of the template to use
        data: Data to populate the template

    Returns:
        List of Node objects ready for Telegraph API

    Raises:
        ValueError: If template not found or required fields missing

    Example:
        >>> nodes = create_from_template('blog_post', {
        ...     'intro': 'Welcome to my blog!',
        ...     'sections': [
        ...         {'heading': 'First Topic', 'content': 'Some content here.'}
        ...     ]
        ... })
    """
    template = get_template(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")

    # Validate required fields
    for field in template.fields:
        if field.required and field.name not in data:
            raise ValueError(f"Required field missing: {field.name}")

    # Generate HTML from template
    html = template.generate(data)

    # Convert to nodes
    return html_to_nodes(html)
