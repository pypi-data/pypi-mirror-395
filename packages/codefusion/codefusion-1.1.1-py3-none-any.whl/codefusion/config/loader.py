# codefusion/config/loader.py
import logging
from pathlib import Path
import typing as t

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  
    except ImportError:
        tomllib = None

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Handles loading and parsing of configuration files."""
    
    def __init__(self, config_path: t.Optional[t.Union[str, Path]] = None):
        self.config_path = Path(config_path) if config_path else None
        self.config = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        # Load default config first
        default_config_path = Path(__file__).parent.parent / "default_config.toml"
        if default_config_path.exists() and tomllib:
            try:
                with open(default_config_path, 'rb') as f:
                    default_data = tomllib.load(f)
                    self.config = default_data
            except Exception as e:
                logger.warning(f"Failed to load default config: {e}")

        if not self.config_path:
            # Look for user config files
            for name in ['.codefusion.toml', 'codefusion.toml', 'pyproject.toml']:
                path = Path.cwd() / name
                if path.exists():
                    self.config_path = path
                    break
        
        if not self.config_path or not self.config_path.exists():
            logger.debug("No user configuration file found")
            return
        
        if not tomllib:
            logger.warning("TOML library not available. Install tomli for config file support.")
            return
        
        try:
            with open(self.config_path, 'rb') as f:
                data = tomllib.load(f)
            
            # Extract codefusion config
            user_config = {}
            if 'tool' in data and 'codefusion' in data['tool']:
                user_config = data['tool']['codefusion']
            elif 'codefusion' in data:
                user_config = data['codefusion']
            
            # Merge user config into default config (deep merge would be better but simple update for now)
            # For groups, we might want to merge or replace. Let's assume replace for top-level keys.
            self.config.update(user_config)
            
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            logger.warning(f"Failed to load config file {self.config_path}: {e}")
    
    def get_config(self) -> t.Dict[str, t.Any]:
        """Get the loaded configuration."""
        return self.config.copy()
