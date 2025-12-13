"""
SheetCell - Python port of the TypeScript SheetCell class.

This module provides a comprehensive cell abstraction that handles all aspects
of spreadsheet cell management including values, formatting, validation, and formulas.
"""

from typing import Any, Dict, List, Optional, Union, Literal, Callable, TypeVar, Generic
import re

from .types import CellData, ExtendedValue, ErrorValue, CellInterface
from .cell_xfs import register_cell_xfs_registry
from .datatype import (
    detect_value_type_and_pattern,
    detect_value_type,
    detect_number_format_type,
    detect_number_format_pattern,
    convert_to_number,
    is_valid_url_or_email,
    is_multiline as check_multiline,
    create_formatted_value,
    create_formatted_color,
)
from .sheet_cell_helpers import AWAITING_CALCULATION


# Type variable for generic CellData
T = TypeVar('T', bound=CellData)

# Constants
DEFAULT_SHEET_ID = 1
DEFAULT_CELL_COORDS = CellInterface(row_index=1, column_index=1)

# Keys to exclude from user cell data
EXCLUDE_KEYS = {
    "userEnteredValue", "ue", "user_entered_value",
    "effectiveValue", "ev", "effective_value",
    "formattedValue", "fv", "formatted_value",
    "effectiveFormat", "ef", "effective_format",
    "userEnteredFormat", "uf", "user_entered_format",
    "dataValidation", "data_validation",
    "imageUrl", "image_url",
    "hyperlink",
    "metaType", "meta_type",
    "note",
    "collapsible",
    "isCollapsed", "is_collapsed",
    "conditionalFormattingResultById", "conditional_formatting_result_by_id",
    "dataValidationResult", "data_validation_result",
    "textFormatRuns", "text_format_runs",
}


