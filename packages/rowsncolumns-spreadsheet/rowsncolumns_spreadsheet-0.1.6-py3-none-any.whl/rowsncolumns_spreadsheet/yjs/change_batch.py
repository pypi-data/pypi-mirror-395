"""
Python port of the TypeScript `changeBatch` interface that operates directly on
pycrdt (Yjs) data structures.

The function in this module mirrors the behavior of the TypeScript version that
updates sheet data, table headers, and sheet dimensions. It expects to receive a
`ydoc` object compatible with pycrdt/ypy documents (i.e. exposing
`get('name', type=Array|Map)` or convenience helpers like `get_array` /
`get_map`). When pycrdt is not available the code gracefully falls back to
lightweight Python data structures, which makes the implementation easy to test.
"""

from __future__ import annotations
import logging
import uuid
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

from ..sheet_cell import SheetCell
from ..types import CellInterface, GridRange
from ..cell_xfs import update_cell_xfs_registry
from .models import CellFormat
from .managers import (
    SheetDataHelpers,
    SheetDataManager,
    SheetsHelpers,
    SheetsManager,
    TablesHelpers,
    TablesManager,
)

DEFAULT_ROW_COUNT = 1000
DEFAULT_COLUMN_COUNT = 100
MAX_ROW_COUNT = 1_048_576
MAX_COLUMN_COUNT = 16_384

logger = logging.getLogger(__name__)

# Attempt to import the real pycrdt classes for type compatibility. When the
# dependency is not available (e.g. in unit tests) the import simply fails and
# we fall back to lightweight Python containers.
try:  # pragma: no cover - optional dependency
    from pycrdt import Array as PycrdtArray  # type: ignore
    from pycrdt import Map as PycrdtMap  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    PycrdtArray = None
    PycrdtMap = None


RangeLike = Union[GridRange, Dict[str, int]]
ValueMatrix = List[List[Union[str, bool, int, float, None]]]
FormatMatrix = List[List[Optional[CellFormat]]]


