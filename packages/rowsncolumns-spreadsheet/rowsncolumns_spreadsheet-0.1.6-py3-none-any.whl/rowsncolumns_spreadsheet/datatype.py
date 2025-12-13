"""
Datatype detection and pattern matching for cell values.

This module provides comprehensive value type detection, number format pattern
detection, and value conversion utilities similar to the TypeScript implementation.
"""

import re
from typing import Optional, Tuple, Union, Any
from datetime import datetime, date

from .types import ExtendedValue, ErrorValue


# Pattern constants
PATTERN_PERCENT = "0%"
PATTERN_PERCENT_DECIMAL = "0.00%"
PATTERN_CURRENCY = '"$"#,##0'
PATTERN_CURRENCY_DECIMAL = '"$"#,##0.00'
DATE_PATTERN = "mm/dd/yyyy"
TIME_PATTERN_BASE = "hh:mm:ss"
TIME_PATTERN = "hh:mm:ss AM/PM"
TIME_PATTERN_SHORT = "h:mm AM/PM"
PATTERN_NUMBER = "#"
PATTERN_NUMBER_THOUSANDS = "#,##0"

# Pre-compile regular expressions for performance
CURRENCY_PATTERN = re.compile(
    r'^[£$€¥₹]'
    r'\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{1,2})?$|'
    r'^\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{1,2})?[£$€¥₹]$'
)
NUMBER_CLEANUP_PATTERN = re.compile(r'[$,%]')
NUMBER_CONVERSION_PATTERN = re.compile(r'[^0-9.-]+')
URL_PATTERN = re.compile(
    r'^(https?://)?(localhost|([\da-z\.-]+)\.([a-z\.]{2,6}))(:\d+)?(/[/\w \.-]*)*(\?[^\s]*)?$',
    re.IGNORECASE
)
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Decimal patterns
DECIMAL_CLEANUP_REGEX = re.compile(r'[^0-9.,]')
DECIMAL_SPLIT_REGEX = re.compile(r'[.]')
DECIMAL_REGEX = re.compile(r'(?P<prefix>[\d#,]+)(?P<decimal>\.)?(?P<suffix>\d{1,})?', re.IGNORECASE)
THOUSAND_REGEX = re.compile(r'(\,[#,0]{3})', re.IGNORECASE)
PATTERN_SEPARATOR = ";"
THOUSAND_PATTERN = ",##0"

# Time regex patterns
TIME_REGEX_FULL_WITH_MERIDIAN = re.compile(r'^(\d{1,2}):(\d{1,2}):(\d{1,2})\s*(AM|PM|a|p)$', re.IGNORECASE)
TIME_REGEX_FULL = re.compile(r'^(\d{1,2}):(\d{1,2}):(\d{1,2})$')
TIME_REGEX_SHORT_WITH_MERIDIAN = re.compile(r'^(\d{1,2}):(\d{1,2})\s*(AM|PM)$', re.IGNORECASE)
TIME_REGEX_SHORT = re.compile(r'^(\d{1,2}):(\d{1,2})$')

# Cache common values
TRUE_UPPER = "TRUE"
FALSE_UPPER = "FALSE"
PERCENT_CHAR = "%"


def is_currency(value: Union[str, int, float, bool, None]) -> bool:
    """
    Check if value is currency format.

    Args:
        value: Value to check

    Returns:
        True if value matches currency pattern

    Examples:
        >>> is_currency("$100")
        True
        >>> is_currency("100€")
        True
        >>> is_currency("100")
        False
    """
    if value is None:
        return False

    text = str(value).strip()
    return bool(CURRENCY_PATTERN.match(text))


def is_boolean(value: Any) -> bool:
    """
    Check if value is boolean.

    Args:
        value: Value to check

    Returns:
        True if value is boolean or "TRUE"/"FALSE" string

    Examples:
        >>> is_boolean(True)
        True
        >>> is_boolean("TRUE")
        True
        >>> is_boolean("false")
        True
    """
    if isinstance(value, bool):
        return True

    if not isinstance(value, (str, int, float)):
        return False

    upper_value = str(value).upper()
    return upper_value in (TRUE_UPPER, FALSE_UPPER)


