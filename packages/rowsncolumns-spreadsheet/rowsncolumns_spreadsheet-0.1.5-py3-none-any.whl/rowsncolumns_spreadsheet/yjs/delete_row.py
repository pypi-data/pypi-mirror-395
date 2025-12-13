"""
Delete-row helper that mutates Y.Doc structures directly.
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
    _map_set,
    _map_set_value,
)
from .change_batch import _create_recalc_patch, _queue_recalc_cells


def delete_row(
    ydoc: Any,
    sheet_id: int,
    row_indices: List[int],
    *,
    user_id: str | int = "agent",
) -> None:
    """
    Delete rows from a sheet inside a Y.Doc.
    """
    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    if not row_indices:
        return

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    sheets_array = _get_structure(ydoc, "sheets", expect="array")
    tables_array = _get_structure(ydoc, "tables", expect="array", optional=True)
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")

    sheet_entry, sheet_index = _find_sheet_entry(sheets_array, sheet_id)
    if sheet_entry is None or sheet_index is None:
        raise ValueError(f"Sheet with id {sheet_id} not found")

    row_count = sheet_entry.get("rowCount") or 0
    sorted_indexes = sorted(row_indices, reverse=True)
    for idx in sorted_indexes:
        if idx < 0 or idx >= row_count:
            raise ValueError("Invalid row index")

    _delete_from_sheet_data(
        sheet_data_map,
        sheet_id,
        sorted_indexes,
    )
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
    row_indices: List[int],
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

    for idx in row_indices:
        if idx < _array_length(sheet_rows):
            _array_delete(sheet_rows, idx, 1)


def _update_sheet_entry(sheet_entry: Any, row_indices: List[int]) -> None:
    row_count = sheet_entry.get("rowCount") or 0
    sheet_entry["rowCount"] = max(0, row_count - len(row_indices))

    frozen_count = sheet_entry.get("frozenRowCount")
    if frozen_count:
        for idx in row_indices:
            if idx < frozen_count:
                frozen_count -= 1
        sheet_entry["frozenRowCount"] = frozen_count

    row_metadata = sheet_entry.get("rowMetadata")
    if isinstance(row_metadata, list):
        for idx in row_indices:
            if idx < len(row_metadata):
                row_metadata.pop(idx)
        sheet_entry["rowMetadata"] = row_metadata

    basic_filter = sheet_entry.get("basicFilter")
    if isinstance(basic_filter, dict):
        range_obj = basic_filter.get("range") or {}
        start = range_obj.get("startRowIndex")
        end = range_obj.get("endRowIndex")
        if start is not None and end is not None:
            min_idx = row_indices[-1]
            max_idx = row_indices[0]
            if min_idx < start:
                shift = len(row_indices)
                range_obj["startRowIndex"] = start - shift
                range_obj["endRowIndex"] = end - shift
            elif min_idx >= start and min_idx <= end:
                range_obj["endRowIndex"] = max(start, end - len(row_indices))
        basic_filter["range"] = range_obj


def _update_tables_for_delete(
    tables_array: Any,
    sheet_id: int,
    row_indices: List[int],
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

        start = table_range.get("startRowIndex")
        end = table_range.get("endRowIndex")
        if start is None or end is None:
            continue

        deleted_count = len(row_indices)
        min_idx = row_indices[-1]
        max_idx = row_indices[0]

        if max_idx < start:
            table_range["startRowIndex"] = start - deleted_count
            table_range["endRowIndex"] = end - deleted_count
        elif min_idx <= end and min_idx >= start:
            table_range["endRowIndex"] = max(start, end - deleted_count)

        table["range"] = table_range
        _array_delete(tables_array, idx, 1)
        _array_insert(tables_array, idx, [table])


def _queue_recalc_for_delete(
    recalc_array: Any,
    user_id: str | int,
    sheet_id: int,
    row_indices: List[int],
) -> None:
    patches: List[List[Any]] = []
    for idx in row_indices:
        patches.append(_create_recalc_patch(sheet_id, idx, 0))
    _queue_recalc_cells(recalc_array, user_id, patches)
