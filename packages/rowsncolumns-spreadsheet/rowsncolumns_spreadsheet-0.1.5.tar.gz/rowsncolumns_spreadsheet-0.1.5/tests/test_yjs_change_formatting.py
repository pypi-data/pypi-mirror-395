from rowsncolumns_spreadsheet.yjs import change_formatting
from tests.test_yjs_change_batch import MockYDoc


def _create_doc() -> MockYDoc:
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 10, "columnCount": 10}])
    return doc


def test_change_formatting_applies_text_format():
    doc = _create_doc()

    change_formatting(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        cell_formats={"textFormat": {"bold": True}},
    )

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    row_entry = sheet_rows.get(0)
    cell = row_entry["values"].get(0)
    assert cell is not None
    assert "uf" in cell


def test_change_formatting_replace_clears_existing_format():
    doc = _create_doc()

    change_formatting(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        cell_formats={"textFormat": {"bold": True}},
    )

    change_formatting(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        cell_formats=None,
        replace=True,
    )

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    row_entry = sheet_rows.get(0)
    cell = row_entry["values"].get(0)
    assert cell is None or "uf" not in cell


def test_change_formatting_records_recalc_for_number_format():
    doc = _create_doc()
    recalc = doc.get_array("recalcCells")

    change_formatting(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        cell_formats={"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}},
        user_id="tester",
    )

    entry = recalc.get(0)
    assert entry["userId"] == "tester"
    assert entry["patches"][0][0] == "1!A1"
