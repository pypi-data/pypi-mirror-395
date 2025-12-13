"""
Apply fill operation - Python port of apply-fill.ts

This module provides functionality to fill cells in a spreadsheet by copying
values from a selection area to a fill area in various directions (up, down, left, right).
"""

from typing import Any, Dict, List, Optional, Callable, Tuple, Set
from dataclasses import dataclass
import copy

from ..types import (
    CellInterface,
    SelectionArea,
    GridRange,
    Direction,
    CellData,
    SpreadsheetState,
    SelectionAttributes,
    RowData,
)
from ..patches import SpreadsheetPatch, PatchType
from .fill import get_auto_fill_values


@dataclass
class ApplyFillConfig:
    """Configuration for apply_fill operation."""

    locale: str = "en-US"
    cell_xfs_registry: Optional[Any] = None
    get_cell_data: Optional[Callable[[int, int, int], Optional[CellData]]] = None
    get_effective_value: Optional[Callable[[int, int, int], Any]] = None
    enqueue_calculation: Optional[Callable[[Dict[str, Any]], None]] = None
    on_change_sheet_data: Optional[Callable[[Callable[[SpreadsheetState], SpreadsheetState]], SpreadsheetState]] = None
    create_history: Optional[Callable[[], Callable[[SpreadsheetPatch], None]]] = None


def get_fill_direction(fill_selection: SelectionArea, selection: SelectionArea) -> Direction:
    """
    Determine the fill direction based on fill selection and original selection.

    Args:
        fill_selection: The target fill area
        selection: The original selection area

    Returns:
        Direction enum value (UP, DOWN, LEFT, RIGHT)
    """
    fill_bounds = fill_selection.range
    sel_range = selection.range

    # Check if filling down
    if fill_bounds.end_row_index > sel_range.end_row_index:
        return Direction.DOWN

    # Check if filling up
    if fill_bounds.start_row_index < sel_range.start_row_index:
        return Direction.UP

    # Check if filling right
    if fill_bounds.end_column_index > sel_range.end_column_index:
        return Direction.RIGHT

    # Check if filling left
    if fill_bounds.start_column_index < sel_range.start_column_index:
        return Direction.LEFT

    # Default to down if no clear direction
    return Direction.DOWN


def selection_from_active_cell(active_cell: CellInterface) -> List[SelectionArea]:
    """
    Create a selection area from an active cell.

    Args:
        active_cell: The active cell coordinates

    Returns:
        List containing a single selection area
    """
    return [
        SelectionArea(
            range=GridRange(
                start_row_index=active_cell.row_index,
                end_row_index=active_cell.row_index,
                start_column_index=active_cell.column_index,
                end_column_index=active_cell.column_index,
            )
        )
    ]


def create_sheet_cell_identifier(sheet_id: int, row_index: int, column_index: int) -> str:
    """
    Create a unique identifier for a sheet cell.

    Args:
        sheet_id: Sheet ID
        row_index: Row index
        column_index: Column index

    Returns:
        String identifier in format "sheetId:rowIndex:columnIndex"
    """
    return f"{sheet_id}:{row_index}:{column_index}"


def create_sheet_draft(draft: Dict[int, Any], sheet_id: int, row_index: int) -> Dict[int, Any]:
    """
    Ensure sheet data structure exists for the given row.

    Args:
        draft: Draft state dictionary
        sheet_id: Sheet ID
        row_index: Row index

    Returns:
        Sheet data dictionary
    """
    # Ensure sheet_data exists
    if 'sheet_data' not in draft:
        draft['sheet_data'] = {}

    # Ensure sheet exists in sheet_data
    if sheet_id not in draft['sheet_data']:
        draft['sheet_data'][sheet_id] = []

    sheet_rows = draft['sheet_data'][sheet_id]

    # Extend rows list if necessary
    while len(sheet_rows) <= row_index:
        sheet_rows.append(None)

    # Ensure row exists
    if sheet_rows[row_index] is None:
        sheet_rows[row_index] = {'values': []}
    elif isinstance(sheet_rows[row_index], RowData):
        # Convert RowData Pydantic model to dict
        row_dict = sheet_rows[row_index].model_dump(by_alias=True, exclude_none=True)
        sheet_rows[row_index] = row_dict

    # Ensure values array exists (now we know it's a dict)
    if 'values' not in sheet_rows[row_index]:
        sheet_rows[row_index]['values'] = []

    return sheet_rows


