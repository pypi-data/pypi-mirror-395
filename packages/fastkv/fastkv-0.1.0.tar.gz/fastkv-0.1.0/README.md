# FastKV

**A high-performance, file-system based key-value database for Python**

FastKV is a pure-Python, high-performance key-value database designed for durability, speed, and simplicity. It implements a log-structured merge-tree (LSM-tree) architecture similar to RocksDB/LevelDB, optimized for SSD storage with asynchronous compaction, bloom filters, and configurable durability modes.

## Features

- **High Performance**: Optimized for write-heavy workloads with sequential I/O patterns
- **ACID Compliant**: Write-ahead logging (WAL) ensures crash recovery
- **Multiple Durability Modes**: Choose between speed and safety
- **Asynchronous Operations**: Built-in async API for non-blocking I/O
- **Efficient Storage**: SSTable-based storage with Bloom filters and compression support
- **Memory Efficient**: Configurable memtable sizes and background compaction
- **Thread-Safe**: Designed for concurrent access
- **Zero Dependencies**: Pure Python implementation (optional msgpack for better performance)
- **Command Line Interface**: Built-in CLI for database operations

## Installation

```bash
pip install fastkv
```

## Quick Start

### Synchronous API

```python
from fastkv import FastKV

# Open a database
db = FastKV("./my_database")

# Store data
db.put("user:1001", {"name": "Alice", "age": 30, "email": "alice@example.com"})
db.put("user:1002", {"name": "Bob", "age": 25})
db.put("config:theme", "dark")
db.put("counter:visits", 42)

# Retrieve data
user = db.get("user:1001")
print(f"User: {user}")  # {"name": "Alice", "age": 30, "email": "alice@example.com"}

# Scan with prefix
users = db.scan("user:")
for key, value in users:
    print(f"{key}: {value}")

# Batch operations
db.batch_put([
    ("order:001", {"item": "Book", "price": 29.99}),
    ("order:002", {"item": "Pen", "price": 1.99})
])

# Delete keys
db.delete("config:theme")

# Get statistics
stats = db.stats()
print(f"Total keys: {stats['total_keys']}")
print(f"Memtable size: {stats['memtable_size']} bytes")

# Close the database
db.close()
```

### Asynchronous API

```python
import asyncio
from fastkv import AsyncFastKV

async def main():
    async with AsyncFastKV("./my_async_db") as db:
        # All operations are asynchronous
        await db.put("async_key", "async_value")
        value = await db.get("async_key")
        print(f"Got: {value}")
        
        # Batch operations
        await db.batch_put([("a", 1), ("b", 2), ("c", 3)])
        
        # Scan
        results = await db.scan(prefix="", limit=10)
        for key, val in results:
            print(f"{key}: {val}")

asyncio.run(main())
```

## Command Line Interface (CLI)

FastKV provides a comprehensive command-line interface accessible via `python -m fastkv`. This allows you to run tests, benchmarks, and use an interactive shell without writing code.

### Basic Usage

```bash
# Run tests
python -m fastkv test

# Run performance benchmarks
python -m fastkv benchmark

# Start interactive shell
python -m fastkv shell --path ./my_database

# Run benchmark with custom database path
python -m fastkv benchmark --path ./benchmark_data

# Start shell with specific database location
python -m fastkv shell --path /var/lib/fastkv/app_data
```

### Interactive Shell

The interactive shell provides a REPL (Read-Eval-Print Loop) interface for database operations:

```bash
python -m fastkv shell --path ./my_database
```

#### Shell Commands:

| Command | Syntax | Description | Example |
|---------|--------|-------------|---------|
| **put** | `put <key> <value>` | Store a key-value pair | `put user:1001 '{"name": "Alice", "age": 30}'` |
| **get** | `get <key>` | Retrieve value by key | `get user:1001` |
| **delete** | `delete <key>` | Remove a key | `delete user:1001` |
| **scan** | `scan [prefix] [limit]` | Scan keys with prefix | `scan user: 10` |
| **stats** | `stats` | Show database statistics | `stats` |
| **bulk** | `bulk <filename.json>` | Bulk load from JSON file | `bulk data.json` |
| **exit** | `exit` or `quit` | Exit the shell | `exit` |

#### Interactive Shell Examples:

```bash
# Start the shell
$ python -m fastkv shell --path ./testdb
Database opened at ./testdb
fastkv> 

# Store data
fastkv> put config:app_name "MyApp"
OK

fastkv> put user:1001 '{"name": "Alice", "active": true}'
OK

# Retrieve data
fastkv> get user:1001
{
  "name": "Alice",
  "active": true
}

# Scan with prefix
fastkv> scan user:
user:1001: {"name": "Alice", "active": true}
Total: 1 items

# Scan with limit
fastkv> scan "" 5
config:app_name: "MyApp"
user:1001: {"name": "Alice", "active": true}
Total: 2 items

# View statistics
fastkv> stats
{
  "memtable_size": 2048,
  "memtable_keys": 2,
  "immutable_memtables": 0,
  "immutable_keys": 0,
  "total_sstables": 0,
  "total_keys": 2,
  "sstable_stats": {},
  "seq_num": 2
}

# Bulk load from JSON file
fastkv> bulk data.json
Loaded 1000 items

# Exit shell
fastkv> exit
Goodbye!
Database closed
```

### JSON Bulk Loading

Create a JSON file for bulk loading:

```json
[
  ["key1", "value1"],
  ["key2", {"nested": "data"}],
  ["key3", [1, 2, 3]],
  ["user:1001", {"name": "Alice", "age": 30}],
  ["user:1002", {"name": "Bob", "age": 25}]
]
```

