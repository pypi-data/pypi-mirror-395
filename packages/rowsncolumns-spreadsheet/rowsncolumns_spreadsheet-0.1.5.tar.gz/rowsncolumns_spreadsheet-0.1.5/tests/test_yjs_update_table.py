from rowsncolumns_spreadsheet.yjs import create_table, update_table
from rowsncolumns_spreadsheet.types import GridRange

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc() -> MockYDoc:
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_map("cellXfs")
    return doc


def test_update_table_extends_columns_and_headers():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 10, "columnCount": 10}])

    table_id = create_table(
        doc,
        sheet_id=1,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=0,
        ),
    )

    tables = doc.get_array("tables")
    table_entry = tables.get(0)

    update_table(
        doc,
        sheet_id=1,
        table_id=table_entry["id"],
        table_updates={
            "range": {
                "startRowIndex": 0,
                "endRowIndex": 0,
                "startColumnIndex": 0,
                "endColumnIndex": 1,
            },
        },
    )

    updated_entry = tables.get(0)
    assert len(updated_entry["columns"]) == 2


def test_update_table_toggle_total_row():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 10, "columnCount": 10}])

    table_id = create_table(
        doc,
        sheet_id=1,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=0,
        ),
    )

    tables = doc.get_array("tables")
    table_entry = tables.get(0)
    original_end_row = table_entry["range"]["endRowIndex"]

    update_table(
        doc,
        sheet_id=1,
        table_id=table_entry["id"],
        table_updates={"totalRow": True},
    )

    updated_entry = tables.get(0)
    assert updated_entry["range"]["endRowIndex"] == original_end_row + 1
