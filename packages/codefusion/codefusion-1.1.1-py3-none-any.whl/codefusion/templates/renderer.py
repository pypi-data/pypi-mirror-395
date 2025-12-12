# codefusion/templates/renderer.py
import typing as t
from .base import BaseTemplate
from .markdown import MarkdownTemplate
from .html import HtmlTemplate
from .default import DefaultTemplate

class TemplateRenderer:
    def __init__(self):
        self.templates: t.Dict[str, BaseTemplate] = {
            'markdown': MarkdownTemplate(),
            'html': HtmlTemplate(),
            'default': DefaultTemplate()
        }

    def _get_template(self, template_name: str) -> BaseTemplate:
        return self.templates.get(template_name, self.templates['default'])

    def render_header(self, template: str, **kwargs) -> str:
        return self._get_template(template).render_header(**kwargs)

    def render_group_header(self, template: str, group_name: str, group_description: str, file_count: int) -> str:
        return self._get_template(template).render_group_header(group_name, group_description, file_count)

    def render_file_header(self, template: str, file_path: str, **kwargs) -> str:
        return self._get_template(template).render_file_header(file_path, **kwargs)

    def render_file_footer(self, template: str, **kwargs) -> str:
        return self._get_template(template).render_file_footer(**kwargs)

    def render_group_footer(self, template: str, **kwargs) -> str:
        return self._get_template(template).render_group_footer(**kwargs)

    def render_footer(self, template: str, **kwargs) -> str:
        return self._get_template(template).render_footer(**kwargs)
