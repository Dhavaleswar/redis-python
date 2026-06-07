import socket
import selectors

from .sels import SEL
from .exceptions import IncompleteData
from .parser import parse_buff


data_buffer = {}
kv_store = {}


def process_buff(conn: socket.socket, mask: int) -> None:
    chunk = conn.recv(1024)

    if not chunk:
        SEL.unregister(conn)
        conn.close()
        data_buffer.pop(conn, None)
        return

    buf = data_buffer.setdefault(conn, bytearray())
    buf.extend(chunk)

    while len(buf) > 0:
        try:
            element, consumed = parse_buff(buf, 0)
            print(f"Received element: {element}, consumed {consumed} bytes")
        except IncompleteData:
            break

        del buf[:consumed]
        print("Matching elements")
        match element:
            case [b"PING"]:
                conn.sendall(b"+PONG\r\n")
            case [b"ECHO", msg]:
                conn.sendall(b"$" + str(len(msg)).encode() + b"\r\n" + msg + b"\r\n")
            case [b"SET", key, value]:
                kv_store[key] = value
                conn.sendall(b"+OK\r\n")
            case [b"GET", key]:
                v_ = kv_store.get(key)
                conn.sendall(b"$" + str(len(v_)).encode() + b"\r\n" + v_ + b"\r\n")
            case _:
                conn.sendall(b"-ERR unknown command\r\n")
