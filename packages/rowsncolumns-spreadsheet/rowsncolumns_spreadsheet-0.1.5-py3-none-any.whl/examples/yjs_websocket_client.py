"""Utilities shared by Yjs websocket examples."""

from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Optional

import websockets
from pycrdt import Doc

logger = logging.getLogger(__name__)

MESSAGE_SYNC = 0
MESSAGE_AWARENESS = 1
MESSAGE_AUTH = 2
MESSAGE_QUERY_AWARENESS = 3

SYNC_STEP1 = 0
SYNC_STEP2 = 1
SYNC_UPDATE = 2


class VarIntEncoder:
    def __init__(self) -> None:
        self._buffer = bytearray()

    def write_var_uint(self, value: int) -> None:
        if value < 0:
            raise ValueError("VarUint cannot encode negative values")
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                self._buffer.append(byte | 0x80)
            else:
                self._buffer.append(byte)
                break

    def write_var_uint8_array(self, data: bytes) -> None:
        self.write_var_uint(len(data))
        self._buffer.extend(data)

    def write_var_string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        self.write_var_uint(len(encoded))
        self._buffer.extend(encoded)

    def to_bytes(self) -> bytes:
        return bytes(self._buffer)

    def __len__(self) -> int:
        return len(self._buffer)


class VarIntDecoder:
    def __init__(self, data: bytes) -> None:
        self._view = memoryview(data)
        self._offset = 0

    def _require(self, count: int) -> None:
        if self._offset + count > len(self._view):
            raise ValueError("Decoder buffer underflow")

    def read_var_uint(self) -> int:
        shift = 0
        value = 0
        while True:
            self._require(1)
            byte = self._view[self._offset]
            self._offset += 1
            value |= (byte & 0x7F) << shift
            if byte < 0x80:
                return value
            shift += 7
            if shift > 35:
                raise ValueError("VarUint is too big")

    def read_var_uint8_array(self) -> bytes:
        length = self.read_var_uint()
        self._require(length)
        start = self._offset
        self._offset += length
        return bytes(self._view[start:self._offset])

    def read_var_string(self) -> str:
        return self.read_var_uint8_array().decode("utf-8")


def write_sync_step1(encoder: VarIntEncoder, doc: Doc) -> None:
    encoder.write_var_uint(SYNC_STEP1)
    encoder.write_var_uint8_array(doc.get_state())


def write_sync_step2(
    encoder: VarIntEncoder, doc: Doc, encoded_state_vector: Optional[bytes] = None
) -> None:
    encoder.write_var_uint(SYNC_STEP2)
    encoder.write_var_uint8_array(doc.get_update(encoded_state_vector))


def write_update(encoder: VarIntEncoder, update: bytes) -> None:
    encoder.write_var_uint(SYNC_UPDATE)
    encoder.write_var_uint8_array(update)


def read_sync_message(
    decoder: VarIntDecoder,
    encoder: VarIntEncoder,
    doc: Doc,
) -> int:
    message_type = decoder.read_var_uint()
    if message_type == SYNC_STEP1:
        state_vector = decoder.read_var_uint8_array()
        write_sync_step2(encoder, doc, state_vector)
    elif message_type in (SYNC_STEP2, SYNC_UPDATE):
        update = decoder.read_var_uint8_array()
        doc.apply_update(update)
    else:
        raise ValueError(f"Unknown sync message type {message_type}")
    return message_type


def read_auth_message(decoder: VarIntDecoder) -> str:
    message_type = decoder.read_var_uint()
    if message_type == 0:
        return decoder.read_var_string()
    return "Unknown auth response"


@dataclass
class YWebsocketClient:
    websocket: websockets.WebSocketClientProtocol
    doc: Doc
    synced: asyncio.Event = field(default_factory=asyncio.Event)

    def __post_init__(self) -> None:
        self._listener: Optional[asyncio.Task[None]] = None

    async def start(self) -> None:
        logger.debug("Sending initial sync step 1")
        await self._send_sync_step1()
        await self._broadcast_empty_awareness()
        self._listener = asyncio.create_task(self._listen_loop())

    async def stop(self) -> None:
        if self._listener:
            self._listener.cancel()
            with suppress(asyncio.CancelledError):
                await self._listener
            self._listener = None

    async def _listen_loop(self) -> None:
        try:
            async for raw in self.websocket:
                data = raw if isinstance(raw, (bytes, bytearray)) else raw.encode("utf-8")
                response = self._handle_message(bytes(data))
                if response:
                    await self.websocket.send(response)
        except websockets.ConnectionClosed:
            logger.debug("Websocket closed")

    def _handle_message(self, data: bytes) -> Optional[bytes]:
        decoder = VarIntDecoder(data)
        message_type = decoder.read_var_uint()
        if message_type == MESSAGE_SYNC:
            encoder = VarIntEncoder()
            encoder.write_var_uint(MESSAGE_SYNC)
            sync_type = read_sync_message(decoder, encoder, self.doc)
            if sync_type == SYNC_STEP2:
                self.synced.set()
            return encoder.to_bytes() if len(encoder) > 1 else None

        if message_type == MESSAGE_AWARENESS:
            _ = decoder.read_var_uint8_array()
            return None

        if message_type == MESSAGE_QUERY_AWARENESS:
            return self._encode_empty_awareness()

        if message_type == MESSAGE_AUTH:
            reason = read_auth_message(decoder)
            logger.error("Permission denied: %s", reason)
            return None

        logger.warning("Received unknown message type: %s", message_type)
        return None

    async def _send_sync_step1(self) -> None:
        encoder = VarIntEncoder()
        encoder.write_var_uint(MESSAGE_SYNC)
        write_sync_step1(encoder, self.doc)
        await self.websocket.send(encoder.to_bytes())

    async def _broadcast_empty_awareness(self) -> None:
        await self.websocket.send(self._encode_empty_awareness())

    def _encode_empty_awareness(self) -> bytes:
        encoder = VarIntEncoder()
        encoder.write_var_uint(MESSAGE_AWARENESS)
        encoder.write_var_uint(0)
        return encoder.to_bytes()

    async def send_doc_update(self, previous_state_vector: Optional[bytes] = None) -> None:
        update = self.doc.get_update(previous_state_vector)
        if not update:
            logger.debug("No Yjs update to send")
            return
        encoder = VarIntEncoder()
        encoder.write_var_uint(MESSAGE_SYNC)
        write_update(encoder, update)
        await self.websocket.send(encoder.to_bytes())
        logger.debug("Sent Yjs update (%s bytes)", len(update))
