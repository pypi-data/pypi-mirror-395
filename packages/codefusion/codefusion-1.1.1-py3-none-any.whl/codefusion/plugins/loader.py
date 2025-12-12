# codefusion/plugins/loader.py
import logging
import typing as t

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        """Load plugins from default locations."""
        logger.debug("Loading plugins... (Not implemented yet)")
        pass
