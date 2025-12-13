import pytest

from rowsncolumns_spreadsheet.yjs.insert_table_column import insert_table_column
from rowsncolumns_spreadsheet.yjs.delete_table_column import delete_table_column

from tests.test_yjs_change_batch import MockYDoc


def _build_doc(column_names):
    doc = MockYDoc()
    doc.get_array("recalcCells")
    doc.get_array("sheetDataV2")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "columnCount": 10}])
    tables = doc.get_array("tables")

    table_entry = {
        "id": "table-1",
        "sheetId": 1,
        "range": {
            "startRowIndex": 0,
            "endRowIndex": 1,
            "startColumnIndex": 0,
            "endColumnIndex": len(column_names) - 1,
        },
        "columns": [{"name": name} for name in column_names],
        "headerRow": True,
    }
    tables.insert(0, [table_entry])

    sheet_data = doc.get_map("sheetDataV2")
    rows = []
    header_values = []
    for idx, name in enumerate(column_names):
        header_values.append({"ue": {"sv": name}, "ev": {"sv": name}, "fv": name})
    rows.append({"values": header_values})
    data_row = []
    for idx, name in enumerate(column_names):
        label = f"R1C{idx}"
        data_row.append({"ue": {"sv": label}, "ev": {"sv": label}})
    rows.append({"values": data_row})
    sheet_data.set("1", rows)

    return doc, table_entry["id"]


def test_insert_table_column_updates_table_and_sheet_data():
    doc, table_id = _build_doc(["First", "Second"])
    insert_table_column(doc, table_id, dimension_index=1, direction="left")

    tables = doc.get_array("tables")
    updated_table = tables.get(0)
    columns = updated_table["columns"]
    assert len(columns) == 3
    assert columns[1]["name"].startswith("Column")
    assert updated_table["range"]["endColumnIndex"] == 2

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    header_values = sheet_rows.get(0)["values"]
    assert header_values.get(1)["ue"]["sv"] == columns[1]["name"]
    data_values = sheet_rows.get(1)["values"]
    assert data_values.get(1) is None

    recalc = doc.get_array("recalcCells")
    entry = recalc.get(0)
    assert len(entry["patches"]) == 2


def test_insert_table_column_invalid_dimension_raises():
    doc, table_id = _build_doc(["First"])
    with pytest.raises(ValueError):
        insert_table_column(doc, table_id, dimension_index=5)


def test_delete_table_column_removes_values_and_updates_range():
    doc, table_id = _build_doc(["First", "Second", "Third"])
    delete_table_column(doc, table_id, dimension_index=1)

    tables = doc.get_array("tables")
    updated_table = tables.get(0)
    assert updated_table["columns"][1]["name"] == "Third"
    assert updated_table["range"]["endColumnIndex"] == 1

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    header_values = sheet_rows.get(0)["values"]
    assert header_values.get(1)["ue"]["sv"] == "Third"
    data_values = sheet_rows.get(1)["values"]
    assert data_values.get(1)["ue"]["sv"] == "R1C2"

    recalc = doc.get_array("recalcCells")
    entry = recalc.get(0)
    assert len(entry["patches"]) == 2


def test_delete_table_column_invalid_dimension_raises():
    doc, table_id = _build_doc(["Only"])
    with pytest.raises(ValueError):
        delete_table_column(doc, table_id, dimension_index=2)
