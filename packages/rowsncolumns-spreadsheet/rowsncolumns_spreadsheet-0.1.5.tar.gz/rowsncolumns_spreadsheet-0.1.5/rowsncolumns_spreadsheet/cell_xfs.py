"""Utilities for managing cellXfs registries shared between SheetCell and Yjs helpers."""

from __future__ import annotations

import logging
import copy
from typing import TYPE_CHECKING, Any, Dict, Optional

__all__ = ["register_cell_xfs_registry", "update_cell_xfs_registry"]

logger = logging.getLogger(__name__)

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from .sheet_cell import SheetCell


def register_cell_xfs_registry(
    cell_xfs_map: Any,
    sheet_cell: Optional["SheetCell"],
    cell_data: Optional[Dict[str, Any]],
) -> None:
    """
    Register the cell's formats in ``cell_xfs_map`` and replace them with style IDs.

    This now relies on the ``SheetCell`` instance so the fully merged effective
    and user-entered formats are captured before the ``cell_data`` entry is
    converted to style references.
    """

    if cell_xfs_map is None or sheet_cell is None or not cell_data:
        return

    format_map = {
        "ef": sheet_cell.get_effective_cell_format(),
        "uf": sheet_cell.get_user_entered_format(),
    }

    for key, format_value in format_map.items():
        if not format_value:
            cell_data.pop(key, None)
            continue

        style_id = _register_format_value(cell_xfs_map, format_value)
        if style_id:
            cell_data[key] = {"sid": style_id}

def update_cell_xfs_registry(cell_xfs_map: Any, sheet_cell: Optional["SheetCell"]) -> None:
    """
    Ensure the registry contains the latest effective and user-entered formats for a cell.

    This should be called after ``SheetCell.get_cell_data`` so that the registry
    has the fully merged formats returned by ``get_effective_cell_format`` and
    ``get_user_entered_format``.
    """
    if cell_xfs_map is None or sheet_cell is None:
        return

    for format_value in (
        sheet_cell.get_effective_cell_format(),
        sheet_cell.get_user_entered_format(),
    ):
        if format_value:
            logger.info(f"Register {cell_xfs_map}, {format_value}")
            _register_format_value(cell_xfs_map, format_value)

def _register_format_value(cell_xfs_map: Any, format_value: Any) -> Optional[str]:
    if not isinstance(format_value, dict):
        return None

    if _is_style_reference_format(format_value):
        return format_value.get("sid") or format_value.get("styleId")

    key = _get_cell_xfs_key(format_value)
    if _map_get(cell_xfs_map, key) is None:
        _map_set(cell_xfs_map, key, copy.deepcopy(format_value))
    return key


def _is_style_reference_format(value: Any) -> bool:
    return isinstance(value, dict) and ("sid" in value or "styleId" in value)


_CELL_XFS_PROPS = [
    "backgroundColor",
    "borders",
    "textFormat",
    "numberFormat",
    "horizontalAlignment",
    "verticalAlignment",
    "wrapStrategy",
    "indent",
    "textRotation",
]


def _get_cell_xfs_key(format_value: Optional[Dict[str, Any]]) -> str:
    if format_value is None:
        return "0"

    obj = _defined_props(format_value) or {}
    state = 0

    for prop in _CELL_XFS_PROPS:
        if isinstance(obj, dict) and prop in obj and obj[prop] is not None:
            state = _hash_string(state, prop)
            state = _hash_value(state, obj[prop])

    if state >= 2**31:
        state -= 2**32
    return str(abs(state))


def _defined_props(value: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not isinstance(value, dict):
        return value
    return {k: v for k, v in value.items() if v is not None}


def _hash_string(state: int, text: str) -> int:
    for ch in text:
        state = ((state << 5) - state + ord(ch)) & 0xFFFFFFFF
    return state


def _hash_value(state: int, value: Any) -> int:
    if value is None:
        return state
    if isinstance(value, dict):
        for key in sorted(value.keys()):
            state = _hash_string(state, key)
            state = _hash_value(state, value[key])
        return state
    if isinstance(value, list):
        for item in value:
            state = _hash_value(state, item)
        return state
    return _hash_string(state, str(value))


def _map_get(target: Any, key: str) -> Any:
    getter = getattr(target, "get", None)
    if callable(getter):
        try:
            return getter(key)
        except Exception:
            pass
    if isinstance(target, dict):
        return target.get(key)
    try:
        return target[key]  # type: ignore[index]
    except Exception:
        return getattr(target, key, None)


def _map_set(target: Any, key: str, value: Any) -> None:
    setter = getattr(target, "set", None)
    if callable(setter):
        setter(key, value)
    elif isinstance(target, dict):
        target[key] = value
    else:
        try:
            target[key] = value  # type: ignore[index]
        except Exception:
            setattr(target, key, value)
