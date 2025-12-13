from typing import Tuple

import pytest

from rowsncolumns_spreadsheet import (
    SpreadsheetDag,
    CellPosition,
    CellRangePosition,
    CircularDependencyError,
    UnknownSheetError,
    NamedRange,
    SheetRange,
    TableView,
    TableColumn,
    GridRange,
)


def test_add_formula_to_graph_simple_references():
    dag = SpreadsheetDag()
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    a2 = CellPosition(sheet_id=1, row_index=1, column_index=0)
    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)

    dag.add_formula_to_graph("=SUM(A1, A2)", b1)

    precedents = dag.get_precedents(b1)
    assert precedents == [b1, a2, a1]

    dependents = dag.get_dependents(a1)
    assert dependents == [b1]


def test_add_formula_with_range_reference_and_dependents():
    dag = SpreadsheetDag()
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    a2 = CellPosition(sheet_id=1, row_index=1, column_index=0)
    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)
    c3 = CellPosition(sheet_id=1, row_index=2, column_index=2)

    dag.add_formula_to_graph("=SUM(A1, A2)", b1)
    dag.add_formula_to_graph("=SUM(A1:B2)", c3)

    precedents = dag.get_precedents(c3)
    assert precedents == [
        c3,
        CellRangePosition(
            sheet_id=1,
            start_row_index=0,
            start_column_index=0,
            end_row_index=1,
            end_column_index=1,
        ),
    ]

    dependents = dag.get_dependents(a1)
    assert dependents == [b1, c3]


def test_circular_dependency_raises():
    dag = SpreadsheetDag()
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)

    with pytest.raises(CircularDependencyError):
        dag.add_formula_to_graph("=A1+10", a1)


def test_cross_sheet_dependency_with_resolver():
    sheet_ids = {"Sheet2": 2}
    dag = SpreadsheetDag(sheet_ids.get)

    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)
    dag.add_formula_to_graph("=Sheet2!A1", b1)

    precedents = dag.get_precedents(b1)
    assert precedents == [
        b1,
        CellPosition(sheet_id=2, row_index=0, column_index=0),
    ]


def test_unknown_sheet_raises():
    dag = SpreadsheetDag()
    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)

    with pytest.raises(UnknownSheetError):
        dag.add_formula_to_graph("=Sheet2!A1", b1)


def test_formula_string_literals_are_ignored():
    dag = SpreadsheetDag()
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)

    dag.add_formula_to_graph('="A1"', b1)

    assert dag.get_precedents(b1) == [b1]
    assert dag.get_dependents(a1) == []


def test_property_access_is_ignored():
    dag = SpreadsheetDag()
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    b1 = CellPosition(sheet_id=1, row_index=1, column_index=1)

    dag.add_formula_to_graph("=SUM(A1.stock_price)", b1)

    precedents = dag.get_precedents(b1)
    assert precedents == [b1, a1]
    assert dag.get_dependents(a1) == [b1]


def test_whole_column_reference_respects_bounds():
    bounds = {1: (100, 26)}

    def resolve_bounds(sheet_id: int) -> Tuple[int, int]:
        return bounds[sheet_id]

    dag = SpreadsheetDag(sheet_bounds_resolver=resolve_bounds)
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    b1 = CellPosition(sheet_id=1, row_index=0, column_index=1)

    dag.add_formula_to_graph("=SUM(A:A)", b1)

    precedents = dag.get_precedents(b1)
    assert precedents == [
        b1,
        CellRangePosition(
            sheet_id=1,
            start_row_index=0,
            start_column_index=0,
            end_row_index=99,
            end_column_index=0,
        ),
    ]
    assert dag.get_dependents(a1) == [b1]


def test_whole_row_reference_respects_bounds():
    bounds = {1: (50, 20)}

    def resolve_bounds(sheet_id: int) -> Tuple[int, int]:
        return bounds[sheet_id]

    dag = SpreadsheetDag(sheet_bounds_resolver=resolve_bounds)
    a1 = CellPosition(sheet_id=1, row_index=0, column_index=0)
    c5 = CellPosition(sheet_id=1, row_index=4, column_index=2)

    dag.add_formula_to_graph("=SUM(1:10)", c5)

    precedents = dag.get_precedents(c5)
    assert precedents == [
        c5,
        CellRangePosition(
            sheet_id=1,
            start_row_index=0,
            start_column_index=0,
            end_row_index=9,
            end_column_index=19,
        ),
    ]
    assert dag.get_dependents(a1) == [c5]


def test_named_range_dependencies():
    named_range = NamedRange(
        named_range_id="NR1",
        name="Sales",
        range=SheetRange(
            sheet_id=1,
            start_row_index=0,
            end_row_index=1,
            start_column_index=0,
            end_column_index=0,
        ),
    )
    dag = SpreadsheetDag(named_ranges=[named_range])
    target = CellPosition(sheet_id=1, row_index=5, column_index=5)
    dag.add_formula_to_graph("=SUM(Sales)", target)

    precedents = dag.get_precedents(target)
    assert precedents == [
        target,
        CellRangePosition(
            sheet_id=1,
            start_row_index=0,
            start_column_index=0,
            end_row_index=1,
            end_column_index=0,
        ),
    ]
    dependents = dag.get_dependents(
        CellPosition(sheet_id=1, row_index=0, column_index=0)
    )
    assert dependents == [target]


def _make_sample_table(header: bool = True, total: bool = False) -> TableView:
    return TableView(
        title="SalesTable",
        sheet_id=1,
        range=GridRange(
            start_row_index=0,
            end_row_index=4 if not total else 5,
            start_column_index=0,
            end_column_index=1,
        ),
        header_row=header,
        total_row=total,
        columns=[
            TableColumn(name="Revenue"),
            TableColumn(name="Units"),
        ],
    )


def test_structured_reference_column():
    table = _make_sample_table()
    dag = SpreadsheetDag(tables=[table])
    target = CellPosition(sheet_id=1, row_index=6, column_index=3)

    dag.add_formula_to_graph("=SUM(SalesTable[Revenue])", target)

    precedents = dag.get_precedents(target)
    assert precedents == [
        target,
        CellRangePosition(
            sheet_id=1,
            start_row_index=1,
            start_column_index=0,
            end_row_index=4,
            end_column_index=0,
        ),
    ]


def test_structured_reference_this_row():
    table = _make_sample_table()
    dag = SpreadsheetDag(tables=[table])
    origin = CellPosition(sheet_id=1, row_index=2, column_index=5)

    dag.add_formula_to_graph("=SalesTable[@Revenue]", origin)

    precedents = dag.get_precedents(origin)
    assert precedents == [
        origin,
        CellPosition(sheet_id=1, row_index=2, column_index=0),
    ]


def test_structured_reference_special_all():
    table = _make_sample_table(total=True)
    dag = SpreadsheetDag(tables=[table])
    target = CellPosition(sheet_id=1, row_index=7, column_index=4)

    dag.add_formula_to_graph("=SUM(SalesTable[#All])", target)

    precedents = dag.get_precedents(target)
    assert precedents == [
        target,
        CellRangePosition(
            sheet_id=1,
            start_row_index=0,
            start_column_index=0,
            end_row_index=5,
            end_column_index=1,
        ),
    ]
