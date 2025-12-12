"""
Utility functions for DataStory
"""

from datetime import datetime
from typing import Any, Union


def format_number(number: Union[int, float], precision: int = 2) -> str:
    """
    Format numbers for readability.
    
    Args:
        number: Number to format
        precision: Decimal precision
    
    Returns:
        str: Formatted number string
    
    Example:
        >>> format_number(1234567)
        '1.23M'
        >>> format_number(1234)
        '1.23K'
    """
    if number is None or (isinstance(number, float) and number != number):  # NaN check
        return "N/A"
    
    abs_num = abs(number)
    
    if abs_num >= 1_000_000_000:
        return f"{number / 1_000_000_000:.{precision}f}B"
    elif abs_num >= 1_000_000:
        return f"{number / 1_000_000:.{precision}f}M"
    elif abs_num >= 1_000:
        return f"{number / 1_000:.{precision}f}K"
    else:
        return f"{number:.{precision}f}"


def format_percentage(value: Union[int, float], precision: int = 1) -> str:
    """
    Format percentage values.
    
    Args:
        value: Percentage value
        precision: Decimal precision
    
    Returns:
        str: Formatted percentage string
    
    Example:
        >>> format_percentage(45.678)
        '45.7%'
    """
    if value is None or (isinstance(value, float) and value != value):
        return "N/A"
    
    return f"{value:.{precision}f}%"


def format_date(date_value: Any, format_str: str = "%B %d, %Y") -> str:
    """
    Format date values.
    
    Args:
        date_value: Date value (datetime, string, or timestamp)
        format_str: Output format string
    
    Returns:
        str: Formatted date string
    
    Example:
        >>> format_date(datetime(2025, 12, 3))
        'December 03, 2025'
    """
    if date_value is None:
        return "N/A"
    
    try:
        if isinstance(date_value, datetime):
            return date_value.strftime(format_str)
        elif isinstance(date_value, str):
            # Try to parse string
            import pandas as pd
            date_obj = pd.to_datetime(date_value)
            return date_obj.strftime(format_str)
        else:
            return str(date_value)
    except:
        return str(date_value)


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], 
                default: Union[int, float] = 0) -> float:
    """
    Safely divide two numbers, handling zero division.
    
    Args:
        numerator: Top number
        denominator: Bottom number
        default: Default value if division fails
    
    Returns:
        float: Division result or default
    
    Example:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0, default=0)
        0
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Return singular or plural form based on count.
    
    Args:
        count: Number of items
        singular: Singular form
        plural: Plural form (defaults to singular + 's')
    
    Returns:
        str: Appropriate form
    
    Example:
        >>> pluralize(1, 'item')
        'item'
        >>> pluralize(5, 'item')
        'items'
    """
    if plural is None:
        plural = singular + 's'
    
    return singular if count == 1 else plural


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        str: Truncated text
    
    Example:
        >>> truncate_text("This is a very long text", 10)
        'This is...'
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_column_name(column_name: str) -> str:
    """
    Clean column name for display.
    
    Args:
        column_name: Raw column name
    
    Returns:
        str: Cleaned, title-cased column name
    
    Example:
        >>> clean_column_name('total_sales_amount')
        'Total Sales Amount'
    """
    # Replace underscores and hyphens with spaces
    cleaned = column_name.replace('_', ' ').replace('-', ' ')
    
    # Title case
    cleaned = cleaned.title()
    
    return cleaned


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
    
    Returns:
        float: Percentage change
    
    Example:
        >>> calculate_percentage_change(100, 150)
        50.0
    """
    if old_value == 0:
        return 0 if new_value == 0 else float('inf')
    
    return ((new_value - old_value) / abs(old_value)) * 100
