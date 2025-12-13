import pytest

from rowsncolumns_spreadsheet.yjs.delete_row import delete_row

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc():
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    doc.get_array("tables")
    return doc


def test_delete_row_removes_entries_from_sheet_data():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 3, "index": 0}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [{"values": [1]}, {"values": [2]}, {"values": [3]}])

    delete_row(doc, 1, [1])

    rows = sheet_data.get("1")
    assert len(rows) == 2
    assert rows[0]["values"][0] == 1
    assert rows[1]["values"][0] == 3


def test_delete_row_updates_row_count():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "index": 0}])

    doc.get_map("sheetDataV2").set("1", [None] * 5)

    delete_row(doc, 1, [1, 2])

    updated_sheet = sheets.get(0)
    assert updated_sheet["rowCount"] == 3


def test_delete_row_invalid_index_raises():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "rowCount": 1, "index": 0}])

    doc.get_map("sheetDataV2").set("1", [None])

    with pytest.raises(ValueError):
        delete_row(doc, 1, [5])
