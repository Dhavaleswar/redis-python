import socket
import selectors

from .sels import SEL
from .handle_buff import process_buff


def accept_connection(sock: socket.socket, mask: int) -> None:
    conn, addr = sock.accept()
    print(f"accepted connection from {addr}")
    conn.setblocking(False)
    SEL.register(conn, selectors.EVENT_READ, process_buff)


def run_server(host: str, port: int):
    server_socket = socket.create_server((host, port), reuse_port=True)
    server_socket.setblocking(False)

    SEL.register(
        server_socket,
        selectors.EVENT_READ,
        accept_connection
    )

    try:
        while True:
            events = SEL.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print("Shutting down...")
        server_socket.close()


if __name__ == "__main__":
    run_server("localhost", 6379)
