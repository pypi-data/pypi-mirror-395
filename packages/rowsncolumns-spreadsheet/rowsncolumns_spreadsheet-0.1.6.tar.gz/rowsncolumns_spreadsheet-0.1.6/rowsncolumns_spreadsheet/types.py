"""
Core data types for the spreadsheet library.

These types mirror the TypeScript definitions but use Python/Pydantic conventions.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field, AliasChoices


class Direction(Enum):
    """Direction for operations like moving cells."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class CellInterface(BaseModel):
    """Represents a single cell coordinate."""
    row_index: int = Field(ge=0, description="Row index (0-based)")
    column_index: int = Field(ge=0, description="Column index (0-based)")


class GridRange(BaseModel):
    """Represents a rectangular range of cells."""
    start_row_index: int = Field(ge=0)
    end_row_index: int = Field(ge=0)
    start_column_index: int = Field(ge=0)
    end_column_index: int = Field(ge=0)

    def model_post_init(self, __context: Any) -> None:
        """Validate that start indices are <= end indices."""
        if self.start_row_index > self.end_row_index:
            raise ValueError("start_row_index must be <= end_row_index")
        if self.start_column_index > self.end_column_index:
            raise ValueError("start_column_index must be <= end_column_index")


class SheetRange(GridRange):
    """GridRange with associated sheet."""
    sheet_id: int = Field(ge=0)


class SelectionAttributes(BaseModel):
    """Attributes for a selection area."""
    in_progress: bool = False
    is_filling: bool = False


class SelectionArea(BaseModel):
    """Represents a selected area in the spreadsheet."""
    range: GridRange
    attributes: Optional[SelectionAttributes] = None


class Color(BaseModel):
    """Color specification - can be theme-based or custom."""
    theme: Optional[int] = Field(None, ge=0, le=10)
    red: Optional[int] = Field(None, ge=0, le=255)
    green: Optional[int] = Field(None, ge=0, le=255)
    blue: Optional[int] = Field(None, ge=0, le=255)
    alpha: Optional[float] = Field(None, ge=0.0, le=1.0)


class FilterView(BaseModel):
    """Represents a filter view on a range."""
    range: GridRange
    title: Optional[str] = None


class MergedCell(BaseModel):
    """Represents a merged cell range."""
    range: GridRange


class RowMetadata(BaseModel):
    """Metadata for a row."""
    size: Optional[float] = None  # Row height
    hidden: bool = False


class ColumnMetadata(BaseModel):
    """Metadata for a column."""
    size: Optional[float] = None  # Column width
    hidden: bool = False


class NamedRange(BaseModel):
    """Represents a named range within a sheet."""
    named_range_id: Union[int, str] = Field(
        validation_alias=AliasChoices("namedRangeId", "named_range_id")
    )
    name: str
    range: Optional[SheetRange] = None
    value: Optional[Any] = None

    model_config = {"populate_by_name": True}


class TableColumn(BaseModel):
    """Column definition for table structured references."""
    name: str
    filter_button: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("filterButton", "filter_button"),
    )
    formula: Optional[str] = None

    model_config = {"populate_by_name": True}


class TableView(FilterView):
    """Represents an Excel-style table definition."""
    title: str
    sheet_id: int = Field(
        ge=0,
        validation_alias=AliasChoices("sheetId", "sheet_id"),
    )
    header_row: Optional[bool] = Field(
        default=True,
        validation_alias=AliasChoices("headerRow", "header_row"),
    )
    total_row: Optional[bool] = Field(
        default=False,
        validation_alias=AliasChoices("totalRow", "total_row"),
    )
    columns: Optional[List[TableColumn]] = None
    model_config = {"populate_by_name": True}


class Sheet(BaseModel):
    """Represents a worksheet."""
    sheet_id: int = Field(ge=0)
    name: str
    index: int = Field(ge=0)
    row_count: int = Field(default=1000, ge=1)
    column_count: int = Field(default=26, ge=1)
    frozen_row_count: Optional[int] = Field(default=None, ge=0)
    frozen_column_count: Optional[int] = Field(default=None, ge=0)
    tab_color: Optional[Color] = None
    hidden: bool = False
    basic_filter: Optional[FilterView] = None
    merges: Optional[List[MergedCell]] = None
    row_metadata: Optional[Dict[int, RowMetadata]] = None
    column_metadata: Optional[Dict[int, ColumnMetadata]] = None


