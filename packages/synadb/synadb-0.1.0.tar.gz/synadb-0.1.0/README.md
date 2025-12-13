# Syna Python Demos

This directory contains Python examples demonstrating Syna's Python wrapper and integrations.

## Prerequisites

### 1. Build the Syna Library

```bash
# From repository root
cargo build --release
```

### 2. Install Python Dependencies

```bash
cd demos/python
pip install -r requirements.txt
```

### 3. Set Library Path (if needed)

```bash
# Linux
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../target/release

# macOS
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:../../target/release

# Or copy the library to this directory
cp ../../target/release/libsynadb.so .  # Linux
cp ../../target/release/libsynadb.dylib .  # macOS
```

## Running Demos

```bash
cd demos/python

# Basic usage
python basic_usage.py

# NumPy integration
python numpy_integration.py

# Pandas integration
python pandas_integration.py

# Async operations
python async_operations.py

# Context manager patterns
python context_manager.py

# RL experience replay
python rl_experience_demo.py
```

## Demo Descriptions

| Demo | File | Description |
|------|------|-------------|
| Basic Usage | `basic_usage.py` | Library loading, CRUD operations, error handling |
| NumPy | `numpy_integration.py` | Zero-copy tensor extraction to numpy arrays |
| Pandas | `pandas_integration.py` | DataFrame loading and time-series indexing |
| Async | `async_operations.py` | Non-blocking operations with asyncio |
| Context Manager | `context_manager.py` | Resource management with `with` statements |
| RL Experience | `rl_experience_demo.py` | Reinforcement learning experience replay |

## Demo Details

### 1. Basic Usage (`basic_usage.py`)

Comprehensive introduction to the Python wrapper:
- Library loading and path discovery
- Database open/close patterns
- All write operations (put_float, put_int, put_text, put_bytes)
- All read operations (get_float, get_int, get_text, get_bytes)
- Delete operations and key listing
- Error handling patterns
- Database compaction
- Data persistence

### 2. NumPy Integration (`numpy_integration.py`)

ML-focused tensor operations:
- Extract history as numpy arrays
- Zero-copy when possible
- Memory efficiency comparison
- Batch operations

```python
from Syna import synadb
import numpy as np

with synadb("sensors.db") as db:
    # Store time-series data
    for temp in temperatures:
        db.put_float("sensor/temp", temp)
    
    # Extract as numpy array for ML
    tensor = db.get_history_tensor("sensor/temp")
    print(f"Shape: {tensor.shape}, dtype: {tensor.dtype}")
```

### 3. Pandas Integration (`pandas_integration.py`)

DataFrame operations:
- Load time-series into DataFrame with timestamp index
- Store DataFrame back to Syna
- Query patterns using pandas

```python
# Load to DataFrame
df = db.to_dataframe("sensor/*")

# Store from DataFrame
db.from_dataframe(df, key_prefix="data/")
```

### 4. Async Operations (`async_operations.py`)

Non-blocking database access:
- Uses `asyncio` with thread pool executor
- Concurrent async reads
- Non-blocking writes

```python
import asyncio
from Syna import synadb

async def async_write(db, key, value):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, db.put_float, key, value)
```

### 5. Context Manager (`context_manager.py`)

Resource management patterns:
- `with` statement usage
- Automatic cleanup on exception
- Nested context managers for multiple DBs

```python
# Recommended pattern
with synadb("my.db") as db:
    db.put_float("key", 3.14)
# Database automatically closed here
```

### 6. RL Experience Replay (`rl_experience_demo.py`)

Reinforcement learning patterns:
- Store experience tuples (state, action, reward, next_state)
- Efficient batch sampling
- Prioritized replay support

## Python Wrapper API

### synadb Class

```python
from Syna import synadb, SynaError

# Open database
db = synadb("my.db")

# Write operations
offset = db.put_float("key", 3.14)
offset = db.put_int("key", 42)
offset = db.put_text("key", "hello")
offset = db.put_bytes("key", b"\x00\x01\x02")

# Read operations
value = db.get_float("key")      # Optional[float]
value = db.get_int("key")        # Optional[int]
value = db.get_text("key")       # Optional[str]
value = db.get_bytes("key")      # Optional[bytes]

# History extraction (for ML)
tensor = db.get_history_tensor("key")  # np.ndarray

# Key operations
exists = db.exists("key")        # bool
keys = db.keys()                 # List[str]
db.delete("key")

# Maintenance
db.compact()
db.close()
```

### Error Handling

```python
from Syna import synadb, SynaError

try:
    with synadb("my.db") as db:
        db.put_float("key", 3.14)
except SynaError as e:
    print(f"Error {e.code}: {e.message}")
```

### Error Codes

| Code | Meaning |
|------|---------|
| 0 | Generic error |
| -1 | Database not found in registry |
| -2 | Invalid path or UTF-8 |
| -3 | I/O error |
| -4 | Serialization error |
| -5 | Key not found |
| -6 | Type mismatch |
| -7 | Empty key not allowed |
| -8 | Key too long |
| -100 | Internal panic |

## Testing

Run the test suite:

```bash
cd demos/python
pytest tests/ -v
```

Run with hypothesis for property-based tests:

```bash
pytest tests/ -v --hypothesis-show-statistics
```

## File Structure

```
demos/python/
├── Syna/               # Python package
│   ├── __init__.py
│   ├── wrapper.py          # Main synadb class
│   └── experience.py       # RL experience helpers
├── tests/                  # Test suite
│   ├── test_wrapper.py
│   └── test_pandas.py
├── basic_usage.py          # Basic operations demo
├── numpy_integration.py    # NumPy demo
├── pandas_integration.py   # Pandas demo
├── async_operations.py     # Async demo
├── context_manager.py      # Context manager demo
├── rl_experience_demo.py   # RL demo
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
└── pytest.ini             # Test configuration
```

## Troubleshooting

### Library Not Found

```
OSError: libsynadb.so: cannot open shared object file
```

Solution: Set `LD_LIBRARY_PATH` or copy the library:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../target/release
# or
cp ../../target/release/libsynadb.so .
```

### Import Error

```
ModuleNotFoundError: No module named 'Syna'
```

Solution: Run from the `demos/python` directory or install the package:
```bash
cd demos/python
pip install -e .
```

### NumPy Version Mismatch

```
RuntimeWarning: numpy.dtype size changed
```

Solution: Upgrade numpy:
```bash
pip install --upgrade numpy
```

