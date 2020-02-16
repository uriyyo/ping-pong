import logging
import pickle
import socket
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Thread
from types import TracebackType
from typing import TYPE_CHECKING, Any, NoReturn, Optional, Type

if TYPE_CHECKING:
    from .commands import CommandQueue

logger = logging.getLogger(__name__)

BYTES_SIZE: int = 32
BYTES_ORDER: str = "big"


class ConnectionType(Enum):
    SERVER = "server"
    CLIENT = "client"


@dataclass
class Connection:
    sock: "socket.socket"

    @classmethod
    def connect(cls, host: "str", port: "int") -> "Connection":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        return cls(s)

    @classmethod
    def accept(cls, host: "str", port: "int") -> "Connection":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with sock:
            sock.bind((host, port))
            sock.listen()
            s, _ = sock.accept()

            return Connection(s)

    def send_obj(self, obj: "Any") -> None:
        data = pickle.dumps(obj)

        data_size = len(data).to_bytes(BYTES_SIZE, BYTES_ORDER)

        logger.debug(f"Send {len(data)} bytes {data!r}")

        self.sock.send(data_size)
        self.sock.send(data)

    def recv_obj(self) -> "Any":
        size = int.from_bytes(self.sock.recv(BYTES_SIZE), BYTES_ORDER)
        data = self.sock.recv(size)

        return pickle.loads(data)

    def __enter__(self) -> "Connection":
        return self

    def __exit__(
        self, exc_type: "Type[Exception]", exc_val: "Exception", exc_tb: "TracebackType"
    ) -> None:
        self.sock.close()


def connect(
    obj: "Any",
    client_type: "ConnectionType",
    host: "str",
    port: "int",
    updates_queue: "Optional[CommandQueue]" = None,
) -> "CommandQueue":
    if client_type == ConnectionType.CLIENT:
        logger.info(f"Connect to {host}:{port}")
    else:
        logger.info(f"Serve on {host}:{port}")

    def start_updaters(conn: "Connection", queue: "CommandQueue") -> None:
        def recv() -> NoReturn:
            while True:
                c = conn.recv_obj()
                logger.info(f"Receive command: {c}")
                try:
                    c(obj)
                except Exception as e:
                    logger.error("Exception during command execution", exc_info=e)

        def send() -> NoReturn:
            while True:
                c = queue.get()
                logger.info(f"Send command: {c}")

                try:
                    conn.send_obj(c)
                except Exception as e:
                    logger.error("Exception during object sending", exc_info=e)

        threads = [
            Thread(name="Receiver", target=recv),
            Thread(name="Sender", target=send),
        ]

        for t in threads:
            t.daemon = True
            t.start()

    if client_type == ConnectionType.SERVER:
        conn = Connection.accept(host, port)
    else:
        conn = Connection.connect(host, port)

    if updates_queue is None:
        updates_queue = Queue()

    start_updaters(conn, updates_queue)

    return updates_queue


__all__ = ["connect", "Connection", "ConnectionType"]
