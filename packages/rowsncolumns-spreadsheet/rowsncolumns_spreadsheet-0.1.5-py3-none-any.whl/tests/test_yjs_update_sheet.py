import pytest

from rowsncolumns_spreadsheet.yjs.models import Sheet as SheetModel
from rowsncolumns_spreadsheet.yjs.update_sheet import update_sheet

from tests.test_yjs_change_batch import MockYDoc


def _setup_doc():
    doc = MockYDoc()
    doc.get_array("sheets")
    doc.get_map("sheetDataV2")
    doc.get_array("recalcCells")
    return doc


def test_update_sheet_changes_title():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "title": "Budget", "index": 0}])

    updated = update_sheet(doc, 1, SheetModel(title="Budget FY24"))

    assert updated["title"] == "Budget FY24"
    assert sheets.get(0)["title"] == "Budget FY24"


def test_update_sheet_reorders_when_index_specified():
    doc = _setup_doc()
    sheets = doc.get_array("sheets")
    sheets.insert(
        0,
        [
            {"sheetId": 1, "title": "One", "index": 0},
            {"sheetId": 2, "title": "Two", "index": 1},
        ],
    )

    update_sheet(doc, 1, SheetModel(index=1))

    assert sheets.get(0)["sheetId"] == 2
    assert sheets.get(1)["sheetId"] == 1


def test_update_sheet_missing_sheet_raises():
    doc = _setup_doc()
    with pytest.raises(ValueError):
        update_sheet(doc, 99, SheetModel(title="Missing"))
