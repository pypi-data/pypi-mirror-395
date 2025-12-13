"""
Tests for apply_fill functionality.

This test module covers the fill operation functionality including:
- Fill down operation
- Fill up operation
- Fill right operation
- Fill left operation
- Direction detection
- Helper functions
- Pattern detection and auto-fill
"""

import pytest
from typing import List
from rowsncolumns_spreadsheet import (
    CellData,
    CellInterface,
    SelectionArea,
    GridRange,
    Direction,
    SpreadsheetState,
    Sheet,
    ExtendedValue,
    apply_fill,
    ApplyFillConfig,
)
from rowsncolumns_spreadsheet.interface.apply_fill import (
    get_fill_direction,
    selection_from_active_cell,
    create_sheet_cell_identifier,
    create_sheet_draft,
)
from rowsncolumns_spreadsheet.interface.fill import (
    detect_fill_type,
    generate_fill_values,
    AutoFillType,
)


# Helper function for tests
def create_test_config(state: SpreadsheetState, recalc_operations: List = None):
    """Create a test configuration with common callbacks."""
    if recalc_operations is None:
        recalc_operations = []

    def on_change(callback):
        return callback(state)

    def enqueue_calc(operation):
        recalc_operations.append(operation)

    def create_history():
        def save_history(patch):
            pass
        return save_history

    def get_cell_data(sheet_id: int, row_index: int, column_index: int):
        if sheet_id in state.sheet_data and row_index < len(state.sheet_data[sheet_id]):
            row = state.sheet_data[sheet_id][row_index]
            if row and 'values' in row and column_index < len(row['values']):
                return row['values'][column_index]
        return None

    def get_effective_value(sheet_id: int, row_index: int, column_index: int):
        cell_data = get_cell_data(sheet_id, row_index, column_index)
        if cell_data and isinstance(cell_data, dict):
            ev = cell_data.get('ev', {})
            if isinstance(ev, dict):
                return ev.get('numberValue') or ev.get('stringValue') or ev.get('boolValue')
        return None

    return ApplyFillConfig(
        locale="en-US",
        on_change_sheet_data=on_change,
        enqueue_calculation=enqueue_calc,
        create_history=create_history,
        get_cell_data=get_cell_data,
        get_effective_value=get_effective_value,
    ), recalc_operations


class TestHelperFunctions:
    """Test helper functions used by apply_fill."""

    def test_get_fill_direction_down(self):
        """Test detecting fill direction downward."""
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=2,
                start_column_index=0,
                end_column_index=0,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=5,
                start_column_index=0,
                end_column_index=0,
            )
        )

        direction = get_fill_direction(fill_selection, selection)
        assert direction == Direction.DOWN

    def test_get_fill_direction_up(self):
        """Test detecting fill direction upward."""
        selection = SelectionArea(
            range=GridRange(
                start_row_index=5,
                end_row_index=7,
                start_column_index=0,
                end_column_index=0,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=7,
                start_column_index=0,
                end_column_index=0,
            )
        )

        direction = get_fill_direction(fill_selection, selection)
        assert direction == Direction.UP

    def test_get_fill_direction_right(self):
        """Test detecting fill direction to the right."""
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=2,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=5,
            )
        )

        direction = get_fill_direction(fill_selection, selection)
        assert direction == Direction.RIGHT

    def test_get_fill_direction_left(self):
        """Test detecting fill direction to the left."""
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=5,
                end_column_index=7,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=7,
            )
        )

        direction = get_fill_direction(fill_selection, selection)
        assert direction == Direction.LEFT

    def test_selection_from_active_cell(self):
        """Test creating selection from active cell."""
        active_cell = CellInterface(row_index=3, column_index=5)
        selections = selection_from_active_cell(active_cell)

        assert len(selections) == 1
        assert selections[0].range.start_row_index == 3
        assert selections[0].range.end_row_index == 3
        assert selections[0].range.start_column_index == 5
        assert selections[0].range.end_column_index == 5

    def test_create_sheet_cell_identifier(self):
        """Test creating unique cell identifiers."""
        identifier = create_sheet_cell_identifier(1, 5, 10)
        assert identifier == "1:5:10"

        identifier2 = create_sheet_cell_identifier(0, 0, 0)
        assert identifier2 == "0:0:0"


class TestFillPatternDetection:
    """Test pattern detection for auto-fill."""

    def test_detect_numeric_series(self):
        """Test detecting numeric series."""
        data = [[1, 2, 3]]
        fill_type = detect_fill_type(data)
        assert fill_type == AutoFillType.FILL_SERIES

    def test_detect_copy_single_value(self):
        """Test detecting single value (should copy)."""
        data = [[5]]
        fill_type = detect_fill_type(data)
        assert fill_type == AutoFillType.FILL_COPY

    def test_detect_day_names(self):
        """Test detecting day names."""
        data = [["Monday", "Tuesday"]]
        fill_type = detect_fill_type(data)
        assert fill_type == AutoFillType.FILL_DAYS

    def test_detect_month_names(self):
        """Test detecting month names."""
        data = [["January", "February"]]
        fill_type = detect_fill_type(data)
        assert fill_type == AutoFillType.FILL_MONTHS

    def test_generate_numeric_series(self):
        """Test generating numeric series."""
        source = [1, 2, 3]
        result = generate_fill_values(source, AutoFillType.FILL_SERIES, 3)
        assert len(result) == 3
        assert result[0] == 4
        assert result[1] == 5
        assert result[2] == 6

    def test_generate_copy_values(self):
        """Test generating copied values."""
        source = ["A", "B"]
        result = generate_fill_values(source, AutoFillType.FILL_COPY, 4)
        assert len(result) == 4
        assert result == ["A", "B", "A", "B"]

    def test_generate_day_names(self):
        """Test generating day names."""
        source = ["Mon"]
        result = generate_fill_values(source, AutoFillType.FILL_DAYS, 3)
        assert len(result) == 3
        # Should continue with Tue, Wed, Thu
        assert "Tue" in result[0] or "tue" in result[0].lower()


