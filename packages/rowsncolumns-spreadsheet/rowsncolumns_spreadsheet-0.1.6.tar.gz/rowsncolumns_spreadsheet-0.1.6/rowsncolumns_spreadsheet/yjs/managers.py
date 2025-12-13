from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SheetDataHelpers:
    get_or_create_row_values: Callable[[Any, int, int], Any]
    set_row_value: Callable[[Any, int, Optional[Dict[str, Any]]], None]


@dataclass(frozen=True)
class TablesHelpers:
    array_length: Callable[[Any], int]
    array_get: Callable[[Any, int], Any]
    array_insert: Callable[[Any, int, Iterable[Any]], None]
    array_set: Callable[[Any, int, Any], None]
    get_with_fallback: Callable[[Any, Sequence[str]], Any]
    set_with_fallback: Callable[[Any, Sequence[str], Any], None]
    create_array_like: Callable[[bool], Any]
    is_pycrdt_map: Callable[[Any], bool]


@dataclass(frozen=True)
class SheetsHelpers:
    array_length: Callable[[Any], int]
    array_get: Callable[[Any, int], Any]
    array_set: Callable[[Any, int, Any], None]
    get_with_fallback: Callable[[Any, Sequence[str]], Any]
    set_with_fallback: Callable[[Any, Sequence[str], Any], None]


class SheetDataManager:
    def __init__(
        self,
        sheet_data_map: Any,
        helpers: SheetDataHelpers,
    ) -> None:
        self._sheet_data_map = sheet_data_map
        self._helpers = helpers

    def get_row_values(self, sheet_id: int, row_index: int) -> Any:
        return self._helpers.get_or_create_row_values(
            self._sheet_data_map, sheet_id, row_index
        )

    def set_cell_value(
        self, row_values: Any, column_index: int, cell_data: Optional[Dict[str, Any]]
    ) -> None:
        self._helpers.set_row_value(row_values, column_index, cell_data)


class TablesManager:
    def __init__(
        self,
        tables_array: Any,
        helpers: TablesHelpers,
    ) -> None:
        self._tables_array = tables_array
        self._helpers = helpers

    def update_header(
        self, sheet_id: int, row_index: int, column_index: int, value: Any
    ) -> None:
        header_text = str(value)

        try:
            total = self._helpers.array_length(self._tables_array)
        except TypeError:
            return

        for index in range(total):
            table = self._helpers.array_get(self._tables_array, index)
            if not table:
                continue

            table_sheet_id = self._helpers.get_with_fallback(
                table, ("sheetId", "sheet_id")
            )
            if table_sheet_id != sheet_id:
                continue

            table_range = self._helpers.get_with_fallback(table, ("range",))
            if not table_range:
                continue

            start_row = self._helpers.get_with_fallback(
                table_range, ("startRowIndex", "start_row_index")
            )
            start_col = self._helpers.get_with_fallback(
                table_range, ("startColumnIndex", "start_column_index")
            )
            end_col = self._helpers.get_with_fallback(
                table_range, ("endColumnIndex", "end_column_index")
            )

            if (
                start_row != row_index
                or start_col is None
                or end_col is None
                or column_index < start_col
                or column_index > end_col
            ):
                continue

            header_index = int(column_index - start_col)
            columns = self._helpers.get_with_fallback(table, ("columns",))
            if columns is None:
                columns = self._helpers.create_array_like(
                    self._helpers.is_pycrdt_map(table)
                )
                self._helpers.set_with_fallback(table, ("columns",), columns)

            while self._helpers.array_length(columns) <= header_index:
                self._helpers.array_insert(columns, self._helpers.array_length(columns), [{}])

            column_entry = self._helpers.array_get(columns, header_index) or {}
            if isinstance(column_entry, dict):
                column_entry["name"] = header_text
            else:
                setattr(column_entry, "name", header_text)

            self._helpers.array_set(columns, header_index, column_entry)
            self._helpers.array_set(self._tables_array, index, table)


class SheetsManager:
    def __init__(
        self,
        sheets_array: Any,
        helpers: SheetsHelpers,
        *,
        default_row_count: int,
        default_column_count: int,
        max_row_count: int,
        max_column_count: int,
    ) -> None:
        self._sheets_array = sheets_array
        self._helpers = helpers
        self._default_row_count = default_row_count
        self._default_column_count = default_column_count
        self._max_row_count = max_row_count
        self._max_column_count = max_column_count

    def update_dimensions(
        self, sheet_id: int, max_row_index: int, max_column_index: int
    ) -> None:
        try:
            total = self._helpers.array_length(self._sheets_array)
        except TypeError:
            return

        for index in range(total):
            sheet = self._helpers.array_get(self._sheets_array, index)
            if not sheet:
                continue

            sheet_id_value = self._helpers.get_with_fallback(
                sheet, ("sheetId", "sheet_id")
            )
            if sheet_id_value != sheet_id:
                continue

            row_count = (
                self._helpers.get_with_fallback(sheet, ("rowCount", "row_count"))
                or self._default_row_count
            )
            column_count = (
                self._helpers.get_with_fallback(sheet, ("columnCount", "column_count"))
                or self._default_column_count
            )

            updated_row_count = min(
                self._max_row_count,
                max(row_count, max_row_index if max_row_index > 0 else row_count),
            )
            updated_column_count = min(
                self._max_column_count,
                max(
                    column_count,
                    max_column_index if max_column_index > 0 else column_count,
                ),
            )

            self._helpers.set_with_fallback(
                sheet, ("rowCount", "row_count"), updated_row_count
            )
            self._helpers.set_with_fallback(
                sheet, ("columnCount", "column_count"), updated_column_count
            )
            self._helpers.array_set(self._sheets_array, index, sheet)
            break
