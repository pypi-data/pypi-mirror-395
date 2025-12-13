"""
Create-new-sheet helper that mutates Y.Doc structures directly.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .change_batch import (
    _array_get,
    _array_insert,
    _array_length,
    _get_structure,
)
from .sheet_utils import (
    dedupe_sheet_name,
    get_sheet_id,
    set_dimension,
    set_sheet_id,
    set_sheet_name,
)
from .models import Sheet as SheetModel

DEFAULT_ROW_COUNT = 1_000
DEFAULT_COLUMN_COUNT = 26


def create_sheet(
    ydoc: Any,
    sheet_spec: SheetModel,
    *,
    default_row_count: int = DEFAULT_ROW_COUNT,
    default_column_count: int = DEFAULT_COLUMN_COUNT,
) -> Dict[str, Any]:
    """
    Insert a new sheet entry into the Y.Doc `sheets` array.

    Args:
        ydoc: Y.Doc (or mock) exposing `get_array`/`get_map`
        sheet_spec: Sheet definition (fields matching the TypeScript Sheet type)
        default_row_count: Default number of rows for the sheet
        default_column_count: Default number of columns for the sheet

    Returns:
        The dictionary representing the created sheet.
    """

    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    sheets_array = _get_structure(ydoc, "sheets", expect="array")

    normalized_spec = {
        key: value
        for key, value in sheet_spec.model_dump(by_alias=True, exclude_unset=True).items()
        if value is not None
    }
    new_sheet_id = _determine_sheet_id(sheets_array, normalized_spec)

    existing_index = _find_sheet_index(sheets_array, new_sheet_id)
    if existing_index is not None:
        existing_entry = _array_get(sheets_array, existing_index)
        return existing_entry if existing_entry is not None else {}

    existing_sheets = _collect_sheets(sheets_array)

    base_title = normalized_spec.get("title") or normalized_spec.get("name")
    if not base_title:
        base_title = f"Sheet{len(existing_sheets) + 1}"
    unique_title = dedupe_sheet_name(base_title, existing_sheets)

    row_count = _coerce_int(
        normalized_spec.get("rowCount"),
        default_row_count,
    )
    column_count = _coerce_int(
        normalized_spec.get("columnCount"),
        default_column_count,
    )

    insert_index = normalized_spec.get("index")
    if not isinstance(insert_index, int) or insert_index < 0:
        insert_index = _array_length(sheets_array)
    else:
        insert_index = min(insert_index, _array_length(sheets_array))

    entry: Dict[str, Any] = dict(normalized_spec)
    set_sheet_id(entry, new_sheet_id)
    set_sheet_name(entry, unique_title)
    set_dimension(entry, "row", row_count)
    set_dimension(entry, "column", column_count)
    entry["hidden"] = entry.get("hidden", False)
    entry["index"] = insert_index

    sheet_model = SheetModel.model_validate(entry)
    entry = sheet_model.model_dump(by_alias=True, exclude_unset=False)

    _array_insert(sheets_array, insert_index, [entry])
    _reindex_sheets_array(sheets_array)

    return entry


def _determine_sheet_id(
    sheets_array: Any,
    spec: Dict[str, Any],
) -> int:
    explicit = spec.get("sheetId")
    if explicit is not None:
        try:
            return int(explicit)
        except (TypeError, ValueError) as exc:
            raise ValueError("sheetSpec.sheetId must be numeric") from exc

    existing_ids = [
        sheet_id
        for sheet_id in (
            get_sheet_id(_array_get(sheets_array, idx))
            for idx in range(_array_length(sheets_array))
        )
        if sheet_id is not None
    ]
    if not existing_ids:
        return 1
    return max(existing_ids) + 1


def _collect_sheets(sheets_array: Any, exclude_index: Optional[int] = None) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    total = _array_length(sheets_array)
    for idx in range(total):
        if exclude_index is not None and idx == exclude_index:
            continue
        entry = _array_get(sheets_array, idx)
        if isinstance(entry, dict):
            entries.append(entry)
        elif entry is not None:
            # Fallback for custom map-like objects
            try:
                entries.append(dict(entry))  # type: ignore[arg-type]
            except Exception:
                continue
    return entries


def _find_sheet_index(sheets_array: Any, sheet_id: int) -> Optional[int]:
    total = _array_length(sheets_array)
    for idx in range(total):
        entry = _array_get(sheets_array, idx)
        if entry is None:
            continue
        if get_sheet_id(entry) == sheet_id:
            return idx
    return None


def _reindex_sheets_array(sheets_array: Any) -> None:
    total = _array_length(sheets_array)
    for idx in range(total):
        entry = _array_get(sheets_array, idx)
        if isinstance(entry, dict):
            entry["index"] = idx


def _coerce_int(value: Any, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
