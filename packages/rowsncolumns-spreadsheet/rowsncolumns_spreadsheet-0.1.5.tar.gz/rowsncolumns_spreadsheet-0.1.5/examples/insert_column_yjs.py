"""
Demo script showing how to call `insert_column_yjs` on a y-websocket room.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import nullcontext

from pycrdt import Doc, Array
import websockets

from rowsncolumns_spreadsheet import insert_column_yjs, delete_column_yjs
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

        sheets_array = ydoc.get("sheets", type=Array)
        if sheets_array is None:
            raise RuntimeError("Y.Doc does not contain a 'sheets' array")
        if not sheets_array:
            sheets_array.insert(0, [{"sheetId": 1, "columnCount": 5, "index": 0}])

        previous_state = ydoc.get_state()
        with doc_transaction(ydoc):
            insert_column_yjs(ydoc, 1, reference_column_index=2, num_columns=1)
            delete_column_yjs(ydoc, 1, [0])

        await client.send_doc_update(previous_state)

        sheets = ydoc.get("sheets", type=Array)
        logger.info("Updated sheets: %s", json.dumps(sheets.to_py()))

        await asyncio.sleep(1)
        await client.stop()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
