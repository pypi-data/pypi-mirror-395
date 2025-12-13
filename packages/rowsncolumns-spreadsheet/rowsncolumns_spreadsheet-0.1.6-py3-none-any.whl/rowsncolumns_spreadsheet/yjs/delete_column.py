"""
Delete-column helper that mutates Y.Doc structures directly.
"""

from __future__ import annotations

from typing import Any, List, Optional

from .change_batch import (
    _array_delete,
    _array_get,
    _array_insert,
    _array_length,
    _create_array_like,
    _create_map_like,
    _get_structure,
    _get_with_fallback,
    _is_pycrdt_array,
    _is_pycrdt_map,
    _map_get,
    _map_get_value,
    _map_set,
    _map_set_value,
)
from .change_batch import _create_recalc_patch, _queue_recalc_cells


def delete_column(
    ydoc: Any,
    sheet_id: int,
    column_indices: List[int],
    *,
    user_id: str | int = "agent",
) -> None:
    """
    Delete columns from a sheet inside a Y.Doc.
    """
    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    if not column_indices:
        return

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    sheets_array = _get_structure(ydoc, "sheets", expect="array")
    tables_array = _get_structure(ydoc, "tables", expect="array", optional=True)
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")

    sheet_entry, sheet_index = _find_sheet_entry(sheets_array, sheet_id)
    if sheet_entry is None or sheet_index is None:
        raise ValueError(f"Sheet with id {sheet_id} not found")

    column_count = sheet_entry.get("columnCount") or 0
    sorted_indexes = sorted(column_indices, reverse=True)
    for idx in sorted_indexes:
        if idx < 0 or idx >= column_count:
            raise ValueError("Invalid column index")

    _delete_from_sheet_data(sheet_data_map, sheet_id, sorted_indexes)
    _update_sheet_entry(sheet_entry, sorted_indexes)
    _update_tables_for_delete(
        tables_array,
        sheet_id,
        sorted_indexes,
    )
    _queue_recalc_for_delete(
        recalc_array,
        user_id,
        sheet_id,
        sorted_indexes,
    )


def _find_sheet_entry(sheets_array: Any, sheet_id: int) -> tuple[Optional[Any], Optional[int]]:
    total = _array_length(sheets_array)
    for idx in range(total):
        entry = _array_get(sheets_array, idx)
        if entry is None:
            continue
        entry_id = entry.get("sheetId")
        if entry_id == sheet_id:
            return entry, idx
    return None, None


def _delete_from_sheet_data(
    sheet_data_map: Any,
    sheet_id: int,
    column_indices: List[int],
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

    total_rows = _array_length(sheet_rows)

    for row_index in range(total_rows):
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

        for column_index in column_indices:
            if column_index < _array_length(values):
                _array_delete(values, column_index, 1)


def _update_sheet_entry(sheet_entry: Any, column_indices: List[int]) -> None:
    column_count = sheet_entry.get("columnCount") or 0
    sheet_entry["columnCount"] = max(0, column_count - len(column_indices))

    frozen_count = sheet_entry.get("frozenColumnCount")
    if frozen_count:
        for idx in column_indices:
            if idx < frozen_count:
                frozen_count -= 1
        sheet_entry["frozenColumnCount"] = frozen_count

    column_metadata = sheet_entry.get("columnMetadata")
    if isinstance(column_metadata, list):
        for idx in column_indices:
            if idx < len(column_metadata):
                column_metadata.pop(idx)
        sheet_entry["columnMetadata"] = column_metadata

    basic_filter = sheet_entry.get("basicFilter")
    if isinstance(basic_filter, dict):
        range_obj = basic_filter.get("range") or {}
        start = range_obj.get("startColumnIndex")
        end = range_obj.get("endColumnIndex")
        if start is not None and end is not None:
            min_idx = column_indices[-1]
            max_idx = column_indices[0]
            if min_idx < start:
                shift = len(column_indices)
                range_obj["startColumnIndex"] = start - shift
                range_obj["endColumnIndex"] = end - shift
            elif min_idx >= start and min_idx <= end:
                range_obj["endColumnIndex"] = max(start, end - len(column_indices))
        basic_filter["range"] = range_obj


def _update_tables_for_delete(
    tables_array: Any,
    sheet_id: int,
    column_indices: List[int],
) -> None:
    if tables_array is None:
        return

    total = _array_length(tables_array)
    for idx in range(total):
        table = _array_get(tables_array, idx)
        if not table:
            continue
        table_sheet_id = _get_with_fallback(table, ("sheetId", "sheet_id"))
        if table_sheet_id != sheet_id:
            continue

        table_range = table.get("range") if isinstance(table, dict) else None
        if not table_range:
            continue

        start = table_range.get("startColumnIndex")
        end = table_range.get("endColumnIndex")
        if start is None or end is None:
            continue

        deleted_count = len(column_indices)
        min_idx = column_indices[-1]
        max_idx = column_indices[0]

        if max_idx < start:
            table_range["startColumnIndex"] = start - deleted_count
            table_range["endColumnIndex"] = end - deleted_count
        elif min_idx <= end and min_idx >= start:
            table_range["endColumnIndex"] = max(start, end - deleted_count)

        table["range"] = table_range
        _array_delete(tables_array, idx, 1)
        _array_insert(tables_array, idx, [table])


def _queue_recalc_for_delete(
    recalc_array: Any,
    user_id: str | int,
    sheet_id: int,
    column_indices: List[int],
) -> None:
    patches: List[List[Any]] = []
    for idx in column_indices:
        patches.append(_create_recalc_patch(sheet_id, 0, idx))
    _queue_recalc_cells(recalc_array, user_id, patches)
