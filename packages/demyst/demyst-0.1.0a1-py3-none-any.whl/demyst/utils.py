import logging
import sys

logger = logging.getLogger("demyst")


def safe_read_file(path: str) -> str:
    """Safely read a file with proper error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with latin-1 as fallback
        logger.debug(f"UTF-8 decode failed for {path}, trying latin-1")
        with open(path, "r", encoding="latin-1") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {path}")
    except IsADirectoryError:
        raise IsADirectoryError(f"Expected a file, got a directory: {path}")