Then load it:
```bash
python -m fastkv shell --path ./mydb
fastkv> bulk data.json
Loaded 5 items
```

### Benchmark Mode

The benchmark mode tests the database performance:

```bash
$ python -m fastkv benchmark
Running benchmark...
```

### Test Mode

Run the built-in test suite:

```bash
$ python -m fastkv test
Running FastKV tests...
✓ Test 1 passed: Basic operations
✓ Test 2 passed: Crash recovery
✓ Test 3 passed: Async operations

All tests passed! ✅
```

## Configuration

### Database Options

```python
from fastkv import FastKV, DurabilityMode

# Custom configuration
db = FastKV(
    db_path="./my_data",
    durability=DurabilityMode.SYNC,  # SYNC, BACKGROUND, or NONE
    max_memtable_size=128 * 1024 * 1024  # 128MB memtable
)
```

### Durability Modes

- `DurabilityMode.NONE`: Maximum performance, data may be lost on crash
- `DurabilityMode.BACKGROUND` (default): Good balance, async fsync
- `DurabilityMode.SYNC`: Maximum durability, sync before return

### Value Encoding

```python
from fastkv import ValueEncoding

# Different serialization formats (default: JSON)
db.put("key", data, encoding=ValueEncoding.JSON)
db.put("key", data, encoding=ValueEncoding.MSGPACK)  # Requires msgpack
db.put("key", data, encoding=ValueEncoding.PICKLE)
```

## Advanced Usage

### Bulk Loading via Python

For initial data import, use bulk loading for better performance:

```python
# Generate sample data
items = [(f"item:{i}", {"id": i, "data": "x" * 100}) for i in range(100000)]

# Bulk load (bypasses WAL for speed)
db.bulk_load(items)
```

### Manual Compaction

Compaction runs automatically in the background, but you can monitor it:

```python
# The database automatically schedules compaction
# when certain thresholds are reached
stats = db.stats()
print(stats['sstable_stats'])  # View SSTable distribution
```

### Custom Serialization

```python
import pickle

class CustomObject:
    def __init__(self, data):
        self.data = data

obj = CustomObject("test")

# Store custom objects
db.put("custom", obj, encoding=ValueEncoding.PICKLE)

# Retrieve
retrieved = db.get("custom")
print(type(retrieved))  # <class '__main__.CustomObject'>
```

## Architecture

FastKV implements an LSM-tree storage engine with these components:

### 1. **Write-Ahead Log (WAL)**
   - Ensures durability and crash recovery
   - Segmented files with rotation
   - Configurable sync modes

### 2. **MemTable**
   - In-memory sorted key-value store
   - Automatically flushed to disk when full
   - Thread-safe with bisect-based ordering

### 3. **Sorted String Tables (SSTables)**
   - Immutable sorted files on disk
   - Block-based storage with Bloom filters
   - Multi-level compaction strategy

### 4. **Compaction**
   - Background merging of SSTables
   - Level-based compaction policy
   - Configurable parallelism

## Performance Tips

1. **Use appropriate durability**: `BACKGROUND` mode offers good balance for most use cases
2. **Batch operations**: Use `batch_put()` for multiple writes
3. **Bulk load initial data**: Use `bulk_load()` for initial imports
4. **Monitor memory usage**: Adjust `max_memtable_size` based on available RAM
5. **Use msgpack**: Install msgpack for faster serialization
6. **Use CLI for quick operations**: The shell is perfect for debugging and administration

## API Reference

### FastKV Class

```python
class FastKV:
    def __init__(self, db_path: Union[str, Path], 
                 durability: DurabilityMode = DurabilityMode.BACKGROUND,
                 max_memtable_size: int = 64 * 1024 * 1024)
    
    def put(self, key: str, value: Any, 
            encoding: ValueEncoding = ValueEncoding.JSON) -> None
    
    def get(self, key: str) -> Optional[Any]
    
    def delete(self, key: str) -> None
    
    def batch_put(self, items: List[Tuple[str, Any]]) -> None
    
    def scan(self, prefix: Optional[str] = None, 
             limit: Optional[int] = None) -> List[Tuple[str, Any]]
    
    def stats(self) -> Dict[str, Any]
    
    def bulk_load(self, items: List[Tuple[str, Any]]) -> None
    
    def close(self) -> None
```

### AsyncFastKV Class

```python
class AsyncFastKV:
    async def open(self) -> None
    async def put(self, key: str, value: Any) -> None
    async def get(self, key: str) -> Optional[Any]
    async def delete(self, key: str) -> None
    async def batch_put(self, items: List[Tuple[str, Any]]) -> None
    async def scan(self, prefix: Optional[str] = None, 
                   limit: Optional[int] = None) -> List[Tuple[str, Any]]
    async def stats(self) -> Dict[str, Any]
    async def bulk_load(self, items: List[Tuple[str, Any]]) -> None
    async def close(self) -> None
```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/arifchy369/FastKV.git
cd fastkv

# Install in development mode
pip install -e .

# Run tests
python -m fastkv test

# Run benchmarks
python -m fastkv benchmark

# Start interactive shell
python -m fastkv shell
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/arifchy369/FastKV/issues)
- **Author**: Arif Chowdhury ([@arifchy369](https://github.com/arifchy369))

## Roadmap

- [ ] Snapshot and backup functionality
- [ ] Transaction support
- [ ] Replication and clustering
- [ ] More compression algorithms (LZ4, Zstd)
- [ ] Query language support
- [ ] TTL (time-to-live) for keys
- [ ] Windows performance optimizations

---

**FastKV** - Fast, durable key-value storage for Python applications.