"""
Rows & Columns Spreadsheet - Python Implementation

A Python library for spreadsheet operations, providing data manipulation
capabilities similar to the TypeScript version.
"""

from .types import (
    CellData,
    GridRange,
    SheetRange,
    SelectionArea,
    Sheet,
    CellInterface,
    Direction,
    SpreadsheetState,
    ExtendedValue,
    ErrorValue,
    Table,
    FilterView,
    MergedCell,
    RowData,
    Color,
    RowMetadata,
    ColumnMetadata,
    HistoryEntry,
    NamedRange,
    TableView,
    TableColumn,
)
from .spreadsheet import Spreadsheet
from .operations import insert_row, delete_row, insert_column, delete_column
# from .interface import SpreadsheetInterface  # Not yet implemented
# from .immer_interface import ImmerSpreadsheetInterface, produce_with_patches, apply_patches  # Not yet implemented
from .interface.apply_fill import apply_fill, ApplyFillConfig
from .interface.fill import (
    get_auto_fill_values,
    detect_fill_type,
    generate_fill_values,
    AutoFillType,
)
from .patches import SpreadsheetPatch, JSONPatch, PatchGenerator
from .sheet_cell import SheetCell, DEFAULT_SHEET_ID, DEFAULT_CELL_COORDS
from .sheet_cell_helpers import (
    create_row_data_from_array,
    is_cell_range,
    combine_map_iterators,
    get_next_table_column_name,
    get_conflicting_table,
    hash_object,
    AWAITING_CALCULATION,
)
from .datatype import (
    detect_value_type_and_pattern,
    detect_value_type,
    detect_number_format_type,
    detect_number_format_pattern,
    detect_decimal_pattern,
    is_currency,
    is_boolean,
    is_percentage,
    is_number,
    is_formula,
    is_valid_url_or_email,
    is_multiline,
    convert_to_number,
    create_formatted_value,
    PATTERN_NUMBER,
    PATTERN_NUMBER_THOUSANDS,
    PATTERN_PERCENT,
    PATTERN_CURRENCY,
)
from .dag import (
    SpreadsheetDag,
    CellPosition,
    CellRangePosition,
    StaticReference,
    CircularDependencyError,
    UnknownSheetError,
)

__version__ = "0.1.1"
__all__ = [
    "CellData",
    "GridRange",
    "SheetRange",
    "SelectionArea",
    "Sheet",
    "CellInterface",
    "Direction",
    "SpreadsheetState",
    "ExtendedValue",
    "ErrorValue",
    "Table",
    "FilterView",
    "MergedCell",
    "RowData",
    "Color",
    "RowMetadata",
    "ColumnMetadata",
    "HistoryEntry",
    "NamedRange",
    "TableView",
    "TableColumn",
    "Spreadsheet",
    # "SpreadsheetInterface",  # Not yet implemented
    # "ImmerSpreadsheetInterface",  # Not yet implemented
    # "produce_with_patches",  # Not yet implemented
    # "apply_patches",  # Not yet implemented
    "apply_fill",
    "ApplyFillConfig",
    "get_auto_fill_values",
    "detect_fill_type",
    "generate_fill_values",
    "AutoFillType",
    "SpreadsheetPatch",
    "JSONPatch",
    "PatchGenerator",
    "insert_row",
    "delete_row",
    "insert_column",
    "delete_column",
    "SheetCell",
    "DEFAULT_SHEET_ID",
    "DEFAULT_CELL_COORDS",
    "create_row_data_from_array",
    "is_cell_range",
    "combine_map_iterators",
    "get_next_table_column_name",
    "get_conflicting_table",
    "hash_object",
    "AWAITING_CALCULATION",
    "detect_value_type_and_pattern",
    "detect_value_type",
    "detect_number_format_type",
    "detect_number_format_pattern",
    "detect_decimal_pattern",
    "is_currency",
    "is_boolean",
    "is_percentage",
    "is_number",
    "is_formula",
    "is_valid_url_or_email",
    "is_multiline",
    "convert_to_number",
    "create_formatted_value",
    "PATTERN_NUMBER",
    "PATTERN_NUMBER_THOUSANDS",
    "PATTERN_PERCENT",
    "PATTERN_CURRENCY",
    "SpreadsheetDag",
    "CellPosition",
    "CellRangePosition",
    "StaticReference",
    "CircularDependencyError",
    "UnknownSheetError",
    "change_batch_yjs",
    "change_formatting_yjs",
    "create_table_yjs",
    "update_table_yjs",
    "create_sheet_yjs",
    "insert_row_yjs",
    "insert_column_yjs",
    "insert_table_column_yjs",
    "delete_row_yjs",
    "delete_column_yjs",
    "delete_table_column_yjs",
]

from .yjs import change_batch as change_batch_yjs
from .yjs import change_formatting as change_formatting_yjs
from .yjs import create_table as create_table_yjs
from .yjs import update_sheet as update_sheet_yjs
from .yjs import update_table as update_table_yjs
from .yjs import create_sheet as create_sheet_yjs
from .yjs import insert_row as insert_row_yjs
from .yjs import insert_column as insert_column_yjs
from .yjs import insert_table_column as insert_table_column_yjs
from .yjs import delete_row as delete_row_yjs
from .yjs import delete_column as delete_column_yjs
from .yjs import delete_table_column as delete_table_column_yjs
