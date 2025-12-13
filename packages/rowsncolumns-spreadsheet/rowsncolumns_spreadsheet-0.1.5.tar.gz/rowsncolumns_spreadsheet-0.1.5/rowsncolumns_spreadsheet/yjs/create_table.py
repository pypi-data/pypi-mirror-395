"""
Python port of the `createTable` interface that operates directly on Y.Doc data.
"""

from __future__ import annotations

import uuid
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from ..sheet_cell import SheetCell
from ..types import CellInterface, GridRange
from ..cell_xfs import update_cell_xfs_registry
from .managers import (
    SheetDataHelpers,
    SheetDataManager,
)
from .change_batch import (
    _get_structure,
    _get_or_create_row_values,
    _set_row_value,
    _array_length,
    _array_get,
    _array_insert,
    _array_set,
    _get_with_fallback,
    _set_with_fallback,
)

logger = logging.getLogger(__name__)

def create_table(
    ydoc: Any,
    sheet_id: int,
    table_range: Union[GridRange, Dict[str, Any], None],
    *,
    locale: str = "en-US",
    table_spec: Optional[Dict[str, Any]] = None,
    theme: str = "TableStyleLight1",
    banded_range: Optional[Dict[str, Any]] = None,
    id_generator: Optional[Callable[[str], str]] = None,
) -> str:
    """
    Create a table at the given range directly on a pycrdt/ypy Y.Doc.

    Args:
        ydoc: pycrdt/ypy document
        sheet_id: sheet identifier
        table_range: range for the new table
        locale: locale for header formatting
        table_spec: optional dictionary with table overrides (id, title, etc.)
        theme: Excel-compatible table theme name
        banded_range: optional banded range definition
        id_generator: optional callback used to produce table ids

    Returns:
        The id of the newly created table
    """

    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    range_input = (
        table_range
        or (table_spec.get("range") if table_spec is not None else None)
    )
    if range_input is None:
        raise ValueError("table_range is required to create a table")

    grid_range = _normalize_range(range_input)

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    tables_array = _get_structure(ydoc, "tables", expect="array")
    sheets_array = _get_structure(ydoc, "sheets", expect="array", optional=True)
    cell_xfs_map = _get_structure(ydoc, "cellXfs", expect="map")

    _ensure_no_table_conflicts(tables_array, sheet_id, grid_range)

    sheet_data_manager = SheetDataManager(
        sheet_data_map,
        SheetDataHelpers(
            get_or_create_row_values=_get_or_create_row_values,
            set_row_value=_set_row_value,
        ),
    )

    columns = _build_table_columns(
        sheet_data_manager,
        sheet_id,
        grid_range,
        locale,
        cell_xfs_map,
    )

    entry = _build_table_entry(
        tables_array,
        sheet_id,
        grid_range,
        columns,
        theme=theme,
        banded_range=banded_range,
        table_spec=table_spec,
        id_generator=id_generator,
    )

    _array_insert(tables_array, _array_length(tables_array), [entry])
    logger.info(f"entry {entry} {tables_array}")

    if sheets_array is not None:
        _clear_matching_basic_filter(sheets_array, sheet_id, grid_range)

    return entry["id"]


def _build_table_entry(
    tables_array: Any,
    sheet_id: int,
    grid_range: GridRange,
    columns: List[Dict[str, Any]],
    *,
    theme: str,
    banded_range: Optional[Dict[str, Any]],
    table_spec: Optional[Dict[str, Any]],
    id_generator: Optional[Callable[[str], str]],
) -> Dict[str, Any]:
    spec = dict(table_spec) if table_spec else {}
    spec.pop("range", None)
    spec.pop("columns", None)

    table_id = spec.get("id")
    if not table_id and id_generator:
        table_id = id_generator("table")
    if not table_id:
        table_id = str(uuid.uuid4())

    default_title = spec.get(
        "title", f"Table {_array_length(tables_array) + 1}"
    )

    entry = {
        "id": table_id,
        "range": {
            "startRowIndex": grid_range.start_row_index,
            "endRowIndex": grid_range.end_row_index,
            "startColumnIndex": grid_range.start_column_index,
            "endColumnIndex": grid_range.end_column_index,
        },
        "sheetId": sheet_id,
        "title": default_title,
        "columns": columns,
        "filterSpecs": [],
        "headerRow": True,
        "filterButton": True,
        "sortSpecs": [],
        "showRowStripes": True,
        "bandedRange": banded_range,
        "theme": theme,
    }
    entry.update(spec)
    return entry


