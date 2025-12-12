# codefusion/core/reader.py
import logging
from pathlib import Path
import typing as t

logger = logging.getLogger(__name__)

def stream_file_content(file_path: Path, chunk_size: int = 8192) -> t.Generator[str, None, t.Optional[str]]:
    """
    Yields file content in chunks.
    Returns error message if any (as the return value of the generator, which is tricky to catch in loop).
    Better: Yields chunks. If error, yields a special error object or raises exception?
    Let's stick to: Yields strings. If error, logs it and maybe yields a specific error marker or just stops.
    Actually, for the writer, we want to know if it failed.
    
    Let's change signature:
    Yields chunks. If error occurs, yields nothing more.
    Caller should wrap in try/catch or we return a tuple generator?
    
    Simpler approach:
    Generator yields strings.
    If error, raises an exception that caller handles.
    """
    try:
        # Prevent reading excessively large files into memory check is still good but we are streaming now.
        # But if it's 100GB, we might still want to warn? 
        # Let's keep the limit for now or make it configurable? 
        # User asked for streaming large files, so we should REMOVE the hard limit or increase it significantly.
        # Let's remove the hard limit for streaming, but maybe keep a sanity check?
        # No, "Stream large files" implies we support them.
        pass
    except Exception:
        pass

    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']
    
    for encoding in encodings:
        try:
            with file_path.open('r', encoding=encoding) as f:
                # Read first chunk to validate encoding
                chunk = f.read(chunk_size)
                if not chunk:
                    yield ""
                    return

                # Validate content isn't mostly binary (only on first chunk)
                non_printable = sum(1 for c in chunk if ord(c) < 32 and c not in '\t\n\r')
                if len(chunk) > 0 and non_printable / len(chunk) > 0.1:
                    continue # Try next encoding

                yield chunk
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            return # Success
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            logger.warning(f"Error streaming {file_path}: {e}")
            raise e # Re-raise to let caller know
            
    # If all encodings fail
    raise ValueError("Unable to decode file with any supported encoding")

def read_file_content(file_path: Path) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """
    Reads entire file content (legacy support).
    """
    try:
        content_parts = []
        for chunk in stream_file_content(file_path):
            content_parts.append(chunk)
        return "".join(content_parts), None
    except Exception as e:
        return None, str(e)
