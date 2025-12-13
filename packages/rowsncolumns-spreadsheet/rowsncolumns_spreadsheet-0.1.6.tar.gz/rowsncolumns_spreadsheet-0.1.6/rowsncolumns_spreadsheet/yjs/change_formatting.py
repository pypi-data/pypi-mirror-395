"""
Python port of the `changeFormatting` helper that operates on Y.Doc data.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

from ..sheet_cell import SheetCell
from ..cell_xfs import update_cell_xfs_registry
from ..types import CellInterface, GridRange
from .models import CellFormat
from .managers import SheetDataHelpers, SheetDataManager
from .change_batch import (
    FormatMatrix,
    RangeLike,
    _append_recalc_entry,
    _array_get,
    _create_recalc_patch,
    _get_or_create_row_values,
    _get_structure,
    _is_sequence,
    _normalize_ranges,
    _resolve_matrix_value,
    _set_row_value,
)

logger = logging.getLogger(__name__)

CellFormatInput = Union[CellFormat, Dict[str, Any], FormatMatrix, None]


def change_formatting(
    ydoc: Any,
    *,
    sheet_id: int,
    ranges: Union[RangeLike, Sequence[RangeLike]],
    cell_formats: CellFormatInput,
    replace: bool = False,
    locale: str = "en-US",
    user_id: Union[str, int] = "agent",
) -> None:
    """
    Apply cell formatting to the specified ranges inside a pycrdt/ypy Y.Doc.
    """

    if ydoc is None:
        raise ValueError("A Y.Doc instance is required")

    range_list = _normalize_ranges(ranges)
    if not range_list:
        logger.debug("change_formatting called with no ranges for sheet_id=%s", sheet_id)
        return

    if cell_formats is None and not replace:
        logger.debug("No formatting supplied for sheet_id=%s; nothing to apply", sheet_id)
        return

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")
    cell_xfs_map = _get_structure(ydoc, "cellXfs", expect="map")

    sheet_data_manager = SheetDataManager(
        sheet_data_map,
        SheetDataHelpers(
            get_or_create_row_values=_get_or_create_row_values,
            set_row_value=_set_row_value,
        ),
    )

    normalized_formats = _normalize_format_source(cell_formats)
    sheet_cell = SheetCell(locale=locale, cell_xfs_registry=cell_xfs_map)
    recalc_patches: List[List[Any]] = []

    for grid in range_list:
        for row_index in range(grid.start_row_index, grid.end_row_index + 1):
            row_values = sheet_data_manager.get_row_values(sheet_id, row_index)
            for column_index in range(
                grid.start_column_index, grid.end_column_index + 1
            ):
                row_offset = row_index - grid.start_row_index
                column_offset = column_index - grid.start_column_index
                format_value = _resolve_matrix_value(
                    normalized_formats, row_offset, column_offset
                )

                existing_data = _array_get(row_values, column_index)
                sheet_cell.assign(
                    sheet_id=sheet_id,
                    coords=CellInterface(row_index=row_index, column_index=column_index),
                    cell_data=existing_data,
                    locale=locale,
                    cell_xfs_registry=cell_xfs_map,
                )

                if replace:
                    sheet_cell.clear_user_entered_format()

                requires_recalc = False
                if isinstance(format_value, dict):
                    for fmt_key, fmt_val in format_value.items():
                        sheet_cell.set_user_entered_format(fmt_key, fmt_val)
                        if fmt_key == "numberFormat":
                            requires_recalc = True

                new_cell_data = sheet_cell.get_cell_data()
                logger.info(f"new_cell_data {sheet_cell.get_effective_cell_format()}")
                sheet_data_manager.set_cell_value(row_values, column_index, new_cell_data)
                update_cell_xfs_registry(cell_xfs_map, sheet_cell)

                if requires_recalc:
                    recalc_patches.append(
                        _create_recalc_patch(sheet_id, row_index, column_index)
                    )

    if len(recalc_patches):
        _append_recalc_entry(recalc_array, user_id, recalc_patches)

    logger.info(
        "change_formatting completed: sheet_id=%s updated_ranges=%s",
        sheet_id,
        len(range_list),
    )


def _normalize_format_source(
    value: CellFormatInput,
) -> Union[Dict[str, Any], List[List[Optional[Dict[str, Any]]]], None]:
    if value is None:
        return None

    if _is_sequence(value):
        seq_value = list(value)  # type: ignore[arg-type]
        if seq_value and _is_sequence(seq_value[0]):
            normalized_rows: List[List[Optional[Dict[str, Any]]]] = []
            for row in seq_value:
                normalized_rows.append(
                    [_normalize_single_format(cell) for cell in row]  # type: ignore[arg-type]
                )
            return normalized_rows
        return [[_normalize_single_format(cell) for cell in seq_value]]

    normalized = _normalize_single_format(value)
    return normalized


def _normalize_single_format(
    value: Union[CellFormat, Dict[str, Any], None]
) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, CellFormat):
        return value.model_dump(exclude_none=True)
    if hasattr(value, "model_dump"):
        try:
            return value.model_dump(exclude_none=True)  # type: ignore[call-arg]
        except Exception:
            pass
    if isinstance(value, dict):
        return value
    return None
