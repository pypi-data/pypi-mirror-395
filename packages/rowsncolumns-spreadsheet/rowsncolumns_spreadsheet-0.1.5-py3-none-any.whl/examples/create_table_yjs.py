"""
Simple script to demonstrate calling the Python Yjs `create_table` helper.

Run this script from the repo root (or `python/` directory). It creates an in-memory
pycrdt Doc, seeds the required collections, invokes
`rowsncolumns_spreadsheet.yjs.create_table`, and prints the resulting table entry and
header row values.
"""

from __future__ import annotations

from typing import Optional

from pycrdt import Doc, Map, Array
import websockets
import asyncio
import logging
import os
import json
from contextlib import nullcontext

from rowsncolumns_spreadsheet.yjs import create_table
from rowsncolumns_spreadsheet.types import GridRange
from yjs_websocket_client import YWebsocketClient

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def doc_transaction(doc: Doc):
    begin_txn = getattr(doc, "begin_transaction", None)
    if callable(begin_txn):
        return begin_txn()
    txn = getattr(doc, "transaction", None)
    if callable(txn):
        return txn()
    return nullcontext()

async def main() -> None:
    ydoc = Doc()
    ydoc.get("tables", type=Array)
    ydoc.get("sheets", type=Array).insert(0, [{"sheetId": 1, "rowCount": 100, "columnCount": 26}])
    ydoc.get("sheetDataV2", type=Map)
    ydoc.get("cellXfs", type=Map)
    ydoc.get("recalcCells", type=Array)
    room = os.environ.get("YSPREADSHEET_ROOM", "y-spreadsheet-demo")
    url = os.environ.get("YSPREADSHEET_WS_URL", "ws://localhost:1234")
    async with websockets.connect(f"{url}/{room}") as websocket:
        client = YWebsocketClient(websocket, ydoc)
        await client.start()

        try:
            await asyncio.wait_for(client.synced.wait(), timeout=5)
            logger.info("Initial Yjs sync completed")
        except asyncio.TimeoutError:
            logger.warning("Timed out waiting for initial sync, continuing anyway")

        logger.info("Creating table...")
        previous_state = ydoc.get_state()
        with doc_transaction(ydoc):
            create_table(
                ydoc,
                sheet_id=1,
                table_range=GridRange(
                    start_row_index=1,
                    end_row_index=2,
                    start_column_index=1,
                    end_column_index=2,
                ),
                theme="TableStyleLight1",
            )

        await client.send_doc_update(previous_state)

        tables = ydoc.get("tables", type=Array)
        logger.info("Updated tables: %s", json.dumps(tables.to_py()))

        await asyncio.sleep(1)
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
