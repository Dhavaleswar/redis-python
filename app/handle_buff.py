import socket
import selectors
import time

from .sels import SEL
from .exceptions import IncompleteData
from .parser import parse_buff


data_buffer = {}
kv_store = {}
key_expires = {}


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
        if b"PING" in element[0]:
            conn.sendall(b"+PONG\r\n")
        elif b"ECHO" in element[0]:
            msg = element[1]
            conn.sendall(b"$" + str(len(msg)).encode() + b"\r\n" + msg + b"\r\n")
        elif b"SET" in element[0]:
            if len(element) > 3:
                key,value,ex_type,expiry = element[1:]
                kv_store[key] = value
                curr_time = time.perf_counter_ns()
                if ex_type == b"EX":
                    expiry = int(expiry) * (1_000_000_000)
                elif ex_type == b"PX":
                    expiry = int(expiry) * (1_000_000)

                key_expires[key] = curr_time + expiry
                conn.sendall(b"+OK\r\n")
            else:
                key,value = element[1:]
                kv_store[key] = value
                conn.sendall(b"+OK\r\n")


        elif b"GET" in element[0]:
            key = element[1]
            if key in key_expires and time.perf_counter_ns() > key_expires[key] + 1_000:
                conn.sendall(b"$-1\r\n")
            else:
                v_ = kv_store.get(key)
                conn.sendall(b"$" + str(len(v_)).encode() + b"\r\n" + v_ + b"\r\n")
        else:
            conn.sendall(b"-ERR unknown command\r\n")