def change_batch(
    ydoc: Any,
    sheet_id: int,
    ranges: Union[RangeLike, Sequence[RangeLike]],
    values: ValueMatrix,
    formatting: FormatMatrix | None = None,
    locale: str = "en-US",
    user_id: Union[str, int] = "agent",
) -> None:
    """
    Apply batch cell updates directly on a pycrdt Y.Doc.

    Args:
        ydoc: pycrdt/ypy document that exposes the spreadsheet state
        sheet_id: Identifier of the sheet to update
        ranges: Single range or list of GridRange-like objects
        values: Matrix of values (matching the ranges) or a scalar
        formatting: Optional matrix/scalar mirroring the shape of ``values``
        locale: Locale passed to ``SheetCell`` for formatting decisions
    """

    if ydoc is None:
        logger.error("change_batch requires a valid ydoc instance")
        raise ValueError("A Y.Doc instance is required")

    range_list = _normalize_ranges(ranges)
    if not range_list:
        logger.debug("change_batch called with no ranges for sheet_id=%s", sheet_id)
        return

    logger.debug(
        "Applying change_batch: sheet_id=%s user_id=%s range_count=%s",
        sheet_id,
        user_id,
        len(range_list),
    )

    updated_cells = 0

    sheet_data_map = _get_structure(ydoc, "sheetDataV2", expect="map")
    tables_array = _get_structure(ydoc, "tables", expect="array", optional=True)
    sheets_array = _get_structure(ydoc, "sheets", expect="array", optional=True)
    recalc_array = _get_structure(ydoc, "recalcCells", expect="array")
    cell_xfs_map = _get_structure(ydoc, "cellXfs", expect="map")

    sheet_data_manager = SheetDataManager(
        sheet_data_map,
        SheetDataHelpers(
            get_or_create_row_values=_get_or_create_row_values,
            set_row_value=_set_row_value,
        ),
    )
    table_manager = (
        TablesManager(
            tables_array,
            TablesHelpers(
                array_length=_array_length,
                array_get=_array_get,
                array_insert=_array_insert,
                array_set=_array_set,
                get_with_fallback=_get_with_fallback,
                set_with_fallback=_set_with_fallback,
                create_array_like=_create_array_like,
                is_pycrdt_map=_is_pycrdt_map,
            ),
        )
        if tables_array is not None
        else None
    )
    sheet_manager = (
        SheetsManager(
            sheets_array,
            SheetsHelpers(
                array_length=_array_length,
                array_get=_array_get,
                array_set=_array_set,
                get_with_fallback=_get_with_fallback,
                set_with_fallback=_set_with_fallback,
            ),
            default_row_count=DEFAULT_ROW_COUNT,
            default_column_count=DEFAULT_COLUMN_COUNT,
            max_row_count=MAX_ROW_COUNT,
            max_column_count=MAX_COLUMN_COUNT,
        )
        if sheets_array is not None
        else None
    )

    sheet_cell = SheetCell(locale=locale, cell_xfs_registry=cell_xfs_map)
    max_row_index = 0
    max_column_index = 0

    if recalc_array is not None:
        _array_delete(recalc_array, 0, _array_length(recalc_array))

    for grid in range_list:
        for row_index in range(grid.start_row_index, grid.end_row_index + 1):
            row_patches: List[List[Any]] = []
            for column_index in range(
                grid.start_column_index, grid.end_column_index + 1
            ):
                row_offset = row_index - grid.start_row_index
                column_offset = column_index - grid.start_column_index

                cell_value = _resolve_matrix_value(values, row_offset, column_offset)
                cell_format = _resolve_matrix_value(
                    formatting, row_offset, column_offset
                )

                row_values = sheet_data_manager.get_row_values(sheet_id, row_index)
                existing_data = _array_get(row_values, column_index)

                coords = CellInterface(row_index=row_index, column_index=column_index)
                sheet_cell.assign(
                    sheet_id=sheet_id,
                    coords=coords,
                    cell_data=existing_data,
                    locale=locale,
                    cell_xfs_registry=cell_xfs_map,
                )

                if _is_empty_cell_value(cell_value):
                    sheet_cell.delete_contents()
                else:
                    sheet_cell.set_user_entered_value(cell_value)

                if isinstance(cell_format, dict):
                    for key, value in cell_format.items():
                        sheet_cell.set_user_entered_format(key, value)

                new_cell_data = sheet_cell.get_cell_data()
                sheet_data_manager.set_cell_value(row_values, column_index, new_cell_data)
                update_cell_xfs_registry(cell_xfs_map, sheet_cell)

                row_patches.append(
                    _create_recalc_patch(sheet_id, row_index, column_index)
                )
                updated_cells += 1

                if table_manager is not None and not _is_empty_cell_value(cell_value):
                    table_manager.update_header(
                        sheet_id, row_index, column_index, cell_value
                    )

            if recalc_array is not None and row_patches:
                _append_recalc_entry(recalc_array, user_id, row_patches)

        max_row_index = max(max_row_index, grid.end_row_index)
        max_column_index = max(max_column_index, grid.end_column_index)

    if sheet_manager is not None:
        sheet_manager.update_dimensions(
            sheet_id, max_row_index, max_column_index
        )

    logger.debug(
        "change_batch completed: sheet_id=%s updated_cells=%s max_row_index=%s max_column_index=%s",
        sheet_id,
        updated_cells,
        max_row_index,
        max_column_index,
    )



# ---------------------------------------------------------------------------
# Normalization helpers


def _normalize_ranges(ranges: Union[RangeLike, Sequence[RangeLike]]) -> List[GridRange]:
    if isinstance(ranges, (list, tuple)):
        return [_normalize_range(value) for value in ranges]
    return [_normalize_range(ranges)]


def _normalize_range(range_like: RangeLike) -> GridRange:
    if isinstance(range_like, GridRange):
        return range_like
    if isinstance(range_like, dict):
        range_like = _convert_range_keys(range_like)
    if hasattr(GridRange, "model_validate"):  # pydantic v2
        try:
            return GridRange.model_validate(range_like)  # type: ignore[arg-type]
        except Exception:
            pass
    return GridRange(**range_like)  # type: ignore[arg-type]


