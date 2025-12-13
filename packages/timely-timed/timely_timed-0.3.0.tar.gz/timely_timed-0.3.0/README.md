# Timely Timed

A robust Python package for fetching UTC time from multiple time servers with automatic fallback logic and extensive customization options.

## Installation

```bash
pip install timely-timed
```

## Features

- **Zero External Dependencies** - Uses only built-in Python modules (`urllib`, `json`, `datetime`)
- **Multiple Time Server Support** - Automatic fallback across multiple servers
- **Extensible Architecture** - Add custom servers and strategies easily
- **Smart Server Management** - Exclude, add, or remove servers at will
- **Strategy Pattern** - Different server types handled by dedicated strategies
- **Comprehensive Error Handling** - Detailed error messages when servers fail
- **Type Hints** - Full type annotations for better IDE support
- **Logging Integration** - Built-in logging for debugging

## Quick Start

### Basic Usage

```python
from timely_timed import get_utc_time

# Get current UTC time from time servers
utc_time = get_utc_time()
print(utc_time)  # datetime object representing current UTC time
```

### Exclude Default Servers

```python
from timely_timed import get_utc_time

# Exclude specific default servers (supports partial matching)
utc_time = get_utc_time(excluded_servers=["worldclockapi"])

# Exclude multiple servers
utc_time = get_utc_time(excluded_servers=["worldclockapi", "aisenseapi"])
```

### Using Custom Time Servers

```python
from timely_timed import get_utc_time, TimeServerClient

# Method 1: Using the convenience function
custom_servers = ["https://your-custom-server.com/time"]
utc_time = get_utc_time(custom_servers=custom_servers)

# Method 2: Using the client class
client = TimeServerClient(custom_servers=["https://your-custom-server.com/time"])
utc_time = client.get_utc_time()

# Method 3: Only use custom servers (no defaults)
client = TimeServerClient(
    custom_servers=["https://your-server.com/time"],
    use_default_servers=False
)
utc_time = client.get_utc_time()
```

## Advanced Usage

### Dynamic Server Management

```python
from timely_timed import TimeServerClient

client = TimeServerClient()

# Add a server with highest priority
client.add_server("https://priority-server.com/time", priority=True)

# Add a server with lowest priority
client.add_server("https://backup-server.com/time", priority=False)

# Remove servers by pattern (supports partial matching)
removed_count = client.remove_server("worldclockapi")
print(f"Removed {removed_count} server(s)")

# Remove by exact URL
client.remove_server("http://worldclockapi.com/api/json/utc/now")

utc_time = client.get_utc_time()
```

### Initialization Options

```python
from timely_timed import TimeServerClient

# Initialize with custom servers and exclusions
client = TimeServerClient(
    custom_servers=["https://my-server.com/time"],
    excluded_servers=["worldclockapi", "aisenseapi"],
    use_default_servers=True  # Still use remaining defaults
)

# Initialize with only custom servers
client = TimeServerClient(
    custom_servers=["https://my-server.com/time"],
    use_default_servers=False  # Disable all defaults
)
```

### Sending POST Body Data

```python
from timely_timed import get_utc_time

# If required by server, include additional data in the POST request
data = {"user": "example", "request_id": "12345"}
utc_time = get_utc_time(body=data)
print(utc_time)
```

### Error Handling

```python
from timely_timed import get_utc_time, AllServersFailedError

try:
    utc_time = get_utc_time()
    print(f"Current UTC time: {utc_time}")
except AllServersFailedError as e:
    print(f"Failed to fetch time: {e}")
    # Error message includes details about which servers failed and why
```

### Logging Integration

```python
import logging
from timely_timed import TimeServerClient

# Enable logging to see which servers are being tried
logging.basicConfig(level=logging.DEBUG)

client = TimeServerClient()
utc_time = client.get_utc_time()
# Logs will show: "Successfully fetched time from https://..."
```

## Default Time Servers

The package includes three default servers, AiSenseAPI, my self-hosted server (powered by Cloudflare Workers), and WorldClockAPI.

All default servers are free, public APIs requiring no authentication.

## Custom Time Server Integration

### Supported Server Formats

The package automatically handles different server types:

#### POST-Based Servers (JSON)

Expected request: POST with optional JSON body
```json
{
  "success": true,
  "result": {
    "utcTime": "2025-12-08T17:05:02.279Z"
  }
}
```

#### AiSenseAPI Format (GET)

Expected request: GET
```json
{
  "datetime": "2025-12-08T17:05:02+00:00"
}
```

#### WorldClockAPI Format (GET)

Expected request: GET
```json
{
  "currentDateTime": "2025-12-08T17:05:02Z"
}
```

### Adding Custom Server Strategies

For servers with custom formats, extend the `TimeServerStrategy` class:

```python
from timely_timed import TimeServerClient, TimeServerStrategy
from datetime import datetime
from urllib.request import Request, urlopen
import json

class MyCustomStrategy(TimeServerStrategy):
    def matches(self, url: str) -> bool:
        return "my-custom-server.com" in url
    
    def fetch_time(self, url: str, body=None) -> datetime:
        req = Request(url, method="GET")
        with urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            time_str = data["timestamp"]  # Your custom field
            return datetime.fromisoformat(time_str)

# Use the custom strategy
client = TimeServerClient(
    custom_servers=["https://my-custom-server.com/api/time"],
    custom_strategies=[MyCustomStrategy()]
)
utc_time = client.get_utc_time()
```

## API Reference

### `get_utc_time(body=None, custom_servers=None, excluded_servers=None)`

Convenience function to fetch UTC time.

**Parameters:**
- `body` (dict, optional): JSON data to send in POST requests
- `custom_servers` (list, optional): Custom server URLs (highest priority)
- `excluded_servers` (list, optional): Server patterns to exclude from defaults

**Returns:** `datetime` object

**Raises:** `AllServersFailedError` if all servers fail

### `TimeServerClient`

Main client class for advanced usage.

**Constructor Parameters:**
- `custom_servers` (list, optional): Custom server URLs
- `custom_strategies` (list, optional): Custom strategy instances
- `use_default_servers` (bool): Whether to include default servers (default: True)
- `excluded_servers` (list, optional): Server patterns to exclude

**Methods:**
- `get_utc_time(body=None)` - Fetch UTC time with fallback logic
- `add_server(server_url, priority=True)` - Add a server dynamically
- `remove_server(server_pattern)` - Remove servers matching pattern
- `add_strategy(strategy, priority=True)` - Add a custom strategy

### `TimeServerStrategy` (Abstract Base Class)

Base class for implementing custom server handlers.

**Methods to Implement:**
- `matches(url)` - Return True if this strategy handles the URL
- `fetch_time(url, body=None)` - Fetch and return datetime from the server

## Exception Classes

- `TimeServerError` - Base exception for time server errors
- `AllServersFailedError` - Raised when all configured servers fail

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper documentation
4. Add tests if applicable
5. Ensure code follows the existing style
6. Submit a pull request

### Development Setup

```bash
git clone https://github.com/yourusername/timely-timed.git
cd timely-timed
pip install -e .
```

## License

MIT License - See LICENSE file for details
