"""Clipboard utilities for copying results."""

from typing import List, Optional

# Try to import pyperclip, but don't fail if not available
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard.
    
    Args:
        text: Text to copy
    
    Returns:
        True if successful, False otherwise
    """
    if not CLIPBOARD_AVAILABLE:
        return False
    
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def copy_results(results: List[str], separator: str = "\n") -> bool:
    """
    Copy results list to clipboard.
    
    Args:
        results: List of results to copy
        separator: Separator between results (default: newline)
    
    Returns:
        True if successful, False otherwise
    """
    text = separator.join(str(r) for r in results)
    return copy_to_clipboard(text)


def is_clipboard_available() -> bool:
    """
    Check if clipboard functionality is available.
    
    Returns:
        True if clipboard is available, False otherwise
    """
    return CLIPBOARD_AVAILABLE


def get_clipboard_status_message() -> str:
    """
    Get status message about clipboard availability.
    
    Returns:
        Status message string
    """
    if CLIPBOARD_AVAILABLE:
        return "Clipboard support enabled"
    else:
        return "Clipboard support unavailable (install pyperclip)"
