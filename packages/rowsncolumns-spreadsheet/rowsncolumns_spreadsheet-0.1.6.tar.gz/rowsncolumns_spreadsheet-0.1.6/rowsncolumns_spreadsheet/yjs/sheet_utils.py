"""
Utility helpers for manipulating sheet dictionaries inside Y.Doc structures.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

SheetDict = Dict[str, Any]


def dedupe_sheet_name(base_name: Optional[str], sheets: List[SheetDict]) -> str:
    """Ensure the sheet name is unique by appending a counter when needed."""
    if not base_name:
        base_name = "Sheet"

    existing = {
        name
        for name in (get_sheet_name(sheet) for sheet in sheets)
        if name
    }

    if base_name not in existing:
        return base_name

    counter = 1
    while f"{base_name}{counter}" in existing:
        counter += 1
    return f"{base_name}{counter}"


def get_sheet_id(sheet: SheetDict) -> Optional[int]:
    """Return the sheet id from the camelCase key."""
    value = sheet.get("sheetId")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def set_sheet_id(sheet: SheetDict, sheet_id: int) -> None:
    """Set sheet identifier using camelCase key."""
    sheet["sheetId"] = sheet_id


def get_sheet_name(sheet: SheetDict) -> Optional[str]:
    """Return the sheet title/name if present."""
    return sheet.get("title")


def set_sheet_name(sheet: SheetDict, name: str) -> None:
    """Set sheet title/name using camelCase keys only."""
    sheet["title"] = name


def set_dimension(sheet: SheetDict, axis: str, value: int) -> None:
    """Set row or column count on a sheet using camelCase keys only."""
    if axis == "row":
        sheet["rowCount"] = value
    else:
        sheet["columnCount"] = value
