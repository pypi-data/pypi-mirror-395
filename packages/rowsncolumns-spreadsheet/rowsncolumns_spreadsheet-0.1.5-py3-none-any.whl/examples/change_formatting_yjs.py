"""
Simple script to demonstrate calling the Python Yjs `change_formatting` helper.
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

from rowsncolumns_spreadsheet.yjs import change_formatting
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

        logger.info("Applying change_formatting...")
        previous_state = ydoc.get_state()
        with doc_transaction(ydoc):
            change_formatting(
                ydoc,
                sheet_id=1,
                ranges={
                    "start_row_index": 1,
                    "end_row_index": 2,
                    "start_column_index": 1,
                    "end_column_index": 2,
                },
                cell_formats={
                    "textFormat": {"bold": False, "fontSize": 10},
                    "wrapStrategy": "wrap",
                },
            )

        await client.send_doc_update(previous_state)

        sheet_data = ydoc.get("sheetDataV2", type=Map)
        cell_xfs = ydoc.get("cellXfs", type=Map)
        logger.info("Updated sheetDataV2: %s", json.dumps(sheet_data.to_py()))
        logger.info("CellXfs patches: %s", json.dumps(cell_xfs.to_py()))

        await asyncio.sleep(1)
        await client.stop()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
