import pickle
from asyncio import StreamWriter, StreamReader, open_connection
from dataclasses import dataclass
from typing import Any

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
