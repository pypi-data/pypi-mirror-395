# codefusion/templates/default.py
from .base import BaseTemplate
from ..utils.constants import HEADER_SEPARATOR, FILE_SEPARATOR

class DefaultTemplate(BaseTemplate):
    def render_header(self, **kwargs) -> str:
        return f"""{HEADER_SEPARATOR}
Project Code Compilation
Generated on: {kwargs.get('timestamp', 'Unknown')}
Source Directory: {kwargs.get('source_dir', 'Unknown')}
File Extensions Included: {kwargs.get('extensions', 'Unknown')}
Total Files: {kwargs.get('total_files', 0)}
{HEADER_SEPARATOR}

"""

    def render_group_header(self, group_name: str, group_description: str, file_count: int) -> str:
        return f"\n\n{HEADER_SEPARATOR}\n{group_description.upper()}\n({file_count} files)\n{HEADER_SEPARATOR}\n\n"

    def render_file_header(self, file_path: str, **kwargs) -> str:
        return f"File: {file_path}\n{FILE_SEPARATOR}\n\n"

    def render_file_footer(self, **kwargs) -> str:
        return f"\n\n{HEADER_SEPARATOR}\n"

    def render_group_footer(self, **kwargs) -> str:
        return ""

    def render_footer(self, **kwargs) -> str:
        return f"""\n\n{HEADER_SEPARATOR}
Compilation Summary:
Total files processed: {kwargs.get('processed_count', 0)}
Files with read errors: {kwargs.get('error_count', 0)}
{HEADER_SEPARATOR}
"""
