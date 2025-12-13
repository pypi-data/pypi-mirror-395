from rowsncolumns_spreadsheet.yjs.create_table import create_table
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


def test_create_table_creates_table_entry_and_headers():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 100, "columnCount": 100}])

    table_id = create_table(
        doc,
        sheet_id=1,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=1,
        ),
    )

    tables = doc.get_array("tables")
    table_entry = tables.get(0)
    assert table_entry["id"] == table_id
    assert len(table_entry["columns"]) == 2
    assert table_entry["columns"][0]["name"] == "Column1"
    assert table_entry["columns"][1]["name"] == "Column2"

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    header_row = sheet_rows.get(0)
    values = header_row["values"]
    assert values.get(0)["ue"]["sv"] == "Column1"
    assert values.get(1)["ue"]["sv"] == "Column2"


def test_create_table_preserves_existing_header_values():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 100, "columnCount": 100}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [None])
    sheet_rows = sheet_data.get("1")
    header_row = {"values": []}
    sheet_rows[0] = header_row
    header_row["values"].append({"ue": {"sv": "Existing"}})

    create_table(
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
    assert table_entry["columns"][0]["name"] == "Existing"


def test_create_table_rejects_overlapping_range():
    doc = _setup_doc()
    doc.get_array("sheets").insert(0, [{"sheetId": 1}])

    create_table(
        doc,
        sheet_id=1,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=0,
        ),
    )

    try:
        create_table(
            doc,
            sheet_id=1,
            table_range=GridRange(
                start_row_index=0,
                end_row_index=0,
                start_column_index=0,
                end_column_index=1,
            ),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for overlapping table range")


def test_create_table_clears_matching_basic_filter():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(
        0,
        [
            {
                "sheetId": 1,
                "basicFilter": {
                    "range": {
                        "start_row_index": 0,
                        "end_row_index": 0,
                        "start_column_index": 0,
                        "end_column_index": 0,
                    }
                },
            }
        ],
    )

    create_table(
        doc,
        sheet_id=1,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=0,
        ),
    )

    sheet_entry = sheets.get(0)
    assert sheet_entry.get("basicFilter") is None
