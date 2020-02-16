import logging
import pickle
from asyncio import (
    Event,
    Queue,
    StreamReader,
    StreamWriter,
    create_task,
    open_connection,
    sleep,
    start_server,
)
from dataclasses import dataclass
from enum import Enum
from typing import Any

BYTES_SIZE = 32
BYTES_ORDER = "big"

logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    SERVER = "server"
    CLIENT = "client"


@dataclass
class Connection:
    reader: StreamReader
    writer: StreamWriter

    @classmethod
    async def create(cls, host: str, port: int) -> "Connection":
        reader, writer = await open_connection(host, port)

        return cls(reader, writer)

    async def send_obj(self, obj: Any):
        data = pickle.dumps(obj)

        data_size = len(data).to_bytes(BYTES_SIZE, BYTES_ORDER)

        logger.debug(f"Send {len(data)} bytes {data!r}")

        self.writer.write(data_size)
        self.writer.write(data)

    async def recv_obj(self) -> Any:
        size = int.from_bytes(await self.reader.readexactly(BYTES_SIZE), BYTES_ORDER)
        data = await self.reader.readexactly(size)

        return pickle.loads(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()


async def server(host, port, handler):
    async def callback(reader, writer):
        await handler(Connection(reader, writer))

    s = await start_server(callback, host, port)
    await s.serve_forever()


class AsyncQueue(Queue):
    async def put(self, item):
        await super().put(item)
        await sleep(0)


async def connect(obj: Any, client_type: ConnectionType, host: str, port: int):
    if client_type == ConnectionType.CLIENT:
        logger.info(f"Connect to {host}:{port}")
    else:
        logger.info(f"Serve on {host}:{port}")

    updates_queue = AsyncQueue()
    connected = Event()

    async def start_updaters(conn: Connection):
        async def recv():
            while True:
                c = await conn.recv_obj()
                logger.info(f"Receive command: {c}")

                c(obj)

        async def send():
            while True:
                c = await updates_queue.get()
                logger.info(f"Send command: {c}")

                await conn.send_obj(c)

        create_task(recv())
        create_task(send())

        connected.set()

    if client_type == ConnectionType.SERVER:
        server_task = create_task(server(host, port, start_updaters))
        await connected.wait()

        server_task.cancel()
    else:
        connection = await Connection.create(host, port)
        create_task(start_updaters(connection))

        await connected.wait()

    return updates_queue


__all__ = ["connect", "Connection", "ConnectionType"]
