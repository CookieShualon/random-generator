"""Input validation utilities for the Textual TUI."""

from typing import Tuple, Optional, Set


def validate_number_range(min_val: str, max_val: str) -> Tuple[bool, Optional[str]]:
    """
    Validate number range inputs.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        min_int = int(min_val)
        max_int = int(max_val)
        
        if min_int >= max_int:
            return False, "Minimum must be less than maximum"
        
        return True, None
    except ValueError:
        return False, "Please enter valid integers"


def validate_float_range(min_val: str, max_val: str) -> Tuple[bool, Optional[str]]:
    """
    Validate float range inputs.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        min_float = float(min_val)
        max_float = float(max_val)
        
        if min_float >= max_float:
            return False, "Minimum must be less than maximum"
        
        return True, None
    except ValueError:
        return False, "Please enter valid numbers"


def validate_count(count: str, max_count: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate count input.
    
    Args:
        count: Count value as string
        max_count: Optional maximum allowed count
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        count_int = int(count)
        
        if count_int < 1:
            return False, "Count must be at least 1"
        
        if max_count and count_int > max_count:
            return False, f"Count cannot exceed {max_count}"
        
        return True, None
    except ValueError:
        return False, "Please enter a valid integer"


def validate_decimals(decimals: str) -> Tuple[bool, Optional[str]]:
    """
    Validate decimal places input.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        dec_int = int(decimals)
        
        if dec_int < 0:
            return False, "Decimal places cannot be negative"
        
        if dec_int > 10:
            return False, "Decimal places cannot exceed 10"
        
        return True, None
    except ValueError:
        return False, "Please enter a valid integer"


def validate_string_length(length: str) -> Tuple[bool, Optional[str]]:
    """
    Validate string length input.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        length_int = int(length)
        
        if length_int < 1:
            return False, "Length must be at least 1"
        
        if length_int > 1000:
            return False, "Length cannot exceed 1000"
        
        return True, None
    except ValueError:
        return False, "Please enter a valid integer"


def parse_exclude_numbers(exclude_str: str) -> Tuple[bool, Optional[Set[int]], Optional[str]]:
    """
    Parse and validate excluded numbers string.
    
    Args:
        exclude_str: Comma-separated numbers to exclude
    
    Returns:
        Tuple of (is_valid, excluded_set, error_message)
    """
    if not exclude_str.strip():
        return True, set(), None
    
    try:
        excluded = set()
        for item in exclude_str.split(','):
            item = item.strip()
            if item:
                excluded.add(int(item))
        return True, excluded, None
    except ValueError:
        return False, None, "Invalid number in exclusion list"


def validate_template(template: str) -> Tuple[bool, Optional[str]]:
    """
    Validate custom template string.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not template.strip():
        return False, "Template cannot be empty"
    
    # Check if template contains at least one placeholder
    valid_placeholders = ['{d}', '{l}', '{u}', '{a}', '{x}', '{s}', '{w}']
    has_placeholder = any(ph in template for ph in valid_placeholders)
    
    if not has_placeholder:
        return False, "Template must contain at least one placeholder"
    
    return True, None


def validate_list_items(items_str: str) -> Tuple[bool, Optional[list], Optional[str]]:
    """
    Parse and validate list items string.
    
    Args:
        items_str: Comma-separated or newline-separated items
    
    Returns:
        Tuple of (is_valid, items_list, error_message)
    """
    if not items_str.strip():
        return False, None, "Please enter at least one item"
    
    # Try newline-separated first, then comma-separated
    if '\n' in items_str:
        items = [line.strip() for line in items_str.split('\n') if line.strip()]
    else:
        items = [item.strip() for item in items_str.split(',') if item.strip()]
    
    if len(items) < 1:
        return False, None, "Please enter at least one item"
    
    return True, items, None


def validate_unique_count(count: int, available: int) -> Tuple[bool, Optional[str]]:
    """
    Validate count for unique selection.
    
    Args:
        count: Number of items to select
        available: Number of available items
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if count > available:
        return False, f"Cannot select {count} unique items from {available} items"
    
    return True, None


def validate_number_generation(min_val: int, max_val: int, exclude: Set[int], count: int) -> Tuple[bool, Optional[str]]:
    """
    Validate complete number generation parameters.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    total_range = max_val - min_val + 1
    excluded_in_range = sum(1 for x in exclude if min_val <= x <= max_val)
    available = total_range - excluded_in_range
    
    if available < count:
        return False, f"Not enough numbers available. Need {count}, have {available}"
    
    return True, None
