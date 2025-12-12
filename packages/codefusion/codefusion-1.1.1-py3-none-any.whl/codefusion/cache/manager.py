# codefusion/cache/manager.py
import logging
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import platform
import shutil
import threading
import os

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages file metadata caching with proper OS-specific directories,
    size limits, and cache invalidation strategies.
    """
    
    # Cache configuration
    MAX_CACHE_SIZE_MB = 50  # Maximum cache size in MB
    MAX_CACHE_AGE_DAYS = 7  # Auto-cleanup entries older than this
    CACHE_VERSION = "1.0"
    
    def __init__(self, project_root: Optional[Path] = None, max_size_mb: int = 50, max_age_days: int = 7):
        """
        Initialize cache handler with OS-appropriate cache directory.
        
        Args:
            project_root: Optional project root for project-specific caching
            max_size_mb: Maximum cache size in MB (default: 50)
            max_age_days: Maximum cache entry age in days (default: 7)
        """
        self.project_root = project_root or Path.cwd()
        self.max_size_mb = max_size_mb
        self.max_age_days = max_age_days
        
        self.cache_dir = self._get_cache_directory()
        self.cache_file = self._get_cache_file()
        self.lock_file = self.cache_dir / f"cache_{self._get_project_hash()}.lock"
        self.cache: Dict[str, Any] = {}
        self._ensure_cache_directory()
        self._load_cache()
        self.lock = threading.Lock()
    
    def _get_project_hash(self) -> str:
        """
        Get a unique hash for the project root.
        """
        return hashlib.md5(
            str(self.project_root.resolve()).encode()
        ).hexdigest()[:12]

    def _get_cache_directory(self) -> Path:
        """
        Get OS-appropriate cache directory following platform conventions.
        
        Returns:
            Path to cache directory
        """
        system = platform.system()
        
        if system == "Windows":
            # Use AppData\Local for cache data
            base = Path.home() / "AppData" / "Local"
        elif system == "Darwin":  # macOS
            # Use ~/Library/Caches
            base = Path.home() / "Library" / "Caches"
        else:  # Linux and other Unix-like
            # Follow XDG Base Directory specification
            xdg_cache = Path.home() / ".cache"
            base = Path(os.environ.get("XDG_CACHE_HOME", xdg_cache))
        
        return base / "codefusion"
    
    def _get_cache_file(self) -> Path:
        """
        Get cache file path, using project hash for project-specific caching.
        
        Returns:
            Path to cache file
        """
        return self.cache_dir / f"cache_{self._get_project_hash()}.json"
    
    def _ensure_cache_directory(self) -> None:
        """Create cache directory if it doesn't exist."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Cache directory: {self.cache_dir}")
        except Exception as e:
            logger.warning(f"Failed to create cache directory: {e}")
    
    def _acquire_lock(self):
        """Acquire a file-based lock for process-safe cache access."""
        try:
            self.lock_file.touch(exist_ok=False)
            return True
        except FileExistsError:
            return False

    def _release_lock(self):
        """Release the file-based lock."""
        try:
            self.lock_file.unlink()
        except FileNotFoundError:
            pass

    def _load_cache(self) -> None:
        """Load cache from file with version checking and validation."""
        if not self.cache_file.exists():
            logger.debug("No existing cache found")
            self._initialize_cache()
            return
        
        if not self._acquire_lock():
            logger.debug("Could not acquire lock, another process may be writing.")
            return

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Version check
            if data.get('version') != self.CACHE_VERSION:
                logger.info("Cache version mismatch, invalidating cache")
                self._initialize_cache()
                return
            
            # Validate cache structure
            if 'metadata' not in data or 'entries' not in data:
                logger.warning("Invalid cache structure, recreating")
                self._initialize_cache()
                return
            
            self.cache = data
            logger.debug(f"Loaded cache with {len(self.cache['entries'])} entries")
            
            # Cleanup old entries
            self._cleanup_old_entries()
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to load cache, recreating: {e}")
            self._initialize_cache()
        finally:
            self._release_lock()

    def _initialize_cache(self) -> None:
        """Initialize a new cache structure."""
        self.cache = {
            'version': self.CACHE_VERSION,
            'metadata': {
                'created': time.time(),
                'last_cleanup': time.time(),
                'project_root': str(self.project_root.resolve())
            },
            'entries': {}
        }
    
    def _save_cache(self) -> None:
        """Save cache to file with size checking."""
        if not self._acquire_lock():
            logger.debug("Could not acquire lock, another process may be writing.")
            return

        try:
            # Check cache size before saving
            cache_size_mb = self._get_cache_size_mb()
            if cache_size_mb > self.max_size_mb:
                logger.info(f"Cache size ({cache_size_mb:.2f}MB) exceeds limit, cleaning up")
                self._enforce_size_limit()
            
            # Update metadata
            self.cache['metadata']['last_modified'] = time.time()
            
            # Write to temporary file first (atomic write)
            temp_file = self.cache_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2)
            
            # Atomic rename
            temp_file.replace(self.cache_file)
            logger.debug(f"Cache saved: {len(self.cache['entries'])} entries")
            
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
        finally:
            self._release_lock()
    
    def _get_cache_size_mb(self) -> float:
        """Calculate current cache size in MB."""
        if not self.cache_file.exists():
            return 0.0
        return self.cache_file.stat().st_size / (1024 * 1024)
    
    def _cleanup_old_entries(self) -> None:
        """Remove cache entries older than max_age_days."""
        current_time = time.time()
        max_age_seconds = self.max_age_days * 86400
        
        entries = self.cache.get('entries', {})
        
        # Remove old entries
        expired_keys = [
            key for key, data in entries.items()
            if current_time - data.get('cached_at', 0) > max_age_seconds
        ]
        
        for key in expired_keys:
            del entries[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
            self.cache['metadata']['last_cleanup'] = current_time
    
    def _enforce_size_limit(self) -> None:
        """
        Enforce cache size limit by removing least recently used entries.
        Uses LRU (Least Recently Used) eviction strategy.
        """
        entries = self.cache.get('entries', {})
        
        # Sort by last access time (oldest first)
        sorted_entries = sorted(
            entries.items(),
            key=lambda x: x[1].get('last_access', 0)
        )
        
        # Remove oldest 30% of entries
        remove_count = max(1, len(sorted_entries) // 3)
        for key, _ in sorted_entries[:remove_count]:
            del entries[key]
        
        logger.info(f"Removed {remove_count} entries to enforce size limit")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """
        Generate a unique hash for a file based on path and modification time.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hash string
        """
        try:
            stat = file_path.stat()
            content = f"{file_path.resolve()}:{stat.st_mtime}:{stat.st_size}"
            return hashlib.md5(content.encode()).hexdigest()
        except Exception:
            return hashlib.md5(str(file_path.resolve()).encode()).hexdigest()
    
    def get(self, file_path: Path, key: str) -> Optional[Any]:
        """
        Get cached value for a file.
        """
        file_hash = self._get_file_hash(file_path)
        entries = self.cache.get('entries', {})
        
        if file_hash not in entries:
            return None
        
        entry = entries[file_hash]
        
        # Validate entry
        try:
            current_mtime = file_path.stat().st_mtime
            if current_mtime != entry.get('mtime'):
                self.invalidate_file(file_path)
                return None
        except Exception:
            self.invalidate_file(file_path)
            return None
            
        # Update last access
        entry['last_access'] = time.time()
        
        return entry.get('data', {}).get(key)

    def set(self, file_path: Path, key: str, value: Any) -> None:
        """
        Set cached value for a file.
        """
        file_hash = self._get_file_hash(file_path)
        entries = self.cache.get('entries', {})
        
        try:
            stat = file_path.stat()
            
            if file_hash not in entries:
                entries[file_hash] = {
                    'path': str(file_path.relative_to(self.project_root)),
                    'mtime': stat.st_mtime,
                    'size': stat.st_size,
                    'cached_at': time.time(),
                    'last_access': time.time(),
                    'data': {}
                }
            
            if 'data' not in entries[file_hash]:
                entries[file_hash]['data'] = {}
                
            entries[file_hash]['data'][key] = value
            entries[file_hash]['last_access'] = time.time()
            
        except Exception as e:
            logger.debug(f"Failed to cache value for {file_path}: {e}")

    def get_cached_content(self, file_path: Path) -> Optional[str]:
        """
        Get cached content for a file if it exists and is valid.
        """
        file_hash = self._get_file_hash(file_path)
        entries = self.cache.get('entries', {})
        
        if file_hash not in entries:
            return None
            
        entry = entries[file_hash]
        
        # Validate entry
        try:
            current_mtime = file_path.stat().st_mtime
            if current_mtime != entry.get('mtime'):
                self.invalidate_file(file_path)
                return None
        except Exception:
            self.invalidate_file(file_path)
            return None
            
        # Check for sidecar file
        sidecar_path = self.cache_dir / f"{file_hash}.content"
        if sidecar_path.exists():
            try:
                # Update access time
                entry['last_access'] = time.time()
                return sidecar_path.read_text(encoding='utf-8')
            except Exception:
                return None
        
        return None

    def set_cached_content(self, file_path: Path, content: str) -> None:
        """
        Cache content for a file in a sidecar file.
        """
        file_hash = self._get_file_hash(file_path)
        entries = self.cache.get('entries', {})
        
        try:
            stat = file_path.stat()
            
            # Update metadata
            entries[file_hash] = {
                'path': str(file_path.relative_to(self.project_root)),
                'mtime': stat.st_mtime,
                'size': stat.st_size,
                'cached_at': time.time(),
                'last_access': time.time(),
                'has_content': True
            }
            
            # Write sidecar file
            sidecar_path = self.cache_dir / f"{file_hash}.content"
            sidecar_path.write_text(content, encoding='utf-8')
            
        except Exception as e:
            logger.debug(f"Failed to cache content for {file_path}: {e}")

    def invalidate_file(self, file_path: Path) -> None:
        """
        Invalidate cache for a specific file.
        """
        file_hash = self._get_file_hash(file_path)
        entries = self.cache.get('entries', {})
        if file_hash in entries:
            # Delete sidecar if exists
            sidecar_path = self.cache_dir / f"{file_hash}.content"
            if sidecar_path.exists():
                try:
                    sidecar_path.unlink()
                except Exception:
                    pass
            del entries[file_hash]
            logger.debug(f"Invalidated cache for {file_path}")
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._initialize_cache()
        # Delete all content files in cache dir
        try:
            for f in self.cache_dir.glob("*.content"):
                f.unlink()
            if self.cache_file.exists():
                self.cache_file.unlink()
        except Exception as e:
            logger.warning(f"Error clearing cache files: {e}")
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        """
        entries = self.cache.get('entries', {})
        cache_size_mb = self._get_cache_size_mb()
        
        # Count content files
        content_files = len(list(self.cache_dir.glob("*.content")))
        
        return {
            'entry_count': len(entries),
            'content_files': content_files,
            'size_mb': cache_size_mb,
            'cache_dir': str(self.cache_dir),
            'cache_file': str(self.cache_file),
            'max_size_mb': self.max_size_mb,
            'max_age_days': self.max_age_days,
            'created': self.cache.get('metadata', {}).get('created'),
            'last_cleanup': self.cache.get('metadata', {}).get('last_cleanup')
        }
    
    def cleanup(self) -> None:
        """Perform cleanup and save cache."""
        self._cleanup_old_entries()
        self._save_cache()
    
    def _cleanup_old_entries(self) -> None:
        """Remove cache entries older than max_age_days."""
        current_time = time.time()
        max_age_seconds = self.max_age_days * 86400
        
        entries = self.cache.get('entries', {})
        
        # Remove old entries
        expired_keys = [
            key for key, data in entries.items()
            if current_time - data.get('cached_at', 0) > max_age_seconds
        ]
        
        for key in expired_keys:
            # Delete sidecar
            sidecar_path = self.cache_dir / f"{key}.content"
            if sidecar_path.exists():
                try:
                    sidecar_path.unlink()
                except Exception:
                    pass
            del entries[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
            self.cache['metadata']['last_cleanup'] = current_time

    @classmethod
    def clear_all_caches(cls) -> None:
        """
        Clear all CodeFusion caches (useful for troubleshooting).
        This is a class method that can be called without instance.
        """
        cache_dir = cls(None)._get_cache_directory()
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                logger.info(f"Cleared all caches from {cache_dir}")
            except Exception as e:
                logger.error(f"Failed to clear caches: {e}")
