"""
Insert-row helper that mutates Y.Doc structures directly.
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
    _set_with_fallback,
    _ensure_array_size,
)
from .change_batch import _create_recalc_patch, _queue_recalc_cells


def insert_row(
    ydoc: Any,
    sheet_id: int,
    reference_row_index: int,
    num_rows: int = 1,
    *,
    user_id: str | int = "agent",
) -> None:
    """
    Insert rows for a sheet inside a Y.Doc.

    Args:
        ydoc: Y.Doc (or compatible mock)
        sheet_id: Identifier of sheet to modify
        reference_row_index: Index where rows are inserted (0-based)
        num_rows: Number of rows to insert
        user_id: Identifier used when enqueuing recalc patches
    """

    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    if num_rows <= 0:
        return

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    sheets_array = _get_structure(ydoc, "sheets", expect="array")
    tables_array = _get_structure(ydoc, "tables", expect="array", optional=True)
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")

    sheet_entry, sheet_index = _find_sheet_entry(sheets_array, sheet_id)
    if sheet_entry is None or sheet_index is None:
        raise ValueError(f"Sheet with id {sheet_id} not found")

    row_count = sheet_entry.get("rowCount") or 0
    if reference_row_index < 0 or reference_row_index > row_count:
        raise ValueError("Invalid reference_row_index")

    _update_tables_for_insert(tables_array, sheet_id, reference_row_index, num_rows)
    _update_sheet_entry(sheet_entry, reference_row_index, num_rows)

    _insert_rows_in_sheet_data(
        sheet_data_map,
        sheet_id,
        reference_row_index,
        num_rows,
    )

    _queue_row_recalc_patches(
        recalc_array,
        user_id,
        sheet_id,
        reference_row_index,
        num_rows,
    )


def _insert_rows_in_sheet_data(
    sheet_data_map: Any,
    sheet_id: int,
    reference_row_index: int,
    num_rows: int,
) -> None:
    sheet_key = str(sheet_id)
    sheet_rows = _map_get(sheet_data_map, sheet_key)
    if sheet_rows is None:
        sheet_rows = _create_array_like(_is_pycrdt_map(sheet_data_map))
        _map_set(sheet_data_map, sheet_key, sheet_rows)
    elif isinstance(sheet_rows, list):
        buffer = _create_array_like(_is_pycrdt_map(sheet_data_map))
        for idx, value in enumerate(sheet_rows):
            _array_insert(buffer, idx, [value])
        sheet_rows = buffer
        _map_set(sheet_data_map, sheet_key, sheet_rows)

    _array_insert(sheet_rows, reference_row_index, [None] * num_rows)


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


def _update_sheet_entry(sheet_entry: Any, reference_row_index: int, num_rows: int) -> None:
    row_count = sheet_entry.get("rowCount") or 0
    sheet_entry["rowCount"] = row_count + num_rows

    frozen_count = sheet_entry.get("frozenRowCount")
    if frozen_count is not None and reference_row_index <= frozen_count:
        sheet_entry["frozenRowCount"] = frozen_count + num_rows

    row_metadata = sheet_entry.get("rowMetadata")
    if isinstance(row_metadata, list):
        for _ in range(num_rows):
            row_metadata.insert(reference_row_index, None)
        sheet_entry["rowMetadata"] = row_metadata

    basic_filter = _get_with_fallback(sheet_entry, ("basicFilter", "basic_filter"))
    if isinstance(basic_filter, dict):
        start = _get_with_fallback(basic_filter, ("range", "range", "startRowIndex"))
        end = _get_with_fallback(basic_filter, ("range", "range", "endRowIndex"))
        if start is not None and reference_row_index < start:
            _adjust_filter_range(basic_filter, num_rows)
        elif (
            start is not None
            and end is not None
            and reference_row_index >= start
            and reference_row_index <= end
        ):
            _extend_filter_range(basic_filter, num_rows)


def _adjust_filter_range(basic_filter: dict, offset: int) -> None:
    range_obj = basic_filter.get("range") or {}
    start = range_obj.get("startRowIndex")
    end = range_obj.get("endRowIndex")
    if start is not None:
        range_obj["startRowIndex"] = start + offset
    if end is not None:
        range_obj["endRowIndex"] = end + offset
    basic_filter["range"] = range_obj


def _extend_filter_range(basic_filter: dict, offset: int) -> None:
    range_obj = basic_filter.get("range") or {}
    end = range_obj.get("endRowIndex")
    if end is not None:
        range_obj["endRowIndex"] = end + offset
    basic_filter["range"] = range_obj


def _update_tables_for_insert(
    tables_array: Any,
    sheet_id: int,
    reference_row_index: int,
    num_rows: int,
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

        start_row = table_range.get("startRowIndex")
        end_row = table_range.get("endRowIndex")

        if start_row is not None and reference_row_index < start_row:
            table_range["startRowIndex"] = start_row + num_rows
            if end_row is not None:
                table_range["endRowIndex"] = end_row + num_rows
        elif (
            start_row is not None
            and end_row is not None
            and reference_row_index >= start_row
            and reference_row_index <= end_row
        ):
            table_range["endRowIndex"] = end_row + num_rows

        table["range"] = table_range
        _array_delete(tables_array, idx, 1)
        _array_insert(tables_array, idx, [table])


def _queue_row_recalc_patches(
    recalc_array: Any,
    user_id: str | int,
    sheet_id: int,
    reference_row_index: int,
    num_rows: int,
) -> None:
    patches: List[List[Any]] = []
    for offset in range(num_rows):
        patches.append(_create_recalc_patch(sheet_id, reference_row_index + offset, 0))
    _queue_recalc_cells(recalc_array, user_id, patches)
