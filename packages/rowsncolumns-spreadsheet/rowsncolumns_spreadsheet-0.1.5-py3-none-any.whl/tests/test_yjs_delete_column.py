import pytest

from rowsncolumns_spreadsheet.yjs.delete_column import delete_column

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc():
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    doc.get_array("tables")
    return doc


def test_delete_column_removes_values():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "columnCount": 3, "index": 0}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [{"values": [1, 2, 3]}])

    delete_column(doc, 1, [1])

    rows = sheet_data.get("1")
    values = rows.get(0)["values"]
    assert values.get(0) == 1
    assert values.get(1) == 3


def test_delete_column_updates_column_count():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "columnCount": 5, "index": 0}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [{"values": [None] * 5}])

    delete_column(doc, 1, [0, 1])

    updated_sheet = sheets.get(0)
    assert updated_sheet["columnCount"] == 3


def test_delete_column_invalid_index_raises():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "columnCount": 1, "index": 0}])

    doc.get_map("sheetDataV2").set("1", [{"values": [None]}])

    with pytest.raises(ValueError):
        delete_column(doc, 1, [5])
