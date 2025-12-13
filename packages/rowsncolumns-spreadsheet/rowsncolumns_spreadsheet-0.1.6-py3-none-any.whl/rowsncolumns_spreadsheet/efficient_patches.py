"""
Efficient patch tracking system that avoids storing full state copies.

This implementation tracks changes incrementally rather than comparing
full states, similar to how Immer works with structural sharing.
"""

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import copy

from .patches import JSONPatch, PatchOperation, PatchType, SpreadsheetPatch


class ChangeType(Enum):
    """Types of changes that can be tracked."""
    SHEET_METADATA = "sheet_metadata"
    CELL_VALUE = "cell_value"
    ROW_INSERT = "row_insert"
    ROW_DELETE = "row_delete"
    COLUMN_INSERT = "column_insert"
    COLUMN_DELETE = "column_delete"
    TABLE_UPDATE = "table_update"
    SELECTION_UPDATE = "selection_update"


@dataclass
class ChangeRecord:
    """Records a single change operation."""
    change_type: ChangeType
    path: str
    old_value: Any = None
    new_value: Any = None
    operation_data: Dict[str, Any] = field(default_factory=dict)


class EfficientPatchTracker:
    """
    Tracks changes incrementally without storing full state copies.

    This approach is much more memory-efficient than comparing full states.
    """

    def __init__(self):
        self.changes: List[ChangeRecord] = []
        self._tracking_enabled = True

    def enable_tracking(self) -> None:
        """Enable change tracking."""
        self._tracking_enabled = True

    def disable_tracking(self) -> None:
        """Disable change tracking."""
        self._tracking_enabled = False

    def clear_changes(self) -> None:
        """Clear all tracked changes."""
        self.changes = []

    def record_cell_change(
        self,
        sheet_id: int,
        row_index: int,
        column_index: int,
        old_value: Any,
        new_value: Any
    ) -> None:
        """Record a cell value change."""
        if not self._tracking_enabled:
            return

        # Path to the specific cell within the row's values array
        path = f"/sheetData/{sheet_id}/{row_index}/values/{column_index}"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.CELL_VALUE,
            path=path,
            old_value=old_value,
            new_value=new_value
        ))

    def record_row_insertion(
        self,
        sheet_id: int,
        reference_row_index: int,
        num_rows: int,
        old_row_count: int
    ) -> None:
        """Record row insertion."""
        if not self._tracking_enabled:
            return

        # Record the sheet row count change
        sheet_path = f"/sheets/{sheet_id}/row_count"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.ROW_INSERT,
            path=sheet_path,
            old_value=old_row_count,
            new_value=old_row_count + num_rows,
            operation_data={
                "sheet_id": sheet_id,
                "reference_row_index": reference_row_index,
                "num_rows": num_rows
            }
        ))

        # Record the data insertion (we'll generate this as array splice operations)
        data_path = f"/sheetData/{sheet_id}"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.ROW_INSERT,
            path=data_path,
            operation_data={
                "operation": "splice",
                "index": reference_row_index,
                "delete_count": 0,
                "insert_count": num_rows,
                "sheet_id": sheet_id
            }
        ))

    def record_row_deletion(
        self,
        sheet_id: int,
        row_indices: List[int],
        old_row_count: int,
        deleted_data: List[Any] = None
    ) -> None:
        """Record row deletion."""
        if not self._tracking_enabled:
            return

        # Record the sheet row count change
        sheet_path = f"/sheets/{sheet_id}/row_count"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.ROW_DELETE,
            path=sheet_path,
            old_value=old_row_count,
            new_value=old_row_count - len(row_indices),
            operation_data={
                "sheet_id": sheet_id,
                "deleted_indices": row_indices,
                "deleted_data": deleted_data
            }
        ))

    def record_column_insertion(
        self,
        sheet_id: int,
        reference_column_index: int,
        num_columns: int,
        old_column_count: int
    ) -> None:
        """Record column insertion."""
        if not self._tracking_enabled:
            return

        sheet_path = f"/sheets/{sheet_id}/column_count"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.COLUMN_INSERT,
            path=sheet_path,
            old_value=old_column_count,
            new_value=old_column_count + num_columns,
            operation_data={
                "sheet_id": sheet_id,
                "reference_column_index": reference_column_index,
                "num_columns": num_columns
            }
        ))

    def record_sheet_metadata_change(
        self,
        sheet_id: int,
        property_name: str,
        old_value: Any,
        new_value: Any
    ) -> None:
        """Record a change to sheet metadata."""
        if not self._tracking_enabled:
            return

        path = f"/sheets/{sheet_id}/{property_name}"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.SHEET_METADATA,
            path=path,
            old_value=old_value,
            new_value=new_value
        ))

    def record_table_change(
        self,
        table_index: int,
        property_name: str,
        old_value: Any,
        new_value: Any
    ) -> None:
        """Record a change to table properties."""
        if not self._tracking_enabled:
            return

        path = f"/tables/{table_index}/{property_name}"
        self.changes.append(ChangeRecord(
            change_type=ChangeType.TABLE_UPDATE,
            path=path,
            old_value=old_value,
            new_value=new_value
        ))

    def generate_json_patches(self) -> List[JSONPatch]:
        """
        Generate JSON patches from tracked changes.

        This is much more efficient than comparing full states.
        """
        patches = []

        for change in self.changes:
            if change.change_type == ChangeType.CELL_VALUE:
                if change.new_value is None:
                    # Cell was deleted
                    patches.append(JSONPatch(
                        op=PatchOperation.REMOVE,
                        path=change.path
                    ))
                elif change.old_value is None:
                    # Cell was added
                    patches.append(JSONPatch(
                        op=PatchOperation.ADD,
                        path=change.path,
                        value=self._serialize_cell_value(change.new_value)
                    ))
                else:
                    # Cell was modified
                    patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=change.path,
                        value=self._serialize_cell_value(change.new_value)
                    ))

            elif change.change_type in [ChangeType.SHEET_METADATA, ChangeType.TABLE_UPDATE]:
                patches.append(JSONPatch(
                    op=PatchOperation.REPLACE,
                    path=change.path,
                    value=change.new_value
                ))

            elif change.change_type == ChangeType.ROW_INSERT:
                if "operation" in change.operation_data:
                    # This is the data insertion part
                    op_data = change.operation_data
                    # Generate patches for inserting empty rows
                    for i in range(op_data["insert_count"]):
                        row_path = f"{change.path}/{op_data['index'] + i}"
                        patches.append(JSONPatch(
                            op=PatchOperation.ADD,
                            path=row_path,
                            value={"values": []}  # Empty RowData
                        ))
                else:
                    # This is the row count change
                    patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=change.path,
                        value=change.new_value
                    ))

            elif change.change_type == ChangeType.ROW_DELETE:
                # For deletions, we need to remove in reverse order
                if "deleted_indices" in change.operation_data:
                    indices = sorted(change.operation_data["deleted_indices"], reverse=True)
                    for idx in indices:
                        row_path = f"/sheetData/{change.operation_data['sheet_id']}/{idx}"
                        patches.append(JSONPatch(
                            op=PatchOperation.REMOVE,
                            path=row_path
                        ))
                else:
                    # Row count change
                    patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=change.path,
                        value=change.new_value
                    ))

        return patches

    def generate_inverse_patches(self) -> List[JSONPatch]:
        """Generate inverse patches for undo operations."""
        inverse_patches = []

        # Process changes in reverse order for undo
        for change in reversed(self.changes):
            if change.change_type == ChangeType.CELL_VALUE:
                if change.old_value is None:
                    # Original was empty, so remove the new value
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.REMOVE,
                        path=change.path
                    ))
                elif change.new_value is None:
                    # Was deleted, so add it back
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.ADD,
                        path=change.path,
                        value=self._serialize_cell_value(change.old_value)
                    ))
                else:
                    # Replace with old value
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=change.path,
                        value=self._serialize_cell_value(change.old_value)
                    ))

            elif change.change_type in [ChangeType.SHEET_METADATA, ChangeType.TABLE_UPDATE]:
                inverse_patches.append(JSONPatch(
                    op=PatchOperation.REPLACE,
                    path=change.path,
                    value=change.old_value
                ))

            elif change.change_type == ChangeType.ROW_INSERT:
                if "operation" in change.operation_data:
                    # Remove the inserted rows
                    op_data = change.operation_data
                    for i in range(op_data["insert_count"]):
                        row_path = f"{change.path}/{op_data['index'] + i}"
                        inverse_patches.append(JSONPatch(
                            op=PatchOperation.REMOVE,
                            path=row_path
                        ))
                else:
                    # Restore old row count
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=change.path,
                        value=change.old_value
                    ))

        return inverse_patches

    def generate_spreadsheet_patch(self) -> SpreadsheetPatch:
        """Generate a SpreadsheetPatch from tracked changes."""
        forward_patches = self.generate_json_patches()
        inverse_patches = self.generate_inverse_patches()

        patch = SpreadsheetPatch()

        # Group patches by type
        sheet_patches = []
        sheet_data_patches = []
        table_patches = []

        for p in forward_patches:
            if p.path.startswith("/sheets/"):
                sheet_patches.append(p)
            elif p.path.startswith("/sheetData/"):
                sheet_data_patches.append(p)
            elif p.path.startswith("/tables/"):
                table_patches.append(p)

        # Group inverse patches similarly
        sheet_inverse_patches = []
        sheet_data_inverse_patches = []
        table_inverse_patches = []

        for p in inverse_patches:
            if p.path.startswith("/sheets/"):
                sheet_inverse_patches.append(p)
            elif p.path.startswith("/sheetData/"):
                sheet_data_inverse_patches.append(p)
            elif p.path.startswith("/tables/"):
                table_inverse_patches.append(p)

        # Create patch types
        if sheet_patches:
            patch.sheets = PatchType(
                patches=sheet_patches,
                inverse_patches=sheet_inverse_patches
            )

        if sheet_data_patches:
            patch.sheet_data = PatchType(
                patches=sheet_data_patches,
                inverse_patches=sheet_data_inverse_patches
            )

        if table_patches:
            patch.tables = PatchType(
                patches=table_patches,
                inverse_patches=table_inverse_patches
            )

        return patch

    def _serialize_cell_value(self, cell_data: Any) -> Dict[str, Any]:
        """Serialize cell data for JSON patches."""
        if cell_data is None:
            return None

        if hasattr(cell_data, 'model_dump'):
            return cell_data.model_dump()
        elif hasattr(cell_data, '__dict__'):
            return cell_data.__dict__
        else:
            return {"value": cell_data, "formula": None}

    def get_memory_usage_estimate(self) -> Dict[str, int]:
        """Get an estimate of memory usage."""
        import sys

        total_size = 0
        change_count = len(self.changes)

        # Estimate size of changes
        for change in self.changes:
            total_size += sys.getsizeof(change)
            total_size += sys.getsizeof(change.path)
            if change.old_value:
                total_size += sys.getsizeof(change.old_value)
            if change.new_value:
                total_size += sys.getsizeof(change.new_value)

        return {
            "total_bytes": total_size,
            "change_count": change_count,
            "avg_bytes_per_change": total_size // max(change_count, 1),
            "estimated_mb": total_size / (1024 * 1024)
        }


# Convenience function for migration
def create_efficient_tracker() -> EfficientPatchTracker:
    """Create a new efficient patch tracker."""
    return EfficientPatchTracker()
