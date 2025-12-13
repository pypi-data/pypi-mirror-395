"""
Dependency graph utilities for spreadsheet formulas.

This module mirrors the behaviour of the TypeScript DAG implementation but
leans on the open-source ``networkx`` package for graph storage and traversal.
``FormulaDependencyParser`` performs a lightweight extraction of cell and range
references from Excel-style formulas so that caller code can register
dependencies using :class:`SpreadsheetDag`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union
import re

import networkx as nx
from openpyxl.formula.tokenizer import Tokenizer

from .sheet_cell import SheetCell
from .types import NamedRange, TableView, SheetRange


class CircularDependencyError(RuntimeError):
    """Raised when adding an edge would introduce a cycle."""


class UnknownSheetError(RuntimeError):
    """Raised when a sheet name in a formula cannot be resolved to an id."""


@dataclass(frozen=True)
class CellPosition:
    """
    Zero-based cell coordinates scoped to a sheet.
    """

    sheet_id: int
    row_index: int
    column_index: int


@dataclass(frozen=True)
class CellRangePosition:
    """
    Zero-based rectangular range representation.
    """

    sheet_id: int
    start_row_index: int
    start_column_index: int
    end_row_index: int
    end_column_index: int

    def contains(self, cell: CellPosition) -> bool:
        """Return True if the cell lies within this range."""
        if cell.sheet_id != self.sheet_id:
            return False
        return (
            self.start_row_index <= cell.row_index <= self.end_row_index
            and self.start_column_index <= cell.column_index <= self.end_column_index
        )


@dataclass(frozen=True)
class StaticReference:
    """
    Static reference (e.g. named range, pipeline id) that participates in the DAG.
    """

    identifier: str


NodePosition = Union[CellPosition, CellRangePosition, StaticReference]


def _column_label_to_index(label: str) -> int:
    """Convert Excel-style column letters (e.g. 'A', 'AA') to a zero-based index."""
    label = label.upper()
    index = 0
    for char in label:
        if not char.isalpha():
            raise ValueError(f"Invalid column label '{label}'")
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def _decode_address(address: str) -> Tuple[int, int]:
    """
    Convert an A1-style address (absolute or relative) to zero-based coordinates.
    """
    clean = address.replace("$", "").upper()
    match = re.fullmatch(r"([A-Z]+)(\d+)", clean)
    if not match:
        raise ValueError(f"Unsupported cell address '{address}'")
    column_label, row_str = match.groups()
    column_index = _column_label_to_index(column_label)
    row_index = int(row_str) - 1
    if row_index < 0:
        raise ValueError(f"Row index must be positive in '{address}'")
    return row_index, column_index


def _normalize_sheet_name(value: Optional[str]) -> Optional[str]:
    """Strip surrounding quotes and whitespace from sheet names."""
    if value is None:
        return None
    name = value.strip()
    if name.endswith("!"):
        name = name[:-1]
    if name.startswith("'") and name.endswith("'") and len(name) >= 2:
        # Excel doubles single quotes inside quoted sheet names.
        name = name[1:-1].replace("''", "'")
    return name


def _make_cell_key(position: CellPosition) -> str:
    """Create a key matching the TypeScript DAG key format."""
    return SheetCell.generate_cell_key(
        position.sheet_id, position.row_index, position.column_index
    )


def _make_range_key(position: CellRangePosition) -> str:
    """Create a canonical key for a range node."""
    start = SheetCell._cell_to_address(
        position.start_row_index, position.start_column_index
    )
    end = SheetCell._cell_to_address(position.end_row_index, position.end_column_index)
    return f"{position.sheet_id}!{start}:{end}"


def _make_static_key(position: StaticReference) -> str:
    return f"static::{position.identifier}"


def _strip_property(reference: str) -> str:
    """
    Remove property accessors (e.g. `.stock_price`) that follow a cell reference.

    Only strips dots that appear outside of structured reference brackets so that
    table column names containing dots continue to work.
    """
    bracket_depth = 0
    in_quotes = False
    idx = 0
    length = len(reference)
    while idx < length:
        char = reference[idx]
        if char == "'":
            if in_quotes and idx + 1 < length and reference[idx + 1] == "'":
                idx += 1  # Skip escaped quote
            else:
                in_quotes = not in_quotes
        elif char == "[" and not in_quotes:
            bracket_depth += 1
        elif char == "]" and not in_quotes:
            bracket_depth = max(bracket_depth - 1, 0)
        elif char == "." and not in_quotes and bracket_depth == 0:
            return reference[:idx]
        idx += 1
    return reference


class FormulaDependencyParser:
    """
    Extract references from formulas using the ``openpyxl`` tokenizer for robust
    handling of nested expressions.
    """

    COLUMN_RANGE_ONLY_RE = re.compile(r"^\$?[A-Z]{1,3}:\$?[A-Z]{1,3}$", re.IGNORECASE)
    ROW_RANGE_ONLY_RE = re.compile(r"^\$?\d+:\$?\d+$", re.IGNORECASE)
    SINGLE_CELL_RE = re.compile(r"^\$?[A-Z]{1,3}\$?\d+$", re.IGNORECASE)
    ARRAY_SPLIT_RE = re.compile(r"[;,]")

    STRUCT_SPECIAL_COLUMN_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*\[#?(?P<special>[A-Za-z\s]+)\],\s*\[(?P<column>[^\]]+)\]\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_THIS_ROW_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*@\[?(?P<column>[^\]]+?)\]?\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_COLUMN_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*(?P<column>(?![#@])[^\]]+?)\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_SPECIAL_ONLY_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*(?P<special>#(?:[A-Za-z\s]+))\s*\]$",
        re.IGNORECASE,
    )

    DEFAULT_MAX_ROWS = 1048576
    DEFAULT_MAX_COLUMNS = 16384

    def __init__(
        self,
        sheet_id_resolver: Optional[Callable[[str], Optional[int]]] = None,
        sheet_bounds_resolver: Optional[
            Callable[[int], Optional[Tuple[int, int]]]
        ] = None,
        default_row_count: int = DEFAULT_MAX_ROWS,
        default_column_count: int = DEFAULT_MAX_COLUMNS,
        named_range_names: Optional[Sequence[str]] = None,
        named_range_resolver: Optional[
            Callable[[str], Iterable[Union[CellPosition, CellRangePosition]]]
        ] = None,
        table_names: Optional[Sequence[str]] = None,
        structured_reference_resolver: Optional[
            Callable[
                [str, Optional[str], bool, Optional[str], CellPosition],
                Iterable[Union[CellPosition, CellRangePosition]],
            ]
        ] = None,
    ) -> None:
        self._resolve_sheet_id = sheet_id_resolver
        self._resolve_bounds = sheet_bounds_resolver
        self._default_row_count = default_row_count
        self._default_column_count = default_column_count
        self._named_range_names: Set[str] = (
            {name.upper() for name in named_range_names} if named_range_names else set()
        )
        self._named_range_resolver = named_range_resolver
        self._table_names: Set[str] = (
            {name.upper() for name in table_names} if table_names else set()
        )
        self._structured_reference_resolver = structured_reference_resolver

    def update_named_ranges(
        self,
        names: Optional[Sequence[str]],
        resolver: Optional[
            Callable[[str], Iterable[Union[CellPosition, CellRangePosition]]]
        ],
    ) -> None:
        self._named_range_names = (
            {name.upper() for name in names} if names else set()
        )
        self._named_range_resolver = resolver

    def update_tables(
        self,
        names: Optional[Sequence[str]],
        resolver: Optional[
            Callable[
                [str, Optional[str], bool, Optional[str], CellPosition],
                Iterable[Union[CellPosition, CellRangePosition]],
            ]
        ],
    ) -> None:
        self._table_names = {name.upper() for name in names} if names else set()
        self._structured_reference_resolver = resolver

    def parse(
        self, formula: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if formula == "":
            raise ValueError("Input must not be empty.")
        expression = formula if formula.startswith("=") else f"={formula}"
        tokenizer = Tokenizer(expression)

        dependencies: List[Union[CellPosition, CellRangePosition]] = []
        seen: Set[str] = set()

        for token in tokenizer.items:
            for position in self._positions_from_token(token, origin):
                if isinstance(position, CellRangePosition):
                    key = _make_range_key(position)
                elif isinstance(position, CellPosition):
                    key = _make_cell_key(position)
                else:
                    key = _make_static_key(position)
                if key not in seen:
                    seen.add(key)
                    dependencies.append(position)
        return dependencies

    def _positions_from_token(
        self, token, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if token.type != "OPERAND":
            return []
        value = token.value
        if value is None:
            return []
        text = str(value).strip()
        if not text:
            return []

        original_text = text
        text = _strip_property(text)
        if not text:
            return []

        subtype = (token.subtype or "").upper()
        property_stripped = text != original_text
        if subtype in {"NUMBER", "TEXT", "LOGICAL", "ERROR"} and not property_stripped:
            return []

        uppercase_text = text.upper()

        if text.startswith('"') and text.endswith('"'):
            return []
        if text.startswith("{") and text.endswith("}"):
            return self._positions_from_array_literal(text, origin)
        if uppercase_text in {"TRUE", "FALSE"}:
            return []
        if text.startswith("#") and uppercase_text not in self._named_range_names:
            return []

        if "[" in text and "]" in text:
            return list(self._structured_reference_positions(text, origin))

        if self._named_range_resolver and uppercase_text in self._named_range_names:
            return list(self._named_range_resolver(text))

        try:
            return self._positions_from_reference_text(text, origin)
        except ValueError:
            return []

    def _positions_from_array_literal(
        self, literal: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        content = literal.strip()[1:-1]
        if not content:
            return []
        positions: List[Union[CellPosition, CellRangePosition]] = []
        for part in self.ARRAY_SPLIT_RE.split(content):
            ref = part.strip()
            if not ref:
                continue
            ref = _strip_property(ref)
            if not ref:
                continue
            if ref.startswith('"') and ref.endswith('"'):
                continue
            if "[" in ref and "]" in ref:
                positions.extend(self._structured_reference_positions(ref, origin))
                continue
            try:
                positions.extend(self._positions_from_reference_text(ref, origin))
            except ValueError:
                continue
        return positions

    def _structured_reference_positions(
        self, value: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if not self._structured_reference_resolver or not self._table_names:
            return []
        stripped = value.strip()
        for pattern, handler in (
            (self.STRUCT_SPECIAL_COLUMN_FULL, self._handle_struct_special_column),
            (self.STRUCT_THIS_ROW_FULL, self._handle_struct_this_row),
            (self.STRUCT_SPECIAL_ONLY_FULL, self._handle_struct_special_only),
            (self.STRUCT_COLUMN_FULL, self._handle_struct_column),
        ):
            match = pattern.fullmatch(stripped)
            if match:
                result = handler(match, origin)
                if result:
                    return list(result)
        return []

    def _positions_from_reference_text(
        self, text: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        text = _strip_property(text)
        if not text:
            return []
        sheet_name, body = self._split_sheet_reference(text)
        sheet_id = self._resolve_sheet(sheet_name, origin.sheet_id)
        body = _strip_property(body.strip())
        if not body:
            return []

        if self.COLUMN_RANGE_ONLY_RE.fullmatch(body):
            start_str, end_str = body.split(":", 1)
            start_col = _column_label_to_index(start_str.replace("$", ""))
            end_col = _column_label_to_index(end_str.replace("$", ""))
            start_col, end_col = sorted((start_col, end_col))
            max_rows, max_columns = self._sheet_bounds(sheet_id)
            max_col_index = max_columns - 1
            start_col = min(start_col, max_col_index)
            end_col = min(end_col, max_col_index)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=0,
                    start_column_index=start_col,
                    end_row_index=max_rows - 1,
                    end_column_index=end_col,
                )
            ]

        if self.ROW_RANGE_ONLY_RE.fullmatch(body):
            start_str, end_str = body.split(":", 1)
            start_row = _decode_row(start_str)
            end_row = _decode_row(end_str)
            start_row, end_row = sorted((start_row, end_row))
            max_rows, max_columns = self._sheet_bounds(sheet_id)
            max_row_index = max_rows - 1
            start_row = min(start_row, max_row_index)
            end_row = min(end_row, max_row_index)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=start_row,
                    start_column_index=0,
                    end_row_index=end_row,
                    end_column_index=max_columns - 1,
                )
            ]

        if ":" in body:
            start_str, end_str = body.split(":", 1)
            start_row, start_col = _decode_address(start_str)
            end_row, end_col = _decode_address(end_str)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=min(start_row, end_row),
                    start_column_index=min(start_col, end_col),
                    end_row_index=max(start_row, end_row),
                    end_column_index=max(start_col, end_col),
                )
            ]

        if not self.SINGLE_CELL_RE.fullmatch(body):
            raise ValueError(f"Unsupported reference '{text}'")

        row_index, column_index = _decode_address(body)
        return [
            CellPosition(
                sheet_id=sheet_id,
                row_index=row_index,
                column_index=column_index,
            )
        ]

    @staticmethod
    def _split_sheet_reference(reference: str) -> Tuple[Optional[str], str]:
        if "!" not in reference:
            return None, reference
        sheet_part, remainder = reference.split("!", 1)
        return _normalize_sheet_name(sheet_part), remainder

    def _resolve_sheet(self, sheet_name: Optional[str], default_id: int) -> int:
        if not sheet_name:
            return default_id
        if self._resolve_sheet_id is None:
            raise UnknownSheetError(
                f"No resolver provided for sheet reference '{sheet_name}'"
            )
        resolved = self._resolve_sheet_id(sheet_name)
        if resolved is None:
            raise UnknownSheetError(f"Unknown sheet '{sheet_name}'")
        return resolved

    def _sheet_bounds(self, sheet_id: int) -> Tuple[int, int]:
        rows = self._default_row_count
        cols = self._default_column_count
        if self._resolve_bounds is not None:
            bounds = self._resolve_bounds(sheet_id)
            if bounds:
                res_rows, res_cols = bounds
                if isinstance(res_rows, int) and res_rows > 0:
                    rows = res_rows
                if isinstance(res_cols, int) and res_cols > 0:
                    cols = res_cols
        return rows, cols

    def _handle_struct_special_column(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        special = "#" + match.group("special").lstrip("#")
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, False, special, origin
        )

    def _handle_struct_this_row(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, True, None, origin
        )

    def _handle_struct_column(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, False, None, origin
        )

    def _handle_struct_special_only(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        special = match.group("special")
        return self._structured_reference_resolver(
            table, None, False, special, origin
        )

def _decode_row(value: str) -> int:
    """Convert a 1-based row indicator (optionally absolute) to zero-based index."""
    row = int(value.replace("$", ""))
    if row <= 0:
        raise ValueError(f"Row references must be >= 1; got '{value}'.")
    return row - 1


class SpreadsheetDag:
    """
    Directed Acyclic Graph storing formula dependencies.

    Example:
        >>> graph = SpreadsheetDag()
        >>> A1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
        >>> A2 = CellPosition(sheet_id=1, row_index=1, column_index=0)
        >>> B1 = CellPosition(sheet_id=1, row_index=0, column_index=1)
        >>> graph.add_formula_to_graph("=SUM(A1, A2)", B1)
        >>> graph.get_precedents(B1)
        [CellPosition(sheet_id=1, row_index=0, column_index=1),
         CellPosition(sheet_id=1, row_index=1, column_index=0),
         CellPosition(sheet_id=1, row_index=0, column_index=0)]
        >>> graph.get_dependents(A1)
        [CellPosition(sheet_id=1, row_index=0, column_index=1)]
    """

    def __init__(
        self,
        sheet_id_resolver: Optional[Callable[[str], Optional[int]]] = None,
        sheet_bounds_resolver: Optional[
            Callable[[int], Optional[Tuple[int, int]]]
        ] = None,
        default_row_count: int = FormulaDependencyParser.DEFAULT_MAX_ROWS,
        default_column_count: int = FormulaDependencyParser.DEFAULT_MAX_COLUMNS,
        named_ranges: Optional[Sequence[NamedRange]] = None,
        tables: Optional[Sequence[TableView]] = None,
    ) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()
        self._positions: Dict[str, NodePosition] = {}
        self._ranges: Dict[str, CellRangePosition] = {}
        self._named_ranges: Dict[str, NamedRange] = {}
        self._tables: Dict[str, TableView] = {}
        self._parser = FormulaDependencyParser(
            sheet_id_resolver,
            sheet_bounds_resolver,
            default_row_count,
            default_column_count,
            named_range_names=[],
            named_range_resolver=None,
            table_names=[],
            structured_reference_resolver=None,
        )
        self.set_named_ranges(named_ranges)
        self.set_tables(tables)

    # --------------------------------------------------------------------- #
    # Node helpers
    # --------------------------------------------------------------------- #

    def _ensure_node(self, position: NodePosition) -> str:
        key = self.make_key(position)
        if key not in self._graph:
            node_type = self._node_type(position)
            self._graph.add_node(key, type=node_type)
            self._positions[key] = position
            if isinstance(position, CellRangePosition):
                self._ranges[key] = position
        else:
            # Update cached position (important when range bounds change)
            self._positions[key] = position
            if isinstance(position, CellRangePosition):
                self._ranges[key] = position
        return key

    @staticmethod
    def _node_type(position: NodePosition) -> str:
        if isinstance(position, CellPosition):
            return "cell"
        if isinstance(position, CellRangePosition):
            return "range"
        return "static"

    def make_key(self, position: NodePosition) -> str:
        if isinstance(position, CellPosition):
            return _make_cell_key(position)
        if isinstance(position, CellRangePosition):
            return _make_range_key(position)
        return _make_static_key(position)

    def _remove_precedents(self, node_key: str) -> None:
        if node_key not in self._graph:
            return
        for predecessor in list(self._graph.predecessors(node_key)):
            self._graph.remove_edge(predecessor, node_key)

    def _topological_sort(
        self,
        start_keys: Sequence[str],
        successor: Callable[[str], Iterable[str]],
    ) -> List[str]:
        """
        Replicate the TypeScript DAG depth-first topological traversal.

        The starting nodes are included in the returned ordering, and inputs
        appear after their dependents (mirroring the TS implementation).
        """
        visited: Set[str] = set()
        ordered: List[str] = []

        def visit(node_key: str) -> None:
            if node_key in visited:
                return
            visited.add(node_key)
            for child_key in successor(node_key):
                visit(child_key)
            ordered.append(node_key)

        for start_key in start_keys:
            visit(start_key)

        ordered.reverse()
        return ordered

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def set_named_ranges(
        self, named_ranges: Optional[Sequence[NamedRange]]
    ) -> None:
        self._named_ranges = {}
        if named_ranges:
            for named_range in named_ranges:
                self._named_ranges[named_range.name.upper()] = named_range
        resolver = self._resolve_named_range if self._named_ranges else None
        self._parser.update_named_ranges(
            list(self._named_ranges.keys()) if self._named_ranges else None,
            resolver,
        )

    def set_tables(self, tables: Optional[Sequence[TableView]]) -> None:
        self._tables = {}
        if tables:
            for table in tables:
                self._tables[table.title.upper()] = table
        resolver = (
            self._resolve_structured_reference if self._tables else None
        )
        self._parser.update_tables(
            list(self._tables.keys()) if self._tables else None, resolver
        )

    def add_formula_to_graph(self, formula: str, cell: CellPosition) -> None:
        """
        Parse ``formula`` and register its precedents for ``cell``.
        """
        node_key = self._ensure_node(cell)
        dependencies = self._parser.parse(formula.lstrip("="), cell)

        # Remove existing precedents before wiring new ones
        self._remove_precedents(node_key)

        for dependency in dependencies:
            dep_key = self._ensure_node(dependency)
            if dep_key == node_key:
                raise CircularDependencyError(
                    "Circular dependency detected: a formula referenced its own cell."
                )
            # Detect cycles prior to linking
            if nx.has_path(self._graph, node_key, dep_key):
                raise CircularDependencyError(
                    "Circular dependency detected while adding formula."
                )
            self._graph.add_edge(dep_key, node_key)

    def remove_formula(self, cell: CellPosition) -> None:
        """Remove all precedents that point to ``cell``."""
        node_key = self.make_key(cell)
        self._remove_precedents(node_key)

    def remove_node(self, position: NodePosition) -> None:
        """Completely remove a node from the graph."""
        key = self.make_key(position)
        if key in self._graph:
            self._graph.remove_node(key)
            self._positions.pop(key, None)
            self._ranges.pop(key, None)

    def get_precedents(self, cell: CellPosition) -> List[NodePosition]:
        """
        Return the cell and its precedents in the same topological order as the
        TypeScript implementation (formula cell first, followed by inputs).
        """
        key = self.make_key(cell)
        if key not in self._graph:
            return []
        ordering = self._topological_sort(
            [key],
            lambda node_key: list(self._graph.predecessors(node_key)),
        )
        return [self._positions[k] for k in ordering]

    def get_dependents(self, cell: CellPosition) -> List[CellPosition]:
        """
        Return downstream cells that depend (directly or indirectly) on ``cell``.
        """
        start_keys = []
        key = self.make_key(cell)
        if key in self._graph:
            start_keys.append(key)

        # Include array/range nodes that cover this cell
        for range_key, range_pos in self._ranges.items():
            if range_pos.contains(cell):
                start_keys.append(range_key)

        dependent_keys: Set[str] = set()
        for start_key in start_keys:
            dependent_keys.update(nx.descendants(self._graph, start_key))

        dependents: List[CellPosition] = []
        for dep_key in dependent_keys:
            position = self._positions.get(dep_key)
            if isinstance(position, CellPosition):
                dependents.append(position)
        dependents.sort(key=lambda pos: (pos.sheet_id, pos.row_index, pos.column_index))
        return dependents

    def _resolve_named_range(
        self, name: str
    ) -> List[Union[CellPosition, CellRangePosition]]:
        named_range = self._named_ranges.get(name.upper())
        if not named_range or not named_range.range:
            return []
        return [self._sheet_range_to_position(named_range.range)]

    @staticmethod
    def _sheet_range_to_position(
        sheet_range: SheetRange,
    ) -> Union[CellPosition, CellRangePosition]:
        if (
            sheet_range.start_row_index == sheet_range.end_row_index
            and sheet_range.start_column_index == sheet_range.end_column_index
        ):
            return CellPosition(
                sheet_id=sheet_range.sheet_id,
                row_index=sheet_range.start_row_index,
                column_index=sheet_range.start_column_index,
            )
        return CellRangePosition(
            sheet_id=sheet_range.sheet_id,
            start_row_index=sheet_range.start_row_index,
            start_column_index=sheet_range.start_column_index,
            end_row_index=sheet_range.end_row_index,
            end_column_index=sheet_range.end_column_index,
        )

    def _resolve_structured_reference(
        self,
        table_name: str,
        column_name: Optional[str],
        this_row: bool,
        special_item: Optional[str],
        origin: CellPosition,
    ) -> List[Union[CellPosition, CellRangePosition]]:
        table = self._tables.get(table_name.upper())
        if not table or table.range is None:
            return []
        row_bounds = self._table_row_bounds(table, special_item, this_row, origin.row_index)
        if row_bounds is None:
            return []
        row_start, row_end = row_bounds

        column_name_normalized = column_name.strip() if column_name else None
        if column_name_normalized:
            column_index = self._table_column_index(table, column_name_normalized)
            if column_index is None:
                return []
            column_start = table.range.start_column_index + column_index
            column_end = column_start
        else:
            column_start = table.range.start_column_index
            column_end = table.range.end_column_index

        if this_row and column_name_normalized:
            return [
                CellPosition(
                    sheet_id=table.sheet_id,
                    row_index=row_start,
                    column_index=column_start,
                )
            ]

        return [
            CellRangePosition(
                sheet_id=table.sheet_id,
                start_row_index=row_start,
                start_column_index=column_start,
                end_row_index=row_end,
                end_column_index=column_end,
            )
        ]

    def _table_row_bounds(
        self,
        table: TableView,
        special_item: Optional[str],
        this_row: bool,
        origin_row: int,
    ) -> Optional[Tuple[int, int]]:
        table_range = table.range
        if table_range is None:
            return None
        start_row = table_range.start_row_index
        end_row = table_range.end_row_index
        header_present = True if table.header_row is None else bool(table.header_row)
        total_present = bool(table.total_row)

        data_start = start_row + (1 if header_present else 0)
        data_end = end_row - (1 if total_present else 0)
        data_start = min(max(data_start, start_row), end_row)
        data_end = max(min(data_end, end_row), data_start)

        if this_row:
            if origin_row < data_start or origin_row > data_end:
                return None
            return origin_row, origin_row

        special_upper = special_item.upper() if special_item else None
        if special_upper in (None, "#DATA"):
            return data_start, data_end
        if special_upper in {"#HEADERS", "#HEADER"}:
            if not header_present:
                return None
            return start_row, start_row
        if special_upper in {"#TOTALS", "#TOTAL"}:
            if not total_present:
                return None
            return end_row, end_row
        if special_upper in {"#ALL", "#ENTIRE TABLE"}:
            first_row = start_row if header_present else data_start
            last_row = end_row if total_present else data_end
            return first_row, last_row
        if special_upper in {"#THIS ROW"}:
            if origin_row < data_start or origin_row > data_end:
                return None
            return origin_row, origin_row
        return data_start, data_end

    @staticmethod
    def _table_column_index(table: TableView, column_name: str) -> Optional[int]:
        if not table.columns:
            return None
        target = column_name.strip().upper()
        for idx, column in enumerate(table.columns):
            if column.name.strip().upper() == target:
                return idx
        return None

    def clear(self) -> None:
        """Reset the graph."""
        self._graph.clear()
        self._positions.clear()
        self._ranges.clear()


__all__ = [
    "CircularDependencyError",
    "UnknownSheetError",
    "CellPosition",
    "CellRangePosition",
    "StaticReference",
    "SpreadsheetDag",
]
class FormulaDependencyParser:
    """
    Extract references from formulas using the ``openpyxl`` tokenizer for robust
    handling of nested expressions.
    """

    COLUMN_RANGE_ONLY_RE = re.compile(r"^\$?[A-Z]{1,3}:\$?[A-Z]{1,3}$", re.IGNORECASE)
    ROW_RANGE_ONLY_RE = re.compile(r"^\$?\d+:\$?\d+$", re.IGNORECASE)
    SINGLE_CELL_RE = re.compile(r"^\$?[A-Z]{1,3}\$?\d+$", re.IGNORECASE)
    ARRAY_SPLIT_RE = re.compile(r"[;,]")

    STRUCT_SPECIAL_COLUMN_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*\[#?(?P<special>[A-Za-z\s]+)\],\s*\[(?P<column>[^\]]+)\]\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_THIS_ROW_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*@\[?(?P<column>[^\]]+?)\]?\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_COLUMN_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*(?P<column>(?![#@])[^\]]+?)\s*\]$",
        re.IGNORECASE,
    )
    STRUCT_SPECIAL_ONLY_FULL = re.compile(
        r"^(?P<table>[A-Za-z_][\w]*)\[\s*(?P<special>#(?:[A-Za-z\s]+))\s*\]$",
        re.IGNORECASE,
    )

    DEFAULT_MAX_ROWS = 1048576
    DEFAULT_MAX_COLUMNS = 16384

    def __init__(
        self,
        sheet_id_resolver: Optional[Callable[[str], Optional[int]]] = None,
        sheet_bounds_resolver: Optional[
            Callable[[int], Optional[Tuple[int, int]]]
        ] = None,
        default_row_count: int = DEFAULT_MAX_ROWS,
        default_column_count: int = DEFAULT_MAX_COLUMNS,
        named_range_names: Optional[Sequence[str]] = None,
        named_range_resolver: Optional[
            Callable[[str], Iterable[Union[CellPosition, CellRangePosition]]]
        ] = None,
        table_names: Optional[Sequence[str]] = None,
        structured_reference_resolver: Optional[
            Callable[
                [str, Optional[str], bool, Optional[str], CellPosition],
                Iterable[Union[CellPosition, CellRangePosition]],
            ]
        ] = None,
    ) -> None:
        self._resolve_sheet_id = sheet_id_resolver
        self._resolve_bounds = sheet_bounds_resolver
        self._default_row_count = default_row_count
        self._default_column_count = default_column_count
        self._named_range_names: Set[str] = (
            {name.upper() for name in named_range_names} if named_range_names else set()
        )
        self._named_range_resolver = named_range_resolver
        self._table_names: Set[str] = (
            {name.upper() for name in table_names} if table_names else set()
        )
        self._structured_reference_resolver = structured_reference_resolver

    def update_named_ranges(
        self,
        names: Optional[Sequence[str]],
        resolver: Optional[
            Callable[[str], Iterable[Union[CellPosition, CellRangePosition]]]
        ],
    ) -> None:
        self._named_range_names = (
            {name.upper() for name in names} if names else set()
        )
        self._named_range_resolver = resolver

    def update_tables(
        self,
        names: Optional[Sequence[str]],
        resolver: Optional[
            Callable[
                [str, Optional[str], bool, Optional[str], CellPosition],
                Iterable[Union[CellPosition, CellRangePosition]],
            ]
        ],
    ) -> None:
        self._table_names = {name.upper() for name in names} if names else set()
        self._structured_reference_resolver = resolver

    def parse(
        self, formula: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if formula == "":
            raise ValueError("Input must not be empty.")
        expression = formula if formula.startswith("=") else f"={formula}"
        tokenizer = Tokenizer(expression)

        dependencies: List[Union[CellPosition, CellRangePosition]] = []
        seen: Set[str] = set()

        for token in tokenizer.items:
            for position in self._positions_from_token(token, origin):
                if isinstance(position, CellRangePosition):
                    key = _make_range_key(position)
                elif isinstance(position, CellPosition):
                    key = _make_cell_key(position)
                else:
                    key = _make_static_key(position)
                if key not in seen:
                    seen.add(key)
                    dependencies.append(position)
        return dependencies

    def _positions_from_token(
        self, token, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if token.type != "OPERAND":
            return []
        value = token.value
        if value is None:
            return []
        text = str(value).strip()
        if not text:
            return []

        original_text = text
        text = _strip_property(text)
        if not text:
            return []

        subtype = (token.subtype or "").upper()
        if subtype in {"NUMBER", "TEXT", "LOGICAL", "ERROR"} and text == original_text:
            return []

        uppercase_text = text.upper()

        if text.startswith('"') and text.endswith('"'):
            return []
        if text.startswith("{") and text.endswith("}"):
            return self._positions_from_array_literal(text, origin)
        if uppercase_text in {"TRUE", "FALSE"}:
            return []
        if text.startswith("#") and uppercase_text not in self._named_range_names:
            return []

        if "[" in text and "]" in text:
            return list(self._structured_reference_positions(text, origin))

        if self._named_range_resolver and uppercase_text in self._named_range_names:
            return list(self._named_range_resolver(text))

        try:
            return self._positions_from_reference_text(text, origin)
        except ValueError:
            return []

    def _positions_from_array_literal(
        self, literal: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        content = literal.strip()[1:-1]
        if not content:
            return []
        positions: List[Union[CellPosition, CellRangePosition]] = []
        for part in self.ARRAY_SPLIT_RE.split(content):
            ref = part.strip()
            if not ref:
                continue
            if ref.startswith('"') and ref.endswith('"'):
                continue
            if "[" in ref and "]" in ref:
                positions.extend(self._structured_reference_positions(ref, origin))
                continue
            try:
                positions.extend(self._positions_from_reference_text(ref, origin))
            except ValueError:
                continue
        return positions

    def _structured_reference_positions(
        self, value: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        if not self._structured_reference_resolver or not self._table_names:
            return []
        stripped = value.strip()
        for pattern, handler in (
            (self.STRUCT_SPECIAL_COLUMN_FULL, self._handle_struct_special_column),
            (self.STRUCT_THIS_ROW_FULL, self._handle_struct_this_row),
            (self.STRUCT_SPECIAL_ONLY_FULL, self._handle_struct_special_only),
            (self.STRUCT_COLUMN_FULL, self._handle_struct_column),
        ):
            match = pattern.fullmatch(stripped)
            if match:
                result = handler(match, origin)
                if result:
                    return list(result)
        return []

    def _positions_from_reference_text(
        self, text: str, origin: CellPosition
    ) -> List[Union[CellPosition, CellRangePosition]]:
        sheet_name, body = self._split_sheet_reference(text)
        sheet_id = self._resolve_sheet(sheet_name, origin.sheet_id)
        body = body.strip()
        if not body:
            return []

        if self.COLUMN_RANGE_ONLY_RE.fullmatch(body):
            start_str, end_str = body.split(":", 1)
            start_col = _column_label_to_index(start_str.replace("$", ""))
            end_col = _column_label_to_index(end_str.replace("$", ""))
            start_col, end_col = sorted((start_col, end_col))
            max_rows, max_columns = self._sheet_bounds(sheet_id)
            max_col_index = max_columns - 1
            start_col = min(start_col, max_col_index)
            end_col = min(end_col, max_col_index)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=0,
                    start_column_index=start_col,
                    end_row_index=max_rows - 1,
                    end_column_index=end_col,
                )
            ]

        if self.ROW_RANGE_ONLY_RE.fullmatch(body):
            start_str, end_str = body.split(":", 1)
            start_row = _decode_row(start_str)
            end_row = _decode_row(end_str)
            start_row, end_row = sorted((start_row, end_row))
            max_rows, max_columns = self._sheet_bounds(sheet_id)
            max_row_index = max_rows - 1
            start_row = min(start_row, max_row_index)
            end_row = min(end_row, max_row_index)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=start_row,
                    start_column_index=0,
                    end_row_index=end_row,
                    end_column_index=max_columns - 1,
                )
            ]

        if ":" in body:
            start_str, end_str = body.split(":", 1)
            start_row, start_col = _decode_address(start_str)
            end_row, end_col = _decode_address(end_str)
            return [
                CellRangePosition(
                    sheet_id=sheet_id,
                    start_row_index=min(start_row, end_row),
                    start_column_index=min(start_col, end_col),
                    end_row_index=max(start_row, end_row),
                    end_column_index=max(start_col, end_col),
                )
            ]

        if not self.SINGLE_CELL_RE.fullmatch(body):
            raise ValueError(f"Unsupported reference '{text}'")

        row_index, column_index = _decode_address(body)
        return [
            CellPosition(
                sheet_id=sheet_id,
                row_index=row_index,
                column_index=column_index,
            )
        ]

    @staticmethod
    def _split_sheet_reference(reference: str) -> Tuple[Optional[str], str]:
        if "!" not in reference:
            return None, reference
        sheet_part, remainder = reference.split("!", 1)
        return _normalize_sheet_name(sheet_part), remainder

    def _resolve_sheet(self, sheet_name: Optional[str], default_id: int) -> int:
        if not sheet_name:
            return default_id
        if self._resolve_sheet_id is None:
            raise UnknownSheetError(
                f"No resolver provided for sheet reference '{sheet_name}'"
            )
        resolved = self._resolve_sheet_id(sheet_name)
        if resolved is None:
            raise UnknownSheetError(f"Unknown sheet '{sheet_name}'")
        return resolved

    def _sheet_bounds(self, sheet_id: int) -> Tuple[int, int]:
        rows = self._default_row_count
        cols = self._default_column_count
        if self._resolve_bounds is not None:
            bounds = self._resolve_bounds(sheet_id)
            if bounds:
                res_rows, res_cols = bounds
                if isinstance(res_rows, int) and res_rows > 0:
                    rows = res_rows
                if isinstance(res_cols, int) and res_cols > 0:
                    cols = res_cols
        return rows, cols

    def _handle_struct_special_column(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        special = "#" + match.group("special").lstrip("#")
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, False, special, origin
        )

    def _handle_struct_this_row(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, True, None, origin
        )

    def _handle_struct_column(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        column = match.group("column")
        return self._structured_reference_resolver(
            table, column, False, None, origin
        )

    def _handle_struct_special_only(
        self, match: re.Match[str], origin: CellPosition
    ) -> Optional[Iterable[Union[CellPosition, CellRangePosition]]]:
        if not self._structured_reference_resolver:
            return None
        table = match.group("table")
        if table.upper() not in self._table_names:
            return None
        special = match.group("special")
        return self._structured_reference_resolver(
            table, None, False, special, origin
        )
