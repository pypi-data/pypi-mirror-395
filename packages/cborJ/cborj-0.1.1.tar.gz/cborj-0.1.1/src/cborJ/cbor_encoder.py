import zlib


def _cbor_encode_text(s: str) -> bytes:
    b = s.encode('utf-8')
    n = len(b)
    if n < 24:
        return bytes([0x60 | n]) + b
    elif n < 256:
        return b'\x78' + bytes([n]) + b
    elif n < 65536:
        return b'\x79' + n.to_bytes(2, 'big') + b
    elif n < 4294967296:
        return b'\x7a' + n.to_bytes(4, 'big') + b
    else:
        return b'\x7b' + n.to_bytes(8, 'big') + b


def encode(json_str: str, compress: bool = False) -> bytes:
    """
    Encode a JSON string to CBOR. 

    Note: I have not implemented all types of CBOR, yet. This only encodes JSON as a UTF-8 text string inside CBOR.

    Args:
        json_str (str): Valid JSON string.
        compress (bool): If True, compress with zlib before CBOR-encoding as byte string.

    Returns:
        bytes: CBOR-encoded data.


    Note: it is recommended to compress the JSON string before CBOR-encoding it.
    """
    if not isinstance(json_str, str):
        raise TypeError("json_str must be a string")

    if not compress:
        return _cbor_encode_text(json_str)
    else:
        compressed = zlib.compress(json_str.encode('utf-8'), level=9)
        n = len(compressed)
        if n < 24:
            header = bytes([0x40 | n])
        elif n < 256:
            header = b'\x58' + bytes([n])
        elif n < 65536:
            header = b'\x59' + n.to_bytes(2, 'big')
        elif n < 4294967296:
            header = b'\x5a' + n.to_bytes(4, 'big')
        else:
            header = b'\x5b' + n.to_bytes(8, 'big')
        return header + compressed


def show_diff(cbor_bytes: bytes):
    first = cbor_bytes[0]
    mt = first >> 5
    if mt == 3:
        length = cbor_bytes[1] if first == 0x78 else (first & 0x1F)
        print(f"[CBOR] Text string, length={length}")
    elif mt == 2:
        length = cbor_bytes[1] if first == 0x58 else (first & 0x1F)
        print(f"[CBOR] Byte string, length={length}")
    print("Hex:", cbor_bytes[:20].hex() + ("..." if len(cbor_bytes) > 20 else ""))