def produce_with_patches(
    state: SpreadsheetState,
    recipe: Callable[[Dict[str, Any]], None]
) -> Tuple[SpreadsheetState, List[Any], List[Any]]:
    """
    Produce a new state with patches using a recipe function.

    This is a simplified version of immer's produceWithPatches.

    Args:
        state: Current state
        recipe: Function that modifies the draft state

    Returns:
        Tuple of (new_state, patches, inverse_patches)
    """
    # Convert Pydantic state to dict for mutation
    if isinstance(state, SpreadsheetState):
        draft = state.model_dump(by_alias=True, exclude_none=False)
    elif hasattr(state, '__dict__'):
        draft = copy.deepcopy(state.__dict__)
    else:
        draft = copy.deepcopy(state)

    # Apply the recipe to the draft
    recipe(draft)

    # For now, return simplified patches (would need full JSON patch implementation)
    patches = []
    inverse_patches = []

    # Reconstruct state from the modified dict
    if isinstance(state, SpreadsheetState):
        new_state = SpreadsheetState.model_validate(draft)
    else:
        new_state = draft

    return new_state, patches, inverse_patches


async def apply_fill(
    config: ApplyFillConfig,
    sheet_id: int,
    active_cell: CellInterface,
    fill_selection: SelectionArea,
    selections: List[SelectionArea],
    fillable_selections: Optional[List[SelectionArea]] = None,
    fill_from_top_left_cell: bool = False,
) -> None:
    """
    Apply fill operation to a range of cells.

    This function fills cells by copying values from a source selection to a target
    fill area. It supports filling in all four directions (up, down, left, right).

    Args:
        config: Configuration object with callbacks and settings
        sheet_id: ID of the sheet to operate on
        active_cell: The active cell coordinates
        fill_selection: The target area to fill
        selections: List of source selection areas
        fillable_selections: Optional list of fillable selections for history
        fill_from_top_left_cell: Whether to fill from the top-left cell only
    """
    print(
        "apply_fill called:",
        sheet_id,
        active_cell,
        fill_selection,
        selections,
        fillable_selections,
        fill_from_top_left_cell,
    )

    # Get final selections
    final_selections = selections if selections else selection_from_active_cell(active_cell)
    selection = final_selections[-1]

    # Get callbacks from config
    save_history = config.create_history() if config.create_history else None
    fill_bounds = fill_selection.range
    direction = get_fill_direction(fill_selection, selection)

    # Track cells for recalculation
    recalc_cells: Dict[str, Dict[str, Any]] = {}

    # Get fill values using the built-in get_auto_fill_values
    fill_values = await get_auto_fill_values(
        sheet_id=sheet_id,
        direction=direction,
        selection=selection,
        fill_bounds=fill_bounds,
        get_cell_data=config.get_cell_data,
        get_effective_value=config.get_effective_value,
        cell_xfs_registry=config.cell_xfs_registry,
        locale=config.locale,
    )

    def get_fill_value(row_index: int, column_index: int) -> Optional[Dict[str, Any]]:
        """Get fill value for a specific cell."""
        if row_index >= len(fill_values):
            return None
        if column_index >= len(fill_values[row_index]):
            return None

        fill_value = fill_values[row_index][column_index]

        # fill_values now comes from get_auto_fill_values which returns proper cell data
        if isinstance(fill_value, dict):
            return fill_value

        return None

    # Apply changes to sheet data
    if config.on_change_sheet_data:
        def apply_fill_changes(prev_sheet_data: SpreadsheetState) -> SpreadsheetState:
            """Apply fill changes to sheet data."""
            next_state, patches, inverse_patches = produce_with_patches(
                prev_sheet_data,
                lambda draft: _apply_fill_by_direction(
                    draft=draft,
                    direction=direction,
                    selection=selection,
                    fill_bounds=fill_bounds,
                    sheet_id=sheet_id,
                    get_fill_value=get_fill_value,
                    recalc_cells=recalc_cells,
                    config=config,
                    fill_from_top_left_cell=fill_from_top_left_cell,
                )
            )

            # Save history if callback is provided
            if save_history:
                patch = SpreadsheetPatch(
                    sheet_data=PatchType(patches=patches, inverse_patches=inverse_patches),
                    recalc_cells={'undo': recalc_cells, 'redo': recalc_cells},
                    sheet_id={'undo': sheet_id, 'redo': sheet_id},
                    active_cell={'undo': active_cell, 'redo': active_cell},
                    selections={
                        'undo': fillable_selections or selections,
                        'redo': [fill_selection],
                    },
                )
                save_history(patch)

            return next_state

        config.on_change_sheet_data(apply_fill_changes)


