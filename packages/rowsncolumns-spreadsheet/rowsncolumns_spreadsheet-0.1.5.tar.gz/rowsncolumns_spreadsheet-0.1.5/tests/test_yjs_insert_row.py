import pytest

from rowsncolumns_spreadsheet.yjs.insert_row import insert_row

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc():
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    doc.get_array("tables")
    return doc


def test_insert_row_adds_blank_rows_and_updates_count():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(
        0,
        [
            {
                "sheetId": 1,
                "rowCount": 2,
                "columnCount": 3,
                "index": 0,
            }
        ],
    )
    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [None, {"values": []}])

    insert_row(doc, 1, reference_row_index=1, num_rows=2)

    updated_sheet = sheets.get(0)
    assert updated_sheet["rowCount"] == 4

    sheet_rows = sheet_data.get("1")
    assert len(sheet_rows) == 4
    assert sheet_rows.get(1) is None
    assert sheet_rows.get(2) is None


def test_insert_row_adjusts_tables():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "rowCount": 5, "index": 0}])
    tables = doc.get_array("tables")
    tables.insert(
        0,
        [
            {
                "sheetId": 1,
                "range": {"startRowIndex": 0, "endRowIndex": 2},
            }
        ],
    )

    insert_row(doc, 1, reference_row_index=0, num_rows=1)

    table_entry = tables.get(0)
    assert table_entry["range"]["startRowIndex"] == 0
    assert table_entry["range"]["endRowIndex"] == 3


def test_insert_row_invalid_reference_raises():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "rowCount": 1, "index": 0}])

    with pytest.raises(ValueError):
        insert_row(doc, 1, reference_row_index=5)
