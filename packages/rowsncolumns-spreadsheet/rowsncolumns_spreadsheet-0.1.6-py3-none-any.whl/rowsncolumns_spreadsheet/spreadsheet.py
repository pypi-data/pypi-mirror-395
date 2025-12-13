"""
Main Spreadsheet class that provides a high-level interface for spreadsheet operations.
"""

from typing import List, Optional, Any, Dict
from .types import (
    SpreadsheetState,
    Sheet,
    CellData,
    RowData,
    GridRange,
    SelectionArea,
    CellInterface,
    Table,
)
from .operations import insert_row, delete_row, insert_column, delete_column


class Spreadsheet:
    """
    Main spreadsheet class providing high-level operations.

    This class manages the spreadsheet state and provides methods for common
    operations like inserting/deleting rows and columns, setting cell values, etc.
    """

    def __init__(self, initial_state: Optional[SpreadsheetState] = None):
        """
        Initialize a new spreadsheet.

        Args:
            initial_state: Optional initial state. If None, creates an empty spreadsheet.
        """
        if initial_state is None:
            # Create a default spreadsheet with one sheet
            default_sheet = Sheet(
                sheet_id=0,
                name="Sheet1",
                index=0,
                row_count=1000,
                column_count=26,
            )
            self._state = SpreadsheetState(
                sheets=[default_sheet],
                active_sheet_id=0,
            )
        else:
            self._state = initial_state

    @property
    def state(self) -> SpreadsheetState:
        """Get the current spreadsheet state."""
        return self._state

    def get_sheet(self, sheet_id: int) -> Optional[Sheet]:
        """Get a sheet by its ID."""
        for sheet in self._state.sheets:
            if sheet.sheet_id == sheet_id:
                return sheet
        return None

    def get_sheet_by_name(self, name: str) -> Optional[Sheet]:
        """Get a sheet by its name."""
        for sheet in self._state.sheets:
            if sheet.name == name:
                return sheet
        return None

    def create_sheet(
        self,
        name: str,
        row_count: int = 1000,
        column_count: int = 26,
    ) -> Sheet:
        """
        Create a new sheet.

        Args:
            name: Name of the new sheet
            row_count: Number of rows in the new sheet
            column_count: Number of columns in the new sheet

        Returns:
            The newly created sheet
        """
        # Find the next available sheet ID
        max_id = max((sheet.sheet_id for sheet in self._state.sheets), default=-1)
        new_sheet_id = max_id + 1

        # Find the next index
        max_index = max((sheet.index for sheet in self._state.sheets), default=-1)
        new_index = max_index + 1

        new_sheet = Sheet(
            sheet_id=new_sheet_id,
            name=name,
            index=new_index,
            row_count=row_count,
            column_count=column_count,
        )

        self._state.sheets.append(new_sheet)
        return new_sheet

    def insert_rows(
        self,
        sheet_id: int,
        reference_row_index: int,
        num_rows: int = 1,
    ) -> None:
        """
        Insert rows into a sheet.

        Args:
            sheet_id: ID of the sheet to modify
            reference_row_index: Index where rows should be inserted (0-based)
            num_rows: Number of rows to insert
        """
        self._state = insert_row(
            self._state,
            sheet_id,
            reference_row_index,
            num_rows,
        )

    def delete_rows(self, sheet_id: int, row_indices: List[int]) -> None:
        """
        Delete rows from a sheet.

        Args:
            sheet_id: ID of the sheet to modify
            row_indices: List of row indices to delete (0-based)
        """
        self._state = delete_row(self._state, sheet_id, row_indices)

    def insert_columns(
        self,
        sheet_id: int,
        reference_column_index: int,
        num_columns: int = 1,
    ) -> None:
        """
        Insert columns into a sheet.

        Args:
            sheet_id: ID of the sheet to modify
            reference_column_index: Index where columns should be inserted (0-based)
            num_columns: Number of columns to insert
        """
        self._state = insert_column(
            self._state,
            sheet_id,
            reference_column_index,
            num_columns,
        )

    def delete_columns(self, sheet_id: int, column_indices: List[int]) -> None:
        """
        Delete columns from a sheet.

        Args:
            sheet_id: ID of the sheet to modify
            column_indices: List of column indices to delete (0-based)
        """
        self._state = delete_column(self._state, sheet_id, column_indices)

    def set_cell_value(
        self,
        sheet_id: int,
        row_index: int,
        column_index: int,
        value: Any,
        formula: Optional[str] = None,
    ) -> None:
        """
        Set the value of a cell.

        Args:
            sheet_id: ID of the sheet
            row_index: Row index (0-based)
            column_index: Column index (0-based)
            value: Value to set
            formula: Optional formula
        """
        # Ensure sheet data exists
        if sheet_id not in self._state.sheet_data:
            self._state.sheet_data[sheet_id] = []

        sheet_data = self._state.sheet_data[sheet_id]

        # Ensure we have enough rows
        while len(sheet_data) <= row_index:
            sheet_data.append(None)

        # Initialize row as RowData if missing
        row = sheet_data[row_index]
        if row is None:
            row = RowData(values=[])
            sheet_data[row_index] = row
        # Type narrowing for static analyzers
        assert row is not None

        # Ensure the row has enough columns
        if row.values is None:
            row.values = []
        while len(row.values) <= column_index:
            row.values.append(None)

        # Set the cell value
        cell_data = CellData(value=value, formula=formula)
        row.values[column_index] = cell_data

    def get_cell_value(
        self,
        sheet_id: int,
        row_index: int,
        column_index: int,
    ) -> Any:
        """
        Get the value of a cell.

        Args:
            sheet_id: ID of the sheet
            row_index: Row index (0-based)
            column_index: Column index (0-based)

        Returns:
            The cell value, or None if the cell is empty
        """
        if sheet_id not in self._state.sheet_data:
            return None

        sheet_data = self._state.sheet_data[sheet_id]

        if row_index >= len(sheet_data):
            return None

        row = sheet_data[row_index]
        if row is None:
            return None
        values = row.values or []
        if column_index >= len(values):
            return None

        cell = values[column_index]
        return cell.value if cell else None

    def get_range_values(
        self,
        sheet_id: int,
        range_spec: GridRange,
    ) -> List[List[Any]]:
        """
        Get values from a range of cells.

        Args:
            sheet_id: ID of the sheet
            range_spec: The range to get values from

        Returns:
            2D list of cell values
        """
        result = []

        for row_index in range(range_spec.start_row_index, range_spec.end_row_index + 1):
            row_values = []
            for col_index in range(range_spec.start_column_index, range_spec.end_column_index + 1):
                value = self.get_cell_value(sheet_id, row_index, col_index)
                row_values.append(value)
            result.append(row_values)

        return result

    def set_range_values(
        self,
        sheet_id: int,
        range_spec: GridRange,
        values: List[List[Any]],
    ) -> None:
        """
        Set values for a range of cells.

        Args:
            sheet_id: ID of the sheet
            range_spec: The range to set values for
            values: 2D list of values to set
        """
        for i, row_index in enumerate(range(range_spec.start_row_index, range_spec.end_row_index + 1)):
            if i >= len(values):
                break

            row_values = values[i]
            for j, col_index in enumerate(range(range_spec.start_column_index, range_spec.end_column_index + 1)):
                if j >= len(row_values):
                    break

                self.set_cell_value(sheet_id, row_index, col_index, row_values[j])

    def get_selections(self, sheet_id: int) -> List[SelectionArea]:
        """Get current selections for a sheet."""
        return self._state.selections.get(sheet_id, [])

    def set_active_sheet(self, sheet_id: int) -> None:
        """Set the active sheet."""
        self._state.active_sheet_id = sheet_id

    def get_active_sheet_id(self) -> Optional[int]:
        """Get the ID of the active sheet."""
        return self._state.active_sheet_id
