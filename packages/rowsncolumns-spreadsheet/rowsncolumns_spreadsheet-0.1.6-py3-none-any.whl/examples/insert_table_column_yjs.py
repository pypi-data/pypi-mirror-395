"""
Demo script showing how to call `insert_table_column_yjs` on a y-websocket room.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import nullcontext
from typing import Any, Dict

from pycrdt import Doc, Array, Map
import websockets

from rowsncolumns_spreadsheet import insert_table_column_yjs
from yjs_websocket_client import YWebsocketClient


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def doc_transaction(doc: Doc):
    begin_txn = getattr(doc, "begin_transaction", None)
    if callable(begin_txn):
        return begin_txn()
    txn = getattr(doc, "transaction", None)
    if callable(txn):
        return txn()
    return nullcontext()


def ensure_sample_table(doc: Doc) -> Dict[str, Any]:
    tables = doc.get("tables", type=Array)
    if tables.length():
        return tables.get(0)

    sheets = doc.get("sheets", type=Array)
    if not sheets.length():
        sheets.insert(0, [{"sheetId": 1, "rowCount": 20, "columnCount": 20}])

    sheet_data = doc.get("sheetDataV2", type=Map)
    sheet_data.set(
        "1",
        [
            {"values": [{"ue": {"sv": "Header"}, "ev": {"sv": "Header"}, "fv": "Header"}]},
            {"values": [{"ue": {"sv": "Value"}, "ev": {"sv": "Value"}}]},
        ],
    )

    table_entry = {
        "id": "sample-table",
        "sheetId": 1,
        "columns": [{"name": "Sample Column"}],
        "range": {
            "startRowIndex": 0,
            "endRowIndex": 1,
            "startColumnIndex": 0,
            "endColumnIndex": 0,
        },
        "headerRow": True,
    }
    tables.insert(0, [table_entry])
    return table_entry


async def main() -> None:
    room = os.environ.get("YSPREADSHEET_ROOM", "y-spreadsheet-demo")
    url = os.environ.get("YSPREADSHEET_WS_URL", "ws://localhost:1234")

    logger.info("Connecting to %s/%s", url, room)
    ydoc = Doc()
    ydoc.get("tables", type=Array)
    ydoc.get("sheetDataV2", type=Map)
    ydoc.get("recalcCells", type=Array)
    ydoc.get("cellXfs", type=Map)
    ydoc.get("sheets", type=Array)

    async with websockets.connect(f"{url}/{room}") as websocket:
        client = YWebsocketClient(websocket, ydoc)
        await client.start()

        try:
            await asyncio.wait_for(client.synced.wait(), timeout=5)
            logger.info("Initial Yjs sync completed")
        except asyncio.TimeoutError:
            logger.warning("Timed out waiting for initial sync, continuing anyway")

        table = ensure_sample_table(ydoc)

        previous_state = ydoc.get_state()
        with doc_transaction(ydoc):
            insert_table_column_yjs(
                ydoc,
                table_id=table["id"],
                dimension_index=0,
                direction="right",
            )

        await client.send_doc_update(previous_state)

        tables = ydoc.get("tables", type=Array)
        logger.info("Updated tables: %s", json.dumps(tables.to_py(), indent=2))

        await asyncio.sleep(1)
        await client.stop()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
