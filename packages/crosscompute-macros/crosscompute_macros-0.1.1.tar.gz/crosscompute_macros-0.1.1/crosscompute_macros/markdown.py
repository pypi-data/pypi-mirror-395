import re

from markdown2 import markdown


OUTER_PARAGRAPH_PATTERN = re.compile(r'^<p>((?:(?!<p>).)*)</p>$', re.DOTALL)
EXTRAS = [
    'break-on-newline',
    'code-friendly',
    'cuddled-lists',
    'fenced-code-blocks',
    'footnotes',
    'markdown-in-html',
    'mermaid',
    'strike',
    'target-blank-links',
    'tables',
    'use-file-vars',
    'task_list']


def get_html_from_markdown(text, extras=EXTRAS):
    return markdown(text, extras=extras).strip()


def remove_outer_paragraph(html):
    return OUTER_PARAGRAPH_PATTERN.sub(r'\g<1>', html)


def remove_inner_paragraphs(html, a, b):
    html = re.sub(r'<p>(\s*(?:[^<X]*X))'.replace('X', a), r'\g<1>', html)
    html = re.sub(r'((?:X[^>]*)\s*)</p>'.replace('X', b), r'\g<1>', html)
    return html