class ErrorValue(BaseModel):
    """Represents an error value for cells, aligning with TypeScript ErrorValue."""
    type: Literal["Error", "Invalid"]
    message: str


class ExtendedValue(BaseModel):
    """Represents the possible primitive values in a cell, similar to TS ExtendedValue.

    Note: Uses camelCase field names (matching TypeScript) as primary names.
    Supports multiple aliases for input:
    - Full camelCase: numberValue, stringValue, etc.
    - Snake_case: number_value, string_value, etc.
    - Shorthand (TS compact): nv, sv, fv, bv, ev

    Serializes using shorthand keys for primitives (nv, sv, fv, bv, ev).
    structuredValue is NOT shortened - it remains as 'structuredValue'.
    """
    numberValue: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("numberValue", "number_value", "nv"),
        serialization_alias="nv"
    )
    stringValue: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stringValue", "string_value", "sv"),
        serialization_alias="sv"
    )
    boolValue: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("boolValue", "bool_value", "bv"),
        serialization_alias="bv"
    )
    formulaValue: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("formulaValue", "formula_value", "fv"),
        serialization_alias="fv"
    )
    errorValue: Optional[ErrorValue] = Field(
        default=None,
        validation_alias=AliasChoices("errorValue", "error_value", "ev"),
        serialization_alias="ev"
    )
    structuredValue: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias=AliasChoices("structuredValue", "structured_value", "stv"),
        serialization_alias="structuredValue"
    )

    model_config = {
        "populate_by_name": True
    }


class CellData(BaseModel):
    """
    Cell data model broadly aligned with the TypeScript `CellData` shape.

    Notes:
    - Keeps legacy fields (value, formula, format) for backward compatibility
    - Supports multiple aliases for TS compatibility:
      - Full camelCase: userEnteredValue, effectiveValue, etc.
      - Snake_case: user_entered_value, effective_value, etc.
      - Shorthand (TS compact): ue, ev, fv, uf, ef, etc.
    """
    # Legacy/simple fields used by current python helpers
    value: Any = None
    formula: Optional[str] = None
    format: Optional[Dict[str, Any]] = None

    # TS-aligned fields with multiple alias support
    user_entered_value: Optional[ExtendedValue] = Field(
        default=None,
        validation_alias=AliasChoices("userEnteredValue", "user_entered_value", "ue")
    )
    effective_value: Optional[ExtendedValue] = Field(
        default=None,
        validation_alias=AliasChoices("effectiveValue", "effective_value", "ev")
    )
    formatted_value: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("formattedValue", "formatted_value", "fv")
    )
    text_format_runs: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        validation_alias=AliasChoices("textFormatRuns", "text_format_runs", "tfr")
    )
    note: Optional[str] = None
    hyperlink: Optional[str] = None
    data_validation: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias=AliasChoices("dataValidation", "data_validation", "dv")
    )
    image_url: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("imageUrl", "image_url", "iu")
    )
    meta_type: Optional[Literal["people"]] = Field(
        default=None,
        validation_alias=AliasChoices("metaType", "meta_type", "mt")
    )
    user_entered_format: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias=AliasChoices("userEnteredFormat", "user_entered_format", "uf")
    )
    effective_format: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias=AliasChoices("effectiveFormat", "effective_format", "ef")
    )
    collapsible: Optional[bool] = None
    is_collapsed: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("isCollapsed", "is_collapsed", "ic")
    )

    model_config = {
        "populate_by_name": True
    }


class RowData(BaseModel):
    """
    RowData mirrors the TypeScript row shape used in SheetData where a row is an
    object that may or may not contain a `values` array.
    """
    values: Optional[List[Optional[CellData]]] = None


class Table(BaseModel):
    """Represents a table within a sheet."""
    sheet_id: int = Field(ge=0)
    range: GridRange
    name: Optional[str] = None


class HistoryEntry(BaseModel):
    """Represents an entry in the operation history for undo/redo."""
    operation: str
    timestamp: float
    data: Dict[str, Any]


class SpreadsheetState(BaseModel):
    """Complete state of a spreadsheet."""
    sheets: List[Sheet] = Field(default_factory=list)
    # SheetData<CellData>: Map of sheetId -> array of (RowData | null)
    sheet_data: Dict[int, List[Optional[RowData]]] = Field(default_factory=dict)
    tables: List[Table] = Field(default_factory=list)
    active_sheet_id: Optional[int] = None
    selections: Dict[int, List[SelectionArea]] = Field(default_factory=dict)
    history: List[HistoryEntry] = Field(default_factory=list)
