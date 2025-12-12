# codefusion/utils/logging.py
import logging
import sys
import typing as t

try:
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def setup_logging(verbose: bool):
    log_level = logging.DEBUG if verbose else logging.INFO
    
    if RICH_AVAILABLE:
        logging.basicConfig(
            level=log_level,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, show_path=verbose)]
        )
    else:
        # Fallback to basic logging if rich is not available
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()
        root_logger.addHandler(handler)

    logger = logging.getLogger(__name__)
    logger.info("Verbose mode enabled." if verbose else "Standard logging.")
