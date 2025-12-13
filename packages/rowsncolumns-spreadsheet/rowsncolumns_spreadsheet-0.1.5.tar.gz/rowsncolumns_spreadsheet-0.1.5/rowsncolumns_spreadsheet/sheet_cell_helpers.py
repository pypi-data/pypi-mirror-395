"""
Helper functions for SheetCell operations.

This module provides utility functions for working with SheetCell instances,
including creating row data from arrays and other common operations.
"""

from typing import Any, List, Optional, TYPE_CHECKING, TypeVar, Union

from .types import CellData

if TYPE_CHECKING:  # pragma: no cover
    from .sheet_cell import SheetCell, DEFAULT_SHEET_ID, DEFAULT_CELL_COORDS


T = TypeVar('T', bound=CellData)


def create_row_data_from_array(
    rows: List[List[Union[str, int, float, bool, None, CellData]]],
    sheet_id: Optional[int] = None,
) -> List[dict]:
    """
    Convert array of values to RowData using SheetCell instances.

    This function takes a 2D array of values and converts them into
    row data suitable for use in a spreadsheet. Each cell value is
    processed through a SheetCell instance to ensure proper formatting
    and type detection.

    Args:
        rows: 2D array of cell values
        sheet_id: Sheet identifier (default: 1)

    Returns:
        List of RowData dictionaries with 'values' key

    Example:
        >>> rows = [
        ...     ["Name", "Age", "Score"],
        ...     ["Alice", 25, 95.5],
        ...     ["Bob", 30, 88.0],
        ... ]
        >>> row_data = create_row_data_from_array(rows)
    """
    from .sheet_cell import SheetCell, DEFAULT_SHEET_ID, DEFAULT_CELL_COORDS

    if sheet_id is None:
        sheet_id = DEFAULT_SHEET_ID

    result = []

    for row in rows:
        values = []
        for value in row:
            sheet_cell = SheetCell(sheet_id=sheet_id, coords=DEFAULT_CELL_COORDS)

            handled_as_cell_data = False

            if isinstance(value, CellData):
                sheet_cell.assign(sheet_id, DEFAULT_CELL_COORDS, value)
                handled_as_cell_data = True
            elif isinstance(value, dict):
                try:
                    sheet_cell.assign(sheet_id, DEFAULT_CELL_COORDS, value)
                    handled_as_cell_data = True
                except Exception:
                    handled_as_cell_data = False
            elif hasattr(value, "model_dump"):
                try:
                    sheet_cell.assign(sheet_id, DEFAULT_CELL_COORDS, value)
                    handled_as_cell_data = True
                except Exception:
                    handled_as_cell_data = False

            if not handled_as_cell_data:
                # Fallback to treating the value as a primitive.
                sheet_cell.set_user_entered_value(value)

            cell_data = sheet_cell.get_cell_data()
            values.append(cell_data)

        result.append({"values": values})

    return result


def is_cell_range(coords: dict) -> bool:
    """
    Check if coordinates represent a range.

    Args:
        coords: Coordinates dictionary

    Returns:
        True if coords is a cell range (has 'from' key)

    Example:
        >>> is_cell_range({"from": {"row": 0, "col": 0}, "to": {"row": 5, "col": 5}})
        True
        >>> is_cell_range({"row": 0, "col": 0})
        False
    """
    return "from" in coords


def combine_map_iterators(*iterators):
    """
    Combine multiple iterators into a single iterator.

    Args:
        *iterators: Variable number of iterators to combine

    Yields:
        Items from all iterators in sequence

    Example:
        >>> iter1 = iter([1, 2, 3])
        >>> iter2 = iter([4, 5, 6])
        >>> combined = combine_map_iterators(iter1, iter2)
        >>> list(combined)
        [1, 2, 3, 4, 5, 6]
    """
    for iterator in iterators:
        yield from iterator


def get_next_table_column_name(columns: Optional[List[dict]] = None) -> str:
    """
    Get unique table column name.

    Generates the next available "ColumnN" name where N is an incrementing number.

    Args:
        columns: List of existing column dictionaries with 'name' key

    Returns:
        Next available column name (e.g., "Column1", "Column2", etc.)

    Example:
        >>> columns = [{"name": "Column1"}, {"name": "Column2"}]
        >>> get_next_table_column_name(columns)
        'Column3'
    """
    if not columns:
        return "Column1"

    i = 1
    existing_names = {col.get("name") for col in columns}
    while f"Column{i}" in existing_names:
        i += 1

    return f"Column{i}"


def get_conflicting_table(
    tables: Optional[List[dict]],
    active_table: dict,
) -> Optional[dict]:
    """
    Check for conflicting tables when inserting or deleting table columns.

    Ensures we are not moving a partial table by checking if any other table
    overlaps with the active table in a conflicting way.

    Args:
        tables: List of table dictionaries
        active_table: The table being modified

    Returns:
        Conflicting table if found, None otherwise

    Example:
        >>> tables = [
        ...     {"sheetId": 1, "id": 1, "range": {"startRowIndex": 0, "endRowIndex": 10, ...}},
        ...     {"sheetId": 1, "id": 2, "range": {"startRowIndex": 5, "endRowIndex": 15, ...}},
        ... ]
        >>> active = tables[0]
        >>> conflict = get_conflicting_table(tables, active)
    """
    if not tables:
        return None

    active_sheet_id = active_table.get("sheetId")
    active_id = active_table.get("id")
    active_range = active_table.get("range", {})

    for table in tables:
        if table.get("sheetId") == active_sheet_id and table.get("id") != active_id:
            table_range = table.get("range", {})

            # Check if table is completely inside active table
            is_table_inside = (
                table_range.get("startRowIndex", 0) >= active_range.get("startRowIndex", 0)
                and table_range.get("endRowIndex", 0) <= active_range.get("endRowIndex", 0)
            )

            # Check if table is completely outside active table
            is_table_outside = (
                table_range.get("startRowIndex", 0) > active_range.get("endRowIndex", 0)
                or table_range.get("endRowIndex", 0) < active_range.get("startRowIndex", 0)
                or table_range.get("endColumnIndex", 0) <= active_range.get("startColumnIndex", 0)
            )

            if not is_table_inside and not is_table_outside:
                return table

    return None


def hash_object(obj: Optional[Union[dict, Any]]) -> int:
    """
    Hash an object and return a number.

    Creates a consistent hash for objects by converting to JSON and
    hashing the string representation.

    Args:
        obj: Object to hash (dict, list, or None)

    Returns:
        Hash value as integer

    Example:
        >>> hash_object({"key": "value", "num": 123})
        1234567890  # Some hash value
        >>> hash_object(None)
        0
    """
    import json

    # Handle null/undefined
    if obj is None:
        return 0

    # Create a detailed string representation
    try:
        # Ensure consistent ordering of object keys
        json_str = json.dumps(obj, sort_keys=True, default=str)
    except (TypeError, ValueError):
        # Fallback for non-serializable objects
        json_str = str(obj)

    # Generate hash from the string
    hash_value = 0
    for char in json_str:
        char_code = ord(char)
        hash_value = ((hash_value << 5) - hash_value) + char_code
        hash_value = hash_value & 0xFFFFFFFF  # Convert to 32-bit integer

    return abs(hash_value)


# Constants
AWAITING_CALCULATION = "Paused"
