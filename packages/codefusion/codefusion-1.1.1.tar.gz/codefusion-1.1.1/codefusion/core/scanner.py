# codefusion/core/scanner.py
import logging
from pathlib import Path
import typing as t
import os
from concurrent.futures import ThreadPoolExecutor

from .filter import FileFilter
from ..ignore.manager import IgnoreManager
from ..cache.manager import CacheManager

logger = logging.getLogger(__name__)

class FileScanner:
    def __init__(self, root_dir: Path, ignore_manager: IgnoreManager,
                 file_filter: FileFilter, include_dirs: t.Optional[t.List[str]] = None,
                 cache_manager: t.Optional[CacheManager] = None):
        self.root_dir = root_dir
        self.ignore_manager = ignore_manager
        self.file_filter = file_filter
        self.include_dirs = include_dirs
        self.cache_manager = cache_manager
        self.detected_extensions: t.Set[str] = set()

    def scan(self) -> t.Tuple[t.List[Path], t.Set[str]]:
        """
        Enhanced file collection with parallel processing and proper caching.
        """
        logger.info("Scanning directory and applying ignore rules...")
        candidate_files: t.List[Path] = []

        # Determine start directories
        search_dirs = []
        if self.include_dirs:
            for inc_dir in self.include_dirs:
                current_dir = (self.root_dir / inc_dir).resolve()
                if current_dir.is_dir():
                    search_dirs.append(current_dir)
                else:
                    logger.warning(f"Directory not found: {current_dir}")
        else:
            search_dirs.append(self.root_dir)

        # Parallel Scanning
        with ThreadPoolExecutor() as executor:
            # We start a future for each search directory
            futures = [executor.submit(self._scan_dir, d) for d in search_dirs]
            
            import concurrent.futures
            while futures:
                # Wait for the first future to complete
                done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                futures = list(not_done)
                
                for future in done:
                    try:
                        files, subdirs = future.result()
                        candidate_files.extend(files)
                        # Submit new tasks for subdirectories
                        for subdir in subdirs:
                            futures.append(executor.submit(self._scan_dir, subdir))
                    except Exception as e:
                        logger.error(f"Error during scan: {e}")

        logger.info(f"Found {len(candidate_files)} candidate files after ignore rules.")

        # Filter text files (with parallel processing if we have many files)
        if len(candidate_files) > 100:
            text_files = self.file_filter.filter_text_files_parallel(candidate_files)
        else:
            text_files = self.file_filter.filter_text_files_sequential(candidate_files)
        
        logger.info(f"Found {len(text_files)} text files after binary filtering.")

        # Handle extensions
        if self.file_filter.user_extensions:
            target_extensions = self.file_filter.expand_extensions(self.file_filter.user_extensions)
            files_to_process = self.file_filter.filter_by_extensions(text_files, target_extensions)
        else:
            files_to_process = []
            for f in text_files:
                if self.file_filter.should_include_file(f):
                    files_to_process.append(f)
                    if f.suffix:
                        self.detected_extensions.add(f.suffix.lower())
                    else:
                        self.detected_extensions.add('[no extension]')
            target_extensions = self.detected_extensions

        logger.info(f"Final file count: {len(files_to_process)}")
        
        # Cleanup cache
        if self.cache_manager:
            self.cache_manager.cleanup()
            final_stats = self.cache_manager.get_stats()
            logger.debug(f"Cache cleanup: {final_stats['entry_count']} entries remaining, "
                        f"{final_stats['size_mb']:.2f}MB")
        
        return files_to_process, target_extensions

    def _scan_dir(self, directory: Path) -> t.Tuple[t.List[Path], t.List[Path]]:
        """
        Scans a single directory using os.scandir for efficiency.
        Returns (files, subdirectories).
        Checks ignore rules IMMEDIATELY.
        """
        files = []
        subdirs = []
        
        try:
            # Check if the directory itself is ignored before scanning
            if self.ignore_manager.is_excluded(directory):
                return [], []

            with os.scandir(directory) as it:
                for entry in it:
                    path = Path(entry.path)
                    
                    # Check ignore rules for this entry
                    if self.ignore_manager.is_excluded(path):
                        continue
                        
                    if entry.is_file():
                        files.append(path)
                    elif entry.is_dir():
                        subdirs.append(path)
        except PermissionError:
            logger.warning(f"Permission denied: {directory}")
        except OSError as e:
            logger.warning(f"Error scanning {directory}: {e}")
            
        return files, subdirs
