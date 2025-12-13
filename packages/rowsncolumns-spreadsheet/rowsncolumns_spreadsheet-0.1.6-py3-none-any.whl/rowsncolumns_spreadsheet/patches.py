"""
JSON Patch system for YJS integration.

This module provides functionality to generate JSON patches that can be applied
to YJS documents, similar to how the TypeScript version uses Immer patches.
"""

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from pydantic import BaseModel

from .types import CellInterface, SelectionArea, SpreadsheetState


class PatchOperation(Enum):
    """JSON Patch operation types."""
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"


@dataclass
class JSONPatch:
    """Represents a single JSON Patch operation."""
    op: PatchOperation
    path: str
    value: Optional[Any] = None
    from_path: Optional[str] = None  # for move/copy operations

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format suitable for YJS."""
        result = {
            "op": self.op.value,
            "path": self.path,
        }
        if self.value is not None:
            result["value"] = self.value
        if self.from_path is not None:
            result["from"] = self.from_path
        return result


class PatchType(BaseModel):
    """Container for forward and reverse patches."""
    patches: List[JSONPatch]
    inverse_patches: List[JSONPatch]


class SpreadsheetPatch(BaseModel):
    """
    Complete patch information for a spreadsheet operation.

    Mirrors the TypeScript SpreadsheetPatch type but uses JSON patches
    instead of Immer patches.
    """
    sheet_data: Optional[PatchType] = None
    active_cell: Optional[Dict[str, CellInterface]] = None  # {"redo": cell, "undo": cell}
    selections: Optional[Dict[str, Optional[List[SelectionArea]]]] = None
    sheets: Optional[PatchType] = None
    tables: Optional[PatchType] = None
    named_ranges: Optional[PatchType] = None
    charts: Optional[PatchType] = None
    embeds: Optional[PatchType] = None
    conditional_formats: Optional[PatchType] = None
    data_validations: Optional[PatchType] = None
    cell_xfs: Optional[PatchType] = None
    theme: Optional[PatchType] = None
    sheet_id: Optional[Dict[str, Optional[int]]] = None


class PatchGenerator:
    """
    Generates JSON patches by comparing before/after states.

    This is similar to what Immer does automatically, but we need to implement
    it manually for Python.
    """

    @staticmethod
    def generate_patches(
        before: Any,
        after: Any,
        base_path: str = ""
    ) -> Tuple[List[JSONPatch], List[JSONPatch]]:
        """
        Generate forward and inverse JSON patches between two states.

        Args:
            before: The previous state
            after: The new state
            base_path: Base path for the patches

        Returns:
            Tuple of (forward_patches, inverse_patches)
        """
        forward_patches = []
        inverse_patches = []

        if isinstance(before, dict) and isinstance(after, dict):
            # Handle dictionary changes
            all_keys = set(before.keys()) | set(after.keys())

            for key in all_keys:
                key_path = f"{base_path}/{key}" if base_path else f"/{key}"

                if key not in before:
                    # Key was added
                    forward_patches.append(JSONPatch(
                        op=PatchOperation.ADD,
                        path=key_path,
                        value=after[key]
                    ))
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.REMOVE,
                        path=key_path
                    ))
                elif key not in after:
                    # Key was removed
                    forward_patches.append(JSONPatch(
                        op=PatchOperation.REMOVE,
                        path=key_path
                    ))
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.ADD,
                        path=key_path,
                        value=before[key]
                    ))
                elif before[key] != after[key]:
                    # Key was modified
                    if isinstance(before[key], (dict, list)) and isinstance(after[key], (dict, list)):
                        # Recursively generate patches for nested objects
                        nested_forward, nested_inverse = PatchGenerator.generate_patches(
                            before[key], after[key], key_path
                        )
                        forward_patches.extend(nested_forward)
                        inverse_patches.extend(nested_inverse)
                    else:
                        # Simple value replacement
                        forward_patches.append(JSONPatch(
                            op=PatchOperation.REPLACE,
                            path=key_path,
                            value=after[key]
                        ))
                        inverse_patches.append(JSONPatch(
                            op=PatchOperation.REPLACE,
                            path=key_path,
                            value=before[key]
                        ))

        elif isinstance(before, list) and isinstance(after, list):
            # Handle list changes
            PatchGenerator._generate_list_patches(
                before, after, base_path, forward_patches, inverse_patches
            )

        elif before != after:
            # Simple value change at the root
            forward_patches.append(JSONPatch(
                op=PatchOperation.REPLACE,
                path=base_path or "/",
                value=after
            ))
            inverse_patches.append(JSONPatch(
                op=PatchOperation.REPLACE,
                path=base_path or "/",
                value=before
            ))

        return forward_patches, inverse_patches

    @staticmethod
    def _generate_list_patches(
        before: List[Any],
        after: List[Any],
        base_path: str,
        forward_patches: List[JSONPatch],
        inverse_patches: List[JSONPatch]
    ) -> None:
        """Generate patches for list changes."""
        before_len = len(before)
        after_len = len(after)

        # Handle common elements first
        min_len = min(before_len, after_len)
        for i in range(min_len):
            if before[i] != after[i]:
                item_path = f"{base_path}/{i}"
                if isinstance(before[i], (dict, list)) and isinstance(after[i], (dict, list)):
                    nested_forward, nested_inverse = PatchGenerator.generate_patches(
                        before[i], after[i], item_path
                    )
                    forward_patches.extend(nested_forward)
                    inverse_patches.extend(nested_inverse)
                else:
                    forward_patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=item_path,
                        value=after[i]
                    ))
                    inverse_patches.append(JSONPatch(
                        op=PatchOperation.REPLACE,
                        path=item_path,
                        value=before[i]
                    ))

        # Handle added elements
        if after_len > before_len:
            for i in range(before_len, after_len):
                forward_patches.append(JSONPatch(
                    op=PatchOperation.ADD,
                    path=f"{base_path}/{i}",
                    value=after[i]
                ))
                inverse_patches.append(JSONPatch(
                    op=PatchOperation.REMOVE,
                    path=f"{base_path}/{i}"
                ))

        # Handle removed elements (process in reverse order)
        elif before_len > after_len:
            for i in range(before_len - 1, after_len - 1, -1):
                forward_patches.append(JSONPatch(
                    op=PatchOperation.REMOVE,
                    path=f"{base_path}/{i}"
                ))
                inverse_patches.append(JSONPatch(
                    op=PatchOperation.ADD,
                    path=f"{base_path}/{i}",
                    value=before[i]
                ))


def serialize_for_patches(obj: Any) -> Any:
    """
    Serialize Pydantic models and other objects to JSON-serializable format.

    This is needed because we need to compare raw data structures for patch generation.
    """
    if hasattr(obj, 'model_dump'):
        # Pydantic model
        return obj.model_dump()
    elif hasattr(obj, '__dict__'):
        # Regular object with attributes
        return {k: serialize_for_patches(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, dict):
        return {k: serialize_for_patches(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_patches(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # Try to convert to string as fallback
        return str(obj)


def apply_patches_to_dict(target: Dict[str, Any], patches: List[JSONPatch]) -> Dict[str, Any]:
    """
    Apply JSON patches to a dictionary.

    This is a simplified implementation for demonstration.
    In practice, you'd use a proper JSON Patch library.
    """
    import copy
    result = copy.deepcopy(target)

    for patch in patches:
        path_parts = [p for p in patch.path.split('/') if p]

        if patch.op == PatchOperation.ADD or patch.op == PatchOperation.REPLACE:
            current = result
            for part in path_parts[:-1]:
                if part.isdigit():
                    current = current[int(part)]
                else:
                    current = current[part]

            if path_parts:
                key = path_parts[-1]
                if key.isdigit():
                    current[int(key)] = patch.value
                else:
                    current[key] = patch.value
            else:
                result = patch.value

        elif patch.op == PatchOperation.REMOVE:
            current = result
            for part in path_parts[:-1]:
                if part.isdigit():
                    current = current[int(part)]
                else:
                    current = current[part]

            if path_parts:
                key = path_parts[-1]
                if key.isdigit():
                    del current[int(key)]
                else:
                    del current[key]

    return result