def is_percentage(value: Union[str, int, float, bool, None]) -> bool:
    """
    Check if value is percentage.

    Args:
        value: Value to check

    Returns:
        True if value ends or starts with %

    Examples:
        >>> is_percentage("50%")
        True
        >>> is_percentage("%50")
        True
        >>> is_percentage("50")
        False
    """
    if value is None:
        return False

    str_value = str(value).strip()
    return str_value.endswith(PERCENT_CHAR) or str_value.startswith(PERCENT_CHAR)


def clean_number_value(value: Union[str, int, float, bool, None]) -> str:
    """
    Clean number value by removing currency and percent symbols.

    Args:
        value: Value to clean

    Returns:
        Cleaned string

    Examples:
        >>> clean_number_value("$100")
        '100'
        >>> clean_number_value("50%")
        '50'
    """
    if isinstance(value, (int, float)):
        return str(value)

    if value is None:
        return ""

    return NUMBER_CLEANUP_PATTERN.sub('', str(value))


def convert_to_number(value: Union[str, int, float, bool, date, None]) -> Optional[float]:
    """
    Convert value to number.

    Args:
        value: Value to convert

    Returns:
        Number or None if conversion fails

    Examples:
        >>> convert_to_number("$100.50")
        100.5
        >>> convert_to_number("50%")
        50.0
    """
    if isinstance(value, (int, float)):
        return float(value)

    if value is None:
        return None

    try:
        cleaned = NUMBER_CONVERSION_PATTERN.sub('', str(value))
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def is_number(value: Any) -> bool:
    """
    Check if value is a number.

    Args:
        value: Value to check

    Returns:
        True if value can be converted to number

    Examples:
        >>> is_number("100")
        True
        >>> is_number("$100.50")
        True
        >>> is_number("abc")
        False
    """
    sanitized = clean_number_value(value)
    if not sanitized:
        return False

    try:
        float(sanitized)
        return True
    except (ValueError, TypeError):
        return False


def is_formula(value: Any) -> bool:
    """
    Check if value is a formula.

    Args:
        value: Value to check

    Returns:
        True if value starts with = or +

    Examples:
        >>> is_formula("=SUM(A1:A10)")
        True
        >>> is_formula("+A1+B1")
        True
    """
    if not isinstance(value, str):
        return False

    value_str = value.strip()
    return value_str.startswith('=') or value_str.startswith('+')


def get_decimal_places(value: str) -> int:
    """
    Get the number of decimal places in a string.

    Args:
        value: String value to check

    Returns:
        Number of decimal places

    Examples:
        >>> get_decimal_places("123.45")
        2
        >>> get_decimal_places("100")
        0
    """
    # Remove non-digit characters except decimal separators
    cleaned_value = DECIMAL_CLEANUP_REGEX.sub('', value)

    # Split by decimal separator
    parts = DECIMAL_SPLIT_REGEX.split(cleaned_value)

    if len(parts) == 1:
        return 0

    # Get the last part after decimal separator
    decimal_part = parts[-1]
    return len(decimal_part)


def detect_decimal_pattern(
    value: Union[str, int, float, bool, date, None],
    default_pattern: str = PATTERN_NUMBER
) -> str:
    """
    Detect decimal pattern for a number value.

    Args:
        value: Value to analyze
        default_pattern: Default pattern to use

    Returns:
        Number format pattern

    Examples:
        >>> detect_decimal_pattern("1,234.56")
        '#,##0.00'
        >>> detect_decimal_pattern("123.456")
        '#.000'
    """
    if value in ("0", 0):
        return "General"

    str_value = str(value)
    has_thousands = ',' in str_value
    decimals_len = get_decimal_places(str_value)

    # Check if number is less than 1 (needs leading zero)
    num_value = convert_to_number(value)
    needs_leading_zero = num_value is not None and abs(num_value) < 1 and num_value != 0

    prefix = PATTERN_NUMBER_THOUSANDS if has_thousands else default_pattern

    if decimals_len != 0:
        # For decimal numbers less than 1, use "0" pattern to show leading zero
        if needs_leading_zero and prefix == PATTERN_NUMBER:
            prefix = "0"
        return change_decimals(prefix, decimals_len, set_to_value=True)

    return prefix


