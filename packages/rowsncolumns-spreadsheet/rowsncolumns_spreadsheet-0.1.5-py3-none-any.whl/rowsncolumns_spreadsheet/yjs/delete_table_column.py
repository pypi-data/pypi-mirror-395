"""
Delete a column from an existing table directly in a Y.Doc.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .change_batch import (
    _array_delete,
    _array_get,
    _array_insert,
    _array_length,
    _create_array_like,
    _get_structure,
    _get_with_fallback,
    _is_pycrdt_map,
    _map_get,
    _map_get_value,
    _map_set,
    _map_set_value,
)
from .change_batch import _queue_recalc_cells, _create_recalc_patch


def delete_table_column(
    ydoc: Any,
    table_id: Any,
    dimension_index: int,
    *,
    user_id: str | int = "agent",
) -> None:
    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    tables_array = _get_structure(ydoc, "tables", expect="array")
    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    table_entry, index = _find_table_entry(tables_array, table_id)
    if table_entry is None or index is None:
        raise ValueError("Table id not found")

    sheet_id = _get_with_fallback(table_entry, ("sheetId", "sheet_id"))
    if sheet_id is None:
        raise ValueError("Table entry missing sheetId")

    table_range = table_entry.get("range")
    if not table_range:
        raise ValueError("Table entry missing range")

    start_col = table_range.get("startColumnIndex", 0)
    end_col = table_range.get("endColumnIndex", start_col)
    table_width = max(0, end_col - start_col + 1)
    if table_width == 0:
        raise ValueError("Table does not contain any columns")
    if dimension_index < 0 or dimension_index >= table_width:
        raise ValueError("dimension_index is outside the table range")

    target_column_index = start_col + dimension_index

    _delete_from_sheet_data(
        sheet_data_map,
        sheet_id,
        target_column_index,
        table_range,
    )

    columns = table_entry.get("columns") or []
    column_array_index = max(0, min(target_column_index - start_col, len(columns) - 1))
    if columns and 0 <= column_array_index < len(columns):
        columns.pop(column_array_index)
    table_entry["columns"] = columns

    table_range["endColumnIndex"] = max(start_col, end_col - 1)
    table_entry["range"] = table_range

    _array_delete(tables_array, index, 1)
    _array_insert(tables_array, index, [table_entry])

    patches: List[List[Any]] = []
    start_row = table_range.get("startRowIndex", 0)
    end_row = table_range.get("endRowIndex", start_row)
    for row_index in range(start_row, end_row + 1):
        patches.append(_create_recalc_patch(sheet_id, row_index, target_column_index))
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")
    _queue_recalc_cells(recalc_array, user_id, patches)


def _find_table_entry(
    tables_array: Any, table_id: Any
) -> tuple[Optional[Dict[str, Any]], Optional[int]]:
    total = _array_length(tables_array)
    for idx in range(total):
        table = _array_get(tables_array, idx)
        if not table:
            continue
        if _get_with_fallback(table, ("id",)) == table_id:
            return table, idx
    return None, None


def _delete_from_sheet_data(
    sheet_data_map: Any,
    sheet_id: int,
    target_column_index: int,
    table_range: Dict[str, Any],
) -> None:
    sheet_key = str(sheet_id)
    sheet_rows = _map_get(sheet_data_map, sheet_key)
    if sheet_rows is None:
        return

    if isinstance(sheet_rows, list):
        buffer = _create_array_like(_is_pycrdt_map(sheet_data_map))
        for idx, value in enumerate(sheet_rows):
            _array_insert(buffer, idx, [value])
        sheet_rows = buffer
        _map_set(sheet_data_map, sheet_key, sheet_rows)

    start_row = table_range.get("startRowIndex", 0)
    end_row = table_range.get("endRowIndex", start_row)
    total_rows = _array_length(sheet_rows)
    if total_rows == 0:
        return

    end_row = min(end_row, total_rows - 1)

    for row_index in range(start_row, end_row + 1):
        row_entry = _array_get(sheet_rows, row_index)
        if row_entry is None:
            continue

        values = _map_get_value(row_entry, "values")
        if values is None:
            continue
        if isinstance(values, list):
            buffer = _create_array_like(_is_pycrdt_map(row_entry))
            for idx, val in enumerate(values):
                _array_insert(buffer, idx, [val])
            values = buffer
            _map_set_value(row_entry, "values", values)

        if target_column_index < _array_length(values):
            _array_delete(values, target_column_index, 1)
