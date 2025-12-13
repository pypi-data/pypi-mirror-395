# -*- encoding: utf-8 -*-
"""
Color constants and utilities for ColorInfo logging system.
"""

class ColorConstants:
    """ANSI color codes for terminal output formatting."""
    
    # Basic colors
    RED = "\033[31m"      # Red
    GREEN = "\033[32m"    # Green  
    YELLOW = '\033[33m'   # Yellow
    BLUE = '\033[34m'    # Blue
    RESET_ALL = '\033[0m' # Reset all formatting
    
    # Additional colors for future extension
    MAGENTA = "\033[35m"  # Magenta
    CYAN = "\033[36m"     # Cyan
    WHITE = "\033[37m"    # White
    BLACK = "\033[30m"    # Black
    
    # Bright variants
    BRIGHT_RED = "\033[91m"     # Bright Red
    BRIGHT_GREEN = "\033[92m"   # Bright Green
    BRIGHT_YELLOW = "\033[93m"  # Bright Yellow
    BRIGHT_BLUE = "\033[94m"    # Bright Blue
    BRIGHT_MAGENTA = "\033[95m" # Bright Magenta
    BRIGHT_CYAN = "\033[96m"    # Bright Cyan
    BRIGHT_WHITE = "\033[97m"   # Bright White
    
    # Background colors
    BG_RED = "\033[41m"     # Red background
    BG_GREEN = "\033[42m"   # Green background
    BG_YELLOW = "\033[43m"  # Yellow background
    BG_BLUE = "\033[44m"   # Blue background
    BG_RESET = "\033[49m"  # Reset background