def _convert_range_keys(range_like: Dict[str, Any]) -> Dict[str, Any]:
    mapping = {
        "startRowIndex": "start_row_index",
        "endRowIndex": "end_row_index",
        "startColumnIndex": "start_column_index",
        "endColumnIndex": "end_column_index",
    }
    converted = {}
    for key, value in range_like.items():
        snake_key = mapping.get(key, key)
        converted[snake_key] = value
    return converted


def _resolve_matrix_value(
    source: ValueMatrix | FormatMatrix | None, row_index: int, column_index: int
) -> Any:
    if _is_sequence(source):
        if (
            len(source) > 0
            and _is_sequence(source[0])
            and column_index < len(source[row_index % len(source)])
        ):
            rows = source  # type: ignore[assignment]
            if row_index < len(rows):
                row_values = rows[row_index]
                if _is_sequence(row_values) and column_index < len(row_values):
                    return row_values[column_index]
            return None
        if row_index < len(source):  # 1D list behaving like column vector
            return source[row_index]
        return None
    return source


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _is_empty_cell_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value == ""
    return False


# ---------------------------------------------------------------------------
def _get_or_create_row_values(
    sheet_data_map: Any, sheet_id: int, row_index: int
) -> Any:
    sheet_key = str(sheet_id)
    sheet_rows = _map_get(sheet_data_map, sheet_key)
    if sheet_rows is None:
        sheet_rows = _create_array_like(_is_pycrdt_map(sheet_data_map))
        _map_set(sheet_data_map, sheet_key, sheet_rows)
        logger.debug(f"Created and integrated sheet_rows for sheet {sheet_id}")
    elif isinstance(sheet_rows, list):
        sheet_rows = _convert_list_to_array(sheet_rows)
        _map_set(sheet_data_map, sheet_key, sheet_rows)

    logger.debug(
        "Ensuring sheet_rows size %s, current size: %s",
        row_index + 1,
        _array_length(sheet_rows),
    )
    _ensure_array_size(sheet_rows, row_index + 1)
    row_entry = _array_get(sheet_rows, row_index)
    if row_entry is None:
        row_entry = _create_map_like(_is_pycrdt_array(sheet_rows))
        _array_set(sheet_rows, row_index, row_entry)
        _check_integrated(row_entry, "row_entry after _array_set")

        values = _create_array_like(_is_pycrdt_map(row_entry))
        _map_set_value(row_entry, "values", values)
        _check_integrated(values, "values after setting into row_entry")
        return values
    elif isinstance(row_entry, list):
        converted = _create_map_like(_is_pycrdt_array(sheet_rows))
        _array_set(sheet_rows, row_index, converted)
        converted_values = _convert_list_to_array(row_entry)
        _map_set_value(converted, "values", converted_values)
        return _map_get_value(converted, "values")

    values = _map_get_value(row_entry, "values")
    if values is None:
        values = _create_array_like()
        _map_set_value(row_entry, "values", values)
    elif isinstance(values, list):
        values = _convert_list_to_array(values)
        _map_set_value(row_entry, "values", values)

    return values


def _check_integrated(obj: Any, name: str) -> None:
    if PycrdtArray is not None and PycrdtMap is not None:
        if isinstance(obj, (PycrdtArray, PycrdtMap)):
            try:
                doc = obj.doc
                logger.debug(f"{name} is integrated: {doc is not None}")
            except RuntimeError as e:
                logger.error(f"{name} is NOT integrated: {e}")
        else:
            logger.debug(f"{name} is not a pycrdt object")
    else:
        logger.debug(f"{name} is not a pycrdt object (pycrdt not available)")


def _set_row_value(
    row_values: Any,
    column_index: int,
    cell_data: Optional[Dict[str, Any]],
) -> None:
    _ensure_array_size(row_values, column_index + 1)
    _array_set(row_values, column_index, cell_data)



# ---------------------------------------------------------------------------
# Table + sheet metadata helpers


# ---------------------------------------------------------------------------
# Generic helpers for pycrdt structures


