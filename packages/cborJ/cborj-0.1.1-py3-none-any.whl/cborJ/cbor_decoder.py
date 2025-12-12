import zlib
from typing import Tuple


def _cbor_decode_text(data: bytes) -> Tuple[str, int]:
    """Decode a CBOR text string (major type 3).
    
    Returns:
        (decoded_str, bytes_consumed)
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if len(data) == 0:
        raise ValueError("Empty input")

    first = data[0]
    if (first & 0xE0) != 0x60:
        raise ValueError("Not a CBOR text string (major type 3)")

    # Determine length and header size
    if first < 0x78:
        length = first & 0x1F
        header_len = 1
    elif first == 0x78:
        if len(data) < 2:
            raise ValueError("Truncated CBOR text string (missing length byte)")
        length = data[1]
        header_len = 2
    elif first == 0x79:
        if len(data) < 3:
            raise ValueError("Truncated CBOR text string (missing 2 length bytes)")
        length = int.from_bytes(data[1:3], 'big')
        header_len = 3
    elif first == 0x7A:
        if len(data) < 5:
            raise ValueError("Truncated CBOR text string (missing 4 length bytes)")
        length = int.from_bytes(data[1:5], 'big')
        header_len = 5
    elif first == 0x7B:
        if len(data) < 9:
            raise ValueError("Truncated CBOR text string (missing 8 length bytes)")
        length = int.from_bytes(data[1:9], 'big')
        header_len = 9
    else:
        raise ValueError(f"Invalid additional information: 0x{first:02x}")

    # Check if enough data is available
    if len(data) < header_len + length:
        raise ValueError(
            f"Truncated text data: expected {header_len + length} bytes, got {len(data)}"
        )

    # Extract and decode UTF-8
    text_bytes = data[header_len:header_len + length]
    try:
        text = text_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError("Invalid UTF-8 in CBOR text string") from e

    return text, header_len + length


def decode(cbor_data: bytes, compress: bool = False) -> str:
    """
    Decode CBOR data back to original JSON string.

    Args:
        cbor_data (bytes): CBOR-encoded data.
        compress (bool): Must match encoding mode.

    Returns:
        str: Original JSON string.
    """
    if not isinstance(cbor_data, bytes):
        raise TypeError("cbor_data must be bytes")
    if not cbor_data:
        raise ValueError("Empty CBOR data")

    if not compress:
        text, consumed = _cbor_decode_text(cbor_data)
        if consumed != len(cbor_data):
            raise ValueError(
                f"Extra data after CBOR item: {len(cbor_data) - consumed} bytes unused"
            )
        return text

    else:
        # Expect CBOR byte string (major type 2)
        first = cbor_data[0]
        if (first & 0xE0) != 0x40:
            raise ValueError(
                "Expected CBOR byte string (major type 2) when compress=True, "
                f"got major type {(first >> 5) & 0x7}"
            )

        # Parse length
        if first < 0x58:
            length = first & 0x1F
            header_len = 1
        elif first == 0x58:
            if len(cbor_data) < 2:
                raise ValueError("Truncated CBOR byte string (missing length byte)")
            length = cbor_data[1]
            header_len = 2
        elif first == 0x59:
            if len(cbor_data) < 3:
                raise ValueError("Truncated CBOR byte string (missing 2 length bytes)")
            length = int.from_bytes(cbor_data[1:3], 'big')
            header_len = 3
        elif first == 0x5A:
            if len(cbor_data) < 5:
                raise ValueError("Truncated CBOR byte string (missing 4 length bytes)")
            length = int.from_bytes(cbor_data[1:5], 'big')
            header_len = 5
        elif first == 0x5B:
            if len(cbor_data) < 9:
                raise ValueError("Truncated CBOR byte string (missing 8 length bytes)")
            length = int.from_bytes(cbor_data[1:9], 'big')
            header_len = 9
        else:
            raise ValueError(f"Invalid additional information for byte string: 0x{first:02x}")

        # Bounds check
        if len(cbor_data) < header_len + length:
            raise ValueError(
                f"Truncated byte data: expected {header_len + length} bytes, got {len(cbor_data)}"
            )

        compressed = cbor_data[header_len:header_len + length]
        if header_len + length != len(cbor_data):
            raise ValueError(
                f"Extra data after CBOR byte string: {len(cbor_data) - (header_len + length)} bytes unused"
            )

        # Decompress and decode
        try:
            decompressed = zlib.decompress(compressed)
        except zlib.error as e:
            raise ValueError("zlib decompression failed") from e

        try:
            return decompressed.decode('utf-8')
        except UnicodeDecodeError as e:
            raise ValueError("UTF-8 decoding failed after decompression") from e
