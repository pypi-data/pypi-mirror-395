# Redis Client Wrapper

A convenient Redis client wrapper with JSON and datetime support.

## Installation

Requires Redis server and `redis-py` library:

```bash
pip install redis
```

## Usage

### Initialization

```python
from dgredis.conf import RedisConfig
from dgredis import RedisClient

config = RedisCoonfig(
    host="localhost",
    port=6379,
    password=None
)

client = RedisClient(config)
```

### Core Methods

#### JSON Operations

```python
# Store JSON data
data = {"name": "John", "date": datetime.now()}
client.set_json_key("user:1", data, ttl=3600)

# Retrieve JSON data
result = client.get_json_key("user:1")
```

#### Basic Key Operations

```python
# Set value
client.set_key("last_update", datetime.now(), ttl=60)

# Get value
last_update = client.get_key("last_update")
```

#### Key Type Check

```python
key_type = client.get_key_type("user:1")
```

### Features

1. Automatic serialization/deserialization:
   - datetime/date objects to/from ISO format
   - Complex structures (dict, list, tuple, set) to/from JSON

2. Time-to-live (TTL) support for keys

3. Support for both JSON documents (`*_json_key` methods) and simple keys

## Technical Details

### Serialization Behavior

- Dates and datetimes are stored in ISO8601 format (UTC)
- Nested structures are automatically handled recursively
- Original Redis types are preserved when possible

### Error Handling

- Invalid dates fall back to string values
- JSON decode errors return raw values

## Requirements

1. Redis server 4.0+ for JSON functionality
2. Python 3.7+ (uses datetime.fromisoformat())

## Limitations

1. JSON operations require RedisJSON module
2. Custom classes are not automatically serialized
3. Timezone-naive datetimes are assumed to be in local timezone

## Examples

### Working with Nested Structures

```python
data = {
    "user": "Alice",
    "login_dates": [datetime(2023,1,1), datetime(2023,1,15)],
    "preferences": {"dark_mode": True}
}
client.set_json_key("user:alice", data)
```

### TTL Management

```python
# Set key with 5 minute expiration
client.set_key("temp_data", {"value": 42}, ttl=300)

# Check remaining TTL (using native redis client)
remaining_ttl = client.client.ttl("temp_data")
```
