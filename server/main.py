import asyncio

from common.network import Connection


async def echo_server(reader, writer):
    with Connection(reader, writer) as connection:
        while True:
            obj = await connection.recv_obj()
            await connection.send_obj(obj)


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)

    await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 5000))
