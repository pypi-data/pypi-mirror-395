import pytest

from rowsncolumns_spreadsheet.yjs.insert_column import insert_column

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc():
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    doc.get_array("tables")
    return doc


def test_insert_column_updates_column_count_and_values():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "columnCount": 2, "index": 0}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [{"values": []}])

    insert_column(doc, 1, reference_column_index=1, num_columns=2)

    updated_sheet = sheets.get(0)
    assert updated_sheet["columnCount"] == 4

    rows = sheet_data.get("1")
    values = rows.get(0)["values"]
    assert len(values) == 4
    assert values.get(1) is None
    assert values.get(2) is None


def test_insert_column_updates_table_ranges():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "columnCount": 5, "index": 0}])

    tables = doc.get_array("tables")
    tables.insert(
        0,
        [
            {
                "sheetId": 1,
                "range": {"startColumnIndex": 0, "endColumnIndex": 2},
            }
        ],
    )

    insert_column(doc, 1, reference_column_index=1, num_columns=1)

    table_entry = tables.get(0)
    assert table_entry["range"]["startColumnIndex"] == 0
    assert table_entry["range"]["endColumnIndex"] == 3


def test_insert_column_invalid_reference_raises():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1, "columnCount": 1, "index": 0}])

    with pytest.raises(ValueError):
        insert_column(doc, 1, reference_column_index=5)
