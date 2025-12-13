# b64fx

`b64fx` is a Python library for encoding and decoding data in various base formats with optional compression support. It provides both synchronous and asynchronous APIs for efficient processing of data.

## Features

- Encode/decode with Base16, Base32, Base32hex, Base64, Base85, Ascii85, and Z85.
- URL-safe Base64 encoding and decoding.
- Optional LZ4 compression/decompression for efficient storage.
- Async file encoding/decoding for handling large data without blocking.
- Compatible with Python 3.8+.

## Installation

### From PyPI (if uploaded)
```bash
pip install b64fx

Usage

All-in-one example:

import asyncio
import b64fx

# Original data
data = "Hello, world! This is a test string."
print("Original:", data)

# ===== Synchronous compression + Base64 =====
encoded = b64fx.encz(data)
print("Compressed + Encoded:", encoded)

decoded = b64fx.decz(encoded)
print("Decoded + Decompressed:", decoded.decode('utf-8'))

# ===== Base Encodings =====
raw_bytes = data.encode('utf-8')

# Base64
b64 = b64fx.standard_b64encode(raw_bytes)
print("Base64:", b64)
print("Base64 Decoded:", b64fx.standard_b64decode(b64))

# URL-safe Base64
url_b64 = b64fx.urlsafe_b64encode(raw_bytes)
print("URL-safe Base64:", url_b64)
print("URL-safe Base64 Decoded:", b64fx.urlsafe_b64decode(url_b64))

# Base32
b32 = b64fx.b32encode(raw_bytes)
print("Base32:", b32)
print("Base32 Decoded:", b64fx.b32decode(b32))

# Base32hex
b32hex = b64fx.b32hexencode(raw_bytes)
print("Base32hex:", b32hex)
print("Base32hex Decoded:", b64fx.b32hexdecode(b32hex))

# Base85 / Ascii85 / Z85
b85 = b64fx.b85encode(raw_bytes)
print("Base85:", b85)
print("Base85 Decoded:", b64fx.b85decode(b85))

a85 = b64fx.a85encode(raw_bytes)
print("Ascii85:", a85)
print("Ascii85 Decoded:", b64fx.a85decode(a85))

z85 = b64fx.z85encode(raw_bytes)
print("Z85:", z85)
print("Z85 Decoded:", b64fx.z85decode(z85))