def _get_structure(
    ydoc: Any,
    key: str,
    *,
    expect: str,
    optional: bool = False,
) -> Any:
    getter = getattr(ydoc, "get", None)
    if callable(getter):
        factory = PycrdtArray if expect == "array" else PycrdtMap
        if factory is not None:
            try:
                structure = getter(key, type=factory)  # type: ignore[arg-type]
                if structure is not None:
                    return structure
            except (TypeError, ValueError):
                pass

    getter = getattr(
        ydoc,
        "get_array" if expect == "array" else "get_map",
        None,
    )
    if callable(getter):
        return getter(key)

    if optional:
        return None
    raise AttributeError(
        f"Y.Doc does not expose a {'Y.Array' if expect == 'array' else 'Y.Map'} named '{key}'"
    )


def _map_get(y_map: Any, key: str) -> Any:
    getter = getattr(y_map, "get", None)
    if callable(getter):
        return getter(key)
    return y_map.get(key)


def _map_set(y_map: Any, key: str, value: Any) -> None:
    setter = getattr(y_map, "set", None)
    if callable(setter):
        setter(key, value)
    else:
        y_map[key] = value


def _array_length(array_like: Any) -> int:
    length = getattr(array_like, "length", None)
    if isinstance(length, int):
        return length
    if callable(length):
        try:
            return length()
        except RuntimeError:
            return 0
    try:
        return len(array_like)
    except RuntimeError:
        return 0


def _array_get(array_like: Any, index: int) -> Any:
    getter = getattr(array_like, "get", None)
    if callable(getter):
        try:
            return getter(index)
        except (IndexError, KeyError, RuntimeError):
            return None
    try:
        return array_like[index]
    except (IndexError, KeyError, TypeError, RuntimeError):
        return None


def _array_insert(array_like: Any, index: int, values: Iterable[Any]) -> None:
    items = list(values)
    try:
        array_like[index:index] = items
        return
    except Exception:
        pass
    inserter = getattr(array_like, "insert", None)
    if callable(inserter):
        if _is_pycrdt_array(array_like):
            for offset, value in enumerate(items):
                inserter(index + offset, value)
        else:
            try:
                inserter(index, items)
            except TypeError:
                for offset, value in enumerate(items):
                    inserter(index + offset, value)
        return
    if isinstance(array_like, list):
        for offset, value in enumerate(items):
            array_like.insert(index + offset, value)
        return
    raise AttributeError("Array-like object does not support insert()")


def _array_delete(array_like: Any, index: int, length: int) -> None:
    try:
        del array_like[index:index + length]
        return
    except Exception:
        pass
    deleter = getattr(array_like, "delete", None)
    if callable(deleter):
        deleter(index, length)
        return
    if hasattr(array_like, "__delitem__"):
        del array_like[index : index + length]
        return
    if hasattr(array_like, "clear") and index == 0:
        array_like.clear()
        return
    if isinstance(array_like, list):
        del array_like[index : index + length]
        return
    raise AttributeError("Array-like object does not support delete()")


def _array_set(array_like: Any, index: int, value: Any) -> None:
    current = _array_length(array_like)
    if index < current:
        try:
            array_like[index] = value
            return
        except Exception:
            pass
        _array_delete(array_like, index, 1)
        _array_insert(array_like, index, [value])
    else:
        _ensure_array_size(array_like, index)
        _array_insert(array_like, index, [value])


def _ensure_array_size(array_like: Any, size: int) -> None:
    current = _array_length(array_like)
    if current >= size:
        return
    padding = [None] * (size - current)
    _array_insert(array_like, current, padding)


def _is_pycrdt_array(value: Any) -> bool:
    return PycrdtArray is not None and isinstance(value, PycrdtArray)


def _is_pycrdt_map(value: Any) -> bool:
    return PycrdtMap is not None and isinstance(value, PycrdtMap)


def _create_array_like(use_pycrdt: bool = False) -> Any:
    if use_pycrdt and PycrdtArray is not None:  # pragma: no cover - optional dependency
        try:
            return PycrdtArray()
        except Exception:
            pass
    return _YArrayBuffer()


