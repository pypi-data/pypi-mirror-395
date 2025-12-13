"""
Simple script to demonstrate calling the Python Yjs `update_table` helper.

This script connects to a running `y-websocket` server, waits for sync, either finds
or creates a table, updates its range, and streams the update back so other clients
see the change.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import nullcontext
from typing import Any

from pycrdt import Doc, Map, Array
import websockets

from rowsncolumns_spreadsheet.yjs import create_table, update_table
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


def ensure_table(doc: Doc, sheet_id: int) -> Dict[str, Any]:
    tables = doc.get("tables", type=Array)
    if tables.length():
        return tables.get(0)

    create_table(
        doc,
        sheet_id=sheet_id,
        table_range=GridRange(
            start_row_index=0,
            end_row_index=0,
            start_column_index=0,
            end_column_index=1,
        ),
    )
    return tables.get(0)


async def main() -> None:
    doc = Doc()
    doc.get("tables", type=Array)
    doc.get("sheetDataV2", type=Map)
    doc.get("cellXfs", type=Map)
    doc.get("recalcCells", type=Array)
    doc.get("sheets", type=Array).insert(0, [{"sheetId": 1, "rowCount": 100, "columnCount": 10}])

    room = os.environ.get("YSPREADSHEET_ROOM", "y-spreadsheet-demo")
    url = os.environ.get("YSPREADSHEET_WS_URL", "ws://localhost:1234")

    async with websockets.connect(f"{url}/{room}") as websocket:
        client = YWebsocketClient(websocket, doc)
        await client.start()

        try:
            await asyncio.wait_for(client.synced.wait(), timeout=5)
            logger.info("Initial Yjs sync completed")
        except asyncio.TimeoutError:
            logger.warning("Timed out waiting for initial sync, continuing anyway")

        previous_state = doc.get_state()
        with doc_transaction(doc):
            updated_range = GridRange(
                start_row_index=1,
                end_row_index=3,
                start_column_index=1,
                end_column_index=2,
            )

            update_table(
                doc,
                sheet_id=1,
                table_id='59b09629-720e-494b-b6e7-e10f9bc0a618',
                table_updates={
                    "range": {
                        "startRowIndex": updated_range.start_row_index,
                        "endRowIndex": updated_range.end_row_index,
                        "startColumnIndex": updated_range.start_column_index,
                        "endColumnIndex": updated_range.end_column_index,
                    }
                },
            )

        await client.send_doc_update(previous_state)

        tables = doc.get("tables", type=Array)
        logger.info("Updated tables: %s", json.dumps(tables.to_py(), indent=2))

        await asyncio.sleep(1)
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
