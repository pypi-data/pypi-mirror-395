"""
Utility functions for spreadsheet operations.
"""

from typing import List, Optional, Dict, Any
from .types import (
    GridRange,
    SelectionArea,
    FilterView,
    MergedCell,
    Direction,
    CellData,
    RowData,
    RowMetadata,
    ColumnMetadata,
)


def move_filter_view(filter_view: FilterView, delta: int, direction: Direction) -> None:
    """Move a filter view by the specified delta in the given direction."""
    if direction == Direction.DOWN:
        filter_view.range.start_row_index += delta
        filter_view.range.end_row_index += delta
    elif direction == Direction.UP:
        filter_view.range.start_row_index -= delta
        filter_view.range.end_row_index -= delta
    elif direction == Direction.RIGHT:
        filter_view.range.start_column_index += delta
        filter_view.range.end_column_index += delta
    elif direction == Direction.LEFT:
        filter_view.range.start_column_index -= delta
        filter_view.range.end_column_index -= delta


def move_merged_cells(
    merges: List[MergedCell],
    operation: str,
    reference_index: int,
    num_rows_or_cols: int = 1
) -> List[MergedCell]:
    """
    Move merged cells based on row/column insertion or deletion.

    Args:
        merges: List of merged cell ranges
        operation: Type of operation ('row-insert', 'row-delete', 'column-insert', 'column-delete')
        reference_index: The index where the operation occurs
        num_rows_or_cols: Number of rows/columns being inserted or deleted
    """
    updated_merges = []

    for merge in merges:
        updated_range = GridRange(**merge.range.model_dump())

        if operation == "row-insert":
            if updated_range.start_row_index >= reference_index:
                updated_range.start_row_index += num_rows_or_cols
                updated_range.end_row_index += num_rows_or_cols
            elif updated_range.end_row_index >= reference_index:
                updated_range.end_row_index += num_rows_or_cols

        elif operation == "row-delete":
            if updated_range.start_row_index >= reference_index + num_rows_or_cols:
                updated_range.start_row_index -= num_rows_or_cols
                updated_range.end_row_index -= num_rows_or_cols
            elif updated_range.end_row_index >= reference_index:
                # Merge overlaps with deleted rows - adjust or remove
                if updated_range.start_row_index < reference_index:
                    updated_range.end_row_index = min(
                        updated_range.end_row_index - num_rows_or_cols,
                        reference_index - 1
                    )
                else:
                    # Entire merge is in deleted range - skip it
                    continue

        elif operation == "column-insert":
            if updated_range.start_column_index >= reference_index:
                updated_range.start_column_index += num_rows_or_cols
                updated_range.end_column_index += num_rows_or_cols
            elif updated_range.end_column_index >= reference_index:
                updated_range.end_column_index += num_rows_or_cols

        elif operation == "column-delete":
            if updated_range.start_column_index >= reference_index + num_rows_or_cols:
                updated_range.start_column_index -= num_rows_or_cols
                updated_range.end_column_index -= num_rows_or_cols
            elif updated_range.end_column_index >= reference_index:
                # Merge overlaps with deleted columns - adjust or remove
                if updated_range.start_column_index < reference_index:
                    updated_range.end_column_index = min(
                        updated_range.end_column_index - num_rows_or_cols,
                        reference_index - 1
                    )
                else:
                    # Entire merge is in deleted range - skip it
                    continue

        # Only add if the range is still valid
        if (updated_range.start_row_index <= updated_range.end_row_index and
            updated_range.start_column_index <= updated_range.end_column_index):
            updated_merges.append(MergedCell(range=updated_range))

    return updated_merges


def clone_row_with_formatting(
    row_data: Optional[RowData]
) -> RowData:
    """
    Clone a row with its formatting, creating a new row that can be inserted.
    Mirrors the idea of copying formatting but resetting values.
    """
    if not row_data or not row_data.values:
        return RowData(values=[])

    cloned_values: List[Optional[CellData]] = []
    for cell in row_data.values:
        if cell is None:
            cloned_values.append(None)
        else:
            # Create a new cell with the same formatting; reset content
            cloned_cell = CellData(
                value=None,
                formula=None,
                format=cell.format.copy() if cell.format else None,
                user_entered_format=(
                    cell.user_entered_format.copy() if isinstance(cell.user_entered_format, dict) else
                    (cell.format.copy() if isinstance(cell.format, dict) else None)
                ),
                effective_format=None,
            )
            cloned_values.append(cloned_cell)

    return RowData(values=cloned_values)


def ensure_sheet_capacity(
    sheet_data: List[Optional[RowData]],
    row_count: int,
    column_count: int
) -> None:
    """
    Ensure the sheet data has enough capacity for the specified dimensions, where
    each row is a RowData with an optional `values` list.
    """
    # Ensure we have enough rows (pad with None rows to match TS's `null` rows)
    while len(sheet_data) < row_count:
        sheet_data.append(None)

    # Ensure each row has enough columns in its values array
    for i, row in enumerate(sheet_data):
        if row is None:
            # Lazily initialize an empty RowData with values
            sheet_data[i] = RowData(values=[None for _ in range(column_count)])
        else:
            if row.values is None:
                row.values = []
            while len(row.values) < column_count:
                row.values.append(None)


def create_new_selections(
    reference_index: int,
    num_rows: int,
    column_count: int
) -> List[SelectionArea]:
    """
    Create selection areas for newly inserted rows.
    """
    return [
        SelectionArea(
            range=GridRange(
                start_row_index=reference_index,
                start_column_index=0,
                end_row_index=reference_index + num_rows - 1,
                end_column_index=column_count - 1,
            )
        )
    ]
