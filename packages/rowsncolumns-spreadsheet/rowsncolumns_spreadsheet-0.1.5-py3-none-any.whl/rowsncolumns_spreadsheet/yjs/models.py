"""Pydantic models for sheet formatting and operations."""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

# ==================== FORMATTING MODELS ====================


class BorderStyle(str, Enum):
    dotted = "dotted"
    dashed = "dashed"
    solid = "solid"
    solid_medium = "solid_medium"
    solid_thick = "solid_thick"
    double = "double"


class ThemeColor(BaseModel):
    theme: int = Field(ge=0, le=10)
    tint: Optional[float] = None


Color = Union[str, ThemeColor]


class BorderModel(BaseModel):
    style: BorderStyle
    width: int
    color: Color = Field(
        default={"theme": 1},
        description="Border color. Defaults to theme color 1 (default black). Always set the color if border width and border style is present",
    )


class BordersModel(BaseModel):
    """
    Border configuration for spreadsheet cells. Set individual borders (top, right, bottom, left) to apply borders around cells.

    Common border patterns:
    - All borders: Set all four sides (top, right, bottom, left) to create borders around every cell
    - Outer border only: For a range A1:C3, only the perimeter cells get borders (first row gets top, last row gets bottom, etc.)
    - Inner borders only: Only borders between cells, not on the outer edges
    - Horizontal lines: Set only top and/or bottom borders
    - Vertical lines: Set only left and/or right borders
    - Single side: Set only one border (e.g., just bottom for underline effect)

    Note: Borders are applied per-cell. Each cell's border properties control which edges of that specific cell have borders. Overlapping borders between adjacent cells will appear as a single line.

    Examples:
    - Box around range: Set all four borders on all cells in the range
    - Table with grid: Set all four borders to create a complete grid
    - Underline header: Set only bottom border on header row
    - Separate sections: Set bottom border to divide content
    """

    top: Optional[BorderModel] = Field(None, description="Top border of the cell")
    right: Optional[BorderModel] = Field(None, description="Right border of the cell")
    bottom: Optional[BorderModel] = Field(None, description="Bottom border of the cell")
    left: Optional[BorderModel] = Field(None, description="Left border of the cell")


HorizontalAlignmentLiteral = Literal["left", "right", "center"]
VerticalAlignmentLiteral = Literal["top", "middle", "bottom"]


class WrapStrategy(str, Enum):
    overflow = "overflow"
    wrap = "wrap"
    clip = "clip"


class TextFormatModel(BaseModel):
    color: Optional[Color] = None
    fontFamily: Optional[str] = None
    fontSize: Optional[int] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    strikethrough: Optional[bool] = None
    underline: Optional[bool] = None


class NumberFormatType(str, Enum):
    GENERAL = "GENERAL"
    NUMBER = "NUMBER"
    CURRENCY = "CURRENCY"
    ACCOUNTING = "ACCOUNTING"
    DATE = "DATE"
    TIME = "TIME"
    DATE_TIME = "DATE_TIME"
    PERCENT = "PERCENT"
    FRACTION = "FRACTION"
    SCIENTIFIC = "SCIENTIFIC"
    TEXT = "TEXT"
    SPECIAL = "SPECIAL"


class NumberFormatModel(BaseModel):
    type: NumberFormatType = Field(
        description="Target number format category (NUMBER, CURRENCY, DATE, etc.)",
    )
    pattern: str = Field(
        ...,
        description=(
            "Excel-compatible format string. If omitted, the server will pick a sensible default "
            "based on the chosen type (e.g. NUMBER → '#,##0', CURRENCY → '$#,##0.00')."
        ),
    )

class GridRange(BaseModel):
    startRowIndex: int = Field(
        ...,
        description=(
            "Start row index (1-based, INCLUSIVE). First row of the range. "
            "For A1 this would be 1, for A5 this would be 5."
        ),
    )
    endRowIndex: int = Field(
        ...,
        description=(
            "End row index (1-based, INCLUSIVE). Last row of the range. "
            "For a range A1:A5, this would be 5. For single cells, equals startRowIndex."
        ),
    )
    startColumnIndex: int = Field(
        ...,
        description=(
            "Start column index (1-based, INCLUSIVE). First column of the range. "
            "A=1, B=2, C=3, etc. For range A1:C5, this would be 1."
        ),
    )
    endColumnIndex: int = Field(
        ...,
        description=(
            "End column index (1-based, INCLUSIVE). Last column of the range. "
            "For range A1:C5, this would be 3. For single columns, equals startColumnIndex."
        ),
    )

class CellFormat(BaseModel):
    backgroundColor: Optional[Color] = None
    borders: Optional[BordersModel] = None
    textFormat: Optional[TextFormatModel] = None
    numberFormat: Optional[NumberFormatModel] = None
    horizontalAlignment: Optional[HorizontalAlignmentLiteral] = None
    verticalAlignment: Optional[VerticalAlignmentLiteral] = None
    wrapStrategy: Optional[WrapStrategy] = None
    indent: Optional[int] = None
    textRotation: Optional[Union[int, Literal["vertical"]]] = None


class DimensionProperties(BaseModel):
    size: Optional[int] = None
    resizedByUser: Optional[bool] = None
    hiddenByUser: Optional[bool] = None
    hiddenByFilter: Optional[bool] = None
    
class Sheet(BaseModel):
    title: Optional[str] = None
    sheetId: Optional[int] = Field(default=None, description="Sheet ID (optional)")
    index: Optional[int] = Field(default=None, description="Sheet ordering index")
    rowCount: Optional[int] = Field(default=None, description="Row count")
    columnCount: Optional[int] = Field(default=None, description="Column count")
    frozenRowCount: Optional[int] = None
    frozenColumnCount: Optional[int] = None
    tabColor: Optional[Color] = None
    hidden: Optional[bool] = None
    showGridLines: Optional[bool] = None
    merges: Optional[List[GridRange]] = None
    basicFilter: Optional[dict] = None
    rowMetadata: Optional[List[Optional[DimensionProperties]]] = None
    columnMetadata: Optional[List[Optional[DimensionProperties]]] = None

    model_config = {"populate_by_name": True, "extra": "allow"}

class FormattingType(str, Enum):
    backgroundColor = "backgroundColor"
    borders = "borders"
    textFormat = "textFormat"
    numberFormat = "numberFormat"
    horizontalAlignment = "horizontalAlignment"
    verticalAlignment = "verticalAlignment"
    wrapStrategy = "wrapStrategy"
    indent = "indent"
    textRotation = "textRotation"
