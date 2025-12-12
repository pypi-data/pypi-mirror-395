# codefusion/core/detector.py
import logging
from pathlib import Path
import mimetypes
from ..utils.constants import BINARY_EXTENSIONS, EXTENSIONLESS_TEXT_FILES

logger = logging.getLogger(__name__)

# Try to import python-magic for better binary detection
try:
    import magic
    MAGIC_AVAILABLE = True
    logger.debug("python-magic is available for enhanced binary detection")
except (ImportError, OSError, Exception) as e:
    MAGIC_AVAILABLE = False
    magic = None
    logger.debug(f"python-magic not available, using fallback binary detection: {e}")

def is_binary_file(file_path: Path, use_magic: bool = True) -> bool:
    """Optimized binary file detection with multiple methods."""
    # Quick check by extension first
    if file_path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    
    # Use python-magic if available and requested
    if MAGIC_AVAILABLE and use_magic:
        # User requested magic, but we are disabling it by default to avoid Windows issues
        # unless explicitly enabled or we want to keep the logic but make it safe.
        # The user asked to "Replace python-magic... or strictly rely on the 'content sampling' fallback"
        # So we will skip magic block or just rely on fallback.
        pass 
        # try:
        #     mime = magic.from_file(str(file_path), mime=True)
        #     return not mime.startswith('text/')
        # except Exception as e:
        #     logger.debug(f"python-magic failed for {file_path}, falling back to content sampling: {e}")
    
    # Optimized content sampling method
    try:
        with open(file_path, 'rb') as f:
            # First, check a smaller chunk for a quick decision
            chunk = f.read(1024)
            if not chunk:
                return False  # Empty file is not binary
            if b'\0' in chunk:
                return True  # Null byte is a strong indicator of a binary file

            # If no null byte, check a larger chunk for non-printable characters
            f.seek(0)
            chunk = f.read(8192)
            
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
            non_text = sum(1 for byte in chunk if byte not in text_chars)
            
            # If more than 30% of the file is non-text, it's likely binary
            return (non_text / len(chunk)) > 0.30

    except Exception as e:
        logger.debug(f"Error reading file {file_path} for binary detection: {e}")
        return True  # Assume binary if can't read
    
    return False

def is_text_file_without_extension(file_path: Path) -> bool:
    """Enhanced detection for extensionless text files."""
    if file_path.suffix:
        return False
    
    file_name_lower = file_path.name.lower()
    
    # Check against known text file names
    if file_name_lower in EXTENSIONLESS_TEXT_FILES:
        return True
    
    # Check common prefixes
    text_prefixes = [
        'dockerfile', '.env', '.git', '.docker', 'makefile',
        'rakefile', 'procfile', 'gemfile', 'vagrantfile'
    ]
    if any(file_name_lower.startswith(prefix) for prefix in text_prefixes):
        return True
    
    # MIME type detection using built-in mimetypes
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type and mime_type.startswith('text/'):
        return True
    
    # Content-based detection (don't use magic here to avoid issues)
    return not is_binary_file(file_path, use_magic=False)
