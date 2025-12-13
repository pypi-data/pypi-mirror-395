"""
Formatting utilities for market data.
"""

def format_float_as_clean_str(val: float, decimals: int = 3, strip_zeros: bool = True) -> str:
    """
    Format float to string with smart cleanup for ID generation.
    
    Args:
        val: The float value to format.
        decimals: Number of decimal places to use.
        strip_zeros: If True, removes trailing zeros and decimal point (e.g. "2.00" -> "2").
                     If False, keeps fixed precision (e.g. "2.00").
    
    Logic:
    1. Format to fixed precision (e.g., 3 decimals: 2.0 -> "2.000", 0.5 -> "0.500")
    2. If strip_zeros is True:
       - Strip trailing zeros (e.g., "2.000" -> "2.", "0.500" -> "0.5")
       - Strip trailing decimal point if it's now an integer (e.g., "2." -> "2")
    
    Why:
    - We want IDs to be human-readable and "clean".
    - "split__2_1" is better than "split__2.000000_1.000000".
    - "dividend__0.5" is better than "dividend__0.5000".
    - Yet we preserve necessary precision for non-integers (e.g. "split__1.5_1").
    """
    formatted = f"{val:.{decimals}f}"
    if strip_zeros:
        return formatted.rstrip('0').rstrip('.')
    return formatted
