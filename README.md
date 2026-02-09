# Redis Caching Proxy

A lightweight HTTP caching proxy server built with FastAPI and Redis that forwards requests to an origin server while intelligently caching GET responses.

Project URL: https://roadmap.sh/projects/caching-server

## Features

- 🚀 **Fast Proxy**: Forwards HTTP requests (GET, POST, PUT, DELETE) to any origin server
- 💾 **Smart Caching**: Automatically caches successful GET responses in Redis
- ⚡ **Performance**: 5-minute TTL on cached responses for optimal performance
- 🔍 **Cache Visibility**: `X-Cache` header shows HIT/MISS status
- 🧹 **Cache Management**: Built-in command to clear cache
- 🛡️ **Error Handling**: Graceful handling of connection failures

## Prerequisites

- Python 3.14+
- Redis server running on `localhost:6379` (or configure custom URL)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/100kgtrotila/caching-proxy.git
cd caching-proxy
```

2. Install dependencies:
```bash
pip install -e .
```

3. Ensure Redis is running:
```bash
redis-server
```

## Usage

### Start the Proxy Server
```bash
python main.py --port 8000 --origin http://dummyjson.com
```

**Arguments:**
- `--port` - Port to run the proxy server on (default: 8000)
- `--origin` - Origin server URL to forward requests to (required)

### Clear Cache
```bash
python main.py --clear-cache
```

### Example Requests
```bash
# First request - cache MISS
curl -i http://localhost:8000/products/1
# X-Cache: MISS

# Second request - cache HIT
curl -i http://localhost:8000/products/1
# X-Cache: HIT
```

## How It Works

1. **Request Forwarding**: All incoming requests are forwarded to the configured origin server
2. **GET Caching**: Successful GET responses (200 status) are cached in Redis with a 5-minute TTL
3. **Cache Key**: Format is `METHOD:path?query` (e.g., `GET:/products/1`)
4. **Cache Hit**: Cached responses are served immediately with `X-Cache: HIT` header
5. **Cache Miss**: Fresh responses from origin include `X-Cache: MISS` header

## Project Structure
```
caching-proxy/
├── main.py          # Application entry point and configuration
├── proxy.py         # Core proxy and caching logic
├── pyproject.toml   # Project dependencies
└── README.md        # This file
```

## Configuration

Default configuration in `main.py`:
```python
config = {
    "origin": "",              # Set via --origin argument
    "port": 8000,              # Set via --port argument
    "redis_url": "redis://localhost:6379"
}
```

To use a different Redis instance, modify `redis_url` in the config dictionary.

## Technical Stack

- **FastAPI** - Modern, fast web framework
- **httpx** - Async HTTP client for forwarding requests
- **Redis** - In-memory data store for caching
- **uvicorn** - ASGI server

## Cache Behavior

- Only **GET** requests are cached
- Only responses with **200 status code** are cached
- Cache **TTL**: 300 seconds (5 minutes)
- Cache includes full response body
- Headers are preserved from origin response

## Error Handling

- Returns **502 Bad Gateway** if origin server is unreachable
- Removes problematic headers (`content-encoding`, `content-length`) to prevent conflicts
- Strips `host` header when forwarding to prevent routing issues

## Development

Run in development mode:
```bash
uvicorn main:app --reload --port 8000
```

## License

This project is created as a solution for the [roadmap.sh Caching Server project](https://roadmap.sh/projects/caching-server).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Built with ❤️ as part of the roadmap.sh backend projects