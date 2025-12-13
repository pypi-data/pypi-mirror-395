"""
Auto-fill functionality - Python port of fill.ts

This module provides pattern detection and auto-fill value generation
for spreadsheet cells, supporting various fill types like series, dates,
days of the week, months, etc.
"""

import re
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple, Union, Callable
from enum import Enum

from ..types import CellData, Direction, SelectionArea, GridRange, CellInterface
from ..sheet_cell import SheetCell, DEFAULT_CELL_COORDS


class AutoFillType(str, Enum):
    """Types of auto-fill operations."""
    FILL_COPY = "FillCopy"
    FILL_DAYS = "FillDays"
    FILL_DEFAULT = "FillDefault"
    FILL_FORMATS = "FillFormats"
    FILL_MONTHS = "FillMonths"
    FILL_SERIES = "FillSeries"
    FILL_VALUES = "FillValues"
    FILL_WEEKDAYS = "FillWeekdays"
    FILL_YEARS = "FillYears"
    FLASH_FILL = "FlashFill"
    GROWTH_TREND = "GrowthTrend"
    LINEAR_TREND = "LinearTrend"


def extract_number(value: str) -> Optional[float]:
    """
    Extract numeric value from a string that may contain text.

    Args:
        value: String to extract number from

    Returns:
        Extracted number or None
    """
    match = re.search(r'-?\d+\.?\d*', value)
    return float(match.group(0)) if match else None


def parse_date(value: Any) -> Optional[datetime]:
    """
    Parse a date from various formats.

    Args:
        value: Value to parse as date

    Returns:
        Parsed datetime or None
    """
    if isinstance(value, datetime):
        return value

    # Don't try to parse numbers as dates
    if isinstance(value, (int, float)):
        return None

    # Don't try to parse simple numeric strings as dates
    if isinstance(value, str) and re.match(r'^\d+$', value.strip()):
        return None

    try:
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        pass

    # Try common date formats
    date_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%m-%d-%Y',
        '%d-%m-%Y',
        '%b %d, %Y',
        '%B %d, %Y',
        '%d %b %Y',
        '%d %B %Y',
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(str(value), fmt)
        except (ValueError, TypeError):
            continue

    return None


