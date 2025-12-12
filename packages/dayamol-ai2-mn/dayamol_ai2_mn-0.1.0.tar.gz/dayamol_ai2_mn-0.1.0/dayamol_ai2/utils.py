"""
utils.py – Utility functions for cleaning and formatting AI output.
"""

import re

def format_response(text: str) -> str:
    """
    Clean and format AI output by removing extra whitespace.

    Args:
        text (str): Text to format.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
