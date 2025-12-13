"""
Production-ready SpreadsheetInterface using jsonpatch (RFC 6902) exactly like Immer.

This implementation uses the standard `jsonpatch` library to generate patches
by comparing states, providing the exact same workflow as the TypeScript version.
"""

from typing import List, Optional, Dict, Any, Tuple, Callable
import copy
try:
    import jsonpatch  # pip install jsonpatch
except ImportError:
    raise ImportError("Please install jsonpatch: pip install jsonpatch")

from .types import SpreadsheetState, Sheet, CellData, RowData, GridRange, SelectionArea
from .operations import insert_row, delete_row, insert_column, delete_column
from .patches import SpreadsheetPatch


class ImmerSpreadsheetInterface:
    """
    Production SpreadsheetInterface using jsonpatch for RFC 6902 JSON Patches.

    This provides exactly the same workflow as the TypeScript version:
    1. Load data from YJS
    2. Perform operations
    3. Get RFC 6902 JSON patches
    4. Apply patches to YJS

    Uses the standard `jsonpatch` library for maximum compatibility.
    """

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        """Initialize the spreadsheet interface."""
        if initial_data:
            self._state = self._load_from_yjs_data(initial_data)
        else:
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

        # Store initial state for patch generation
        self._initial_state_dict = self._serialize_state(self._state)
        self._patches: List[SpreadsheetPatch] = []

    @property
    def state(self) -> SpreadsheetState:
        """Get the current spreadsheet state."""
        return self._state

    @property
    def patches(self) -> List[SpreadsheetPatch]:
        """Get accumulated patches."""
        return self._patches

    def clear_patches(self) -> None:
        """Clear accumulated patches and reset baseline."""
        self._patches = []
        self._initial_state_dict = self._serialize_state(self._state)

    def _load_from_yjs_data(self, data: Dict[str, Any]) -> SpreadsheetState:
        """Load spreadsheet state from YJS document data."""
        sheets_data = data.get('sheets', [])
        sheets = [Sheet(**sheet_data) for sheet_data in sheets_data]

        # Load sheet data
        sheet_data = data.get('sheetData', {})
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

    def _serialize_state(self, state: SpreadsheetState) -> Dict[str, Any]:
        """Serialize state to dict for patch comparison."""
        result = {}

        # Serialize sheets
        if state.sheets:
            result['sheets'] = [sheet.model_dump() for sheet in state.sheets]

        # Serialize sheet data
        if state.sheet_data:
            sheet_data_dict = {}
            for sheet_id, rows in state.sheet_data.items():
                serialized_rows = []
                for row in rows:
                    if row is None:
                        serialized_rows.append(None)
                    else:
                        serialized_values = []
                        for cell in (row.values or []):
                            if cell is None:
                                serialized_values.append(None)
                            else:
                                serialized_values.append(cell.model_dump())
                        serialized_rows.append({"values": serialized_values})
                sheet_data_dict[str(sheet_id)] = serialized_rows
            result['sheetData'] = sheet_data_dict

        # Serialize tables
        if state.tables:
            result['tables'] = [table.model_dump() for table in state.tables]

        # Other fields
        if state.active_sheet_id is not None:
            result['activeSheetId'] = state.active_sheet_id

        if state.selections:
            result['selections'] = {
                str(k): [sel.model_dump() for sel in v]
                for k, v in state.selections.items()
            }

        return result

    def _generate_patches(self) -> SpreadsheetPatch:
        """Generate patches by comparing current state to initial state."""
        current_state_dict = self._serialize_state(self._state)

        # Generate RFC 6902 JSON patches using jsonpatch
        patch_obj = jsonpatch.make_patch(self._initial_state_dict, current_state_dict)
        forward_patches = patch_obj.patch

        # Generate inverse patches for undo
        inverse_patch_obj = jsonpatch.make_patch(current_state_dict, self._initial_state_dict)
        inverse_patches = inverse_patch_obj.patch

        # Create SpreadsheetPatch by categorizing patches
        spreadsheet_patch = SpreadsheetPatch()

        # Categorize patches by path
        sheet_patches = []
        sheet_data_patches = []
        table_patches = []
        selection_patches = []

        for patch in forward_patches:
            path = patch.get('path', '')
            if path.startswith('/sheets'):
                sheet_patches.append(patch)
            elif path.startswith('/sheetData'):
                sheet_data_patches.append(patch)
            elif path.startswith('/tables'):
                table_patches.append(patch)
            elif path.startswith('/selections'):
                selection_patches.append(patch)

        # Same for inverse patches
        sheet_inverse_patches = []
        sheet_data_inverse_patches = []
        table_inverse_patches = []

        for patch in inverse_patches:
            path = patch.get('path', '')
            if path.startswith('/sheets'):
                sheet_inverse_patches.append(patch)
            elif path.startswith('/sheetData'):
                sheet_data_inverse_patches.append(patch)
            elif path.startswith('/tables'):
                table_inverse_patches.append(patch)

        # Build SpreadsheetPatch
        if sheet_patches:
            spreadsheet_patch.sheets = {
                'patches': sheet_patches,
                'inverse_patches': sheet_inverse_patches
            }

        if sheet_data_patches:
            spreadsheet_patch.sheet_data = {
                'patches': sheet_data_patches,
                'inverse_patches': sheet_data_inverse_patches
            }

        if table_patches:
            spreadsheet_patch.tables = {
                'patches': table_patches,
                'inverse_patches': table_inverse_patches
            }

        return spreadsheet_patch

    def insert_rows(self, sheet_id: int, reference_row_index: int, num_rows: int = 1) -> None:
        """Insert rows and generate patches."""
        new_state = insert_row(self._state, sheet_id, reference_row_index, num_rows, save_history=False)
        self._state = new_state

        # Generate and store patch
        patch = self._generate_patches()
        if self._has_changes(patch):
            self._patches.append(patch)
            # Update baseline for next operation
            self._initial_state_dict = self._serialize_state(self._state)

    def delete_rows(self, sheet_id: int, row_indices: List[int]) -> None:
        """Delete rows and generate patches."""
        new_state = delete_row(self._state, sheet_id, row_indices, save_history=False)
        self._state = new_state

        patch = self._generate_patches()
        if self._has_changes(patch):
            self._patches.append(patch)
            self._initial_state_dict = self._serialize_state(self._state)

    def insert_columns(self, sheet_id: int, reference_column_index: int, num_columns: int = 1) -> None:
        """Insert columns and generate patches."""
        new_state = insert_column(self._state, sheet_id, reference_column_index, num_columns, save_history=False)
        self._state = new_state

        patch = self._generate_patches()
        if self._has_changes(patch):
            self._patches.append(patch)
            self._initial_state_dict = self._serialize_state(self._state)

    def delete_columns(self, sheet_id: int, column_indices: List[int]) -> None:
        """Delete columns and generate patches."""
        new_state = delete_column(self._state, sheet_id, column_indices, save_history=False)
        self._state = new_state

        patch = self._generate_patches()
        if self._has_changes(patch):
            self._patches.append(patch)
            self._initial_state_dict = self._serialize_state(self._state)

    def set_cell_value(self, sheet_id: int, row_index: int, column_index: int, value: Any, formula: Optional[str] = None) -> None:
        """Set cell value and generate patches."""
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

        if row.values is None:
            row.values = []
        while len(row.values) <= column_index:
            row.values.append(None)

        # Set the cell value
        cell_data = CellData(value=value, formula=formula)
        row.values[column_index] = cell_data

        # Generate and store patch
        patch = self._generate_patches()
        if self._has_changes(patch):
            self._patches.append(patch)
            self._initial_state_dict = self._serialize_state(self._state)

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
        return cell.value if cell else None

    def generate_yjs_patches(self) -> List[Dict[str, Any]]:
        """Generate all patches in YJS-compatible format (RFC 6902 JSON Patches)."""
        all_patches = []

        for spreadsheet_patch in self._patches:
            # Add sheet patches
            if spreadsheet_patch.sheets and 'patches' in spreadsheet_patch.sheets:
                all_patches.extend(spreadsheet_patch.sheets['patches'])

            # Add sheet data patches
            if spreadsheet_patch.sheet_data and 'patches' in spreadsheet_patch.sheet_data:
                all_patches.extend(spreadsheet_patch.sheet_data['patches'])

            # Add table patches
            if spreadsheet_patch.tables and 'patches' in spreadsheet_patch.tables:
                all_patches.extend(spreadsheet_patch.tables['patches'])

        return all_patches

    def get_patch_tuples(self, operation_type: str = "redo") -> List[Tuple[SpreadsheetPatch, str]]:
        """Get patches as tuples for YJS application."""
        return [(patch, operation_type) for patch in self._patches]

    def to_yjs_data(self) -> Dict[str, Any]:
        """Convert current state to YJS data format."""
        return self._serialize_state(self._state)

    def _has_changes(self, patch: SpreadsheetPatch) -> bool:
        """Check if a patch contains any actual changes."""
        return any([
            patch.sheets and patch.sheets.get('patches'),
            patch.sheet_data and patch.sheet_data.get('patches'),
            patch.tables and patch.tables.get('patches'),
        ])

    def apply_patches_from_yjs(self, patches: List[Dict[str, Any]]) -> None:
        """
        Apply RFC 6902 JSON patches received from YJS.

        This allows the Python backend to sync with changes from other clients.
        """
        current_dict = self._serialize_state(self._state)

        # Apply patches using jsonpatch
        patch_obj = jsonpatch.JsonPatch(patches)
        updated_dict = patch_obj.apply(current_dict)

        # Convert back to SpreadsheetState
        self._state = self._deserialize_state(updated_dict)

        # Update baseline
        self._initial_state_dict = updated_dict

    def _deserialize_state(self, state_dict: Dict[str, Any]) -> SpreadsheetState:
        """Convert dictionary back to SpreadsheetState."""
        # Deserialize sheets
        sheets = []
        for sheet_data in state_dict.get('sheets', []):
            sheets.append(Sheet(**sheet_data))

        # Deserialize sheet data
        sheet_data = {}
        for sheet_id_str, rows in state_dict.get('sheetData', {}).items():
            sheet_id = int(sheet_id_str)
            deserialized_rows = []
            for row in rows:
                if row is None:
                    deserialized_rows.append(None)
                else:
                    values = []
                    for cell in row.get('values', []):
                        if cell is None:
                            values.append(None)
                        else:
                            values.append(CellData(**cell))
                    deserialized_rows.append(RowData(values=values))
            sheet_data[sheet_id] = deserialized_rows

        # Deserialize tables
        tables = []
        for table_data in state_dict.get('tables', []):
            tables.append(Table(**table_data))

        # Deserialize selections
        selections = {}
        for sheet_id_str, sel_list in state_dict.get('selections', {}).items():
            sheet_id = int(sheet_id_str)
            selections[sheet_id] = [SelectionArea(**sel) for sel in sel_list]

        return SpreadsheetState(
            sheets=sheets,
            sheet_data=sheet_data,
            tables=tables,
            active_sheet_id=state_dict.get('activeSheetId'),
            selections=selections,
            history=[]
        )