class SheetCell(Generic[T]):
    """
    SheetCell provides a comprehensive abstraction for managing individual cell data.

    This class handles:
    - Multiple value types (string, number, boolean, formula, date)
    - User-entered and effective values
    - Cell formatting (text, number, borders, etc.)
    - Data validation
    - Conditional formatting
    - Hyperlinks and images
    - Formula management and relative references
    """

    def __init__(
        self,
        sheet_id: int = DEFAULT_SHEET_ID,
        coords: Optional[CellInterface] = None,
        cell_data: Optional[T] = None,
        get_range_values: Optional[Callable[[str], List[Any]]] = None,
        locale: str = "en-US",
        cell_xfs_registry: Optional[Any] = None,
    ):
        """
        Initialize a SheetCell instance.

        Args:
            sheet_id: Sheet identifier (default: 1)
            coords: Cell coordinates (row_index, column_index)
            cell_data: Optional cell data to initialize with
            get_range_values: Optional function to get range values for validation
            locale: Locale for formatting (default: "en-US")
            cell_xfs_registry: Optional registry for cell formatting styles
        """
        # Core properties
        self.sheet_id: int = sheet_id
        self.coords: CellInterface = coords or DEFAULT_CELL_COORDS
        self.cell_data: Optional[T] = None
        self.cell_xfs_registry: Optional[Any] = cell_xfs_registry

        # Value properties
        self.value: Optional[str] = None
        self.user_entered_value: Optional[ExtendedValue] = None
        self.effective_value: Optional[ExtendedValue] = None
        self.formatted_value: Optional[str] = None
        self.text_format_runs: Optional[List[Dict[str, Any]]] = None

        # Format properties
        self.user_entered_format: Optional[Dict[str, Any]] = None
        self.effective_format: Optional[Dict[str, Any]] = None
        self.original_user_entered_format: Optional[Dict[str, Any]] = None
        self.original_effective_format: Optional[Dict[str, Any]] = None

        # Validation and conditional formatting
        self.data_validation: Optional[Dict[str, Any]] = None
        self.conditional_formatting_result_by_id: Optional[Dict[Union[int, str], Any]] = None
        self.data_validation_result: Optional[Any] = None

        # Additional properties
        self.hyperlink: Optional[str] = None
        self.image_url: Optional[str] = None
        self.note: Optional[str] = None
        self.meta_type: Optional[Literal["people"]] = None
        self.collapsible: Optional[bool] = None
        self.is_collapsed: Optional[bool] = None

        # Formatting defaults
        self.default_pattern: str = "General"
        self.loading_value: str = "Loading..."
        self.is_loading: bool = False
        self.format_color: Optional[str] = None

        # Functions
        self.get_range_values: Optional[Callable[[str], List[Any]]] = get_range_values
        self.locale: str = locale

        # Initialize with cell data if provided
        if cell_data is not None:
            self.assign(
                sheet_id=sheet_id,
                coords=coords or DEFAULT_CELL_COORDS,
                cell_data=cell_data,
                get_range_values=get_range_values,
                locale=locale,
                cell_xfs_registry=cell_xfs_registry,
            )

    def assign(
        self,
        sheet_id: int = DEFAULT_SHEET_ID,
        coords: Optional[CellInterface] = None,
        cell_data: Optional[T] = None,
        get_range_values: Optional[Callable[[str], List[Any]]] = None,
        locale: str = "en-US",
        cell_xfs_registry: Optional[Any] = None,
    ) -> 'SheetCell[T]':
        """
        Assign data to the cell, replacing existing data.

        Args:
            sheet_id: Sheet identifier
            coords: Cell coordinates
            cell_data: Cell data to assign
            get_range_values: Function to get range values
            locale: Locale for formatting
            cell_xfs_registry: Cell formatting registry

        Returns:
            Self for method chaining
        """
        self.sheet_id = sheet_id
        self.coords = coords or DEFAULT_CELL_COORDS
        self.cell_data = cell_data
        self.cell_xfs_registry = cell_xfs_registry
        self.locale = locale
        self.get_range_values = get_range_values

        if cell_data is None:
            # Reset to defaults
            self.user_entered_value = None
            self.effective_value = None
            self.formatted_value = None
            self.user_entered_format = None
            self.effective_format = None
            self.data_validation = None
            self.image_url = None
            self.hyperlink = None
            self.note = None
            self.text_format_runs = None
            return self

        # Extract values from cell_data
        self.user_entered_value = self._get_cell_user_entered_value(cell_data)
        self.effective_value = self._get_cell_effective_value(cell_data)
        self.formatted_value = self._get_cell_formatted_value(cell_data)

        # Extract formats
        user_format = self._get_cell_user_entered_format(cell_data)
        effective_format = self._get_cell_effective_format(cell_data)

        # Handle style references if cell_xfs_registry is available
        self.user_entered_format = self._resolve_format(user_format, cell_xfs_registry)
        self.effective_format = self._resolve_format(effective_format, cell_xfs_registry)
        self.original_user_entered_format = user_format
        self.original_effective_format = effective_format

        # Extract other properties
        self.data_validation = getattr(cell_data, 'data_validation', None)
        self.conditional_formatting_result_by_id = getattr(
            cell_data, 'conditional_formatting_result_by_id', None
        )
        self.data_validation_result = getattr(cell_data, 'data_validation_result', None)
        self.image_url = getattr(cell_data, 'image_url', None)
        self.hyperlink = getattr(cell_data, 'hyperlink', None)
        self.meta_type = getattr(cell_data, 'meta_type', None)
        self.note = getattr(cell_data, 'note', None)
        self.collapsible = getattr(cell_data, 'collapsible', None)
        self.is_collapsed = getattr(cell_data, 'is_collapsed', None)
        self.text_format_runs = getattr(cell_data, 'text_format_runs', None)

        self.is_loading = False

        return self

    def set_locale(self, locale: str) -> None:
        """Set the locale for this cell."""
        self.locale = locale

    @property
    def key(self) -> str:
        """Generate unique cell key in format: {sheetId}!{cellAddress}"""
        return self.generate_cell_key(
            self.sheet_id,
            self.coords.row_index,
            self.coords.column_index
        )

    @staticmethod
    def generate_cell_key(sheet_id: int, row_index: int, column_index: int) -> str:
        """
        Generate a unique cell key.

        Args:
            sheet_id: Sheet identifier
            row_index: Row index
            column_index: Column index

        Returns:
            Cell key in format: {sheetId}!{cellAddress}
        """
        cell_address = SheetCell._cell_to_address(row_index, column_index)
        return f"{sheet_id}!{cell_address}"

    @staticmethod
    def _cell_to_address(row_index: int, column_index: int) -> str:
        """
        Convert cell coordinates to A1 notation.

        Args:
            row_index: Zero-based row index
            column_index: Zero-based column index

        Returns:
            Cell address in A1 notation (e.g., "A1", "B2")
        """
        # Convert column index to letter(s)
        column = ""
        col = column_index + 1
        while col > 0:
            col -= 1
            column = chr(65 + (col % 26)) + column
            col //= 26

        # Row is 1-indexed
        return f"{column}{row_index + 1}"

    @property
    def formula(self) -> Optional[str]:
        """Get the formula from user-entered value."""
        if self.user_entered_value is None:
            return None
        return self.user_entered_value.formulaValue

    @property
    def is_modified(self) -> bool:
        """Check if the cell has been modified from its original data."""
        original_data = self.cell_data
        current_data = self.get_cell_data()
        return original_data != current_data

    def is_formula(self) -> bool:
        """Check if this cell contains a formula."""
        return self.formula is not None and self.formula != ""

    def is_structured_reference_formula(self) -> bool:
        """
        Check if formula contains table references.

        Examples: [Column], [@Column], TableName[Column]
        """
        if not self.formula:
            return False
        # Regex matches table references
        return bool(re.search(r'(\w+\[[@]?\w+\]|\[[@]?\w+\])', self.formula))

    def ephemeral(self) -> bool:
        """Check if formula contains absolute references or is a table reference."""
        return self.is_structured_reference_formula() or (
            self.formula is not None and "$" in self.formula
        )

    def is_empty(self) -> bool:
        """Check if the cell is empty."""
        if self.user_entered_value is None:
            return True
        return self.user_entered_value.stringValue is None or self.user_entered_value.stringValue == ""

    def is_multiline(self) -> bool:
        """Check if value contains multiline text."""
        user_value = self.get_user_entered_value()
        if isinstance(user_value, str):
            return check_multiline(user_value)
        return False

    def delete_contents(self) -> None:
        """
        Delete cell contents while preserving formatting.

        Note: Only deletes data validation if user double-deletes or it's a boolean cell.
        """
        # Only delete data validation if empty or boolean type
        if (
            not self.user_entered_value
            or (
                self.data_validation is not None
                and isinstance(self.data_validation, dict)
                and self.data_validation.get('condition', {}).get('type') == 'BOOLEAN'
            )
        ):
            self.data_validation = None

        # Clear cell data and values
        self.cell_data = None
        self.user_entered_value = None
        self.effective_value = None
        self.effective_format = None
        self.formatted_value = None
        self.image_url = None
        self.hyperlink = None
        self.meta_type = None
        self.note = None
        self.text_format_runs = None

        # Smart format deletion
        if self.user_entered_format is not None:
            number_format = self.user_entered_format.get('numberFormat')
            if number_format and isinstance(number_format, dict):
                nf_type = number_format.get('type')
                nf_pattern = number_format.get('pattern')
                # Remove basic number or text formats
                if (
                    (nf_type == 'NUMBER' and nf_pattern in ['0', '#,##0'])
                    or nf_type == 'TEXT'
                ):
                    self.user_entered_format = None

        # Preserve data validation result only if data validation exists
        if not self.data_validation:
            self.data_validation_result = None

    def clear_user_entered_value(self) -> None:
        """Clear the user-entered value."""
        self.user_entered_value = None
        self.formatted_value = None
        self.text_format_runs = None
        self.effective_value = None

    def clear_effective_value_for_formula(self) -> None:
        """Clear effective value (used for formulas awaiting calculation)."""
        self.effective_value = None
        self.text_format_runs = None
        self.formatted_value = ""

    def clone_with_formatting(self) -> 'SheetCell[T]':
        """Clone cell while deleting contents."""
        self.delete_contents()
        return self

    def update_note(self, note: Optional[str]) -> None:
        """Update cell note/comment."""
        self.note = note

    def set_loading(self) -> None:
        """Mark cell as loading."""
        self.is_loading = True
        self.effective_value = None

    def hide_loading(self) -> None:
        """Mark cell as not loading."""
        self.is_loading = False

    def inherit_cell_data(self, cell_data: Optional[T]) -> None:
        """Inherit a different set of cell data."""
        self.cell_data = cell_data

    def extend_cell_data(self, new_cell_data: Optional[T]) -> None:
        """Extend cell data with new data by reassigning."""
        self.assign(
            sheet_id=self.sheet_id,
            coords=self.coords,
            cell_data=new_cell_data,
            get_range_values=self.get_range_values,
            locale=self.locale,
            cell_xfs_registry=self.cell_xfs_registry,
        )

    def _set_user_entered_value_by_type(
        self,
        value_type: str,
        value: Union[str, int, float, bool],
        text_format_runs: Optional[List[Dict[str, Any]]] = None,
        number_format_type: Optional[str] = None,
        number_value: Optional[float] = None,
        pattern: Optional[str] = None,
    ) -> None:
        """
        Set user-entered value by detected type.

        Args:
            value_type: Detected value type key
            value: Original value
            text_format_runs: Text formatting runs
            number_format_type: Number format type
            number_value: Converted number value
            pattern: Format pattern
        """
        if value_type == "boolValue":
            self._set_boolean_value(value)
        elif value_type == "numberValue":
            self._set_number_value_with_format(value, number_format_type, number_value, pattern)
        elif value_type == "formulaValue":
            self.set_formula_value(str(value))
        elif value_type == "stringValue":
            # Check if it's a URL
            if isinstance(value, str) and is_valid_url_or_email(value):
                self.set_url(value)
            else:
                self._set_string_value(str(value), text_format_runs)

    def _set_boolean_value(self, value: Union[bool, str, int, float]) -> None:
        """Set boolean value."""
        effective_value = str(value).upper() == 'TRUE'

        self.user_entered_value = ExtendedValue(boolValue=effective_value)
        self.effective_value = ExtendedValue(boolValue=effective_value)
        self.formatted_value = str(value).upper()

        # Remove number format
        if self.user_entered_format and 'numberFormat' in self.user_entered_format:
            del self.user_entered_format['numberFormat']
        if self.effective_format and 'numberFormat' in self.effective_format:
            del self.effective_format['numberFormat']

        # Set alignment
        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'center'

    def _set_number_value(self, value: Union[int, float]) -> None:
        """Set number value (simple version without format detection)."""
        self.user_entered_value = ExtendedValue(stringValue=str(value))
        self.effective_value = ExtendedValue(numberValue=float(value))
        self.formatted_value = str(value)

        # Set alignment
        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'right'

    def _set_number_value_with_format(
        self,
        value: Union[str, int, float],
        number_format_type: Optional[str] = None,
        number_value: Optional[float] = None,
        pattern: Optional[str] = None,
    ) -> None:
        """
        Set number value with format detection.

        Args:
            value: Original value
            number_format_type: Detected format type
            number_value: Converted number value
            pattern: Format pattern
        """
        # Check if we should preserve existing format
        existing_format = None
        if self.user_entered_format is not None:
            num_fmt = self.user_entered_format.get('numberFormat')
            if isinstance(num_fmt, dict):
                existing_format = num_fmt

        final_format_type = number_format_type
        final_pattern = pattern

        # Excel-like behavior: preserve existing format for plain numbers
        if existing_format is not None and self._should_preserve_existing_format(
            number_format_type, existing_format, pattern
        ):
            final_format_type = existing_format.get('type')
            final_pattern = existing_format.get('pattern')

        # Calculate string value for user entered value
        string_value = self._get_string_value_for_format(value, number_value, final_format_type)

        # Create formatted display value
        if (
            isinstance(value, str)
            and final_format_type in {"CURRENCY", "ACCOUNTING"}
            and value.strip()
        ):
            self.formatted_value = value
        elif number_value is not None and final_pattern:
            self.formatted_value = create_formatted_value(
                number_value, "numberValue", final_pattern
            )
        else:
            self.formatted_value = str(number_value or value)

        # Set color from pattern
        if number_value is not None and final_pattern:
            format_color = create_formatted_color(number_value, "numberValue", final_pattern)
            self.set_effective_text_format_color(format_color)

        # Set values
        self.user_entered_value = ExtendedValue(stringValue=string_value)
        self.effective_value = ExtendedValue(numberValue=number_value)

        # Set alignment
        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'right'

        # Apply number format if specified
        if final_format_type:
            if not self.effective_format:
                self.effective_format = {}
            self.effective_format['numberFormat'] = {
                'type': final_format_type,
                'pattern': final_pattern
            }

            if not self.user_entered_format:
                self.user_entered_format = {}
            self.user_entered_format['numberFormat'] = {
                'type': final_format_type,
                'pattern': final_pattern
            }

    def _should_preserve_existing_format(
        self,
        new_format_type: Optional[str],
        existing_format: Dict[str, Any],
        new_pattern: Optional[str]
    ) -> bool:
        """
        Check if existing format should be preserved.

        Args:
            new_format_type: New format type
            existing_format: Existing format
            new_pattern: New pattern (unused but kept for API compatibility)

        Returns:
            True if existing format should be preserved
        """
        existing_type = existing_format.get('type')

        # Preserve date/datetime when entering numbers
        if (self.is_date(existing_format) or self.is_date_time(existing_format)) and new_format_type == 'NUMBER':
            return True

        # Preserve date pattern when entering date
        if self.is_date(existing_format) and new_format_type == 'DATE':
            return True

        # Preserve datetime pattern when entering datetime
        if self.is_date_time(existing_format) and new_format_type == 'DATE_TIME':
            return True

        # Preserve meaningful formats when entering plain numbers
        if new_format_type == 'NUMBER' and existing_type in ['CURRENCY', 'PERCENT', 'ACCOUNTING', 'FRACTION', 'SCIENTIFIC']:
            return True

        return False

    def _get_string_value_for_format(
        self,
        value: Union[str, int, float],
        number_value: Optional[float],
        format_type: Optional[str]
    ) -> str:
        """
        Get string value based on format type.

        Args:
            value: Original value
            number_value: Converted number
            format_type: Format type

        Returns:
            String value for user-entered value
        """
        if format_type == 'PERCENT':
            return str(value)

        if number_value is not None:
            return str(number_value)

        return str(value)

    def _set_string_value(
        self,
        value: str,
        text_format_runs: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Set string value."""
        self.user_entered_value = ExtendedValue(stringValue=value)
        self.effective_value = ExtendedValue(stringValue=value)
        self.formatted_value = value
        self.text_format_runs = text_format_runs

        # Remove number format
        if self.user_entered_format and 'numberFormat' in self.user_entered_format:
            del self.user_entered_format['numberFormat']
        if self.effective_format and 'numberFormat' in self.effective_format:
            del self.effective_format['numberFormat']

        # Set alignment
        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'left'

    def set_user_entered_value(
        self,
        value: Union[str, int, float, bool, None],
        text_format_runs: Optional[List[Dict[str, Any]]] = None,
    ) -> 'SheetCell[T]':
        """
        Set user-entered value.

        This method automatically detects the value type and sets appropriate
        formatting. Supports strings, numbers, booleans, dates, and formulas.

        Args:
            value: The value to set
            text_format_runs: Optional text formatting runs

        Returns:
            Self for method chaining
        """
        if value == "" or value is None:
            self.clear_user_entered_value()
            return self

        # Detect value type and pattern
        value_type, number_format_type, number_value, pattern = detect_value_type_and_pattern(
            value, self.locale
        )

        # Check if user forced this cell to be text
        user_num_format = None
        if self.user_entered_format is not None:
            user_num_format = self.user_entered_format.get('numberFormat')
        force_string = self.is_text(user_num_format if isinstance(user_num_format, dict) else None)
        final_value_type = "stringValue" if force_string else value_type

        # Set value by detected type
        self._set_user_entered_value_by_type(
            final_value_type,
            value,
            text_format_runs,
            number_format_type,
            number_value,
            pattern
        )

        # Validate (skip for formulas - validate after calculation)
        if not self.is_formula():
            self.validate()

        return self

    def set_effective_value(
        self,
        value: Union[str, int, float, bool, None, ErrorValue, Dict[str, Any]],
        is_preview: bool = False,
    ) -> 'SheetCell[T]':
        """
        Set effective value (typically from formula calculation).

        Args:
            value: The calculated value
            is_preview: Whether this is a preview value

        Returns:
            Self for method chaining
        """
        self.hide_loading()

        if value is None:
            self._clear_effective_value()
            return self

        # Handle error values
        if isinstance(value, ErrorValue):
            self._set_error_value(value)
            return self

        if isinstance(value, dict):
            # Treat dicts with type/message as error payloads
            if 'type' in value and 'message' in value:
                self._set_error_value(value)
                return self

            # Structured results (hyperlink, image, sparkline, etc.)
            if 'kind' in value:
                self._remove_error_value()
                self.set_structured_value(value)
                return self

        self._remove_error_value()

        # Handle loading placeholder
        if value == AWAITING_CALCULATION:
            if (
                self.effective_value is None
                or getattr(self.effective_value, 'structuredValue', None) is None
                or self.formatted_value == self.loading_value
            ):
                self.formatted_value = self.loading_value
            return self

        if isinstance(value, bool):
            self._set_effective_boolean_value(value)
        else:
            value_type = detect_value_type(value, self.locale)
            if value_type == "numberValue":
                self._set_effective_number_value(value)
            elif value_type == "boolValue":
                self._set_effective_boolean_value(bool(value))
            else:
                self._set_effective_string_value(str(value))

        if not is_preview:
            self.refresh_formatted_value()

        return self

    def set_structured_value(self, structured_value: Dict[str, Any]) -> None:
        """
        Apply a structured value result to the cell.

        Args:
            structured_value: Structured result dictionary with a `kind` key
        """
        if not structured_value:
            return

        kind = structured_value.get('kind')

        if kind == 'hyperlink':
            url = structured_value.get('url')
            title = structured_value.get('title')
            if url:
                self.set_url(url, title)

            effective = self.effective_value or ExtendedValue()
            effective.structuredValue = structured_value
            self.effective_value = effective
            return

        if kind == 'image':
            self.image_url = structured_value.get('imageUrl')
            self.hyperlink = None
            self.formatted_value = ""
            if not self.effective_format:
                self.effective_format = {}
            self.effective_format['horizontalAlignment'] = 'left'
            self.effective_value = ExtendedValue(structuredValue=structured_value)
            return

        if kind == 'sparkline':
            self.formatted_value = structured_value.get('formattedValue', "")
            self.effective_value = ExtendedValue(structuredValue=structured_value)
            return

        # Default structured value handling
        formatted_value = structured_value.get('formattedValue')
        if formatted_value is not None:
            self.formatted_value = formatted_value

        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'left'

        self.effective_value = ExtendedValue(structuredValue=structured_value)

    def set_formula_value(self, formula_value: str) -> None:
        """
        Set formula value with validation.

        Args:
            formula_value: The formula string (should start with = or +)
        """
        # Ensure formula starts with =
        if formula_value.startswith('+'):
            formula_value = '=' + formula_value[1:]
        elif not formula_value.startswith('='):
            formula_value = '=' + formula_value

        # Create ExtendedValue with formula
        self.user_entered_value = ExtendedValue(formulaValue=formula_value)

        # Clear number formats (formulas don't have pre-defined formats)
        if self.user_entered_format and 'numberFormat' in self.user_entered_format:
            del self.user_entered_format['numberFormat']
        if self.effective_format and 'numberFormat' in self.effective_format:
            del self.effective_format['numberFormat']

        # Clear effective value until calculation
        self.clear_effective_value_for_formula()

    def set_url(self, url: str, title: Optional[str] = None) -> None:
        """
        Set URL/hyperlink.

        Args:
            url: The URL
            title: Optional display title
        """
        self.hyperlink = url

        if title:
            self.formatted_value = title
        elif url:
            self.formatted_value = url

        # Update effective value
        if title:
            self.effective_value = ExtendedValue(stringValue=title)

        # Set formatting
        if self.effective_format is None:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'left'
        if 'textFormat' not in self.effective_format:
            self.effective_format['textFormat'] = {}
        text_fmt = self.effective_format['textFormat']
        if isinstance(text_fmt, dict):
            text_fmt['underline'] = True

    def delete_url(self) -> None:
        """Delete URL/hyperlink."""
        self.hyperlink = None

    def clear_hyperlink(self) -> None:
        """Clear hyperlink."""
        self.hyperlink = None

    def set_image(self, image_url: str) -> None:
        """
        Set image URL.

        Args:
            image_url: The image URL
        """
        self.image_url = image_url
        self.user_entered_value = None
        self.hyperlink = None
        self.formatted_value = ""

    def set_data_validation(self, data_validation: Dict[str, Any]) -> None:
        """
        Set data validation rule.

        Args:
            data_validation: The validation rule
        """
        self.data_validation = data_validation

        # Clear value for boolean validation
        condition = data_validation.get('condition')
        if (
            isinstance(condition, dict)
            and condition.get('type') == 'BOOLEAN'
            and not self.is_formula()
        ):
            effective_value = self.get_effective_value()
            if effective_value is not None:
                self._set_boolean_value(effective_value)

    def delete_data_validation(self) -> None:
        """Delete data validation rule."""
        self.data_validation = None

        # Remove any error values
        if self.effective_value is not None:
            self.effective_value.errorValue = None

    def get_effective_value(self) -> Union[str, int, float, bool, None]:
        """
        Get the effective value.

        Returns:
            The effective value as a primitive type
        """
        if not self.effective_value:
            return None

        # Check for different value types
        if self.effective_value.numberValue is not None:
            return self.effective_value.numberValue
        if self.effective_value.stringValue is not None:
            return self.effective_value.stringValue
        if self.effective_value.boolValue is not None:
            return self.effective_value.boolValue

        return None

    def get_user_entered_value(self) -> Union[str, int, float, bool, None]:
        """
        Get the user-entered value.

        Returns:
            The user-entered value as a primitive type
        """
        if not self.user_entered_value:
            return None

        # Check for different value types
        if self.user_entered_value.formulaValue is not None:
            return self.user_entered_value.formulaValue
        if self.user_entered_value.numberValue is not None:
            return self.user_entered_value.numberValue
        if self.user_entered_value.stringValue is not None:
            return self.user_entered_value.stringValue
        if self.user_entered_value.boolValue is not None:
            return self.user_entered_value.boolValue

        return None

    def get_number_format(self) -> Optional[Dict[str, Any]]:
        """Get the number format."""
        if self.effective_format is not None:
            num_fmt = self.effective_format.get('numberFormat')
            if isinstance(num_fmt, dict):
                return num_fmt
        return None

    def get_user_cell_data(self) -> Optional[Dict[str, Any]]:
        """
        Get user cell data excluding internal properties.

        Returns:
            User cell data dictionary
        """
        if not self.cell_data:
            return None

        result = {}
        if hasattr(self.cell_data, 'model_dump'):
            cell_dict = self.cell_data.model_dump(by_alias=True, exclude_none=True)
        elif isinstance(self.cell_data, dict):
            cell_dict = dict(self.cell_data)
        else:
            cell_dict = {}

        for key, value in cell_dict.items():
            if key not in EXCLUDE_KEYS and value is not None:
                result[key] = value

        return result if result else None

    @staticmethod
    def _extended_value_to_shorthand(extended_value: ExtendedValue) -> Dict[str, Any]:
        """
        Convert ExtendedValue to shorthand dict format (matching TypeScript).

        Args:
            extended_value: ExtendedValue object

        Returns:
            Dictionary with shorthand keys (nv, sv, fv, bv, ev) and full 'structuredValue'
        """
        result = {}

        if extended_value.numberValue is not None:
            result['nv'] = extended_value.numberValue
        if extended_value.stringValue is not None:
            result['sv'] = extended_value.stringValue
        if extended_value.boolValue is not None:
            result['bv'] = extended_value.boolValue
        if extended_value.formulaValue is not None:
            result['fv'] = extended_value.formulaValue
        if extended_value.errorValue is not None:
            result['ev'] = extended_value.errorValue.model_dump(exclude_none=True) if hasattr(extended_value.errorValue, 'model_dump') else extended_value.errorValue
        if extended_value.structuredValue is not None:
            result['structuredValue'] = extended_value.structuredValue

        return result

    def get_cell_data(self) -> Optional[Dict[str, Any]]:
        """
        Get complete cell data object.

        Returns:
            Complete cell data as dictionary with shorthand keys (matching TypeScript)
        """
        new_cell_data = {}

        # User cell data
        user_data = self.get_user_cell_data()
        if user_data:
            new_cell_data.update(user_data)

        # Add all tracked properties
        if self.text_format_runs:
            new_cell_data['textFormatRuns'] = self.text_format_runs

        if self.conditional_formatting_result_by_id:
            new_cell_data['conditionalFormattingResultById'] = self.conditional_formatting_result_by_id

        if self.data_validation_result:
            new_cell_data['dataValidationResult'] = self.data_validation_result

        if self.user_entered_value:
            # Convert to shorthand dict
            ue_dict = self._extended_value_to_shorthand(self.user_entered_value)
            if ue_dict:
                new_cell_data['ue'] = ue_dict

        if self.effective_value:
            # Convert to shorthand dict
            ev_dict = self._extended_value_to_shorthand(self.effective_value)
            if ev_dict:
                new_cell_data['ev'] = ev_dict

        if self.formatted_value is not None or self.is_loading:
            new_cell_data['fv'] = self.loading_value if self.is_loading else self.formatted_value

        # Formats
        if self.effective_format:
            effective_output = self._prepare_format_output(self.effective_format)
            if effective_output:
                new_cell_data['ef'] = effective_output

        if self.user_entered_format:
            user_output = self._prepare_format_output(self.user_entered_format)
            if user_output:
                new_cell_data['uf'] = user_output

        if self.cell_xfs_registry is not None and new_cell_data:
            register_cell_xfs_registry(self.cell_xfs_registry, self, new_cell_data)

        if self.data_validation:
            new_cell_data['dataValidation'] = self.data_validation

        if self.image_url:
            new_cell_data['imageUrl'] = self.image_url

        if self.hyperlink:
            new_cell_data['hyperlink'] = self.hyperlink

        if self.meta_type:
            new_cell_data['metaType'] = self.meta_type

        if self.note:
            new_cell_data['note'] = self.note

        if self.collapsible:
            new_cell_data['collapsible'] = self.collapsible
            new_cell_data['isCollapsed'] = self.is_collapsed

        return new_cell_data if new_cell_data else None

    # Private helper methods

    def _get_cell_user_entered_value(self, cell_data: T) -> Optional[ExtendedValue]:
        """Extract user-entered value from cell data."""
        # Try aliased field first
        if hasattr(cell_data, 'user_entered_value'):
            return cell_data.user_entered_value
        # Try looking in dict
        if isinstance(cell_data, dict):
            value = cell_data.get('ue') or cell_data.get('userEnteredValue')
            if value is not None and isinstance(value, dict):
                return ExtendedValue.model_validate(value)
            return value
        return None

    def _get_cell_effective_value(self, cell_data: T) -> Optional[ExtendedValue]:
        """Extract effective value from cell data."""
        if hasattr(cell_data, 'effective_value'):
            return cell_data.effective_value
        if isinstance(cell_data, dict):
            value = cell_data.get('ev') or cell_data.get('effectiveValue')
            if value is not None and isinstance(value, dict):
                return ExtendedValue.model_validate(value)
            return value
        return None

    def _get_cell_formatted_value(self, cell_data: T) -> Optional[str]:
        """Extract formatted value from cell data."""
        if hasattr(cell_data, 'formatted_value'):
            return cell_data.formatted_value
        if isinstance(cell_data, dict):
            return cell_data.get('fv') or cell_data.get('formattedValue')
        return None

    def _get_cell_user_entered_format(self, cell_data: T) -> Optional[Dict[str, Any]]:
        """Extract user-entered format from cell data."""
        if hasattr(cell_data, 'user_entered_format'):
            return cell_data.user_entered_format
        if isinstance(cell_data, dict):
            return cell_data.get('uf') or cell_data.get('userEnteredFormat')
        return None

    def _get_cell_effective_format(self, cell_data: T) -> Optional[Dict[str, Any]]:
        """Extract effective format from cell data."""
        if hasattr(cell_data, 'effective_format'):
            return cell_data.effective_format
        if isinstance(cell_data, dict):
            return cell_data.get('ef') or cell_data.get('effectiveFormat')
        return None

    def _resolve_format(
        self,
        format_data: Optional[Dict[str, Any]],
        cell_xfs_registry: Optional[Any],
    ) -> Optional[Dict[str, Any]]:
        """Resolve format, handling style references if registry is available."""
        if not format_data:
            return None

        # Check if it's a style reference
        if isinstance(format_data, dict) and ('styleId' in format_data or 'sid' in format_data):
            if cell_xfs_registry:
                style_id = format_data.get('styleId') or format_data.get('sid')
                resolved = self._lookup_cell_xfs(cell_xfs_registry, style_id)
                return resolved
            return None

        return format_data

    def _lookup_cell_xfs(self, registry: Any, style_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not style_id:
            return None
        try:
            getter = getattr(registry, "get", None)
        except Exception:
            getter = None
        value: Any = None
        if callable(getter):
            try:
                value = getter(style_id)
            except Exception:
                pass
        try:
            if hasattr(registry, "__getitem__"):
                value = registry[style_id]
        except Exception:
            return None
        if value is None:
            return None
        return value if isinstance(value, dict) else getattr(value, "to_py", lambda: value)()

    def _prepare_format_output(
        self, format_data: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not format_data:
            return None
        prepared = dict(format_data)
        if prepared.get("horizontalAlignment") == "left":
            prepared.pop("horizontalAlignment")
        return prepared or None


    def _get_existing_number_format(self) -> Optional[Dict[str, Any]]:
        """Get existing number format from user-entered or effective formats."""
        if self.user_entered_format is not None:
            num_fmt = self.user_entered_format.get('numberFormat')
            if isinstance(num_fmt, dict):
                return num_fmt

        if self.effective_format is not None:
            num_fmt = self.effective_format.get('numberFormat')
            if isinstance(num_fmt, dict):
                return num_fmt

        return None

    def _determine_number_format(
        self,
        value: Union[str, int, float, bool],
        number_value: Optional[float],
    ) -> Dict[str, Optional[str]]:
        """
        Determine number format type and pattern using existing formats as hints.
        """
        existing_format = self._get_existing_number_format()
        format_type = existing_format.get('type') if existing_format else None
        pattern = existing_format.get('pattern') if existing_format else None

        if format_type is None:
            format_type = detect_number_format_type(value, self.locale)

        if pattern is None:
            pattern = detect_number_format_pattern(
                value,
                number_value,
                format_type,
                self.locale,
            )

        return {
            'type': format_type,
            'pattern': pattern,
        }

    def _set_effective_number_value(self, value: Union[int, float, str]) -> None:
        """Set effective number value."""
        number_value = convert_to_number(value)
        if number_value is None:
            # Fallback to string handling if conversion fails
            self._set_effective_string_value(str(value))
            return

        format_info = self._determine_number_format(value, number_value)
        pattern = format_info.get('pattern') or self.default_pattern

        self.effective_value = ExtendedValue(numberValue=number_value)

        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'right'

        if format_info.get('type') or format_info.get('pattern'):
            self.effective_format['numberFormat'] = {
                key: fmt_value
                for key, fmt_value in format_info.items()
                if fmt_value
            }
        else:
            self.effective_format.pop('numberFormat', None)

        format_color = create_formatted_color(number_value, "numberValue", pattern)
        self.set_effective_text_format_color(format_color)

        self.formatted_value = create_formatted_value(
            number_value,
            "numberValue",
            pattern,
        )

    def _set_effective_string_value(self, value: str) -> None:
        """Set effective string value."""
        self.effective_value = ExtendedValue(stringValue=value)

        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'left'

        # Remove number format when switching to strings
        if 'numberFormat' in self.effective_format:
            self.effective_format.pop('numberFormat', None)

        self.formatted_value = create_formatted_value(
            value,
            "stringValue",
            self.default_pattern,
        )

    def _set_effective_boolean_value(self, value: bool) -> None:
        """Set effective boolean value."""
        self.effective_value = ExtendedValue(boolValue=bool(value))

        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'center'

        # Remove number format when switching to booleans
        if 'numberFormat' in self.effective_format:
            self.effective_format.pop('numberFormat', None)

        self.formatted_value = create_formatted_value(
            value,
            "boolValue",
            self.default_pattern,
        )

    def _clear_effective_value(self) -> None:
        """Clear effective value."""
        self.effective_value = None
        self.effective_format = None
        self.formatted_value = None
        self.cell_data = None

    def _set_error_value(self, error: Union[Dict[str, str], ErrorValue]) -> None:
        """Set error value."""
        error_obj: ErrorValue
        if isinstance(error, dict):
            error_obj = ErrorValue(
                type=error.get('type', 'Error'),  # type: ignore
                message=error.get('message', 'Unknown error')
            )
        else:
            error_obj = error

        self.effective_value = ExtendedValue(errorValue=error_obj)
        self.formatted_value = error_obj.message

        if self.effective_format is None:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'center'

    def _remove_error_value(self) -> None:
        """Remove error value."""
        if self.effective_value is not None and hasattr(self.effective_value, 'errorValue'):
            self.effective_value.errorValue = None

    @staticmethod
    def _get_nested(obj: Optional[Dict[str, Any]], key: str) -> Any:
        """Safely get nested dict value."""
        if obj is None:
            return None
        return obj.get(key)

    # Formatting methods

    def set_user_entered_format(self, format_type: str, value: Any) -> None:
        """
        Set user-entered format.

        Args:
            format_type: Type of format (e.g., 'textFormat', 'numberFormat', 'borders')
            value: Format value
        """
        if self.user_entered_format is None:
            self.user_entered_format = {}

        if format_type == 'textFormat':
            self._set_text_format(value)
        elif format_type == 'numberFormat':
            self._set_number_format(value)
        else:
            self.user_entered_format[format_type] = value

    def set_effective_format(self, format_type: str, value: Any) -> None:
        """
        Set effective format (usually from copy/paste).

        Args:
            format_type: Type of format
            value: Format value
        """
        if self.effective_format is None:
            self.effective_format = {}

        if format_type == 'textFormat':
            self._set_effective_text_format(value)
        else:
            self.effective_format[format_type] = value

    def _set_text_format(self, value: Dict[str, Any]) -> None:
        """Set text format on user-entered format."""
        if self.user_entered_format is None:
            self.user_entered_format = {}
        if 'textFormat' not in self.user_entered_format:
            self.user_entered_format['textFormat'] = {}

        text_fmt = self.user_entered_format['textFormat']
        if isinstance(text_fmt, dict):
            for key, val in value.items():
                text_fmt[key] = val

    def _set_effective_text_format(self, value: Dict[str, Any]) -> None:
        """Set text format on effective format."""
        if self.effective_format is None:
            self.effective_format = {}
        if 'textFormat' not in self.effective_format:
            self.effective_format['textFormat'] = {}

        text_fmt = self.effective_format['textFormat']
        if isinstance(text_fmt, dict):
            for key, val in value.items():
                text_fmt[key] = val

    def _set_number_format(self, value: Optional[Dict[str, Any]]) -> None:
        """Set number format."""
        if self.user_entered_format is None:
            self.user_entered_format = {}

        self.user_entered_format['numberFormat'] = value

        # Handle format changes
        effective_value = self.get_effective_value()
        if effective_value is None:
            return

        # TODO: Implement full number format conversion logic
        # For now, just store the format

    def set_effective_text_format_color(self, color: Optional[str]) -> None:
        """
        Set effective text format color.

        Args:
            color: Color string or None to remove
        """
        if color:
            if self.effective_format is None:
                self.effective_format = {}
            if 'textFormat' not in self.effective_format:
                self.effective_format['textFormat'] = {}
            text_fmt = self.effective_format['textFormat']
            if isinstance(text_fmt, dict):
                text_fmt['color'] = color
        else:
            if self.effective_format is not None and 'textFormat' in self.effective_format:
                text_fmt = self.effective_format['textFormat']
                if isinstance(text_fmt, dict):
                    text_fmt.pop('color', None)

    def set_effective_number_format(self, number_format: Dict[str, Any]) -> None:
        """
        Set effective number format.

        Args:
            number_format: Number format dict with 'type' and optional 'pattern'
        """
        # If this is an error cell, skip
        if self.effective_value is not None and self.effective_value.errorValue is not None:
            return

        if self.effective_format is None:
            self.effective_format = {}

        self.effective_format['numberFormat'] = number_format

        self.refresh_formatted_value()

    def clear_user_entered_format(self) -> None:
        """Clear user-entered formatting."""
        if self.user_entered_format is not None:
            # Don't clear number format
            for key in list(self.user_entered_format.keys()):
                if key != 'numberFormat':
                    if self.effective_format is not None and key in self.effective_format:
                        del self.effective_format[key]

        # Handle case where only effective format exists
        if self.user_entered_format is None and self.effective_format is not None:
            for key in list(self.effective_format.keys()):
                if key not in ['numberFormat', 'horizontalAlignment']:
                    del self.effective_format[key]

        self.user_entered_format = None

    def clear_formatting(self) -> None:
        """Clear all formatting."""
        self.user_entered_format = None
        self.effective_format = None

    def delete_user_entered_format(self) -> None:
        """Delete user-entered format."""
        self.user_entered_format = None
        self.original_user_entered_format = None

    def delete_effective_format(self) -> None:
        """Delete effective format."""
        self.effective_format = None
        self.original_effective_format = None

    # Border methods

    def set_border(self, position: str, border: Dict[str, Any]) -> None:
        """
        Set border on specific position.

        Args:
            position: Border position ('top', 'bottom', 'left', 'right')
            border: Border specification
        """
        if not border.get('color'):
            # User is trying to clear the border
            if self.user_entered_format is not None and 'borders' in self.user_entered_format:
                borders = self.user_entered_format['borders']
                if isinstance(borders, dict):
                    borders[position] = None
        else:
            if self.user_entered_format is None:
                self.user_entered_format = {}
            if 'borders' not in self.user_entered_format:
                self.user_entered_format['borders'] = {}
            borders = self.user_entered_format['borders']
            if isinstance(borders, dict):
                borders[position] = border

    def set_effective_border(self, position: str, border: Dict[str, Any]) -> None:
        """
        Set effective border on specific position.

        Args:
            position: Border position
            border: Border specification
        """
        if not border.get('color'):
            if self.effective_format is not None and 'borders' in self.effective_format:
                borders = self.effective_format['borders']
                if isinstance(borders, dict):
                    borders[position] = None
        else:
            if self.effective_format is None:
                self.effective_format = {}
            if 'borders' not in self.effective_format:
                self.effective_format['borders'] = {}
            borders = self.effective_format['borders']
            if isinstance(borders, dict):
                borders[position] = border

    def set_all_borders(self, border: Dict[str, Any]) -> None:
        """
        Set all borders at once.

        Args:
            border: Border specification
        """
        if not border.get('color'):
            self.clear_all_borders()
        else:
            if self.user_entered_format is None:
                self.user_entered_format = {}
            self.user_entered_format['borders'] = {
                'top': border,
                'bottom': border,
                'left': border,
                'right': border,
            }

    def clear_all_borders(self) -> None:
        """Clear all borders."""
        if self.user_entered_format is not None:
            self.user_entered_format.pop('borders', None)

    # Decimal and indent methods

    def change_decimals(self, delta: int = 1) -> None:
        """
        Change decimal places.

        Args:
            delta: Amount to change (positive to increase, negative to decrease)
        """
        # TODO: Implement full decimal handling
        # This requires number format pattern manipulation
        pass

    def increase_decimals(self) -> None:
        """Increase decimal places by 1."""
        self.change_decimals(1)

    def decrease_decimals(self) -> None:
        """Decrease decimal places by 1."""
        self.change_decimals(-1)

    def change_indent(self, size: int = 1) -> None:
        """
        Change cell indent.

        Args:
            size: Amount to change indent (default: 1)
        """
        if self.user_entered_format is None:
            self.user_entered_format = {}

        current_indent = self.user_entered_format.get('indent', 0)
        if not isinstance(current_indent, int):
            current_indent = 0
        self.user_entered_format['indent'] = max(0, current_indent + size)

    def increase_indent(self) -> None:
        """Increase indent by 2."""
        self.change_indent(2)

    def decrease_indent(self) -> None:
        """Decrease indent by 2."""
        self.change_indent(-2)

    # Type check methods

    def is_date(self, number_format: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if format is DATE type.

        Args:
            number_format: Optional number format to check (defaults to effective format)

        Returns:
            True if format is DATE
        """
        if number_format is None:
            number_format = self.get_number_format()

        if not number_format:
            return False

        return number_format.get('type') == 'DATE'

    def is_date_time(self, number_format: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if format is DATE_TIME type.

        Args:
            number_format: Optional number format to check

        Returns:
            True if format is DATE_TIME
        """
        if number_format is None:
            number_format = self.get_number_format()

        if not number_format:
            return False

        return number_format.get('type') == 'DATE_TIME'

    def is_text(self, number_format: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if format is TEXT type.

        Args:
            number_format: Optional number format to check

        Returns:
            True if format is TEXT
        """
        if number_format is None:
            number_format = self.get_number_format()

        if not number_format:
            return False

        return number_format.get('type') == 'TEXT'

    def is_number_type(self, num_type: Optional[str]) -> bool:
        """
        Check if number format type is a numeric type.

        Args:
            num_type: Number format type to check

        Returns:
            True if it's a number type
        """
        return num_type in [
            'NUMBER',
            'CURRENCY',
            'PERCENT',
            'ACCOUNTING',
            'FRACTION',
            'SCIENTIFIC',
        ]

    # Conditional formatting and validation

    def set_conditional_format_result(
        self,
        rule_id: Union[int, str],
        value: Any,
    ) -> None:
        """
        Set conditional formatting result.

        Args:
            rule_id: Rule identifier
            value: Calculation result
        """
        if self.conditional_formatting_result_by_id is None:
            self.conditional_formatting_result_by_id = {}

        self.conditional_formatting_result_by_id[rule_id] = value

    def set_data_validation_result(self, value: Any) -> None:
        """
        Set data validation result.

        Args:
            value: Validation result
        """
        self.data_validation_result = value

        # Validate
        self.validate()

    def validate(self) -> None:
        """
        Validate cell against data validation rules.

        Sets error value if validation fails.
        """
        if self.data_validation is None:
            # Remove any errors
            if self.effective_value is not None:
                self.effective_value.errorValue = None
            return

        # TODO: Implement full validation logic
        # For now, just a placeholder

    def refresh_formatted_value(self) -> None:
        """
        Refresh formatted value from effective value and format.

        This recalculates the display value based on current effective value
        and formatting.
        """
        if self.effective_value is None:
            return

        structured_value = getattr(self.effective_value, 'structuredValue', None)
        if isinstance(structured_value, dict):
            formatted = structured_value.get('formattedValue')
            if formatted is not None:
                self.formatted_value = formatted
            return

        effective_value = self.get_effective_value()
        if effective_value is None:
            return

        value_type = detect_value_type(effective_value, self.locale)

        if value_type == "numberValue":
            number_value = convert_to_number(effective_value)
            if number_value is None and isinstance(effective_value, (int, float)):
                number_value = float(effective_value)

            if number_value is None:
                # Fall back to plain string formatting
                self.formatted_value = create_formatted_value(
                    str(effective_value),
                    "stringValue",
                    self.default_pattern,
                )
                return

            pattern = None
            if self.effective_format and isinstance(self.effective_format.get('numberFormat'), dict):
                pattern = self.effective_format['numberFormat'].get('pattern')

            if not pattern:
                format_info = self._determine_number_format(effective_value, number_value)
                pattern = format_info.get('pattern')

            pattern = pattern or self.default_pattern

            self.formatted_value = create_formatted_value(
                number_value,
                "numberValue",
                pattern,
            )

            if not self.effective_format:
                self.effective_format = {}
            self.effective_format['horizontalAlignment'] = 'right'
            return

        if value_type == "boolValue":
            self.formatted_value = create_formatted_value(
                effective_value,
                "boolValue",
                self.default_pattern,
            )
            if not self.effective_format:
                self.effective_format = {}
            self.effective_format['horizontalAlignment'] = 'center'
            if 'numberFormat' in self.effective_format:
                self.effective_format.pop('numberFormat', None)
            return

        # Default to string formatting
        self.formatted_value = create_formatted_value(
            str(effective_value),
            "stringValue",
            self.default_pattern,
        )
        if not self.effective_format:
            self.effective_format = {}
        self.effective_format['horizontalAlignment'] = 'left'
        if 'numberFormat' in self.effective_format:
            self.effective_format.pop('numberFormat', None)

    def set_formatted_value(self, value: Optional[str]) -> None:
        """
        Overwrite formatted value.

        Args:
            value: New formatted value
        """
        self.formatted_value = value

    # Formula methods

    def move_formula(
        self,
        from_coords: CellInterface,
        to_coords: CellInterface,
        exclusion_range: Optional[Dict[str, int]] = None,
        ignore_circular: bool = False,
        row_count: Optional[int] = None,
        column_count: Optional[int] = None,
        preserve_absolutes: bool = False,
    ) -> None:
        """
        Move formula with relative reference updates.

        Args:
            from_coords: Original cell coordinates
            to_coords: New cell coordinates
            exclusion_range: Optional range to exclude from updates
            ignore_circular: Whether to ignore circular references
            row_count: Number of rows (for range formulas)
            column_count: Number of columns (for range formulas)
            preserve_absolutes: Whether to preserve absolute references
        """
        if not self.is_formula():
            return

        # TODO: Implement formula relative reference conversion
        # This requires formula parsing and cell reference updating
        pass

    def change_formula_sheet_name(self, name: str, old_name: str) -> None:
        """
        Update formula sheet name references.

        Args:
            name: New sheet name
            old_name: Old sheet name
        """
        if not self.formula:
            return

        # TODO: Implement sheet name updating in formulas
        pass

    def change_named_range_name(self, name: str, old_name: str) -> None:
        """
        Update named range references in formula.

        Args:
            name: New named range name
            old_name: Old named range name
        """
        if not self.formula:
            return

        # TODO: Implement named range updating in formulas
        pass

    def change_formula_column_name(self, name: str, previous_name: str) -> None:
        """
        Update column name references in formula.

        Args:
            name: New column name
            previous_name: Previous column name
        """
        if not self.formula:
            return

        # TODO: Implement column name updating in formulas
        pass

    @staticmethod
    def get_relative_formula(
        value: str,
        from_coords: CellInterface,
        to_coords: CellInterface,
        exclusion_range: Optional[Dict[str, int]] = None,
        ignore_circular: bool = False,
        row_count: Optional[int] = None,
        column_count: Optional[int] = None,
        preserve_absolutes: bool = False,
    ) -> Optional[str]:
        """
        Get relative formula calculation.

        Args:
            value: Formula string
            from_coords: Original coordinates
            to_coords: Target coordinates
            exclusion_range: Optional exclusion range
            ignore_circular: Ignore circular references
            row_count: Row count for ranges
            column_count: Column count for ranges
            preserve_absolutes: Preserve absolute references

        Returns:
            Updated formula or None
        """
        # TODO: Implement relative formula conversion
        return None

    # Cell data methods

    def process_derived_cell(self, cell_data: T) -> None:
        """
        Process derived cell data.

        Args:
            cell_data: Cell data to process
        """
        self.image_url = getattr(cell_data, 'image_url', None)
        self.hyperlink = getattr(cell_data, 'hyperlink', None)

    def get_user_entered_format(self) -> Optional[Dict[str, Any]]:
        """
        Get user-entered format.

        Returns style reference if no registry is available.

        Returns:
            User-entered format or style reference
        """
        if self._is_style_reference(self.original_user_entered_format) and not self.cell_xfs_registry:
            return self.original_user_entered_format

        return self.user_entered_format

    def get_effective_cell_format(self) -> Optional[Dict[str, Any]]:
        """
        Get merged effective cell format.

        Combines effective format and user-entered format.

        Returns:
            Merged cell format
        """
        if self._is_style_reference(self.original_effective_format) and not self.cell_xfs_registry:
            return self.original_effective_format

        if not self.effective_format and not self.user_entered_format and not self.is_loading:
            return None

        result: Dict[str, Any] = {}

        if self.effective_format:
            result.update(self.effective_format)

        if self.user_entered_format:
            result.update(self.user_entered_format)

        merged_text_format: Dict[str, Any] = {}
        merged_borders: Dict[str, Any] = {}

        if self.effective_format:
            text_format = self.effective_format.get('textFormat')
            if isinstance(text_format, dict):
                merged_text_format.update(text_format)
            borders = self.effective_format.get('borders')
            if isinstance(borders, dict):
                merged_borders.update(borders)

        if self.user_entered_format:
            text_format = self.user_entered_format.get('textFormat')
            if isinstance(text_format, dict):
                merged_text_format.update(text_format)
            borders = self.user_entered_format.get('borders')
            if isinstance(borders, dict):
                merged_borders.update(borders)

        if merged_text_format:
            result['textFormat'] = merged_text_format
        elif 'textFormat' in result:
            result.pop('textFormat', None)

        if merged_borders:
            result['borders'] = merged_borders
        elif 'borders' in result:
            result.pop('borders', None)

        if self.is_loading:
            result['horizontalAlignment'] = 'center'
        elif self.user_entered_format and 'horizontalAlignment' in self.user_entered_format:
            result['horizontalAlignment'] = self.user_entered_format['horizontalAlignment']
        elif self.effective_format and 'horizontalAlignment' in self.effective_format:
            result['horizontalAlignment'] = self.effective_format['horizontalAlignment']
        else:
            result.pop('horizontalAlignment', None)

        return result

    def get_cell_formats(self) -> Dict[str, Any]:
        """
        Get both user-entered and effective formats.

        Returns:
            Dictionary with 'ef' and 'uf' keys
        """
        result = {}

        effective_format = self.get_effective_cell_format()
        if effective_format:
            result['ef'] = effective_format

        if self.user_entered_format:
            result['uf'] = self.user_entered_format

        return result

    @staticmethod
    def _is_style_reference(obj: Any) -> bool:
        """
        Check if object is a style reference.

        Args:
            obj: Object to check

        Returns:
            True if it's a style reference
        """
        if not isinstance(obj, dict):
            return False

        return 'styleId' in obj or 'sid' in obj
