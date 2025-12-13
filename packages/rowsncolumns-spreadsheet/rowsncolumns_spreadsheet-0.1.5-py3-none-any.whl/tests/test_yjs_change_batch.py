from typing import Any, Dict

from rowsncolumns_spreadsheet.sheet_cell import SheetCell
from rowsncolumns_spreadsheet.yjs import change_batch


class MockYArray:
    def __init__(self):
        self._items = []

    def length(self):
        return len(self._items)

    def get(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def insert(self, index, values):
        for offset, value in enumerate(values):
            self._items.insert(index + offset, value)

    def delete(self, index, length):
        del self._items[index : index + length]
    
    def __len__(self):
        return len(self._items)


class MockYMap:
    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value


class MockYDoc:
    def __init__(self):
        self._arrays = {}
        self._maps = {}

    def get(self, name, type=None):
        if type is MockYArray:
            return self.get_array(name)
        if type is MockYMap:
            return self.get_map(name)
        raise ValueError("Unsupported type")

    def get_array(self, name):
        if name not in self._arrays:
            self._arrays[name] = MockYArray()
        return self._arrays[name]

    def get_map(self, name):
        if name not in self._maps:
            self._maps[name] = MockYMap()
        return self._maps[name]


def test_change_batch_updates_sheet_data():
    doc = MockYDoc()
    doc.get_array("tables")  # Ensure tables array exists
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "columnCount": 5}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 1,
            "endRowIndex": 1,
            "startColumnIndex": 1,
            "endColumnIndex": 1,
        },
        values=[["Hello"]],
    )

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    assert sheet_rows is not None
    row_entry = sheet_rows.get(1)
    assert row_entry is not None
    values = row_entry["values"]
    cell = values.get(1)
    assert cell["ue"]["sv"] == "Hello"
    assert cell["ev"]["sv"] == "Hello"


def test_change_batch_updates_table_headers():
    doc = MockYDoc()
    tables = doc.get_array("tables")
    doc.get_array("recalcCells")
    tables.insert(
        0,
        [
            {
                "sheetId": 1,
                "range": {
                    "startRowIndex": 2,
                    "endRowIndex": 5,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4,
                },
                "columns": [{"name": "First"}, {"name": "Second"}],
            }
        ],
    )
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 10, "columnCount": 10}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 2,
            "endRowIndex": 2,
            "startColumnIndex": 3,
            "endColumnIndex": 3,
        },
        values=[["Updated"]],
    )

    updated_table = tables.get(0)
    assert updated_table["columns"][0]["name"] == "Updated"


def test_change_batch_expands_sheet_bounds():
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "columnCount": 5}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 20,
            "endRowIndex": 20,
            "startColumnIndex": 40,
            "endColumnIndex": 40,
        },
        values="Value",
    )

    updated_sheet = sheets.get(0)
    assert updated_sheet["rowCount"] >= 20
    assert updated_sheet["columnCount"] >= 40


def test_change_batch_emits_recalc_cells():
    doc = MockYDoc()
    doc.get_array("tables")
    recalc = doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "columnCount": 5}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        values=[["X"]],
        user_id="tester",
    )

    entry = recalc.get(0)
    assert entry["userId"] == "tester"
    assert entry["patches"][0][0] == "1!A1"
    assert entry["patches"][0][1]["rowIndex"] == 0


def test_change_batch_registers_cell_xfs():
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 5, "columnCount": 5}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "startRowIndex": 0,
            "endRowIndex": 0,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        values=[["styled"]],
        formatting=[[{"textFormat": {"bold": True}}]],
    )

    cell_xfs = doc.get_map("cellXfs")
    assert len(cell_xfs._store) == 2

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    row_entry = sheet_rows.get(0)
    values = row_entry["values"]
    cell = values.get(0)

    uf_sid = cell["uf"]["sid"]
    ef_sid = cell["ef"]["sid"]

    assert uf_sid in cell_xfs._store
    assert ef_sid in cell_xfs._store

    uf_format = cell_xfs._store[uf_sid]
    ef_format = cell_xfs._store[ef_sid]

    assert uf_format == {"textFormat": {"bold": True}}
    assert ef_format["textFormat"]["bold"] is True
    assert ef_format.get("horizontalAlignment") == "left"


def test_change_batch_handles_snake_case_range_keys():
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1, "rowCount": 1, "columnCount": 1}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={
            "start_row_index": 2,
            "end_row_index": 2,
            "start_column_index": 2,
            "end_column_index": 2,
        },
        values=[["Offset"]],
    )

    sheet_rows = doc.get_map("sheetDataV2").get("1")
    row_entry = sheet_rows.get(2)
    values = row_entry["values"]
    assert values.get(2)["ue"]["sv"] == "Offset"


def test_change_batch_upgrades_python_list_rows():
    doc = MockYDoc()
    doc.get_array("tables")
    doc.get_array("recalcCells")
    sheets = doc.get_array("sheets")
    sheets.insert(0, [{"sheetId": 1}])

    sheet_data = doc.get_map("sheetDataV2")
    sheet_data.set("1", [None, {"values": []}])

    change_batch(
        doc,
        sheet_id=1,
        ranges={"startRowIndex": 1, "endRowIndex": 1, "startColumnIndex": 1, "endColumnIndex": 1},
        values=[["ListRow"]],
    )

    sheet_rows = sheet_data.get("1")
    row_entry = sheet_rows.get(1)
    values = row_entry["values"]
    assert values.get(1)["ue"]["sv"] == "ListRow"


def test_sheet_cell_omits_default_left_alignment():
    cell = SheetCell()
    cell.set_user_entered_format("textFormat", {"bold": True})
    cell.set_user_entered_format("horizontalAlignment", "left")

    data = cell.get_cell_data()
    assert data is not None
    assert data["uf"]["textFormat"]["bold"] is True
    assert "horizontalAlignment" not in data["uf"]


def test_sheet_cell_returns_style_ids_when_registry_present():
    registry: Dict[str, Dict[str, Any]] = {}
    cell = SheetCell(cell_xfs_registry=registry)
    cell.set_user_entered_format(
        "numberFormat",
        {"type": "CURRENCY", "pattern": '"$"#,##0.0'},
    )
    cell.set_user_entered_format("horizontalAlignment", "right")

    data = cell.get_cell_data()
    assert data is not None
    assert data["uf"] == {"sid": next(iter(registry.keys()))}
    assert data["ef"] == data["uf"]
    assert any(
        fmt.get("numberFormat", {}).get("type") == "CURRENCY"
        for fmt in registry.values()
    )