def _build_table_columns(
    sheet_data_manager: SheetDataManager,
    sheet_id: int,
    grid_range: GridRange,
    locale: str,
    cell_xfs_map: Any,
) -> List[Dict[str, Any]]:
    row_values = sheet_data_manager.get_row_values(
        sheet_id, grid_range.start_row_index
    )
    sheet_cell = SheetCell(locale=locale, cell_xfs_registry=cell_xfs_map)
    columns: List[Dict[str, Any]] = []

    for column_index in range(
        grid_range.start_column_index, grid_range.end_column_index + 1
    ):
        existing_data = _array_get(row_values, column_index)
        sheet_cell.assign(
            sheet_id=sheet_id,
            coords=CellInterface(
                row_index=grid_range.start_row_index, column_index=column_index
            ),
            cell_data=existing_data,
            locale=locale,
            cell_xfs_registry=cell_xfs_map,
        )

        formatted_value = sheet_cell.formatted_value
        if not formatted_value:
            formatted_value = _extended_value_to_string(sheet_cell.user_entered_value)

        column_name = formatted_value or _get_next_table_column_name(columns)

        if not formatted_value:
            sheet_cell.set_user_entered_value(column_name)
            new_cell_data = sheet_cell.get_cell_data()
            sheet_data_manager.set_cell_value(row_values, column_index, new_cell_data)
            update_cell_xfs_registry(cell_xfs_map, sheet_cell)

        columns.append({"name": column_name})

    return columns


def _ensure_no_table_conflicts(
    tables_array: Any,
    sheet_id: int,
    target_range: GridRange,
) -> None:
    try:
        total = _array_length(tables_array)
    except TypeError:
        return

    for index in range(total):
        table = _array_get(tables_array, index)
        if not table:
            continue

        table_sheet_id = _get_with_fallback(table, ("sheetId", "sheet_id"))
        if table_sheet_id != sheet_id:
            continue

        entry_range = _get_with_fallback(table, ("range",))
        if entry_range is None:
            continue

        existing_range = _normalize_range(entry_range)
        if _ranges_intersect(existing_range, target_range):
            raise ValueError("Table range intersects with an existing table")


def _clear_matching_basic_filter(
    sheets_array: Any,
    sheet_id: int,
    target_range: GridRange,
) -> None:
    try:
        total = _array_length(sheets_array)
    except TypeError:
        return

    for index in range(total):
        sheet = _array_get(sheets_array, index)
        if not sheet:
            continue

        sheet_id_value = _get_with_fallback(sheet, ("sheetId", "sheet_id"))
        if sheet_id_value != sheet_id:
            continue

        basic_filter = _get_with_fallback(sheet, ("basicFilter", "basic_filter"))
        if not basic_filter:
            break

        filter_range = _get_with_fallback(basic_filter, ("range",))
        if filter_range and _ranges_equal(
            _normalize_range(filter_range), target_range
        ):
            _set_with_fallback(sheet, ("basicFilter", "basic_filter"), None)
            _array_set(sheets_array, index, sheet)
            break


def _extended_value_to_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    for attr in ("stringValue", "formulaValue", "numberValue", "boolValue"):
        attr_value = getattr(value, attr, None)
        if attr_value is not None:
            return str(attr_value)
    return None


def _normalize_range(range_like: Union[GridRange, Dict[str, Any]]) -> GridRange:
    if isinstance(range_like, GridRange):
        return range_like
    if isinstance(range_like, dict):
        return GridRange(**_convert_range_keys(range_like))
    raise TypeError("range must be GridRange or dict")


def _convert_range_keys(range_like: Dict[str, Any]) -> Dict[str, Any]:
    mapping = {
        "startRowIndex": "start_row_index",
        "endRowIndex": "end_row_index",
        "startColumnIndex": "start_column_index",
        "endColumnIndex": "end_column_index",
    }
    converted = {}
    for key, value in range_like.items():
        converted[mapping.get(key, key)] = value
    return converted


def _ranges_intersect(a: GridRange, b: GridRange) -> bool:
    rows_overlap = not (a.end_row_index < b.start_row_index or b.end_row_index < a.start_row_index)
    cols_overlap = not (
        a.end_column_index < b.start_column_index or b.end_column_index < a.start_column_index
    )
    return rows_overlap and cols_overlap


def _ranges_equal(a: GridRange, b: GridRange) -> bool:
    return (
        a.start_row_index == b.start_row_index
        and a.end_row_index == b.end_row_index
        and a.start_column_index == b.start_column_index
        and a.end_column_index == b.end_column_index
    )


def _get_next_table_column_name(columns: List[Dict[str, Any]]) -> str:
    existing = {col.get("name") for col in columns if isinstance(col, dict)}
    index = 1
    while f"Column{index}" in existing:
        index += 1
    return f"Column{index}"
