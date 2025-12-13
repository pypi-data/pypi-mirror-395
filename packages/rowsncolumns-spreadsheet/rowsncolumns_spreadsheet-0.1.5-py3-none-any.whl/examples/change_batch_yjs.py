"""
Simple script to demonstrate calling the Python Yjs `change_batch` helper.

This script connects to a running `y-websocket` server (default ws://localhost:1234),
waits for the initial sync, applies `change_batch`, and streams the resulting Yjs
update back to the server so every connected client observes the change.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import nullcontext
from typing import Optional

from pycrdt import Doc, Map, Array
import websockets

from rowsncolumns_spreadsheet.yjs import change_batch
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
    room = os.environ.get("YSPREADSHEET_ROOM", "y-spreadsheet-demo")
    url = os.environ.get("YSPREADSHEET_WS_URL", "ws://localhost:1234")

    logger.info("Connecting to %s/%s", url, room)
    ydoc = Doc()

    async with websockets.connect(f"{url}/{room}") as websocket:
        client = YWebsocketClient(websocket, ydoc)
        await client.start()

        try:
            await asyncio.wait_for(client.synced.wait(), timeout=5)
            logger.info("Initial Yjs sync completed")
        except asyncio.TimeoutError:
            logger.warning("Timed out waiting for initial sync, continuing anyway")

        logger.info("Applying change_batch...")
        previous_state = ydoc.get_state()
        with doc_transaction(ydoc):
            change_batch(
                ydoc,
                sheet_id=1,
                ranges={
                    "start_row_index": 1,
                    "end_row_index": 2,
                    "start_column_index": 1,
                    "end_column_index": 2,
                },
                values=[
                    ["Language", "Columns1"],
                    ["HelloPython", "HelloWorld"],
                ],
            )

        await client.send_doc_update(previous_state)

        ymap = ydoc.get("sheetDataV2", type=Map)
        tables = ydoc.get("tables", type=Array)
        recalc_cells = ydoc.get('recalcCells', type=Array)
        logger.info("Updated Y.Doc sheetDataV2: %s", json.dumps(ymap.to_py()))
        logger.info("Updated CellXfs: %s", json.dumps(tables.to_py()))
        logger.info("Updated recalc_cells: %s", json.dumps(recalc_cells.to_py()))

        await asyncio.sleep(1)
        await client.stop()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
