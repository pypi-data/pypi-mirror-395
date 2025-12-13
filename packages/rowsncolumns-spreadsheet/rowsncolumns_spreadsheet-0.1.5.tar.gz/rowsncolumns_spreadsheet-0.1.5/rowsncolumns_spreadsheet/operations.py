"""
Spreadsheet operations like insert_row, delete_row, etc.

This module contains the core operations that can be performed on spreadsheets,
mirroring the TypeScript implementation but adapted for Python patterns.
"""

from typing import List, Optional, Dict, Any, Callable
from copy import deepcopy

from .types import (
    SpreadsheetState,
    Sheet,
    GridRange,
    SelectionArea,
    Table,
    CellData,
    RowData,
    Direction,
    HistoryEntry,
)
from .utils import (
    move_filter_view,
    move_merged_cells,
    clone_row_with_formatting,
    ensure_sheet_capacity,
    create_new_selections,
)


def insert_row(
    state: SpreadsheetState,
    sheet_id: int,
    reference_row_index: int,
    num_rows: int = 1,
    save_history: bool = True,
) -> SpreadsheetState:
    """
    Insert rows into a spreadsheet.

    Args:
        state: The current spreadsheet state
        sheet_id: ID of the sheet to modify
        reference_row_index: Index where rows should be inserted (0-based)
        num_rows: Number of rows to insert
        save_history: Whether to save this operation in history

    Returns:
        New spreadsheet state with rows inserted

    Raises:
        ValueError: If sheet_id is not found or reference_row_index is invalid
    """
    # Create a deep copy of the state to avoid mutations
    new_state = SpreadsheetState(**state.model_dump())

    # Find the target sheet
    target_sheet = None
    sheet_index = -1
    for i, sheet in enumerate(new_state.sheets):
        if sheet.sheet_id == sheet_id:
            target_sheet = sheet
            sheet_index = i
            break

    if target_sheet is None:
        raise ValueError(f"Sheet with ID {sheet_id} not found")

    if reference_row_index < 0 or reference_row_index > target_sheet.row_count:
        raise ValueError(f"Invalid reference_row_index: {reference_row_index}")

    # Update tables
    for table in new_state.tables:
        if table.sheet_id != sheet_id:
            continue

        # Move tables that are entirely below the insertion point
        if reference_row_index < table.range.start_row_index:
            move_filter_view(table, num_rows, Direction.DOWN)

        # Extend tables that contain the insertion point
        if (reference_row_index >= table.range.start_row_index and
            reference_row_index <= table.range.end_row_index):
            table.range.end_row_index += num_rows

    # Update sheet metadata
    # Update row metadata - shift existing metadata
    if target_sheet.row_metadata:
        new_row_metadata = {}
        for row_idx, metadata in target_sheet.row_metadata.items():
            if row_idx >= reference_row_index:
                new_row_metadata[row_idx + num_rows] = metadata
            else:
                new_row_metadata[row_idx] = metadata
        target_sheet.row_metadata = new_row_metadata

    # Update basic filter
    if target_sheet.basic_filter:
        if target_sheet.basic_filter.range.start_row_index >= reference_row_index:
            move_filter_view(target_sheet.basic_filter, num_rows, Direction.DOWN)
        elif (reference_row_index >= target_sheet.basic_filter.range.start_row_index and
              reference_row_index <= target_sheet.basic_filter.range.end_row_index):
            target_sheet.basic_filter.range.end_row_index += num_rows

    # Update frozen row count
    if (target_sheet.frozen_row_count is not None and
        reference_row_index <= target_sheet.frozen_row_count):
        target_sheet.frozen_row_count += num_rows

    # Update merges
    if target_sheet.merges:
        target_sheet.merges = move_merged_cells(
            target_sheet.merges,
            "row-insert",
            reference_row_index,
            num_rows
        )

    # Update row count
    target_sheet.row_count += num_rows

    # Update sheet data
    if sheet_id not in new_state.sheet_data:
        new_state.sheet_data[sheet_id] = []

    sheet_data = new_state.sheet_data[sheet_id]
    ensure_sheet_capacity(sheet_data, target_sheet.row_count, target_sheet.column_count)

    # Get the row to clone for formatting (the row at reference_row_index)
    source_row: Optional[RowData] = None
    if reference_row_index < len(sheet_data):
        source_row = sheet_data[reference_row_index]

    # Create new rows based on the source row's formatting
    new_rows: List[RowData] = []
    for _ in range(num_rows):
        new_row = clone_row_with_formatting(source_row)
        # Ensure the new row has the correct length
        if new_row.values is None:
            new_row.values = []
        while len(new_row.values) < target_sheet.column_count:
            new_row.values.append(None)
        new_rows.append(new_row)

    # Insert the new rows at the reference index
    for i, new_row in enumerate(new_rows):
        sheet_data.insert(reference_row_index + i, new_row)

    # Update selections to highlight the newly inserted rows
    new_selections = create_new_selections(
        reference_row_index,
        num_rows,
        target_sheet.column_count
    )
    new_state.selections[sheet_id] = new_selections

    # Save to history if requested
    if save_history:
        history_entry = HistoryEntry(
            operation="insert_row",
            timestamp=0.0,  # In a real implementation, use time.time()
            data={
                "sheet_id": sheet_id,
                "reference_row_index": reference_row_index,
                "num_rows": num_rows,
                "previous_row_count": target_sheet.row_count - num_rows,
            }
        )
        new_state.history.append(history_entry)

    return new_state


