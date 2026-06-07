from .exceptions import IncompleteData

def parse_buff(buf: bytes, pos:int) -> tuple[bytes | list[bytes], int]:
    if pos >= len(buf):
        raise IncompleteData
    prefix = buf[pos:pos+1]

    match prefix:
        case b"*":
            return _handle_array(buf, pos)
        case b"$":
            return _handle_bulk_string(buf, pos)
        case b"+":
            return _handle_simple_string(buf, pos)
        case b":":
            pass
        case b"_":
            pass
        case _:
            raise ValueError(f"Unknown RESP type: {prefix}")

def _handle_simple_string(buf: bytes, pos:int) -> tuple[bytes | list[bytes], int]:
    line_end = buf.find(b"\r\n", pos)
    if line_end == -1:
        raise IncompleteData
    return bytes(buf[pos+1:line_end]), line_end+2

def _handle_array(buf: bytes, pos:int) -> tuple[bytes | list[bytes], int]:
    line_end = buf.find(b"\r\n", pos)
    if line_end == -1:
        raise IncompleteData
    count = int(buf[pos+1:line_end])
    pos = line_end + 2
    elements = []
    for _ in range(count):
        child, pos = parse_buff(buf, pos)
        elements.append(child)
    return elements, pos

def _handle_bulk_string(buf: bytes, pos:int) -> tuple[bytes | list[bytes], int]:
    line_end = buf.find(b"\r\n", pos)
    if line_end == -1:
        raise IncompleteData
    length = int(buf[pos+1:line_end])
    start = line_end + 2
    end = start + length

    if len(buf) < end + 2:
        raise IncompleteData

    return bytes(buf[start:end]), end+2