def _apply_fill_by_direction(
    draft: Dict[str, Any],
    direction: Direction,
    selection: SelectionArea,
    fill_bounds: GridRange,
    sheet_id: int,
    get_fill_value: Callable[[int, int], Optional[CellData]],
    recalc_cells: Dict[str, Dict[str, Any]],
    config: ApplyFillConfig,
    fill_from_top_left_cell: bool,
) -> None:
    """
    Apply fill based on direction.

    Args:
        draft: Draft state to modify
        direction: Fill direction
        selection: Source selection area
        fill_bounds: Target fill bounds
        sheet_id: Sheet ID
        get_fill_value: Function to get fill value for a cell
        recalc_cells: Dictionary to track cells for recalculation
        config: Configuration object
        fill_from_top_left_cell: Whether to fill from top-left cell only
    """
    if direction == Direction.DOWN:
        _fill_down(
            draft, selection, fill_bounds, sheet_id,
            get_fill_value, recalc_cells, config, fill_from_top_left_cell
        )
    elif direction == Direction.UP:
        _fill_up(
            draft, selection, fill_bounds, sheet_id,
            get_fill_value, recalc_cells, config
        )
    elif direction == Direction.RIGHT:
        _fill_right(
            draft, selection, fill_bounds, sheet_id,
            get_fill_value, recalc_cells, config
        )
    elif direction == Direction.LEFT:
        _fill_left(
            draft, selection, fill_bounds, sheet_id,
            get_fill_value, recalc_cells, config
        )


def _fill_down(
    draft: Dict[str, Any],
    selection: SelectionArea,
    fill_bounds: GridRange,
    sheet_id: int,
    get_fill_value: Callable[[int, int], Optional[CellData]],
    recalc_cells: Dict[str, Dict[str, Any]],
    config: ApplyFillConfig,
    fill_from_top_left_cell: bool,
) -> None:
    """Fill cells downward."""
    start = selection.range.end_row_index + (0 if fill_from_top_left_cell else 1)
    end = fill_bounds.end_row_index
    counter = 0

    for i in range(start, end + 1):
        row_index = selection.range.start_row_index + counter
        if row_index > selection.range.end_row_index:
            counter = 0
            row_index = selection.range.start_row_index

        rolling_row_index = 0 if fill_from_top_left_cell else i - start

        for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
            # Skip the first cell if filling from top-left
            if (fill_from_top_left_cell and i == start and
                column_index == selection.range.start_column_index):
                continue

            rolling_column_index = 0 if fill_from_top_left_cell else column_index - selection.range.start_column_index

            new_sheet = create_sheet_draft(draft, sheet_id, i)
            new_cell_data = get_fill_value(rolling_row_index, rolling_column_index)

            # Ensure values array is long enough
            row_values = new_sheet[i]['values']
            while len(row_values) <= column_index:
                row_values.append(None)

            # Convert CellData to dict if needed
            if new_cell_data:
                row_values[column_index] = (
                    new_cell_data.model_dump(by_alias=True, exclude_none=True)
                    if hasattr(new_cell_data, 'model_dump')
                    else new_cell_data
                )
            else:
                row_values[column_index] = None

            # Enqueue calculation
            if config.enqueue_calculation:
                config.enqueue_calculation({
                    'position': {'rowIndex': i, 'columnIndex': column_index, 'sheetId': sheet_id},
                    'type': 'add',
                    'force': True,
                })

            # Track for recalculation
            cell_id = create_sheet_cell_identifier(sheet_id, i, column_index)
            recalc_cells[cell_id] = {'rowIndex': i, 'columnIndex': column_index, 'sheetId': sheet_id}

        counter += 1


def _fill_up(
    draft: Dict[str, Any],
    selection: SelectionArea,
    fill_bounds: GridRange,
    sheet_id: int,
    get_fill_value: Callable[[int, int], Optional[CellData]],
    recalc_cells: Dict[str, Dict[str, Any]],
    config: ApplyFillConfig,
) -> None:
    """Fill cells upward."""
    start = selection.range.start_row_index - 1
    end = fill_bounds.start_row_index
    counter = 0

    for i in range(start, end - 1, -1):
        row_index = selection.range.end_row_index + counter
        if row_index < selection.range.start_row_index:
            counter = 0
            row_index = selection.range.end_row_index

        rolling_row_index = start - i

        for column_index in range(selection.range.start_column_index, selection.range.end_column_index + 1):
            rolling_column_index = column_index - selection.range.start_column_index

            new_sheet = create_sheet_draft(draft, sheet_id, i)
            new_cell_data = get_fill_value(rolling_row_index, rolling_column_index)

            # Ensure values array is long enough
            row_values = new_sheet[i]['values']
            while len(row_values) <= column_index:
                row_values.append(None)

            # Convert CellData to dict if needed
            if new_cell_data:
                row_values[column_index] = (
                    new_cell_data.model_dump(by_alias=True, exclude_none=True)
                    if hasattr(new_cell_data, 'model_dump')
                    else new_cell_data
                )
            else:
                row_values[column_index] = None

            # Enqueue calculation
            if config.enqueue_calculation:
                config.enqueue_calculation({
                    'position': {'rowIndex': i, 'columnIndex': column_index, 'sheetId': sheet_id},
                    'type': 'add',
                    'force': True,
                })

            # Track for recalculation
            cell_id = create_sheet_cell_identifier(sheet_id, i, column_index)
            recalc_cells[cell_id] = {'rowIndex': i, 'columnIndex': column_index, 'sheetId': sheet_id}

        counter -= 1