def delete_row(
    state: SpreadsheetState,
    sheet_id: int,
    row_indices: List[int],
    save_history: bool = True,
) -> SpreadsheetState:
    """
    Delete rows from a spreadsheet.

    Args:
        state: The current spreadsheet state
        sheet_id: ID of the sheet to modify
        row_indices: List of row indices to delete (0-based)
        save_history: Whether to save this operation in history

    Returns:
        New spreadsheet state with rows deleted
    """
    # Create a deep copy of the state to avoid mutations
    new_state = SpreadsheetState(**state.model_dump())

    # Find the target sheet
    target_sheet = None
    for sheet in new_state.sheets:
        if sheet.sheet_id == sheet_id:
            target_sheet = sheet
            break

    if target_sheet is None:
        raise ValueError(f"Sheet with ID {sheet_id} not found")

    # Sort indices in descending order to delete from bottom up
    sorted_indices = sorted(row_indices, reverse=True)

    # Validate all indices
    for idx in sorted_indices:
        if idx < 0 or idx >= target_sheet.row_count:
            raise ValueError(f"Invalid row index: {idx}")

    # Delete rows from sheet data
    if sheet_id in new_state.sheet_data:
        sheet_data = new_state.sheet_data[sheet_id]
        for idx in sorted_indices:
            if idx < len(sheet_data):
                del sheet_data[idx]

    # Update row count
    target_sheet.row_count -= len(row_indices)

    # Save to history if requested
    if save_history:
        history_entry = HistoryEntry(
            operation="delete_row",
            timestamp=0.0,  # In a real implementation, use time.time()
            data={
                "sheet_id": sheet_id,
                "row_indices": row_indices,
                "previous_row_count": target_sheet.row_count + len(row_indices),
            }
        )
        new_state.history.append(history_entry)

    return new_state


def insert_column(
    state: SpreadsheetState,
    sheet_id: int,
    reference_column_index: int,
    num_columns: int = 1,
    save_history: bool = True,
) -> SpreadsheetState:
    """
    Insert columns into a spreadsheet.

    Args:
        state: The current spreadsheet state
        sheet_id: ID of the sheet to modify
        reference_column_index: Index where columns should be inserted (0-based)
        num_columns: Number of columns to insert
        save_history: Whether to save this operation in history

    Returns:
        New spreadsheet state with columns inserted
    """
    # Create a deep copy of the state to avoid mutations
    new_state = SpreadsheetState(**state.model_dump())

    # Find the target sheet
    target_sheet = None
    for sheet in new_state.sheets:
        if sheet.sheet_id == sheet_id:
            target_sheet = sheet
            break

    if target_sheet is None:
        raise ValueError(f"Sheet with ID {sheet_id} not found")

    if reference_column_index < 0 or reference_column_index > target_sheet.column_count:
        raise ValueError(f"Invalid reference_column_index: {reference_column_index}")

    # Update column count
    target_sheet.column_count += num_columns

    # Update sheet data - insert columns in each row
    if sheet_id in new_state.sheet_data:
        sheet_data = new_state.sheet_data[sheet_id]
        for i, row in enumerate(sheet_data):
            if row is None:
                sheet_data[i] = RowData(values=[])
                row = sheet_data[i]
            if row.values is None:
                row.values = []
            # Insert None values for the new columns
            for _ in range(num_columns):
                row.values.insert(reference_column_index, None)

    # Save to history if requested
    if save_history:
        history_entry = HistoryEntry(
            operation="insert_column",
            timestamp=0.0,  # In a real implementation, use time.time()
            data={
                "sheet_id": sheet_id,
                "reference_column_index": reference_column_index,
                "num_columns": num_columns,
                "previous_column_count": target_sheet.column_count - num_columns,
            }
        )
        new_state.history.append(history_entry)

    return new_state


def delete_column(
    state: SpreadsheetState,
    sheet_id: int,
    column_indices: List[int],
    save_history: bool = True,
) -> SpreadsheetState:
    """
    Delete columns from a spreadsheet.

    Args:
        state: The current spreadsheet state
        sheet_id: ID of the sheet to modify
        column_indices: List of column indices to delete (0-based)
        save_history: Whether to save this operation in history

    Returns:
        New spreadsheet state with columns deleted
    """
    # Create a deep copy of the state to avoid mutations
    new_state = SpreadsheetState(**state.model_dump())

    # Find the target sheet
    target_sheet = None
    for sheet in new_state.sheets:
        if sheet.sheet_id == sheet_id:
            target_sheet = sheet
            break

    if target_sheet is None:
        raise ValueError(f"Sheet with ID {sheet_id} not found")

    # Sort indices in descending order to delete from right to left
    sorted_indices = sorted(column_indices, reverse=True)

    # Validate all indices
    for idx in sorted_indices:
        if idx < 0 or idx >= target_sheet.column_count:
            raise ValueError(f"Invalid column index: {idx}")

    # Delete columns from sheet data
    if sheet_id in new_state.sheet_data:
        sheet_data = new_state.sheet_data[sheet_id]
        for row in sheet_data:
            if row is None or row.values is None:
                continue
            for idx in sorted_indices:
                if idx < len(row.values):
                    del row.values[idx]

    # Update column count
    target_sheet.column_count -= len(column_indices)

    # Save to history if requested
    if save_history:
        history_entry = HistoryEntry(
            operation="delete_column",
            timestamp=0.0,  # In a real implementation, use time.time()
            data={
                "sheet_id": sheet_id,
                "column_indices": column_indices,
                "previous_column_count": target_sheet.column_count + len(column_indices),
            }
        )
        new_state.history.append(history_entry)

    return new_state
