"""
Interface module for spreadsheet operations.

This module contains high-level interface functions for spreadsheet operations
like fill, copy-paste, and other interactive features.
"""

from .apply_fill import apply_fill, ApplyFillConfig
from .fill import (
    get_auto_fill_values,
    detect_fill_type,
    generate_fill_values,
    AutoFillType,
)

__all__ = [
    'apply_fill',
    'ApplyFillConfig',
    'get_auto_fill_values',
    'detect_fill_type',
    'generate_fill_values',
    'AutoFillType',
]
