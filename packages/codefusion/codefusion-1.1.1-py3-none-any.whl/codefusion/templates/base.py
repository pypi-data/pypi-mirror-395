# codefusion/templates/base.py
from abc import ABC, abstractmethod
import typing as t

class BaseTemplate(ABC):
    @abstractmethod
    def render_header(self, **kwargs) -> str:
        pass

    @abstractmethod
    def render_group_header(self, group_name: str, group_description: str, file_count: int) -> str:
        pass

    @abstractmethod
    def render_file_header(self, file_path: str, **kwargs) -> str:
        pass

    @abstractmethod
    def render_file_footer(self, **kwargs) -> str:
        pass

    @abstractmethod
    def render_group_footer(self, **kwargs) -> str:
        pass

    @abstractmethod
    def render_footer(self, **kwargs) -> str:
        pass
