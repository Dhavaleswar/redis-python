import asyncio


HOST = '127.0.0.1'
PORT = 8888

async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while

async def run_server() -> None:
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())