def get_day_names(locale: str = "en") -> List[str]:
    """
    Get day names array for a given locale.

    Args:
        locale: Locale string (simplified, only 'en' fully supported)

    Returns:
        List of day names
    """
    # For Python, we'll use a simple English implementation
    # Full i18n would require babel or similar library
    return [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def get_month_names(locale: str = "en") -> List[str]:
    """
    Get month names array for a given locale.

    Args:
        locale: Locale string (simplified, only 'en' fully supported)

    Returns:
        List of month names
    """
    return [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]


def detect_fill_type(
    selection_data: List[List[Union[str, int, float, bool, datetime, None]]]
) -> AutoFillType:
    """
    Detect the fill type based on selection data.

    Args:
        selection_data: 2D array of cell values

    Returns:
        Detected AutoFillType
    """
    if not selection_data or not selection_data[0]:
        return AutoFillType.FILL_COPY

    # Flatten the selection to analyze patterns
    values = [v for row in selection_data for v in row if v is not None]

    if len(values) == 0:
        return AutoFillType.FILL_COPY
    if len(values) == 1:
        return AutoFillType.FILL_COPY

    # Check for dates first (before numeric series)
    dates = [d for d in (parse_date(v) for v in values) if d is not None]

    if len(dates) >= 2:
        time_diff = (dates[1] - dates[0]).total_seconds()
        day_diff = time_diff / (60 * 60 * 24)

        if abs(day_diff - 1) < 0.1:
            return AutoFillType.FILL_DAYS
        if abs(day_diff - 7) < 0.1:
            return AutoFillType.FILL_WEEKDAYS

        # Check for months
        month_diff = (dates[1].year - dates[0].year) * 12 + (dates[1].month - dates[0].month)

        if month_diff == 1:
            return AutoFillType.FILL_MONTHS
        if dates[1].year - dates[0].year == 1:
            return AutoFillType.FILL_YEARS

    # Check for numeric series (after dates)
    non_date_values = [v for v in values if not isinstance(v, datetime)]
    numbers = [
        n for n in (
            v if isinstance(v, (int, float)) else extract_number(str(v))
            for v in non_date_values
        ) if n is not None
    ]

    # Only consider it a series if ALL non-Date values can be converted to numbers
    if len(numbers) >= 2 and len(numbers) == len(non_date_values):
        diff = numbers[1] - numbers[0]
        is_linear_series = all(
            i == 0 or abs(numbers[i] - numbers[i - 1] - diff) < 0.0001
            for i in range(len(numbers))
        )

        if is_linear_series and diff != 0:
            return AutoFillType.FILL_SERIES

    # Check for text patterns (days/months)
    day_names = get_day_names()
    month_names = get_month_names()
    text_values = [str(v).lower() for v in values]

    if any(
        len(v) >= 3 and any(
            day.lower() in v or v in day.lower()
            for day in day_names
        )
        for v in text_values
    ):
        return AutoFillType.FILL_DAYS

    if any(
        len(v) >= 3 and any(
            month.lower() in v or v in month.lower()
            for month in month_names
        )
        for v in text_values
    ):
        return AutoFillType.FILL_MONTHS

    return AutoFillType.FILL_DEFAULT


def generate_fill_values(
    source_values: List[Any],
    fill_type: AutoFillType,
    count: int,
    locale: str = "en-US"
) -> List[Any]:
    """
    Generate fill values based on type and pattern.

    Args:
        source_values: Source values to base the fill on
        fill_type: Type of fill to perform
        count: Number of values to generate
        locale: Locale for date/number formatting

    Returns:
        List of generated fill values
    """
    result: List[Any] = []

    if fill_type == AutoFillType.FILL_COPY:
        for i in range(count):
            result.append(source_values[i % len(source_values)])

    elif fill_type == AutoFillType.FILL_SERIES:
        numbers = [
            n for n in (
                v if isinstance(v, (int, float)) else extract_number(str(v))
                for v in source_values
            ) if n is not None
        ]
        if len(numbers) >= 2:
            diff = numbers[1] - numbers[0]
            last_value = numbers[-1]
            for i in range(count):
                last_value += diff
                result.append(last_value)
        else:
            result.extend([source_values[-1]] * count)

    elif fill_type == AutoFillType.FILL_DAYS:
        # Check if we're dealing with day names (text) or actual dates
        last_day_value = source_values[-1]
        last_date = parse_date(last_day_value)

        if last_date:
            # Handle actual dates
            for i in range(count):
                new_date = last_date + timedelta(days=i + 1)
                result.append(new_date.strftime('%m/%d/%Y'))
        elif isinstance(last_day_value, str):
            # Handle day names (like "Mon", "Tue", "Wed")
            all_day_names = get_day_names(locale)
            all_day_abbrevs = [d[:3] for d in all_day_names]

            # Find which day we're at
            last_day_lower = last_day_value.lower()
            day_index = -1
            for idx, day in enumerate(all_day_names):
                if day.lower() in last_day_lower or last_day_lower in day.lower():
                    day_index = idx
                    break

            if day_index != -1:
                # Determine if we're using full names or abbreviations
                is_abbreviated = len(last_day_value) <= 3

                for i in range(count):
                    next_day_index = (day_index + i + 1) % 7
                    day_name = all_day_abbrevs[next_day_index] if is_abbreviated else all_day_names[next_day_index]
                    result.append(day_name)

    elif fill_type == AutoFillType.FILL_WEEKDAYS:
        last_weekday = parse_date(source_values[-1])
        if last_weekday:
            current_date = last_weekday
            for i in range(count):
                while True:
                    current_date += timedelta(days=1)
                    if current_date.weekday() < 5:  # Monday=0, Sunday=6
                        break
                result.append(current_date.strftime('%m/%d/%Y'))

    elif fill_type == AutoFillType.FILL_MONTHS:
        # Check if we're dealing with month names (text) or actual dates
        last_value = source_values[-1]
        last_month = parse_date(last_value)

        if last_month:
            # Handle actual dates
            for i in range(count):
                # Add months
                month = last_month.month + i + 1
                year = last_month.year
                while month > 12:
                    month -= 12
                    year += 1
                new_date = last_month.replace(year=year, month=month)
                result.append(new_date.strftime('%m/%d/%Y'))
        elif isinstance(last_value, str):
            # Handle month names (like "Jan", "Feb", "Mar")
            all_month_names = get_month_names(locale)
            all_month_abbrevs = [m[:3] for m in all_month_names]

            # Find which month we're at
            last_value_lower = last_value.lower()
            month_index = -1
            for idx, month in enumerate(all_month_names):
                if month.lower() in last_value_lower or last_value_lower in month.lower():
                    month_index = idx
                    break

            if month_index != -1:
                # Determine if we're using full names or abbreviations
                is_abbreviated = len(last_value) <= 3

                for i in range(count):
                    next_month_index = (month_index + i + 1) % 12
                    month_name = all_month_abbrevs[next_month_index] if is_abbreviated else all_month_names[next_month_index]
                    result.append(month_name)

    elif fill_type == AutoFillType.FILL_YEARS:
        last_year = parse_date(source_values[-1])
        if last_year:
            for i in range(count):
                new_date = last_year.replace(year=last_year.year + i + 1)
                result.append(new_date.strftime('%m/%d/%Y'))

    elif fill_type == AutoFillType.LINEAR_TREND:
        num_values = [
            n for n in (
                float(v) if isinstance(v, (int, float)) else (
                    float(v) if isinstance(v, str) and v.replace('.', '', 1).replace('-', '', 1).isdigit() else None
                )
                for v in source_values
            ) if n is not None
        ]
        if len(num_values) >= 2:
            # Simple linear regression
            n = len(num_values)
            sum_x = sum(range(n))
            sum_y = sum(num_values)
            sum_xy = sum(i * val for i, val in enumerate(num_values))
            sum_xx = sum(i * i for i in range(n))

            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n

            for i in range(count):
                x = len(num_values) + i
                result.append(slope * x + intercept)

    elif fill_type == AutoFillType.GROWTH_TREND:
        growth_values = [
            n for n in (
                float(v) if isinstance(v, (int, float)) else (
                    float(v) if isinstance(v, str) and v.replace('.', '', 1).replace('-', '', 1).isdigit() else None
                )
                for v in source_values
            ) if n is not None and n > 0
        ]
        if len(growth_values) >= 2:
            # Calculate growth rate
            ratios = [growth_values[i] / growth_values[i - 1] for i in range(1, len(growth_values))]
            avg_ratio = sum(ratios) / len(ratios)

            last_value = growth_values[-1]
            for i in range(count):
                last_value *= avg_ratio
                result.append(last_value)

    elif fill_type == AutoFillType.FILL_VALUES:
        # Similar to FillSeries but preserves text formatting
        for i in range(count):
            source_index = i % len(source_values)
            value = source_values[source_index]

            if isinstance(value, str):
                num = extract_number(value)
                if num is not None and len(source_values) >= 2:
                    next_num = extract_number(str(source_values[(source_index + 1) % len(source_values)]))
                    if next_num is not None:
                        diff = next_num - num
                        cycles = i // len(source_values)
                        new_num = num + diff * (cycles + 1)
                        value = value.replace(str(int(num) if num.is_integer() else num), str(int(new_num) if new_num % 1 == 0 else new_num))
            result.append(value)

    elif fill_type == AutoFillType.FILL_FORMATS:
        # Only copy formatting, not values
        result.extend([""] * count)

    elif fill_type == AutoFillType.FLASH_FILL:
        # Advanced pattern recognition - simplified implementation
        result.extend([source_values[-1]] * count)

    else:  # FillDefault - intelligent copy
        for i in range(count):
            result.append(source_values[i % len(source_values)])

    return result


async def get_auto_fill_values(
    sheet_id: int,
    direction: Direction,
    selection: SelectionArea,
    fill_bounds: GridRange,
    get_cell_data: Optional[Callable[[int, int, int], Optional[CellData]]],
    get_effective_value: Optional[Callable[[int, int, int], Any]],
    cell_xfs_registry: Optional[Any] = None,
    locale: str = "en-US",
    fill_type: Optional[AutoFillType] = None,
) -> List[List[Union[CellData, str, int, float, None]]]:
    """
    Get auto fill values based on selection and direction.

    Args:
        sheet_id: Sheet ID
        direction: Fill direction
        selection: Source selection area
        fill_bounds: Target fill bounds
        get_cell_data: Function to get cell data
        get_effective_value: Function to get effective cell value
        cell_xfs_registry: Optional cell format registry
        locale: Locale for formatting
        fill_type: Optional explicit fill type (auto-detects if None)

    Returns:
        2D list of fill values (can be CellData objects or primitives)
    """
    # Create a cell helper
    sheet_cell = SheetCell(
        sheet_id=sheet_id,
        coords=DEFAULT_CELL_COORDS,
        cell_data=None,
        get_range_values=None,
        locale=locale,
        cell_xfs_registry=cell_xfs_registry,
    )

    # Get selection data for pattern analysis
    selection_data: List[List[Union[str, int, float, bool, None]]] = []
    for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
        row_data: List[Union[str, int, float, bool, None]] = []
        for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
            cell_value = get_effective_value(sheet_id, row_index, column_index) if get_effective_value else None
            row_data.append(cell_value)
        selection_data.append(row_data)

    # Calculate fill dimensions
    selection_rows = selection.range.end_row_index - selection.range.start_row_index + 1
    selection_cols = selection.range.end_column_index - selection.range.start_column_index + 1

    fill_values: List[List[Union[CellData, str, int, float, None]]] = []

    if direction == Direction.DOWN:
        fill_count = fill_bounds.end_row_index - selection.range.end_row_index

        for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
            # Get source values for this column
            source_values = []
            for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
                cell_value = get_effective_value(sheet_id, row_index, column_index) if get_effective_value else None
                source_values.append(cell_value)

            # Detect fill type for this specific column
            column_data = [source_values]
            actual_fill_type = fill_type or detect_fill_type(column_data)

            # Generate fill values for this column
            new_values = generate_fill_values(source_values, actual_fill_type, fill_count, locale)

            # Fallback to FillDefault if no values were generated
            if len(new_values) == 0 and actual_fill_type != AutoFillType.FILL_DEFAULT:
                new_values = generate_fill_values(source_values, AutoFillType.FILL_DEFAULT, fill_count, locale)

            # Apply the values
            for i in range(fill_count):
                target_row_index = selection.range.end_row_index + 1 + i
                target_column_index = column_index

                if len(fill_values) <= i:
                    fill_values.append([])

                if actual_fill_type == AutoFillType.FILL_FORMATS:
                    # Copy format but not value
                    while len(fill_values[i]) <= (target_column_index - fill_bounds.start_column_index):
                        fill_values[i].append(None)
                    fill_values[i][target_column_index - fill_bounds.start_column_index] = ""
                else:
                    # Get a source cell for formatting/properties
                    source_row_index = selection.range.start_row_index + (i % selection_rows)
                    source_cell_data = get_cell_data(sheet_id, source_row_index, column_index) if get_cell_data else None

                    sheet_cell.assign(
                        sheet_id=sheet_id,
                        coords=CellInterface(row_index=source_row_index, column_index=column_index),
                        cell_data=source_cell_data,
                        get_range_values=None,
                        locale=locale,
                        cell_xfs_registry=cell_xfs_registry,
                    )

                    if sheet_cell.is_formula():
                        sheet_cell.move_formula(
                            from_coords=CellInterface(row_index=source_row_index, column_index=column_index),
                            to_coords=CellInterface(row_index=target_row_index, column_index=target_column_index),
                            exclusion_range=None,
                            ignore_circular=False,
                            row_count=None,
                            column_count=None,
                            preserve_absolutes=True,
                        )
                        # Remove effective value for formulas
                        sheet_cell.clear_effective_value_for_formula()
                    else:
                        # Use the generated fill value
                        sheet_cell.set_user_entered_value(new_values[i])

                    cell_data = sheet_cell.get_cell_data()
                    while len(fill_values[i]) <= (target_column_index - fill_bounds.start_column_index):
                        fill_values[i].append(None)
                    fill_values[i][target_column_index - fill_bounds.start_column_index] = cell_data

    elif direction == Direction.UP:
        fill_count = selection.range.start_row_index - fill_bounds.start_row_index

        for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
            # Get source values for this column (in reverse order)
            source_values = []
            for row_index in range(selection.range.end_row_index, selection.range.start_row_index - 1, -1):
                cell_value = get_effective_value(sheet_id, row_index, column_index) if get_effective_value else None
                source_values.append(cell_value)

            column_data = [source_values]
            actual_fill_type = fill_type or detect_fill_type(column_data)

            new_values = generate_fill_values(source_values, actual_fill_type, fill_count, locale)

            if len(new_values) == 0 and actual_fill_type != AutoFillType.FILL_DEFAULT:
                new_values = generate_fill_values(source_values, AutoFillType.FILL_DEFAULT, fill_count, locale)

            # Apply the values (in reverse order)
            for i in range(fill_count):
                target_row_index = selection.range.start_row_index - 1 - i
                target_column_index = column_index

                if len(fill_values) <= (fill_count - 1 - i):
                    while len(fill_values) <= (fill_count - 1 - i):
                        fill_values.append([])

                if actual_fill_type == AutoFillType.FILL_FORMATS:
                    while len(fill_values[fill_count - 1 - i]) <= (target_column_index - fill_bounds.start_column_index):
                        fill_values[fill_count - 1 - i].append(None)
                    fill_values[fill_count - 1 - i][target_column_index - fill_bounds.start_column_index] = ""
                else:
                    source_row_index = selection.range.end_row_index - (i % selection_rows)
                    source_cell_data = get_cell_data(sheet_id, source_row_index, column_index) if get_cell_data else None

                    sheet_cell.assign(
                        sheet_id=sheet_id,
                        coords=CellInterface(row_index=source_row_index, column_index=column_index),
                        cell_data=source_cell_data,
                        get_range_values=None,
                        locale=locale,
                        cell_xfs_registry=cell_xfs_registry,
                    )

                    if sheet_cell.is_formula():
                        sheet_cell.move_formula(
                            from_coords=CellInterface(row_index=source_row_index, column_index=column_index),
                            to_coords=CellInterface(row_index=target_row_index, column_index=target_column_index),
                            preserve_absolutes=True,
                        )
                        sheet_cell.clear_effective_value_for_formula()
                    else:
                        sheet_cell.set_user_entered_value(new_values[i])

                    cell_data = sheet_cell.get_cell_data()
                    while len(fill_values[fill_count - 1 - i]) <= (target_column_index - fill_bounds.start_column_index):
                        fill_values[fill_count - 1 - i].append(None)
                    fill_values[fill_count - 1 - i][target_column_index - fill_bounds.start_column_index] = cell_data

    elif direction == Direction.RIGHT:
        fill_count = fill_bounds.end_column_index - selection.range.end_column_index

        for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
            # Get source values for this row
            source_values = []
            for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
                cell_value = get_effective_value(sheet_id, row_index, column_index) if get_effective_value else None
                source_values.append(cell_value)

            row_data = [source_values]
            actual_fill_type = fill_type or detect_fill_type(row_data)

            new_values = generate_fill_values(source_values, actual_fill_type, fill_count, locale)

            if len(new_values) == 0 and actual_fill_type != AutoFillType.FILL_DEFAULT:
                new_values = generate_fill_values(source_values, AutoFillType.FILL_DEFAULT, fill_count, locale)

            # Apply the values
            target_row_index = row_index - fill_bounds.start_row_index
            if len(fill_values) <= target_row_index:
                while len(fill_values) <= target_row_index:
                    fill_values.append([])

            for i in range(fill_count):
                target_column_index = selection.range.end_column_index + 1 + i

                if actual_fill_type == AutoFillType.FILL_FORMATS:
                    while len(fill_values[target_row_index]) <= i:
                        fill_values[target_row_index].append(None)
                    fill_values[target_row_index][i] = ""
                else:
                    source_column_index = selection.range.start_column_index + (i % selection_cols)
                    source_cell_data = get_cell_data(sheet_id, row_index, source_column_index) if get_cell_data else None

                    sheet_cell.assign(
                        sheet_id=sheet_id,
                        coords=CellInterface(row_index=row_index, column_index=source_column_index),
                        cell_data=source_cell_data,
                        get_range_values=None,
                        locale=locale,
                        cell_xfs_registry=cell_xfs_registry,
                    )

                    if sheet_cell.is_formula():
                        sheet_cell.move_formula(
                            from_coords=CellInterface(row_index=row_index, column_index=source_column_index),
                            to_coords=CellInterface(row_index=row_index, column_index=target_column_index),
                            preserve_absolutes=True,
                        )
                        sheet_cell.clear_effective_value_for_formula()
                    else:
                        sheet_cell.set_user_entered_value(new_values[i])

                    cell_data = sheet_cell.get_cell_data()
                    while len(fill_values[target_row_index]) <= i:
                        fill_values[target_row_index].append(None)
                    fill_values[target_row_index][i] = cell_data

    elif direction == Direction.LEFT:
        fill_count = selection.range.start_column_index - fill_bounds.start_column_index

        for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
            # Get source values for this row (in reverse order)
            source_values = []
            for column_index in range(selection.range.end_column_index, selection.range.start_column_index - 1, -1):
                cell_value = get_effective_value(sheet_id, row_index, column_index) if get_effective_value else None
                source_values.append(cell_value)

            row_data = [source_values]
            actual_fill_type = fill_type or detect_fill_type(row_data)

            new_values = generate_fill_values(source_values, actual_fill_type, fill_count, locale)

            if len(new_values) == 0 and actual_fill_type != AutoFillType.FILL_DEFAULT:
                new_values = generate_fill_values(source_values, AutoFillType.FILL_DEFAULT, fill_count, locale)

            # Apply the values (in reverse order)
            target_row_index = row_index - fill_bounds.start_row_index
            if len(fill_values) <= target_row_index:
                while len(fill_values) <= target_row_index:
                    fill_values.append([])

            for i in range(fill_count):
                target_column_index = selection.range.start_column_index - 1 - i

                if actual_fill_type == AutoFillType.FILL_FORMATS:
                    while len(fill_values[target_row_index]) <= (fill_count - 1 - i):
                        fill_values[target_row_index].append(None)
                    fill_values[target_row_index][fill_count - 1 - i] = ""
                else:
                    source_column_index = selection.range.end_column_index - (i % selection_cols)
                    source_cell_data = get_cell_data(sheet_id, row_index, source_column_index) if get_cell_data else None

                    sheet_cell.assign(
                        sheet_id=sheet_id,
                        coords=CellInterface(row_index=row_index, column_index=source_column_index),
                        cell_data=source_cell_data,
                        get_range_values=None,
                        locale=locale,
                        cell_xfs_registry=cell_xfs_registry,
                    )

                    if sheet_cell.is_formula():
                        sheet_cell.move_formula(
                            from_coords=CellInterface(row_index=row_index, column_index=source_column_index),
                            to_coords=CellInterface(row_index=row_index, column_index=target_column_index),
                            preserve_absolutes=True,
                        )
                        sheet_cell.clear_effective_value_for_formula()
                    else:
                        sheet_cell.set_user_entered_value(new_values[i])

                    cell_data = sheet_cell.get_cell_data()
                    while len(fill_values[target_row_index]) <= (fill_count - 1 - i):
                        fill_values[target_row_index].append(None)
                    fill_values[target_row_index][fill_count - 1 - i] = cell_data

    return fill_values
