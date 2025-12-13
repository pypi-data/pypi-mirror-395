import pytest

from rowsncolumns_spreadsheet.yjs.create_new_sheet import create_sheet
from rowsncolumns_spreadsheet.yjs.models import Sheet as SheetModel

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc() -> MockYDoc:
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    return doc


def test_create_new_sheet_appends_entry():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(
        0,
        [
            {
                "sheetId": 1,
                "title": "Sheet 1",
                "rowCount": 10,
                "columnCount": 5,
                "index": 0,
            }
        ],
    )

    entry = create_sheet(doc, SheetModel(title="Budget"))

    assert entry["sheetId"] == 2
    assert entry["title"] == "Budget"
    assert len(sheets) == 2
    assert sheets.get(1)["index"] == 1


def test_create_new_sheet_deduplicates_title():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "title": "Budget", "index": 0}])

    entry = create_sheet(doc, SheetModel(title="Budget"))

    assert entry["title"] != "Budget"
    assert entry["title"].startswith("Budget")
    assert len(sheets) == 2


def test_create_new_sheet_uses_explicit_sheet_id():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 5, "title": "First", "index": 0}])

    entry = create_sheet(doc, SheetModel(sheetId=10, title="Second"))

    assert entry["sheetId"] == 10
    assert len(sheets) == 2


def test_create_new_sheet_returns_existing_when_id_conflicts():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    existing = {"sheetId": 3, "title": "Existing", "index": 0}
    sheets.insert(0, [existing])

    entry = create_sheet(doc, SheetModel(sheetId=3))

    assert entry is existing
    assert len(sheets) == 1


def test_create_new_sheet_rejects_non_numeric_id():
    doc = _setup_doc()
    with pytest.raises(ValueError):
        create_sheet(doc, SheetModel(sheetId="not-a-number"))  # type: ignore[arg-type]
