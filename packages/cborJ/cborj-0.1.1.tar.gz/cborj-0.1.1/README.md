# Cbor-J
Lightweight pure-Python library to encode/decode JSON strings to/from CBOR — with optional zlib compression.

Perfect for reducing storage size of large JSON files.

## Features

- Pure Python, no dependencies
- Simple API: `encode(json_str, compress=False) → bytes`, `decode(bytes, compress=False) → str`
- Optional zlib compression (like EU Digital COVID Certificate format, *without* signing/Base45)
- Includes CLI tool

## Installation

```bash
pip install cborJ
```

## Usage

```python
import json

from cborJ import decode, encode

json_data = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
        "isMember": True,
        "favorites": {
            "color": "blue",
            "food": "pizza"
        },
        "shoppingList": ["eggs", "milk", "bread"]
    }
json_str = json.dumps(json_data)


print("--------------Encoding--------------")

# Encode → (no compression)
encoded = encode(json_str, compress=False)
print(f"Original: {json_str.encode()}\n")
print(f"CBOR:     {encoded}\n")

# Encode → (with compression)
encoded_zip = encode(json_str, compress=True)
print(f"Original: {json_str.encode()}\n")
print(f"CBOR:     {encoded_zip}\n")

print("--------------Decoding--------------")

# Decode → (with compression)
decoded_zip = decode(encoded_zip, compress=True)
print(f"CBOR:     {encoded_zip}\n")
print(f"Original: {decoded_zip.encode()}\n")
```

## CLI Tool

### Encode JSON file to CBOR (stdout)
```bash
cborJ encode data.json > data.cbor
```

### Decode back
```bash
cborJ decode data.cbor > data.json
```

### With compression
```bash
cborJ encode --compress big.json > big.cbor
```
