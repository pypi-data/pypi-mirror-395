"""
Insert-column helper that mutates Y.Doc structures directly.
"""

from __future__ import annotations

from typing import Any, List, Optional

from .change_batch import (
    _array_delete,
    _array_get,
    _array_insert,
    _array_length,
    _array_set,
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
    _set_with_fallback,
    _ensure_array_size,
)
from .change_batch import _create_recalc_patch, _queue_recalc_cells


def insert_column(
    ydoc: Any,
    sheet_id: int,
    reference_column_index: int,
    num_columns: int = 1,
    *,
    user_id: str | int = "agent",
) -> None:
    """
    Insert columns for a sheet inside a Y.Doc.
    """
    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    if num_columns <= 0:
        return

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    sheets_array = _get_structure(ydoc, "sheets", expect="array")
    tables_array = _get_structure(ydoc, "tables", expect="array", optional=True)
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")

    sheet_entry, sheet_index = _find_sheet_entry(sheets_array, sheet_id)
    if sheet_entry is None or sheet_index is None:
        raise ValueError(f"Sheet with id {sheet_id} not found")

    column_count = sheet_entry.get("columnCount") or 0
    if reference_column_index < 0 or reference_column_index > column_count:
        raise ValueError("Invalid reference_column_index")

    _update_tables_for_insert(
        tables_array,
        sheet_id,
        reference_column_index,
        num_columns,
    )
    _update_sheet_entry(sheet_entry, reference_column_index, num_columns)
    _insert_columns_in_sheet_data(
        sheet_data_map,
        sheet_id,
        reference_column_index,
        num_columns,
    )
    _queue_column_recalc_patches(
        recalc_array,
        user_id,
        sheet_id,
        reference_column_index,
        num_columns,
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


def _update_sheet_entry(
    sheet_entry: Any,
    reference_column_index: int,
    num_columns: int,
) -> None:
    column_count = sheet_entry.get("columnCount") or 0
    sheet_entry["columnCount"] = column_count + num_columns

    frozen_count = sheet_entry.get("frozenColumnCount")
    if frozen_count is not None and reference_column_index <= frozen_count:
        sheet_entry["frozenColumnCount"] = frozen_count + num_columns

    column_metadata = sheet_entry.get("columnMetadata")
    if isinstance(column_metadata, list):
        for _ in range(num_columns):
            column_metadata.insert(reference_column_index, None)
        sheet_entry["columnMetadata"] = column_metadata

    basic_filter = sheet_entry.get("basicFilter")
    if isinstance(basic_filter, dict):
        range_obj = basic_filter.get("range") or {}
        start = range_obj.get("startColumnIndex")
        end = range_obj.get("endColumnIndex")

        if start is not None and reference_column_index < start:
            range_obj["startColumnIndex"] = start + num_columns
            if end is not None:
                range_obj["endColumnIndex"] = end + num_columns
        elif (
            start is not None
            and end is not None
            and reference_column_index >= start
            and reference_column_index <= end
        ):
            range_obj["endColumnIndex"] = end + num_columns

        basic_filter["range"] = range_obj


def _update_tables_for_insert(
    tables_array: Any,
    sheet_id: int,
    reference_column_index: int,
    num_columns: int,
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

        start_col = table_range.get("startColumnIndex")
        end_col = table_range.get("endColumnIndex")

        if start_col is not None and reference_column_index < start_col:
            table_range["startColumnIndex"] = start_col + num_columns
            if end_col is not None:
                table_range["endColumnIndex"] = end_col + num_columns
        elif (
            start_col is not None
            and end_col is not None
            and reference_column_index >= start_col
            and reference_column_index <= end_col
        ):
            table_range["endColumnIndex"] = end_col + num_columns

        table["range"] = table_range
        _array_delete(tables_array, idx, 1)
        _array_insert(tables_array, idx, [table])


def _insert_columns_in_sheet_data(
    sheet_data_map: Any,
    sheet_id: int,
    reference_column_index: int,
    num_columns: int,
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
            row_entry = _create_map_like(_is_pycrdt_array(sheet_rows))
            _array_set(sheet_rows, row_index, row_entry)

        values = _map_get_value(row_entry, "values")
        if values is None:
            values = _create_array_like()
            _map_set_value(row_entry, "values", values)
        elif isinstance(values, list):
            buffer = _create_array_like(_is_pycrdt_map(row_entry))
            for idx, val in enumerate(values):
                _array_insert(buffer, idx, [val])
            values = buffer
            _map_set_value(row_entry, "values", values)

        _ensure_array_size(values, reference_column_index)
        if _array_length(values) <= reference_column_index:
            _ensure_array_size(values, reference_column_index + 1)
        _array_insert(values, reference_column_index, [None] * num_columns)


def _queue_column_recalc_patches(
    recalc_array: Any,
    user_id: str | int,
    sheet_id: int,
    reference_column_index: int,
    num_columns: int,
) -> None:
    patches: List[List[Any]] = []
    for offset in range(num_columns):
        patches.append(_create_recalc_patch(sheet_id, 0, reference_column_index + offset))
    _queue_recalc_cells(recalc_array, user_id, patches)
