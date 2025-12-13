"""
Demo script showing how to invoke `create_sheet_yjs` (and `update_sheet_yjs`)
on a live y-websocket room.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import nullcontext
from typing import Optional

from pycrdt import Doc, Array
import websockets

from rowsncolumns_spreadsheet import create_sheet_yjs, update_sheet_yjs
from rowsncolumns_spreadsheet.yjs.models import Sheet as SheetModel
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

        previous_state = ydoc.get_state()
        logger.info("Creating sheets via create_sheet_yjs...")
        with doc_transaction(ydoc):
            first = create_sheet_yjs(
                ydoc,
                SheetModel(title="Python Budget", rowCount=500, columnCount=40),
            )
            create_sheet_yjs(ydoc, SheetModel(title="Forecast"))
            update_sheet_yjs(ydoc, first["sheetId"], SheetModel(index=1))

        await client.send_doc_update(previous_state)

        sheets_array = ydoc.get("sheets", type=Array)
        logger.info("Updated sheets: %s", json.dumps(sheets_array.to_py()))

        await asyncio.sleep(1)
        await client.stop()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
