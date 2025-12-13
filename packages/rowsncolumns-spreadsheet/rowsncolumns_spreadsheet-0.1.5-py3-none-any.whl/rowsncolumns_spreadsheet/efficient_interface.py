"""
Memory-efficient SpreadsheetInterface that tracks changes incrementally.

This version avoids storing full state copies and only tracks actual changes,
making it much more memory-efficient for large spreadsheets.
"""

from typing import List, Optional, Dict, Any, Tuple
import copy

from .types import SpreadsheetState, Sheet, CellData, RowData, GridRange, SelectionArea
from .operations import insert_row, delete_row, insert_column, delete_column
from .patches import SpreadsheetPatch
from .efficient_patches import EfficientPatchTracker, ChangeType


class EfficientSpreadsheetInterface:
    """
    Memory-efficient interface for spreadsheet operations with YJS patch tracking.

    This version uses incremental change tracking instead of full state comparison,
    dramatically reducing memory usage for large spreadsheets.
    """

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the spreadsheet interface.

        Args:
            initial_data: Initial data loaded from YJS document
        """
        if initial_data:
            self._state = self._load_from_yjs_data(initial_data)
        else:
            # Create default state
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

        # Use efficient patch tracker
        self._patch_tracker = EfficientPatchTracker()

    @property
    def state(self) -> SpreadsheetState:
        """Get the current spreadsheet state."""
        return self._state

    def clear_patches(self) -> None:
        """Clear the accumulated patches."""
        self._patch_tracker.clear_changes()

    def get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage statistics."""
        return self._patch_tracker.get_memory_usage_estimate()

    def _load_from_yjs_data(self, data: Dict[str, Any]) -> SpreadsheetState:
        """Load spreadsheet state from YJS document data."""
        # Convert YJS data to SpreadsheetState
        sheets_data = data.get('sheets', [])
        sheets = []

        for sheet_data in sheets_data:
            sheet = Sheet(**sheet_data)
            sheets.append(sheet)

        # Load other data
        sheet_data = data.get('sheetData', {})
        # Convert string keys to int keys
        int_sheet_data: Dict[int, List[Optional[RowData]]] = {}
        for sheet_id_str, rows in sheet_data.items():
            sheet_id = int(sheet_id_str)
            converted_rows: List[Optional[RowData]] = []
            for row in rows:
                if row is None:
                    converted_rows.append(None)
                    continue
                converted_values = []
                for cell in row.get('values', []):
                    if cell is None:
                        converted_values.append(None)
                    else:
                        converted_values.append(CellData(**cell))
                converted_rows.append(RowData(values=converted_values))
            int_sheet_data[sheet_id] = converted_rows

        return SpreadsheetState(
            sheets=sheets,
            sheet_data=int_sheet_data,
            tables=data.get('tables', []),
            active_sheet_id=data.get('activeSheetId'),
            selections=data.get('selections', {}),
        )

    def insert_rows(
        self,
        sheet_id: int,
        reference_row_index: int,
        num_rows: int = 1,
    ) -> None:
        """Insert rows and track patches efficiently."""
        # Get the target sheet for old values
        target_sheet = None
        for sheet in self._state.sheets:
            if sheet.sheet_id == sheet_id:
                target_sheet = sheet
                break

        if target_sheet is None:
            raise ValueError(f"Sheet with ID {sheet_id} not found")

        old_row_count = target_sheet.row_count

        # Record the change BEFORE performing the operation
        self._patch_tracker.record_row_insertion(
            sheet_id=sheet_id,
            reference_row_index=reference_row_index,
            num_rows=num_rows,
            old_row_count=old_row_count
        )

        # Perform the operation
        new_state = insert_row(
            self._state,
            sheet_id,
            reference_row_index,
            num_rows,
            save_history=False,
        )

        # Update state
        self._state = new_state

    def delete_rows(self, sheet_id: int, row_indices: List[int]) -> None:
        """Delete rows and track patches efficiently."""
        # Get old data before deletion
        target_sheet = None
        for sheet in self._state.sheets:
            if sheet.sheet_id == sheet_id:
                target_sheet = sheet
                break

        if target_sheet is None:
            raise ValueError(f"Sheet with ID {sheet_id} not found")

        old_row_count = target_sheet.row_count

        # Get data that will be deleted (for undo)
        deleted_data = []
        if sheet_id in self._state.sheet_data:
            sheet_data = self._state.sheet_data[sheet_id]
            for row_idx in sorted(row_indices):
                if row_idx < len(sheet_data):
                    deleted_data.append(sheet_data[row_idx])

        # Record the change
        self._patch_tracker.record_row_deletion(
            sheet_id=sheet_id,
            row_indices=row_indices,
            old_row_count=old_row_count,
            deleted_data=deleted_data
        )

        # Perform the operation
        new_state = delete_row(self._state, sheet_id, row_indices, save_history=False)
        self._state = new_state

    def insert_columns(
        self,
        sheet_id: int,
        reference_column_index: int,
        num_columns: int = 1,
    ) -> None:
        """Insert columns and track patches efficiently."""
        # Get the target sheet for old values
        target_sheet = None
        for sheet in self._state.sheets:
            if sheet.sheet_id == sheet_id:
                target_sheet = sheet
                break

        if target_sheet is None:
            raise ValueError(f"Sheet with ID {sheet_id} not found")

        old_column_count = target_sheet.column_count

        # Record the change
        self._patch_tracker.record_column_insertion(
            sheet_id=sheet_id,
            reference_column_index=reference_column_index,
            num_columns=num_columns,
            old_column_count=old_column_count
        )

        # Perform the operation
        new_state = insert_column(
            self._state, sheet_id, reference_column_index, num_columns, save_history=False
        )
        self._state = new_state

    def delete_columns(self, sheet_id: int, column_indices: List[int]) -> None:
        """Delete columns and track patches efficiently."""
        # Similar implementation to delete_rows but for columns
        target_sheet = None
        for sheet in self._state.sheets:
            if sheet.sheet_id == sheet_id:
                target_sheet = sheet
                break

        if target_sheet is None:
            raise ValueError(f"Sheet with ID {sheet_id} not found")

        old_column_count = target_sheet.column_count

        # Record the change (simplified for this example)
        for col_idx in column_indices:
            self._patch_tracker.record_sheet_metadata_change(
                sheet_id=sheet_id,
                property_name="column_count",
                old_value=old_column_count,
                new_value=old_column_count - len(column_indices)
            )

        # Perform the operation
        new_state = delete_column(self._state, sheet_id, column_indices, save_history=False)
        self._state = new_state

    def set_cell_value(
        self,
        sheet_id: int,
        row_index: int,
        column_index: int,
        value: Any,
        formula: Optional[str] = None,
    ) -> None:
        """Set cell value and track patches efficiently."""
        # Get old value for change tracking
        old_value = self.get_cell_value(sheet_id, row_index, column_index)

        # Create new cell data
        new_cell_data = CellData(value=value, formula=formula)

        # Record the change
        self._patch_tracker.record_cell_change(
            sheet_id=sheet_id,
            row_index=row_index,
            column_index=column_index,
            old_value=old_value,
            new_value=new_cell_data
        )

        # Ensure sheet data exists
        if sheet_id not in self._state.sheet_data:
            self._state.sheet_data[sheet_id] = []

        sheet_data = self._state.sheet_data[sheet_id]

        # Ensure we have enough rows
        while len(sheet_data) <= row_index:
            sheet_data.append(None)

        # Ensure the row exists and has values
        row = sheet_data[row_index]
        if row is None:
            row = RowData(values=[])
            sheet_data[row_index] = row
        # Type narrowing for static analyzers
        assert row is not None
        if row.values is None:
            row.values = []
        while len(row.values) <= column_index:
            row.values.append(None)

        # Set the cell value
        row.values[column_index] = new_cell_data

    def get_cell_value(self, sheet_id: int, row_index: int, column_index: int) -> Any:
        """Get cell value."""
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
        return cell if cell else None

    def generate_yjs_patches(self) -> List[Dict[str, Any]]:
        """Generate patches in a format suitable for YJS."""
        json_patches = self._patch_tracker.generate_json_patches()
        return [patch.to_dict() for patch in json_patches]

    def get_patch_tuples(
        self, operation_type: str = "redo"
    ) -> List[Tuple[SpreadsheetPatch, str]]:
        """Get patches as tuples for YJS application."""
        spreadsheet_patch = self._patch_tracker.generate_spreadsheet_patch()
        return [(spreadsheet_patch, operation_type)]

    def to_yjs_data(self) -> Dict[str, Any]:
        """Convert current state to YJS data format."""
        # This is the same as the original implementation
        # We only serialize when explicitly requested
        result = {
            "sheets": [sheet.model_dump() for sheet in self._state.sheets],
            "tables": [table.model_dump() for table in self._state.tables],
            "activeSheetId": self._state.active_sheet_id,
            "selections": self._state.selections,
        }

        # Convert sheet data with string keys
        string_sheet_data: Dict[str, Any] = {}
        for sheet_id, rows in self._state.sheet_data.items():
            serialized_rows = []
            for row in rows:
                if row is None:
                    serialized_rows.append(None)
                else:
                    serialized_row = []
                    for cell in (row.values or []):
                        if cell is None:
                            serialized_row.append(None)
                        else:
                            serialized_row.append(cell.model_dump())
                    serialized_rows.append({"values": serialized_row})
            string_sheet_data[str(sheet_id)] = serialized_rows

        result["sheetData"] = string_sheet_data
        return result

    def reset_tracking(self) -> None:
        """Reset change tracking."""
        self._patch_tracker.clear_changes()

    def batch_operations(self, operations: List[callable]) -> None:
        """
        Perform multiple operations in a batch and generate patches efficiently.

        This is useful for complex operations that involve multiple changes.
        """
        # Disable tracking temporarily
        self._patch_tracker.disable_tracking()

        try:
            # Perform all operations
            for operation in operations:
                operation()
        finally:
            # Re-enable tracking
            self._patch_tracker.enable_tracking()

        # Now track the batch as a single change
        # (This would require more sophisticated implementation for real use)