def _fill_right(
    draft: Dict[str, Any],
    selection: SelectionArea,
    fill_bounds: GridRange,
    sheet_id: int,
    get_fill_value: Callable[[int, int], Optional[CellData]],
    recalc_cells: Dict[str, Dict[str, Any]],
    config: ApplyFillConfig,
) -> None:
    """Fill cells to the right."""
    for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
        start = selection.range.end_column_index + 1
        end = fill_bounds.end_column_index
        counter = 0
        rolling_row_index = row_index - selection.range.start_row_index

        for j in range(start, end + 1):
            column_index = selection.range.start_column_index + counter
            if column_index > selection.range.end_column_index:
                counter = 0
                column_index = selection.range.start_column_index

            rolling_column_index = j - start

            new_sheet = create_sheet_draft(draft, sheet_id, row_index)
            new_cell_data = get_fill_value(rolling_row_index, rolling_column_index)

            # Ensure values array is long enough
            row_values = new_sheet[row_index]['values']
            while len(row_values) <= j:
                row_values.append(None)

            # Convert CellData to dict if needed
            if new_cell_data:
                row_values[j] = (
                    new_cell_data.model_dump(by_alias=True, exclude_none=True)
                    if hasattr(new_cell_data, 'model_dump')
                    else new_cell_data
                )
            else:
                row_values[j] = None

            # Enqueue calculation
            if config.enqueue_calculation:
                config.enqueue_calculation({
                    'position': {'rowIndex': row_index, 'columnIndex': j, 'sheetId': sheet_id},
                    'type': 'add',
                    'force': True,
                })

            # Track for recalculation
            cell_id = create_sheet_cell_identifier(sheet_id, row_index, j)
            recalc_cells[cell_id] = {'rowIndex': row_index, 'columnIndex': j, 'sheetId': sheet_id}

            counter += 1


def _fill_left(
    draft: Dict[str, Any],
    selection: SelectionArea,
    fill_bounds: GridRange,
    sheet_id: int,
    get_fill_value: Callable[[int, int], Optional[CellData]],
    recalc_cells: Dict[str, Dict[str, Any]],
    config: ApplyFillConfig,
) -> None:
    """Fill cells to the left."""
    for row_index in range(selection.range.start_row_index, selection.range.end_row_index + 1):
        start = selection.range.start_column_index - 1
        end = fill_bounds.start_column_index
        rolling_row_index = row_index - selection.range.start_row_index
        counter = 0

        for j in range(start, end - 1, -1):
            column_index = selection.range.end_column_index + counter
            if column_index < selection.range.start_column_index:
                counter = 0
                column_index = selection.range.end_column_index

            rolling_column_index = start - j

            new_sheet = create_sheet_draft(draft, sheet_id, row_index)
            new_cell_data = get_fill_value(rolling_row_index, rolling_column_index)

            # Ensure values array is long enough
            row_values = new_sheet[row_index]['values']
            while len(row_values) <= j:
                row_values.append(None)

            # Convert CellData to dict if needed
            if new_cell_data:
                row_values[j] = (
                    new_cell_data.model_dump(by_alias=True, exclude_none=True)
                    if hasattr(new_cell_data, 'model_dump')
                    else new_cell_data
                )
            else:
                row_values[j] = None

            # Enqueue calculation
            if config.enqueue_calculation:
                config.enqueue_calculation({
                    'position': {'rowIndex': row_index, 'columnIndex': j, 'sheetId': sheet_id},
                    'type': 'add',
                    'force': True,
                })

            # Track for recalculation
            cell_id = create_sheet_cell_identifier(sheet_id, row_index, j)
            recalc_cells[cell_id] = {'rowIndex': row_index, 'columnIndex': j, 'sheetId': sheet_id}

            counter -= 1
