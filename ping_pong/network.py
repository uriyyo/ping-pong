import pickle
from asyncio import (
    create_task,
    Event,
    open_connection,
    Queue,
    sleep,
    start_server,
    StreamReader,
    StreamWriter,
)
from dataclasses import dataclass
from typing import Any

from ping_pong.models import (
    ClientType,
    Game,
)

BYTES_SIZE = 32
BYTES_ORDER = "big"


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


class SyncQueue(Queue):
    async def put(self, item):
        await super().put(item)
        await sleep(0)


async def create_connection(
        game: Game,
        client_type: ClientType,
        host: str,
        port: int,
):
    updates_queue = SyncQueue()
    connected = Event()

    async def start_updaters(conn: Connection):
        async def recv():
            while True:
                c = await conn.recv_obj()
                print(c)
                c(game)

        async def send():
            while True:
                c = await updates_queue.get()
                await conn.send_obj(c)

        create_task(recv())
        create_task(send())
        connected.set()

    if client_type == ClientType.SERVER:
        server_task = create_task(server(host, port, start_updaters))
        await connected.wait()

        server_task.cancel()
    else:
        connection = await Connection.create(host, port)
        create_task(start_updaters(connection))

        await connected.wait()

    return updates_queue