# Example usage comparison
def demonstrate_memory_efficiency():
    """
    Demonstrate the memory efficiency difference.
    """
    print("=== Memory Efficiency Comparison ===")

    # Create a large spreadsheet state
    large_data = {
        "sheets": [{"sheet_id": 0, "name": "Large Sheet", "index": 0, "row_count": 10000, "column_count": 100}],
        "sheetData": {"0": []},  # We'll add data programmatically
        "tables": [],
        "activeSheetId": 0,
        "selections": {}
    }

    # Add some data to make it realistic
    rows = []
    for i in range(1000):  # 1000 rows with data
        values = []
        for j in range(50):  # 50 columns with data
            values.append({"value": f"Cell_{i}_{j}", "formula": None})
        rows.append({"values": values})
    large_data["sheetData"]["0"] = rows

    print(f"Initial data: ~{len(str(large_data))} characters")

    # Test efficient interface
    efficient_interface = EfficientSpreadsheetInterface(large_data)

    # Perform some operations
    efficient_interface.insert_rows(sheet_id=0, reference_row_index=100, num_rows=5)
    efficient_interface.set_cell_value(0, 100, 0, "New Value 1")
    efficient_interface.set_cell_value(0, 101, 1, "New Value 2")

    # Check memory usage
    memory_stats = efficient_interface.get_memory_usage()
    print(f"Efficient tracker memory usage: {memory_stats}")

    # Generate patches
    patches = efficient_interface.generate_yjs_patches()
    print(f"Generated {len(patches)} patches")
    print(f"Estimated patch size: ~{len(str(patches))} characters")

    print("\nMemory efficiency benefits:")
    print("- No full state copies stored")
    print("- Only actual changes tracked")
    print("- Minimal memory overhead per operation")
    print("- Scales linearly with changes, not with total data size")


if __name__ == "__main__":
    demonstrate_memory_efficiency()
