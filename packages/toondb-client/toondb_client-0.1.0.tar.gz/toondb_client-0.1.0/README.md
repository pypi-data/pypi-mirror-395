# ToonDB Client

[![PyPI version](https://badge.fury.io/py/toondb-client.svg)](https://badge.fury.io/py/toondb-client)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**ToonDB is an AI-native database with token-optimized output, O(|path|) lookups, built-in vector search, and durable transactions.**

Python client SDK for [ToonDB](https://github.com/toondb/toondb) - the database optimized for LLM context retrieval.

## Features

- 🚀 **Embedded Mode**: Direct FFI access to ToonDB for single-process applications
- 🔗 **IPC Mode**: Multi-process access via Unix domain sockets
- 📁 **Path-Native API**: Hierarchical data organization with O(|path|) lookups
- 💾 **ACID Transactions**: Full transaction support with snapshot isolation
- 🔍 **Range Scans**: Efficient prefix and range queries
- 🎯 **Token-Optimized**: TOON format output designed for LLM context windows

## Installation

```bash
pip install toondb-client
```

## Quick Start

### Embedded Mode (Recommended for single-process apps)

```python
from toondb import Database

# Open a database (creates if doesn't exist)
with Database.open("./my_database") as db:
    # Simple key-value operations
    db.put(b"user:123", b'{"name": "Alice", "email": "alice@example.com"}')
    value = db.get(b"user:123")
    
    # Path-native API
    db.put_path("users/alice/email", b"alice@example.com")
    email = db.get_path("users/alice/email")
    
    # Transactions
    with db.transaction() as txn:
        txn.put(b"key1", b"value1")
        txn.put(b"key2", b"value2")
        # Automatically commits on exit, or aborts on exception
```

### IPC Mode (For multi-process access)

```python
from toondb import IpcClient

# Connect to a running ToonDB IPC server
client = IpcClient.connect("/tmp/toondb.sock")

# Same API as embedded mode
client.put(b"key", b"value")
value = client.get(b"key")

# Query Builder
results = client.query("users/") \
    .limit(10) \
    .select(["name", "email"]) \
    .to_list()
```

## Use Cases

### User Session Management

```python
from toondb import Database
import json

with Database.open("./sessions") as db:
    # Store session
    session = {"user_id": "123", "token": "abc", "expires": "2024-12-31"}
    db.put(b"session:abc123", json.dumps(session).encode())
    
    # Retrieve session
    data = db.get(b"session:abc123")
    if data:
        session = json.loads(data.decode())
```

### Configuration Store

```python
from toondb import Database

with Database.open("./config") as db:
    # Hierarchical configuration
    db.put_path("api/auth/timeout", b"30")
    db.put_path("api/auth/retries", b"3")
    db.put_path("api/storage/endpoint", b"https://storage.example.com")
    
    # Read config
    timeout = db.get_path("api/auth/timeout")  # b"30"
```

### Document Storage with Indexing

```python
from toondb import Database
import json

with Database.open("./docs") as db:
    # Store document with category index
    doc = {"title": "Hello World", "category": "tutorials"}
    doc_id = "doc_001"
    
    with db.transaction() as txn:
        txn.put(f"docs:{doc_id}".encode(), json.dumps(doc).encode())
        txn.put(f"idx:category:tutorials:{doc_id}".encode(), b"1")
    
    # Query by category using prefix scan
    for key, _ in db.scan(b"idx:category:tutorials:", b"idx:category:tutorials;"):
        doc_id = key.decode().split(":")[-1]
        print(f"Found: {doc_id}")
```

## Building the Native Library

For embedded mode, you need to build the Rust library:

```bash
# Clone ToonDB
git clone https://github.com/toondb/toondb.git
cd toondb

# Build release
cargo build --release

# Set library path
export TOONDB_LIB_PATH=$(pwd)/target/release
```

## API Reference

### Database (Embedded Mode)

| Method | Description |
|--------|-------------|
| `Database.open(path)` | Open/create database |
| `put(key, value)` | Store key-value pair |
| `get(key)` | Retrieve value (None if missing) |
| `delete(key)` | Delete a key |
| `put_path(path, value)` | Store at hierarchical path |
| `get_path(path)` | Retrieve by path |
| `scan(start, end)` | Iterate key range |
| `transaction()` | Begin ACID transaction |
| `checkpoint()` | Force durability checkpoint |
| `stats()` | Get storage statistics |

### IpcClient

| Method | Description |
|--------|-------------|
| `IpcClient.connect(path)` | Connect to IPC server |
| `ping()` | Check latency |
| `query(prefix)` | Create query builder |
| `scan(prefix)` | Scan keys with prefix |
| `begin_transaction()` | Start transaction |
| `commit(txn_id)` | Commit transaction |
| `abort(txn_id)` | Abort transaction |

## Documentation

- [Full SDK Documentation](https://github.com/toondb/toondb/tree/main/toondb-python-sdk/docs)
- [Examples](https://github.com/toondb/toondb/tree/main/toondb-python-sdk/examples)
- [ToonDB Repository](https://github.com/toondb/toondb)

## Requirements

- Python 3.9+
- For embedded mode: ToonDB native library (Rust)

## License

Apache License 2.0

## Author

**Sushanth** - [GitHub](https://github.com/sushanthpy)
