import logging
import pickle
import socket
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Thread
from typing import Any

BYTES_SIZE = 32
BYTES_ORDER = "big"

logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    SERVER = "server"
    CLIENT = "client"


@dataclass
class Connection:
    sock: socket.socket

    @classmethod
    def connect(cls, host: str, port: int) -> "Connection":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        return cls(s)

    @classmethod
    def accept(cls, host: str, port: int) -> "Connection":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with sock:
            sock.bind((host, port))
            sock.listen()
            s, _ = sock.accept()

            return Connection(s)

    def send_obj(self, obj: Any):
        data = pickle.dumps(obj)

        data_size = len(data).to_bytes(BYTES_SIZE, BYTES_ORDER)

        logger.debug(f"Send {len(data)} bytes {data!r}")

        self.sock.send(data_size)
        self.sock.send(data)

    def recv_obj(self) -> Any:
        size = int.from_bytes(self.sock.recv(BYTES_SIZE), BYTES_ORDER)
        data = self.sock.recv(size)

        return pickle.loads(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


def connect(obj: Any, client_type: ConnectionType, host: str, port: int):
    if client_type == ConnectionType.CLIENT:
        logger.info(f"Connect to {host}:{port}")
    else:
        logger.info(f"Serve on {host}:{port}")

    updates_queue = Queue()

    def start_updaters(conn: Connection):
        def recv():
            while True:
                c = conn.recv_obj()
                logger.info(f"Receive command: {c}")

                c(obj)

        def send():
            while True:
                c = updates_queue.get()
                logger.info(f"Send command: {c}")

                conn.send_obj(c)

        threads = [
            Thread(name='Receiver', target=recv),
            Thread(name='Sender', target=send),
        ]

        for t in threads:
            t.daemon = True
            t.start()

    if client_type == ConnectionType.SERVER:
        conn = Connection.accept(host, port)
    else:
        conn = Connection.connect(host, port)

    start_updaters(conn)

    return updates_queue


__all__ = ["connect", "Connection", "ConnectionType"]
