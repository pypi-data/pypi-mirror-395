"""
Python port of the TypeScript `updateTable` helper that operates on Y.Doc structures.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Optional, Tuple

from ..sheet_cell import SheetCell
from ..cell_xfs import update_cell_xfs_registry
from ..types import CellInterface, GridRange
from .managers import SheetDataHelpers, SheetDataManager
from .change_batch import (
    _array_get,
    _array_insert,
    _array_length,
    _array_set,
    _convert_range_keys,
    _create_array_like,
    _get_structure,
    _get_with_fallback,
    _is_pycrdt_map,
    _set_with_fallback,
    _get_or_create_row_values,
    _set_row_value,
)


def update_table(
    ydoc: Any,
    *,
    sheet_id: int,
    table_id: Any,
    table_updates: Dict[str, Any],
    locale: str = "en-US",
) -> Dict[str, Any]:
    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    tables_array = _get_structure(ydoc, "tables", expect="array")
    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    cell_xfs_map = _get_structure(ydoc, "cellXfs", expect="map")

    sheet_data_manager = SheetDataManager(
        sheet_data_map,
        SheetDataHelpers(
            get_or_create_row_values=_get_or_create_row_values,
            set_row_value=_set_row_value,
        ),
    )

    original_entry, index = _find_table_entry(tables_array, table_id, sheet_id)
    if original_entry is None or index is None:
        raise ValueError("Table id not found")

    merged_entry = copy.deepcopy(original_entry)
    merged_entry.update(table_updates)

    normalized_range = _normalize_range(merged_entry.get("range") or original_entry.get("range"))
    _populate_header_cells(
        sheet_data_manager,
        sheet_id,
        normalized_range,
        locale,
        cell_xfs_map,
    )

    updated_entry = _finalize_table_entry(
        tables_array,
        index,
        merged_entry,
        normalized_range,
        cell_xfs_map,
        locale,
        sheet_id,
    )

    _apply_total_row_range_adjustment(updated_entry, original_entry)

    return updated_entry


def _normalize_range(range_like: Optional[Dict[str, Any]]) -> GridRange:
    if range_like is None:
        raise ValueError("Table range is required")
    if isinstance(range_like, GridRange):
        return range_like
    if isinstance(range_like, dict):
        return GridRange(**_convert_range_keys(range_like))
    raise TypeError("range must be a GridRange or dict")


def _populate_header_cells(
    sheet_data_manager: SheetDataManager,
    sheet_id: int,
    grid_range: GridRange,
    locale: str,
    cell_xfs_map: Any,
) -> None:
    row_values = sheet_data_manager.get_row_values(sheet_id, grid_range.start_row_index)
    sheet_cell = SheetCell(locale=locale, cell_xfs_registry=cell_xfs_map)

    for column_index in range(
        grid_range.start_column_index, grid_range.end_column_index + 1
    ):
        existing = _array_get(row_values, column_index)
        sheet_cell.assign(
            sheet_id=sheet_id,
            coords=CellInterface(
                row_index=grid_range.start_row_index,
                column_index=column_index,
            ),
            cell_data=existing,
            locale=locale,
            cell_xfs_registry=cell_xfs_map,
        )

        if sheet_cell.formatted_value:
            continue

        column_name = f"Column{column_index - grid_range.start_column_index + 1}"
        sheet_cell.set_user_entered_value(column_name)
        new_cell_data = sheet_cell.get_cell_data()
        sheet_data_manager.set_cell_value(row_values, column_index, new_cell_data)
        update_cell_xfs_registry(cell_xfs_map, sheet_cell)


def _find_table_entry(
    tables_array: Any,
    table_id: Any,
    sheet_id: int,
) -> Tuple[Optional[Dict[str, Any]], Optional[int]]:
    try:
        total = _array_length(tables_array)
    except TypeError:
        return None, None

    for index in range(total):
        table = _array_get(tables_array, index)
        if not table:
            continue
        if _get_with_fallback(table, ("id",)) == table_id and _get_with_fallback(
            table, ("sheetId", "sheet_id")
        ) == sheet_id:
            return table, index
    return None, None


def _finalize_table_entry(
    tables_array: Any,
    index: int,
    updated_table: Dict[str, Any],
    grid_range: GridRange,
    cell_xfs_map: Any,
    locale: str,
    sheet_id: int,
) -> Dict[str, Any]:
    entry = copy.deepcopy(updated_table)
    entry["range"] = {
        "startRowIndex": grid_range.start_row_index,
        "endRowIndex": grid_range.end_row_index,
        "startColumnIndex": grid_range.start_column_index,
        "endColumnIndex": grid_range.end_column_index,
    }

    if entry.get("headerRow"):
        _sync_table_columns(entry, grid_range, sheet_id, locale, cell_xfs_map)

    _array_set(tables_array, index, entry)
    return entry


def _sync_table_columns(
    entry: Dict[str, Any],
    grid_range: GridRange,
    sheet_id: int,
    locale: str,
    cell_xfs_map: Any,
) -> None:
    columns = entry.get("columns")
    if columns is None:
        columns = []
    entry["columns"] = columns

    desired_length = grid_range.end_column_index - grid_range.start_column_index + 1
    columns[:] = columns[:desired_length]

    for column_index in range(desired_length):
        if column_index >= len(columns) or columns[column_index] is None:
            columns.append({"name": f"Column{column_index + 1}"})


def _apply_total_row_range_adjustment(
    entry: Dict[str, Any],
    previous_table: Dict[str, Any],
) -> None:
    had_total = bool(previous_table.get("totalRow"))
    will_have_total = bool(entry.get("totalRow"))

    if had_total == will_have_total:
        return

    range_dict = entry.get("range", {})
    end_row = range_dict.get("endRowIndex")
    if end_row is None:
        return
    range_dict["endRowIndex"] = end_row + 1 if will_have_total else end_row - 1
