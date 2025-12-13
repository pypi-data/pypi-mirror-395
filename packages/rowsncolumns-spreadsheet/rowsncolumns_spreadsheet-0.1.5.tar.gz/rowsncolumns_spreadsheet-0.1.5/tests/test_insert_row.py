"""
Tests for the insert_row functionality.
"""

import pytest
from rowsncolumns_spreadsheet import (
    Spreadsheet,
    Sheet,
    SpreadsheetState,
    GridRange,
    CellData,
    Table,
    FilterView,
    MergedCell,
)
from rowsncolumns_spreadsheet.operations import insert_row


class TestInsertRow:
    """Test cases for the insert_row operation."""

    def test_insert_single_row_empty_sheet(self):
        """Test inserting a single row into an empty sheet."""
        # Create a simple spreadsheet
        spreadsheet = Spreadsheet()
        initial_sheet = spreadsheet.get_sheet(0)
        initial_row_count = initial_sheet.row_count

        # Insert a row at the beginning
        spreadsheet.insert_rows(sheet_id=0, reference_row_index=0, num_rows=1)

        # Verify the row count increased
        updated_sheet = spreadsheet.get_sheet(0)
        assert updated_sheet.row_count == initial_row_count + 1

        # Verify selections were updated
        selections = spreadsheet.get_selections(0)
        assert len(selections) == 1
        assert selections[0].range.start_row_index == 0
        assert selections[0].range.end_row_index == 0

    def test_insert_multiple_rows(self):
        """Test inserting multiple rows."""
        spreadsheet = Spreadsheet()
        initial_sheet = spreadsheet.get_sheet(0)
        initial_row_count = initial_sheet.row_count

        # Insert 3 rows at index 5
        spreadsheet.insert_rows(sheet_id=0, reference_row_index=5, num_rows=3)

        # Verify the row count increased by 3
        updated_sheet = spreadsheet.get_sheet(0)
        assert updated_sheet.row_count == initial_row_count + 3

        # Verify selections span the 3 new rows
        selections = spreadsheet.get_selections(0)
        assert len(selections) == 1
        assert selections[0].range.start_row_index == 5
        assert selections[0].range.end_row_index == 7

    def test_insert_row_with_existing_data(self):
        """Test inserting a row into a sheet with existing data."""
        spreadsheet = Spreadsheet()

        # Set some initial data
        spreadsheet.set_cell_value(0, 0, 0, "A1")
        spreadsheet.set_cell_value(0, 1, 0, "A2")
        spreadsheet.set_cell_value(0, 2, 0, "A3")

        # Insert a row at index 1 (between A1 and A2)
        spreadsheet.insert_rows(sheet_id=0, reference_row_index=1, num_rows=1)

        # Verify the data shifted correctly
        assert spreadsheet.get_cell_value(0, 0, 0) == "A1"  # A1 stays in place
        assert spreadsheet.get_cell_value(0, 1, 0) is None  # New row is empty
        assert spreadsheet.get_cell_value(0, 2, 0) == "A2"  # A2 moved down
        assert spreadsheet.get_cell_value(0, 3, 0) == "A3"  # A3 moved down

    def test_insert_row_updates_frozen_count(self):
        """Test that inserting rows updates frozen row count correctly."""
        # Create a sheet with frozen rows
        sheet = Sheet(
            sheet_id=0,
            name="Test",
            index=0,
            row_count=100,
            column_count=26,
            frozen_row_count=2,
        )
        state = SpreadsheetState(sheets=[sheet])

        # Insert a row before the frozen area
        new_state = insert_row(state, sheet_id=0, reference_row_index=1, num_rows=1)

        # Frozen count should increase
        updated_sheet = new_state.sheets[0]
        assert updated_sheet.frozen_row_count == 3

    def test_insert_row_updates_tables(self):
        """Test that inserting rows updates table ranges correctly."""
        # Create a sheet with a table
        sheet = Sheet(sheet_id=0, name="Test", index=0)
        table = Table(
            sheet_id=0,
            range=GridRange(
                start_row_index=5,
                end_row_index=10,
                start_column_index=0,
                end_column_index=5,
            ),
            name="TestTable",
        )
        state = SpreadsheetState(sheets=[sheet], tables=[table])

        # Insert rows before the table
        new_state = insert_row(state, sheet_id=0, reference_row_index=3, num_rows=2)

        # Table should move down
        updated_table = new_state.tables[0]
        assert updated_table.range.start_row_index == 7
        assert updated_table.range.end_row_index == 12

    def test_insert_row_extends_table(self):
        """Test that inserting rows within a table extends the table."""
        # Create a sheet with a table
        sheet = Sheet(sheet_id=0, name="Test", index=0)
        table = Table(
            sheet_id=0,
            range=GridRange(
                start_row_index=5,
                end_row_index=10,
                start_column_index=0,
                end_column_index=5,
            ),
            name="TestTable",
        )
        state = SpreadsheetState(sheets=[sheet], tables=[table])

        # Insert rows within the table
        new_state = insert_row(state, sheet_id=0, reference_row_index=7, num_rows=2)

        # Table should extend to include new rows
        updated_table = new_state.tables[0]
        assert updated_table.range.start_row_index == 5  # Start unchanged
        assert updated_table.range.end_row_index == 12   # End extended by 2

    def test_insert_row_updates_basic_filter(self):
        """Test that inserting rows updates basic filter correctly."""
        # Create a sheet with a basic filter
        filter_view = FilterView(
            range=GridRange(
                start_row_index=2,
                end_row_index=8,
                start_column_index=0,
                end_column_index=5,
            )
        )
        sheet = Sheet(
            sheet_id=0,
            name="Test",
            index=0,
            basic_filter=filter_view,
        )
        state = SpreadsheetState(sheets=[sheet])

        # Insert rows before the filter
        new_state = insert_row(state, sheet_id=0, reference_row_index=1, num_rows=2)

        # Filter should move down
        updated_filter = new_state.sheets[0].basic_filter
        assert updated_filter.range.start_row_index == 4
        assert updated_filter.range.end_row_index == 10

    def test_insert_row_updates_merges(self):
        """Test that inserting rows updates merged cell ranges."""
        # Create a sheet with merged cells
        merge = MergedCell(
            range=GridRange(
                start_row_index=3,
                end_row_index=5,
                start_column_index=1,
                end_column_index=3,
            )
        )
        sheet = Sheet(
            sheet_id=0,
            name="Test",
            index=0,
            merges=[merge],
        )
        state = SpreadsheetState(sheets=[sheet])

        # Insert rows before the merge
        new_state = insert_row(state, sheet_id=0, reference_row_index=2, num_rows=1)

        # Merge should move down
        updated_merge = new_state.sheets[0].merges[0]
        assert updated_merge.range.start_row_index == 4
        assert updated_merge.range.end_row_index == 6

    def test_insert_row_invalid_sheet_id(self):
        """Test that inserting into non-existent sheet raises error."""
        state = SpreadsheetState(sheets=[])

        with pytest.raises(ValueError, match="Sheet with ID 999 not found"):
            insert_row(state, sheet_id=999, reference_row_index=0, num_rows=1)

    def test_insert_row_invalid_reference_index(self):
        """Test that invalid reference index raises error."""
        sheet = Sheet(sheet_id=0, name="Test", index=0, row_count=100)
        state = SpreadsheetState(sheets=[sheet])

        # Test negative index
        with pytest.raises(ValueError, match="Invalid reference_row_index: -1"):
            insert_row(state, sheet_id=0, reference_row_index=-1, num_rows=1)

        # Test index beyond row count
        with pytest.raises(ValueError, match="Invalid reference_row_index: 101"):
            insert_row(state, sheet_id=0, reference_row_index=101, num_rows=1)

    def test_insert_row_saves_history(self):
        """Test that insert_row operation is saved to history."""
        sheet = Sheet(sheet_id=0, name="Test", index=0)
        state = SpreadsheetState(sheets=[sheet])

        # Perform insert with history enabled
        new_state = insert_row(
            state,
            sheet_id=0,
            reference_row_index=5,
            num_rows=2,
            save_history=True,
        )

        # Verify history entry was created
        assert len(new_state.history) == 1
        history_entry = new_state.history[0]
        assert history_entry.operation == "insert_row"
        assert history_entry.data["sheet_id"] == 0
        assert history_entry.data["reference_row_index"] == 5
        assert history_entry.data["num_rows"] == 2

    def test_insert_row_no_history(self):
        """Test that insert_row can skip history saving."""
        sheet = Sheet(sheet_id=0, name="Test", index=0)
        state = SpreadsheetState(sheets=[sheet])

        # Perform insert with history disabled
        new_state = insert_row(
            state,
            sheet_id=0,
            reference_row_index=5,
            num_rows=2,
            save_history=False,
        )

        # Verify no history entry was created
        assert len(new_state.history) == 0