def _create_map_like(use_pycrdt: bool = False) -> Any:
    if use_pycrdt and PycrdtMap is not None:  # pragma: no cover - optional dependency
        try:
            return PycrdtMap()
        except Exception:
            pass
    return {}


def _convert_list_to_array(value_list: List[Any]) -> Any:
    array_like = _YArrayBuffer()
    for item in value_list:
        _array_insert(array_like, _array_length(array_like), [item])
    return array_like


def _get_with_fallback(target: Any, names: Tuple[str, ...]) -> Any:
    for name in names:
        if isinstance(target, dict) and name in target:
            return target[name]
        if hasattr(target, name):
            return getattr(target, name)
    return None


def _set_with_fallback(target: Any, names: Tuple[str, ...], value: Any) -> None:
    if isinstance(target, dict):
        for name in names:
            if name in target:
                target[name] = value
                return
        target[names[0]] = value
        return

    for name in names:
        if hasattr(target, name):
            setattr(target, name, value)
            return
    setattr(target, names[0], value)


def _create_recalc_patch(sheet_id: int, row_index: int, column_index: int) -> List[Any]:
    address = SheetCell._cell_to_address(row_index, column_index)
    return [
        f"{sheet_id}!{address}",
        {
            "rowIndex": row_index,
            "columnIndex": column_index,
            "sheetId": sheet_id,
        },
        "agent",
    ]


def _append_recalc_entry(
    recalc_array: Any, user_id: Union[str, int], patches: List[List[Any]]
) -> None:
    entry = {
        "userId": str(user_id) if user_id is not None else str(uuid.uuid4()),
        "patches": patches,
    }
    _array_insert(recalc_array, _array_length(recalc_array), [entry])




def _get_cell_xfs_key(format_value: Optional[Dict[str, Any]]) -> str:
    if format_value is None:
        return "0"

    obj = _defined_props(format_value) or {}
    state = 0

    for prop in _CELL_XFS_PROPS:
        if isinstance(obj, dict) and prop in obj and obj[prop] is not None:
            state = _hash_string(state, prop)
            state = _hash_value(state, obj[prop])

    if state >= 2**31:
        state -= 2**32
    return str(abs(state))


class _YArrayBuffer:
    """
    Minimal array implementation used when pycrdt is not available.

    The buffer mimics the subset of the Y.Array API that change_batch relies on
    (length, get, insert, delete). It stores native Python objects, which are
    perfectly acceptable values for Yjs documents.
    """

    def __init__(self) -> None:
        self._items: List[Any] = []

    def length(self) -> int:
        return len(self._items)

    def get(self, index: int) -> Any:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def insert(self, index: int, values: List[Any]) -> None:
        for offset, value in enumerate(values):
            self._items.insert(index + offset, value)

    def delete(self, index: int, length: int) -> None:
        del self._items[index : index + length]

    # Python protocol helpers -------------------------------------------------
    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._items[index] = value


def _map_get_value(target: Any, key: str) -> Any:
    getter = getattr(target, "get", None)
    if callable(getter):
        try:
            return getter(key)
        except RuntimeError:
            pass
    if isinstance(target, dict):
        return target.get(key)
    return getattr(target, key, None)


def _map_set_value(target: Any, key: str, value: Any) -> None:
    setter = getattr(target, "set", None)
    if callable(setter):
        setter(key, value)
        return

    # Try using [] operator (works for both dict and pycrdt.Map)
    if hasattr(target, "__setitem__"):
        target[key] = value
        return

    # Special case for list - create a map-like entry
    if isinstance(target, list):
        entry = _create_map_like()
        _map_set_value(entry, key, value)
        target.append(entry)
        return

    # Fallback to setattr for other types
    setattr(target, key, value)


def _queue_recalc_cells(
    recalc_array: Any, user_id: Union[str, int], patches: List[List[Any]]
) -> None:
    document = {"userId": user_id, "patches": patches}
    length = _array_length(recalc_array)
    if length:
        _array_delete(recalc_array, 0, length)
    _array_insert(recalc_array, _array_length(recalc_array), [document])