# Convenience functions matching Immer API
def produce_with_patches(base_state: SpreadsheetState, recipe: Callable[[SpreadsheetState], SpreadsheetState]) -> Tuple[SpreadsheetState, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Standalone function that works exactly like Immer's produceWithPatches.

    Args:
        base_state: The initial state
        recipe: Function that returns the modified state

    Returns:
        Tuple of (new_state, forward_patches, inverse_patches)
    """
    interface = ImmerSpreadsheetInterface()

    # Serialize initial state
    before_dict = interface._serialize_state(base_state)

    # Apply recipe
    new_state = recipe(base_state.model_copy(deep=True))
    after_dict = interface._serialize_state(new_state)

    # Generate patches
    forward_patch_obj = jsonpatch.make_patch(before_dict, after_dict)
    inverse_patch_obj = jsonpatch.make_patch(after_dict, before_dict)

    return new_state, forward_patch_obj.patch, inverse_patch_obj.patch


def apply_patches(state: SpreadsheetState, patches: List[Dict[str, Any]]) -> SpreadsheetState:
    """
    Apply RFC 6902 JSON patches to a state.

    Args:
        state: The state to apply patches to
        patches: List of RFC 6902 JSON patches

    Returns:
        New state with patches applied
    """
    interface = ImmerSpreadsheetInterface()
    interface._state = state
    interface.apply_patches_from_yjs(patches)
    return interface._state