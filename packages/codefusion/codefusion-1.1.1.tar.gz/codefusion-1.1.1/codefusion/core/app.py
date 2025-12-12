# codefusion/core/app.py
import logging
import typing as t
from pathlib import Path
import os

from .scanner import FileScanner
from .writer import CodeWriter
from .filter import FileFilter
from .grouper import FileGrouper
from ..ignore.manager import IgnoreManager
from ..cache.manager import CacheManager
from ..config.loader import ConfigLoader

logger = logging.getLogger(__name__)

class CodeFusionApp:
    def __init__(self,
                 directory: t.Optional[t.Union[str, Path]] = None,
                 output_file: t.Optional[t.Union[str, Path]] = None,
                 ignore_file_name: str = ".codeignore",
                 use_gitignore: bool = True,
                 extensions: t.Optional[t.Set[str]] = None,
                 verbose: bool = False,
                 extra_exclude_patterns: t.Optional[t.List[str]] = None,
                 num_workers: int = 1,
                 dry_run: bool = False,
                 include_empty: bool = False,
                 min_size: int = 0,
                 max_size: t.Optional[int] = None,
                 to_stdout: bool = False,
                 include_dirs: t.Optional[t.List[str]] = None,
                 template: str = "default",
                 no_grouping: bool = False,
                 use_cache: bool = True,
                 cache_size: int = 50,
                 cache_max_age: int = 7,
                 copy_to_clipboard: bool = False,
                 resume: bool = False,
                 detect_secrets: bool = False):
        
        self.root_dir: Path = Path(directory or Path.cwd()).resolve()
        self.copy_to_clipboard: bool = copy_to_clipboard
        self.output_file: t.Optional[Path] = Path(output_file) if output_file else None
        self.verbose: bool = verbose
        self.num_workers: int = num_workers
        self.dry_run: bool = dry_run
        self.to_stdout: bool = to_stdout
        self.template: str = template
        self.no_grouping: bool = no_grouping
        self.use_cache: bool = use_cache
        self.resume: bool = resume
        self.detect_secrets: bool = detect_secrets

        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose mode enabled.")

        if not self.root_dir.is_dir():
            raise ValueError(f"Invalid directory: {self.root_dir}")

        logger.info(f"Source directory: {self.root_dir}")
        if self.output_file is not None:
            logger.info(f"Output file: {self.output_file.resolve()}")
        elif self.to_stdout:
            logger.info("Output will be printed to stdout.")

        # Load configuration
        self.config_loader = ConfigLoader()
        self.config = self.config_loader.get_config()
        
        # Initialize Grouper
        self.grouper = FileGrouper(groups_config=self.config.get('groups'))

        self.ignore_manager = IgnoreManager(
            root_dir=self.root_dir,
            ignore_file_name=ignore_file_name,
            use_gitignore=use_gitignore,
            extra_exclude_patterns=extra_exclude_patterns,
            output_file=self.output_file
        )
        
        self.cache_manager = CacheManager(project_root=self.root_dir, max_size_mb=cache_size, max_age_days=cache_max_age) if use_cache else None

        self.file_filter = FileFilter(
            root_dir=self.root_dir,
            user_extensions=extensions,
            include_empty=include_empty,
            min_size=min_size,
            max_size=max_size,
            cache_manager=self.cache_manager
        )

        self.scanner = FileScanner(
            root_dir=self.root_dir,
            ignore_manager=self.ignore_manager,
            file_filter=self.file_filter,
            include_dirs=include_dirs,
            cache_manager=self.cache_manager
        )

        self.writer = CodeWriter(
            root_dir=self.root_dir,
            output_file=self.output_file,
            grouper=self.grouper,
            template=template,
            no_grouping=no_grouping,
            to_stdout=to_stdout,
            num_workers=num_workers,
            resume=resume,
            detect_secrets=detect_secrets
        )

    def scan(self) -> t.Tuple[t.List[Path], t.Set[str]]:
        """Scan for files to process."""
        return self.scanner.scan()

    def compile(self) -> bool:
        """Run the full compilation process."""
        files_to_process, final_extensions = self.scan()
        total_files = len(files_to_process)

        if total_files == 0:
            logger.warning("No files found to process. Check ignore rules and extensions.")
            return False

        if self.dry_run:
            # In dry run, we just return True after scanning (caller might want to see files)
            # But CodeWriter handles dry run printing? No, CodeCompiler did.
            # Let's let the caller handle dry run display using the scanned files.
            return True

        return self.writer.write(files_to_process, final_extensions)
