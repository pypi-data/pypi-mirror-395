"""
Update-sheet helper that mutates Y.Doc structures directly.
"""

from __future__ import annotations

from typing import Any, Dict

from .sheet_utils import set_sheet_id, set_sheet_name
from .change_batch import (
    _array_delete,
    _array_get,
    _array_insert,
    _array_length,
    _get_structure,
    _set_with_fallback,
)
from .create_new_sheet import (
    DEFAULT_COLUMN_COUNT,
    DEFAULT_ROW_COUNT,
    _find_sheet_index,
    _reindex_sheets_array,
)
from .models import Sheet as SheetModel


def update_sheet(
    ydoc: Any,
    sheet_id: int,
    sheet_spec: SheetModel,
) -> Dict[str, Any]:
    """
    Update properties on an existing sheet entry.

    Args:
        ydoc: Y.Doc (or mock)
        sheet_id: Identifier of the sheet to update
        sheet_spec: Sheet definition (fields matching the TypeScript Sheet type)

    Returns:
        The updated sheet entry
    """

    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    sheets_array = _get_structure(ydoc, "sheets", expect="array")
    normalized_spec = {
        key: value
        for key, value in sheet_spec.model_dump(by_alias=True, exclude_none=True).items()
        if value is not None
    }

    index = _find_sheet_index(sheets_array, sheet_id)    
    if index is None:
        raise ValueError(f"Sheet with id {sheet_id} not found")

    entry = _array_get(sheets_array, index)
    if entry is None:
        raise ValueError(f"Sheet data missing at index {index}")
    if not isinstance(entry, dict):
        entry = dict(entry)
        _array_delete(sheets_array, index, 1)
        _array_insert(sheets_array, index, [entry])

    entry.update(normalized_spec)


    desired_index = normalized_spec.pop("index", None)
    if isinstance(desired_index, int):
        target_index = max(0, min(desired_index, _array_length(sheets_array) - 1))
        _array_delete(sheets_array, index, 1)
        _array_insert(sheets_array, target_index, [entry])
        index = target_index
    _set_with_fallback(entry, ("index",), index)

    if "rowCount" not in entry:
        entry["rowCount"] = DEFAULT_ROW_COUNT
    if "columnCount" not in entry:
        entry["columnCount"] = DEFAULT_COLUMN_COUNT

    sheet_model = SheetModel.model_validate(entry)
    normalized_entry = sheet_model.model_dump(by_alias=True, exclude_unset=False)
    entry.clear()
    entry.update(normalized_entry)
    entry.pop("sheet_id", None)
    _array_delete(sheets_array, index, 1)
    _array_insert(sheets_array, index, [entry])

    _reindex_sheets_array(sheets_array)
    return entry