def create_zeros(length: int) -> str:
    """
    Create string of zeros.

    Args:
        length: Number of zeros

    Returns:
        String of zeros

    Examples:
        >>> create_zeros(3)
        '000'
    """
    return '0' * length


def change_decimals(
    pattern: Optional[str] = "",
    change_by: int = 1,
    delta: bool = True,
    set_to_value: bool = False
) -> str:
    """
    Change decimal places in a number format pattern.

    Args:
        pattern: Current pattern
        change_by: Amount to change by (or set to if set_to_value=True)
        delta: If True, change by delta; if False, set to exact value
        set_to_value: If True, set to exact value instead of changing

    Returns:
        Updated pattern

    Examples:
        >>> change_decimals("#", 2, set_to_value=True)
        '#.00'
        >>> change_decimals("#.00", 1, delta=True)
        '#.000'
    """
    if not pattern:
        pattern = ""

    patterns = pattern.split(PATTERN_SEPARATOR)
    result_patterns = []

    for p in patterns:
        match = DECIMAL_REGEX.search(p)

        if match:
            groups = match.groupdict()
            decimal = groups.get('decimal')
            suffix = groups.get('suffix')

            # No decimal point
            if not decimal:
                new_decimals = max(change_by, 0) if set_to_value else max(change_by, 0)
                zeros = create_zeros(new_decimals)
                if zeros:
                    result_patterns.append(DECIMAL_REGEX.sub(r'\g<prefix>.' + zeros, p))
                else:
                    result_patterns.append(p)
                continue

            # Has decimal point
            new_suffix = 0
            if suffix:
                if set_to_value or not delta:
                    new_suffix = max(change_by, 0)
                else:
                    new_suffix = max(len(suffix) + change_by, 0)
            else:
                new_suffix = max(change_by, 0)

            zeros = create_zeros(new_suffix)
            if zeros:
                result_patterns.append(DECIMAL_REGEX.sub(r'\g<prefix>.' + zeros, p))
            else:
                result_patterns.append(DECIMAL_REGEX.sub(r'\g<prefix>', p))
        elif not p:
            # Empty pattern
            new_decimals = max(change_by, 0)
            zeros = create_zeros(new_decimals)
            result_patterns.append(f"0{('.' + zeros) if zeros else ''}")
        else:
            result_patterns.append(p)

    return PATTERN_SEPARATOR.join(result_patterns)


def is_valid_url_or_email(value: str) -> bool:
    """
    Check if string is a valid URL or email.

    Args:
        value: String to check

    Returns:
        True if valid URL or email

    Examples:
        >>> is_valid_url_or_email("https://example.com")
        True
        >>> is_valid_url_or_email("user@example.com")
        True
    """
    if not value or not isinstance(value, str):
        return False

    # Quick check for email
    if '@' in value:
        return bool(EMAIL_PATTERN.match(value))

    # Quick check for URL
    if '://' in value:
        return bool(URL_PATTERN.match(value))

    return bool(URL_PATTERN.match(value) or EMAIL_PATTERN.match(value))


def is_multiline(value: Any) -> bool:
    """
    Check if string contains newlines.

    Args:
        value: Value to check

    Returns:
        True if contains newline

    Examples:
        >>> is_multiline("Line 1\\nLine 2")
        True
    """
    return '\n' in str(value)


