"""
Immer-like patch system using RFC 6902 JSON Patch with efficient state tracking.

This uses the `jsonpatch` library which is the standard RFC 6902 implementation
for Python, providing the same patch format as Immer but without storing full states.
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import jsonpatch  # pip install jsonpatch
from pydantic import BaseModel

from .types import SpreadsheetState
from .patches import SpreadsheetPatch


class ImmerLikePatchTracker:
    """
    Tracks changes using RFC 6902 JSON Patch format, similar to Immer.

    This avoids storing full states by only tracking the specific changes
    and generating patches on-demand.
    """

    def __init__(self):
        self._patches: List[SpreadsheetPatch] = []
        self._tracking_enabled = True

    def enable_tracking(self) -> None:
        """Enable patch tracking."""
        self._tracking_enabled = True

    def disable_tracking(self) -> None:
        """Disable patch tracking."""
        self._tracking_enabled = False

    def clear_patches(self) -> None:
        """Clear all tracked patches."""
        self._patches = []

    @property
    def patches(self) -> List[SpreadsheetPatch]:
        """Get all tracked patches."""
        return self._patches

    def produce_with_patches(
        self,
        base_state: SpreadsheetState,
        recipe: callable
    ) -> Tuple[SpreadsheetState, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Apply a recipe function and generate JSON patches, similar to Immer's produceWithPatches.

        Args:
            base_state: The initial state
            recipe: Function that modifies the state

        Returns:
            Tuple of (new_state, forward_patches, inverse_patches)
        """
        if not self._tracking_enabled:
            # Just apply the recipe without tracking
            new_state = recipe(base_state.model_copy(deep=True))
            return new_state, [], []

        # Convert to dict for jsonpatch
        before_dict = self._serialize_state(base_state)

        # Apply the recipe to a copy
        new_state = recipe(base_state.model_copy(deep=True))
        after_dict = self._serialize_state(new_state)

        # Generate patches using jsonpatch
        forward_patches = jsonpatch.make_patch(before_dict, after_dict).patch
        inverse_patches = jsonpatch.make_patch(after_dict, before_dict).patch

        return new_state, forward_patches, inverse_patches

    def record_operation_patches(
        self,
        operation_name: str,
        before_state: SpreadsheetState,
        after_state: SpreadsheetState,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SpreadsheetPatch:
        """
        Record patches for a specific operation.

        Args:
            operation_name: Name of the operation (e.g., "insert_row")
            before_state: State before the operation
            after_state: State after the operation
            metadata: Additional operation metadata

        Returns:
            SpreadsheetPatch containing the changes
        """
        if not self._tracking_enabled:
            return SpreadsheetPatch()

        # Convert states to dicts for comparison
        before_dict = self._serialize_state(before_state)
        after_dict = self._serialize_state(after_state)

        # Generate patches for different components
        patch = SpreadsheetPatch()

        # Check for sheet changes
        if before_dict.get('sheets') != after_dict.get('sheets'):
            forward_patches = jsonpatch.make_patch(
                before_dict.get('sheets', []),
                after_dict.get('sheets', [])
            ).patch
            inverse_patches = jsonpatch.make_patch(
                after_dict.get('sheets', []),
                before_dict.get('sheets', [])
            ).patch

            patch.sheets = {
                'patches': forward_patches,
                'inverse_patches': inverse_patches
            }

        # Check for sheet data changes
        if before_dict.get('sheet_data') != after_dict.get('sheet_data'):
            forward_patches = jsonpatch.make_patch(
                before_dict.get('sheet_data', {}),
                after_dict.get('sheet_data', {})
            ).patch
            inverse_patches = jsonpatch.make_patch(
                after_dict.get('sheet_data', {}),
                before_dict.get('sheet_data', {})
            ).patch

            patch.sheet_data = {
                'patches': forward_patches,
                'inverse_patches': inverse_patches
            }

        # Check for table changes
        if before_dict.get('tables') != after_dict.get('tables'):
            forward_patches = jsonpatch.make_patch(
                before_dict.get('tables', []),
                after_dict.get('tables', [])
            ).patch
            inverse_patches = jsonpatch.make_patch(
                after_dict.get('tables', []),
                before_dict.get('tables', [])
            ).patch

            patch.tables = {
                'patches': forward_patches,
                'inverse_patches': inverse_patches
            }

        # Add metadata if provided
        if metadata:
            patch.metadata = metadata

        # Store the patch
        self._patches.append(patch)
        return patch

    def _serialize_state(self, state: SpreadsheetState) -> Dict[str, Any]:
        """
        Serialize state to dict for patch comparison.
        Only serializes the parts we actually need to compare.
        """
        result = {}

        # Serialize sheets
        if state.sheets:
            result['sheets'] = [sheet.model_dump() for sheet in state.sheets]

        # Serialize sheet data efficiently
        if state.sheet_data:
            sheet_data_dict = {}
            for sheet_id, rows in state.sheet_data.items():
                serialized_rows = []
                for row in rows:
                    if row is None:
                        serialized_rows.append(None)
                    else:
                        serialized_rows.append(row.model_dump())
                sheet_data_dict[str(sheet_id)] = serialized_rows
            result['sheet_data'] = sheet_data_dict

        # Serialize tables
        if state.tables:
            result['tables'] = [table.model_dump() for table in state.tables]

        # Add other fields that might change
        if state.active_sheet_id is not None:
            result['active_sheet_id'] = state.active_sheet_id

        if state.selections:
            result['selections'] = {
                str(k): [sel.model_dump() for sel in v]
                for k, v in state.selections.items()
            }

        return result

    def apply_patches_to_state(
        self,
        state: SpreadsheetState,
        patches: List[Dict[str, Any]]
    ) -> SpreadsheetState:
        """
        Apply JSON patches to a state object.

        Args:
            state: The state to apply patches to
            patches: List of RFC 6902 JSON patches

        Returns:
            New state with patches applied
        """
        # Serialize current state
        state_dict = self._serialize_state(state)

        # Apply patches
        patch_obj = jsonpatch.JsonPatch(patches)
        updated_dict = patch_obj.apply(state_dict)

        # Convert back to SpreadsheetState
        return self._deserialize_state(updated_dict)

    def _deserialize_state(self, state_dict: Dict[str, Any]) -> SpreadsheetState:
        """Convert a dictionary back to SpreadsheetState."""
        from .types import Sheet, Table, SelectionArea, RowData, CellData, GridRange

        # Deserialize sheets
        sheets = []
        for sheet_data in state_dict.get('sheets', []):
            sheets.append(Sheet(**sheet_data))

        # Deserialize sheet data
        sheet_data = {}
        for sheet_id_str, rows in state_dict.get('sheet_data', {}).items():
            sheet_id = int(sheet_id_str)
            deserialized_rows = []
            for row in rows:
                if row is None:
                    deserialized_rows.append(None)
                else:
                    # Convert cells
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
            active_sheet_id=state_dict.get('active_sheet_id'),
            selections=selections,
            history=[]  # History is not serialized in patches
        )

    def get_yjs_compatible_patches(self) -> List[Dict[str, Any]]:
        """
        Get all patches in YJS-compatible format.

        Returns:
            List of RFC 6902 JSON patches that can be applied to YJS documents
        """
        all_patches = []

        for spreadsheet_patch in self._patches:
            # Add sheet patches
            if spreadsheet_patch.sheets and 'patches' in spreadsheet_patch.sheets:
                for patch in spreadsheet_patch.sheets['patches']:
                    # Adjust path for YJS compatibility
                    yjs_patch = patch.copy()
                    yjs_patch['path'] = f"/sheets{patch['path']}" if not patch['path'].startswith('/sheets') else patch['path']
                    all_patches.append(yjs_patch)

            # Add sheet data patches
            if spreadsheet_patch.sheet_data and 'patches' in spreadsheet_patch.sheet_data:
                for patch in spreadsheet_patch.sheet_data['patches']:
                    yjs_patch = patch.copy()
                    yjs_patch['path'] = f"/sheetData{patch['path']}" if not patch['path'].startswith('/sheetData') else patch['path']
                    all_patches.append(yjs_patch)

            # Add table patches
            if spreadsheet_patch.tables and 'patches' in spreadsheet_patch.tables:
                for patch in spreadsheet_patch.tables['patches']:
                    yjs_patch = patch.copy()
                    yjs_patch['path'] = f"/tables{patch['path']}" if not patch['path'].startswith('/tables') else patch['path']
                    all_patches.append(yjs_patch)

        return all_patches

    def get_patch_tuples(self, operation_type: str = "redo") -> List[Tuple[SpreadsheetPatch, str]]:
        """Get patches as tuples, compatible with TypeScript interface."""
        return [(patch, operation_type) for patch in self._patches]

    def create_history_callback(self) -> callable:
        """
        Create a history callback function similar to the TypeScript version.

        Returns:
            Function that can be used to save patches to history
        """
        def save_history(patch: SpreadsheetPatch) -> None:
            if self._tracking_enabled:
                self._patches.append(patch)

        return save_history


# Convenience functions for easy migration
def produce_with_patches(
    base_state: SpreadsheetState,
    recipe: callable
) -> Tuple[SpreadsheetState, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Standalone function that works like Immer's produceWithPatches.

    Args:
        base_state: The initial state
        recipe: Function that modifies the state

    Returns:
        Tuple of (new_state, forward_patches, inverse_patches)
    """
    tracker = ImmerLikePatchTracker()
    return tracker.produce_with_patches(base_state, recipe)


def apply_patches(
    state: SpreadsheetState,
    patches: List[Dict[str, Any]]
) -> SpreadsheetState:
    """
    Apply JSON patches to a state.

    Args:
        state: The state to apply patches to
        patches: List of RFC 6902 JSON patches

    Returns:
        New state with patches applied
    """
    tracker = ImmerLikePatchTracker()
    return tracker.apply_patches_to_state(state, patches)