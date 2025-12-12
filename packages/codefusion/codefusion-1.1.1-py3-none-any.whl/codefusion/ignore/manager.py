# codefusion/ignore/manager.py
import logging
import fnmatch
from pathlib import Path
import typing as t
import sys

try:
    import gitignore_parser
except ImportError:
    # Don't sys.exit here, let the app handle it or warn
    gitignore_parser = None
    print("Warning: 'gitignore_parser' library not found. .gitignore support will be disabled.")
    print("Please install it: pip install gitignore-parser")

from ..utils.constants import DEFAULT_EXCLUDE_PATTERNS

logger = logging.getLogger(__name__)

class IgnoreManager:
    """Handles file and directory exclusion based on various ignore rules."""

    def __init__(self, root_dir: Path, ignore_file_name: str = ".codeignore",
                 use_gitignore: bool = True, extra_exclude_patterns: t.Optional[t.List[str]] = None,
                 output_file: t.Optional[Path] = None):
        self.root_dir = root_dir
        self.ignore_file_name = ignore_file_name
        self.use_gitignore = use_gitignore
        self.all_exclude_patterns: t.List[str] = list(DEFAULT_EXCLUDE_PATTERNS)
        if extra_exclude_patterns:
            self.all_exclude_patterns.extend(extra_exclude_patterns)

        self.custom_ignore_patterns: t.List[str] = []
        # Cache for gitignore matchers: Path (directory) -> Matcher function
        self.gitignore_matchers: t.Dict[Path, t.Optional[t.Callable[[t.Union[str, Path]], bool]]] = {}
        self.output_file = output_file

        self._load_custom_ignore_rules()

    def _load_custom_ignore_rules(self) -> None:
        """Load patterns from custom ignore file."""
        custom_ignore_path = self.root_dir / self.ignore_file_name
        if custom_ignore_path.is_file():
            try:
                with custom_ignore_path.open('r', encoding='utf-8') as f:
                    self.custom_ignore_patterns = [
                        line.strip() for line in f if line.strip() and not line.startswith('#')
                    ]
                logger.info(f"Loaded {len(self.custom_ignore_patterns)} patterns from {self.ignore_file_name}")
            except Exception as e:
                logger.warning(f"Failed to load ignore file {custom_ignore_path}: {e}")

        logger.debug(f"Total default/extra exclude patterns: {len(self.all_exclude_patterns)}")

    def _get_gitignore_matcher(self, directory: Path) -> t.Optional[t.Callable[[t.Union[str, Path]], bool]]:
        """Get or create a gitignore matcher for a specific directory."""
        if not self.use_gitignore:
            return None

        if directory in self.gitignore_matchers:
            return self.gitignore_matchers[directory]

        gitignore_path = directory / '.gitignore'
        matcher = None
        if gitignore_path.is_file():
            try:
                matcher = gitignore_parser.parse_gitignore(str(gitignore_path))
                logger.debug(f"Loaded .gitignore for {directory}")
            except Exception as e:
                logger.warning(f"Failed to load or parse .gitignore file {gitignore_path}: {e}")
        
        self.gitignore_matchers[directory] = matcher
        return matcher

    def is_excluded(self, file_path: Path) -> bool:
        """
        Check if a file should be ignored based on all rules.

        Args:
            file_path: The absolute Path object of the file.

        Returns:
            True if the file should be ignored, False otherwise.
        """
        try:
            rel_path = file_path.relative_to(self.root_dir)
            rel_path_str = rel_path.as_posix()
        except ValueError:
            logger.warning(f"Could not get relative path for {file_path}")
            return True

        # 1. Check default/extra exclusion patterns
        for pattern in self.all_exclude_patterns:
            if fnmatch.fnmatch(rel_path_str, pattern) or \
               any(fnmatch.fnmatch(part, pattern) for part in rel_path.parts):
                 logger.debug(f"Ignoring '{rel_path_str}' due to default/extra pattern: '{pattern}'")
                 return True

        # 2. Check custom ignore patterns (.codeignore)
        if any(fnmatch.fnmatch(rel_path_str, pattern) for pattern in self.custom_ignore_patterns):
            logger.debug(f"Ignoring '{rel_path_str}' due to custom ignore pattern.")
            return True

        # 3. Check .gitignore patterns (Recursive)
        if self.use_gitignore:
            # Check from the file's directory up to the root directory
            current_dir = file_path.parent
            while True:
                # Ensure we don't go above root_dir
                try:
                    current_dir.relative_to(self.root_dir)
                except ValueError:
                    break
                
                matcher = self._get_gitignore_matcher(current_dir)
                if matcher and matcher(file_path):
                    logger.debug(f"Ignoring '{rel_path_str}' due to .gitignore in {current_dir}")
                    return True
                
                if current_dir == self.root_dir:
                    break
                current_dir = current_dir.parent

        # 4. Exclude the output file itself
        if self.output_file and file_path.resolve() == self.output_file.resolve():
            logger.debug(f"Ignoring '{rel_path_str}' as it is the output file.")
            return True

        return False