# Simplified date validation (Python doesn't have the complex date-parser)
def is_valid_date(value: Union[str, int, float, bool, date, None], locale: Optional[str] = None) -> bool:
    """
    Check if value is a valid date.

    This is a simplified implementation. The full TypeScript version uses
    a complex date parser library.

    Args:
        value: Value to check
        locale: Locale for parsing (not used in this simplified version)

    Returns:
        True if value appears to be a date
    """
    if not isinstance(value, str):
        return False

    # Simple date patterns
    date_patterns = [
        r'^\d{1,2}/\d{1,2}/\d{2,4}$',  # MM/DD/YYYY or M/D/YY
        r'^\d{4}-\d{2}-\d{2}$',         # YYYY-MM-DD
        r'^\d{1,2}-\d{1,2}-\d{2,4}$',  # MM-DD-YYYY
    ]

    for pattern in date_patterns:
        if re.match(pattern, value.strip()):
            return True

    return False


def is_valid_date_time(value: Union[str, int, float, bool, date, None]) -> bool:
    """
    Check if value is a valid date/time.

    Args:
        value: Value to check

    Returns:
        True if value appears to be a time
    """
    if not isinstance(value, str):
        return False

    str_value = value.strip()

    # Check all time patterns
    time_patterns = [
        TIME_REGEX_FULL_WITH_MERIDIAN,
        TIME_REGEX_FULL,
        TIME_REGEX_SHORT_WITH_MERIDIAN,
        TIME_REGEX_SHORT,
    ]

    for pattern in time_patterns:
        if pattern.match(str_value):
            return True

    return False


def detect_number_format_type(
    value: Any,
    locale: Optional[str] = None
) -> Optional[str]:
    """
    Detect number format type of a value.

    Args:
        value: Value to analyze
        locale: Locale for date parsing

    Returns:
        Number format type or None

    Examples:
        >>> detect_number_format_type("$100")
        'CURRENCY'
        >>> detect_number_format_type("50%")
        'PERCENT'
        >>> detect_number_format_type("123")
        'NUMBER'
    """
    if is_currency(value):
        return "CURRENCY"

    if is_percentage(value):
        return "PERCENT"

    if is_number(value):
        return "NUMBER"

    if is_valid_date(value, locale):
        return "DATE"

    if is_valid_date_time(value):
        return "DATE_TIME"

    return None


def detect_number_format_pattern(
    value: Union[str, int, float, bool, date, None],
    number_value: Optional[float],
    format_type: Optional[str],
    locale: Optional[str] = None
) -> Optional[str]:
    """
    Detect pattern of a number format.

    Args:
        value: Original value
        number_value: Converted number value
        format_type: Number format type
        locale: Locale for formatting

    Returns:
        Format pattern or None

    Examples:
        >>> detect_number_format_pattern("50%", 0.5, "PERCENT", None)
        '0%'
        >>> detect_number_format_pattern("$100.50", 100.5, "CURRENCY", None)
        '"$"#,##0.00'
    """
    if format_type == "PERCENT":
        return detect_decimal_pattern(value, PATTERN_PERCENT)

    if format_type == "CURRENCY":
        return detect_decimal_pattern(number_value, PATTERN_CURRENCY)

    if format_type == "DATE":
        # Simplified - would need full date parser for pattern detection
        return DATE_PATTERN

    if format_type == "DATE_TIME":
        # Simplified - would need full time parser for pattern detection
        return TIME_PATTERN

    if format_type == "NUMBER":
        return detect_decimal_pattern(value)

    return None


def detect_value_type(
    value: Any,
    locale: Optional[str] = None
) -> str:
    """
    Detect datatype of a value.

    Args:
        value: Value to analyze
        locale: Locale for date parsing

    Returns:
        Value type key ('stringValue', 'numberValue', 'boolValue', 'formulaValue')

    Examples:
        >>> detect_value_type("=SUM(A1:A10)")
        'formulaValue'
        >>> detect_value_type(True)
        'boolValue'
        >>> detect_value_type(42)
        'numberValue'
    """
    if is_formula(value):
        return "formulaValue"

    if is_boolean(value):
        return "boolValue"

    # Dates are treated as numbers
    if is_number(value) or is_valid_date(value, locale) or is_valid_date_time(value):
        return "numberValue"

    return "stringValue"