class TestApplyFillDown:
    """Test apply_fill with downward direction."""

    @pytest.mark.asyncio
    async def test_fill_down_simple_series(self):
        """Test filling down with a numeric series."""
        state = SpreadsheetState(
            sheets=[Sheet(sheet_id=0, name="Sheet1", index=0)],
            sheet_data={
                0: [
                    {'values': [
                        {'ue': {'stringValue': '1'}, 'ev': {'numberValue': 1.0}, 'fv': '1'}
                    ]},
                    {'values': [
                        {'ue': {'stringValue': '2'}, 'ev': {'numberValue': 2.0}, 'fv': '2'}
                    ]},
                ]
            },
        )

        config, recalc_operations = create_test_config(state)

        active_cell = CellInterface(row_index=0, column_index=0)
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=1,
                start_column_index=0,
                end_column_index=0,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=4,
                start_column_index=0,
                end_column_index=0,
            )
        )

        await apply_fill(
            config=config,
            sheet_id=0,
            active_cell=active_cell,
            fill_selection=fill_selection,
            selections=[selection],
        )

        # Should fill 3 cells (rows 2, 3, 4)
        assert len(recalc_operations) == 3


class TestApplyFillUp:
    """Test apply_fill with upward direction."""

    @pytest.mark.asyncio
    async def test_fill_up_simple(self):
        """Test filling up."""
        state = SpreadsheetState(
            sheets=[Sheet(sheet_id=0, name="Sheet1", index=0)],
            sheet_data={
                0: [
                    None,
                    None,
                    None,
                    None,
                    None,
                    {'values': [
                        {'ue': {'stringValue': '5'}, 'ev': {'numberValue': 5.0}, 'fv': '5'}
                    ]},
                ]
            },
        )

        config, recalc_operations = create_test_config(state)

        active_cell = CellInterface(row_index=5, column_index=0)
        selection = SelectionArea(
            range=GridRange(
                start_row_index=5,
                end_row_index=5,
                start_column_index=0,
                end_column_index=0,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=2,
                end_row_index=5,
                start_column_index=0,
                end_column_index=0,
            )
        )

        await apply_fill(
            config=config,
            sheet_id=0,
            active_cell=active_cell,
            fill_selection=fill_selection,
            selections=[selection],
        )

        # Should fill 3 cells (rows 4, 3, 2)
        assert len(recalc_operations) == 3


class TestApplyFillRight:
    """Test apply_fill with rightward direction."""

    @pytest.mark.asyncio
    async def test_fill_right_simple(self):
        """Test filling right."""
        state = SpreadsheetState(
            sheets=[Sheet(sheet_id=0, name="Sheet1", index=0)],
            sheet_data={
                0: [
                    {'values': [
                        {'ue': {'stringValue': 'A'}, 'ev': {'stringValue': 'A'}, 'fv': 'A'}
                    ]},
                ]
            },
        )

        config, recalc_operations = create_test_config(state)

        active_cell = CellInterface(row_index=0, column_index=0)
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=0,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=3,
            )
        )

        await apply_fill(
            config=config,
            sheet_id=0,
            active_cell=active_cell,
            fill_selection=fill_selection,
            selections=[selection],
        )

        # Should fill 3 cells (columns 1, 2, 3)
        assert len(recalc_operations) == 3


class TestApplyFillLeft:
    """Test apply_fill with leftward direction."""

    @pytest.mark.asyncio
    async def test_fill_left_simple(self):
        """Test filling left."""
        state = SpreadsheetState(
            sheets=[Sheet(sheet_id=0, name="Sheet1", index=0)],
            sheet_data={
                0: [
                    {'values': [
                        None, None, None, None, None,
                        {'ue': {'stringValue': 'Z'}, 'ev': {'stringValue': 'Z'}, 'fv': 'Z'}
                    ]},
                ]
            },
        )

        config, recalc_operations = create_test_config(state)

        active_cell = CellInterface(row_index=0, column_index=5)
        selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=5,
                end_column_index=5,
            )
        )
        fill_selection = SelectionArea(
            range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=2,
                end_column_index=5,
            )
        )

        await apply_fill(
            config=config,
            sheet_id=0,
            active_cell=active_cell,
            fill_selection=fill_selection,
            selections=[selection],
        )

        # Should fill 3 cells (columns 4, 3, 2)
        assert len(recalc_operations) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
