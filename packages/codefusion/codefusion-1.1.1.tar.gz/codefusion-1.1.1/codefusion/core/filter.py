# codefusion/core/filter.py
import logging
from pathlib import Path
import typing as t
from concurrent.futures import ThreadPoolExecutor, as_completed

from .detector import is_binary_file, is_text_file_without_extension
# from ..utils.helpers import ensure_leading_dot  # Removed, handled at input boundary
from ..cache.manager import CacheManager

logger = logging.getLogger(__name__)

class FileFilter:
    def __init__(self, root_dir: Path, 
                 user_extensions: t.Optional[t.Set[str]] = None,
                 include_empty: bool = False,
                 min_size: int = 0,
                 max_size: t.Optional[int] = None,
                 cache_manager: t.Optional[CacheManager] = None):
        self.root_dir = root_dir
        self.user_extensions = user_extensions
        self.include_empty = include_empty
        self.min_size = min_size
        self.max_size = max_size
        self.cache = cache_manager

    def check_if_text(self, file_path: Path) -> t.Tuple[bool, bool]:
        """Check if a file is text, using cache if available. Returns (is_text, was_cached)."""
        is_text = None
        was_cached = False

        if self.cache:
            is_text = self.cache.get(file_path, 'is_text')
            if is_text is not None:
                was_cached = True

        if is_text is None:
            is_text = not is_binary_file(file_path)
            if not is_text and not file_path.suffix:
                is_text = is_text_file_without_extension(file_path)
            
            if self.cache:
                self.cache.set(file_path, 'is_text', is_text)

        return is_text, was_cached

    def filter_text_files_sequential(self, files: t.List[Path]) -> t.List[Path]:
        """Filter out binary files sequentially (for smaller file lists)."""
        text_files = []
        cache_hits = 0
        cache_misses = 0
        
        for file_path in files:
            try:
                is_text, was_cached = self.check_if_text(file_path)
                if was_cached:
                    cache_hits += 1
                else:
                    cache_misses += 1

                if is_text:
                    text_files.append(file_path)
                    
            except Exception as e:
                logger.debug(f"Error processing file {file_path}: {e}")
                continue
        
        if self.cache and (cache_hits + cache_misses) > 0:
            hit_rate = (cache_hits / (cache_hits + cache_misses)) * 100
            logger.debug(f"Cache hit rate: {hit_rate:.1f}% ({cache_hits}/{cache_hits + cache_misses})")
        
        return text_files

    def filter_text_files_parallel(self, files: t.List[Path]) -> t.List[Path]:
        """Filter out binary files using parallel processing."""
        text_files = []
        cache_hits = 0
        cache_misses = 0
        
        def check_file_wrapper(file_path: Path) -> t.Tuple[Path, bool, bool]:
            """Wrapper for parallel execution."""
            try:
                is_text, was_cached = self.check_if_text(file_path)
                return file_path, is_text, was_cached
            except Exception as e:
                logger.debug(f"Error checking file {file_path}: {e}")
                return file_path, False, False

        # Use parallel processing for binary detection
        max_workers = min(8, len(files), 4)  # Limit concurrent file operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(check_file_wrapper, f): f for f in files}
            
            for future in as_completed(future_to_file):
                try:
                    file_path, is_text, was_cached = future.result()
                    
                    if was_cached:
                        cache_hits += 1
                    else:
                        cache_misses += 1
                    
                    if is_text:
                        text_files.append(file_path)
                except Exception as e:
                    logger.debug(f"Error in parallel file processing: {e}")
                    continue
        
        if cache_hits + cache_misses > 0:
            hit_rate = (cache_hits / (cache_hits + cache_misses)) * 100
            logger.debug(f"Cache hit rate: {hit_rate:.1f}% ({cache_hits}/{cache_hits + cache_misses})")
        
        return text_files

    def expand_extensions(self, extensions: t.Set[str]) -> t.Set[str]:
        """Expand extensions with common variants."""
        expanded = set()
        from ..utils.helpers import ensure_leading_dot
        
        for ext in extensions:
            # Extensions are already normalized at input boundary
            ext = ensure_leading_dot(ext)
            ext_lower = ext.lower()
            expanded.add(ext_lower)
            # Add common variants
            if ext_lower == '.yml':
                expanded.add('.yaml')
            elif ext_lower == '.yaml':
                expanded.add('.yml')
            elif ext_lower == '.js':
                expanded.add('.mjs')
                expanded.add('.jsx')
            elif ext_lower == '.ts':
                expanded.add('.tsx')
        return expanded

    def filter_by_extensions(self, files: t.List[Path], extensions: t.Set[str]) -> t.List[Path]:
        """Filter files by extensions."""
        filtered = []
        for f in files:
            if f.suffix.lower() in extensions or ('*' in extensions and not f.suffix):
                if self.should_include_file(f):
                    filtered.append(f)
        return filtered

    def should_include_file(self, f: Path) -> bool:
        """Enhanced file inclusion check."""
        try:
            file_size = f.stat().st_size
            
            # Check empty files
            if not self.include_empty and file_size == 0:
                logger.debug(f"Skipping empty file: {f.relative_to(self.root_dir)}")
                return False
            
            # Check size limits
            if file_size < self.min_size:
                logger.debug(f"Skipping file {f.relative_to(self.root_dir)} (too small: {file_size} bytes)")
                return False
            
            if self.max_size and file_size > self.max_size:
                logger.debug(f"Skipping file {f.relative_to(self.root_dir)} (too large: {file_size} bytes)")
                return False
            
            return True
        except Exception as e:
            logger.warning(f"Error checking file {f}: {e}")
            return False