def detect_value_type_and_pattern(
    value: Union[str, int, float, bool, date, None],
    locale: Optional[str] = None
) -> Tuple[str, Optional[str], Optional[float], Optional[str]]:
    """
    Detect value type and number format pattern.

    This is the main detection function that analyzes a value and returns
    comprehensive type information.

    Args:
        value: Value to analyze
        locale: Locale for date/number parsing

    Returns:
        Tuple of (value_type, number_format_type, number_value, pattern)

    Examples:
        >>> detect_value_type_and_pattern("=A1+B1")
        ('formulaValue', None, None, None)
        >>> detect_value_type_and_pattern(True)
        ('boolValue', None, None, None)
        >>> detect_value_type_and_pattern("$100.50")
        ('numberValue', 'CURRENCY', 100.5, '"$"#,##0.00')
        >>> detect_value_type_and_pattern("50%")
        ('numberValue', 'PERCENT', 0.5, '0%')
    """
    if is_formula(value):
        return ("formulaValue", None, None, None)

    if is_boolean(value):
        return ("boolValue", None, None, None)

    if is_number(value):
        number_value = convert_to_number(value)

        # Check for currency
        if is_currency(value):
            pattern = detect_decimal_pattern(value, PATTERN_CURRENCY)
            return ("numberValue", "CURRENCY", number_value, pattern)

        # Check for percentage
        if is_percentage(value):
            pattern = detect_decimal_pattern(value, PATTERN_PERCENT)
            percent_value = (number_value or 0) / 100
            return ("numberValue", "PERCENT", percent_value, pattern)

        # Regular number
        pattern = detect_number_format_pattern(value, number_value, "NUMBER", locale)
        return ("numberValue", "NUMBER", number_value, pattern)

    # TODO: Add full date parsing when date-parser library is available
    # For now, simplified date handling
    if is_valid_date(value, locale):
        return ("numberValue", "DATE", None, DATE_PATTERN)

    if is_valid_date_time(value):
        return ("numberValue", "DATE_TIME", None, TIME_PATTERN)

    return ("stringValue", None, None, None)


def create_formatted_value(
    value: Any,
    value_type: Optional[str],
    pattern: str
) -> str:
    """
    Create formatted value string.

    This is a simplified version. The full TypeScript implementation uses
    ssf (spreadsheet format) library for proper Excel-like formatting.

    Args:
        value: Value to format
        value_type: Type of value
        pattern: Format pattern

    Returns:
        Formatted string

    Examples:
        >>> create_formatted_value(True, 'boolValue', 'General')
        'TRUE'
        >>> create_formatted_value(100.5, 'numberValue', '#.00')
        '100.50'
    """
    if value_type == "boolValue":
        return TRUE_UPPER if str(value).upper() == TRUE_UPPER else FALSE_UPPER

    if value is None:
        return ""

    # Simplified formatting - would use ssf library in full implementation
    if isinstance(value, (int, float)):
        if pattern and '.' in pattern:
            # Count decimal places in pattern
            decimal_part = pattern.split('.')[-1]
            decimal_count = len(re.findall(r'[0#]', decimal_part))
            return f"{value:.{decimal_count}f}"
        return str(int(value) if isinstance(value, float) and value.is_integer() else value)

    return str(value)


def create_formatted_color(
    value: Any,
    value_type: Optional[str],
    pattern: str
) -> Optional[str]:
    """
    Create formatted color from pattern.

    The full TypeScript implementation extracts color from ssf format patterns.
    This is a placeholder for future implementation.

    Args:
        value: Value
        value_type: Type of value
        pattern: Format pattern

    Returns:
        Color string or None
    """
    # TODO: Implement full color extraction from patterns
    # This would require implementing the ssf format color extraction
    return None
