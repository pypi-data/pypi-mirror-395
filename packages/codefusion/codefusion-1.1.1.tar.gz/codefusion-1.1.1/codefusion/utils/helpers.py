# codefusion/utils/helpers.py

def ensure_leading_dot(ext: str) -> str:
    """Ensure the extension starts with a dot."""
    if not ext:
        return ""
    return '.' + ext.strip().lower().lstrip('.')

def format_size(size: int) -> str:
    """Format size in bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            if unit == 'B':
                return f"{size} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"
