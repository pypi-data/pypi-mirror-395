# GIS MCP Client

Lightweight Python client that connects to remote GIS MCP servers via SSE (Server-Sent Events) to enable agentic AI operations on the cloud. Perform geospatial operations remotely without installing heavy GIS libraries.

## Features

- 🔹 **Lightweight** - No heavy GIS libraries required, just MCP client dependencies
- 🔹 **SSE Connection** - Connects to remote GIS MCP servers via Server-Sent Events for real-time agentic AI operations
- 🔹 **Cloud-Based** - Perform agentic AI operations on the cloud without local GIS dependencies
- 🔹 **HTTP & SSE Support** - Connect via HTTP or Server-Sent Events
- 🔹 **Remote Storage** - Upload/download files to/from remote server storage
- 🔹 **Authentication** - Support for token-based and basic authentication
- 🔹 **Easy to Use** - Simple API for calling remote GIS operations

## Installation

```bash
pip install gis-mcp-client
```

## Quick Start

### Basic Usage

```python
from gis_mcp_client import GISMCPClient

# Connect to a GIS MCP server
client = GISMCPClient("http://localhost:9010/mcp")

# List available tools
tools = client.list_tools()
print(f"Available tools: {[t['name'] for t in tools]}")

# Call a remote GIS operation
result = client.call_tool("buffer", {
    "geometry": "POINT(0 0)",
    "distance": 10
})
print(result)
```

### With Authentication

```python
# Token-based authentication
client = GISMCPClient(
    "http://remote-server:9010/mcp",
    credentials={"token": "your-api-token"}
)

# Username/password authentication
client = GISMCPClient(
    "http://remote-server:9010/mcp",
    credentials={"username": "user", "password": "pass"}
)
```

### Remote Storage

```python
from gis_mcp_client import RemoteStorage

# Connect to remote storage
storage = RemoteStorage("http://localhost:9010/storage")

# Upload a file
result = storage.upload("local_file.shp", "remote_file.shp")
print(result['message'])

# Download a file
result = storage.download("remote_file.shp", "downloaded_file.shp")
print(result['message'])

# List files
files = storage.list_files()
print(files['files'])
```

### Context Manager

```python
# Use as context manager for automatic cleanup
with GISMCPClient("http://localhost:9010/mcp") as client:
    result = client.call_tool("transform_coordinates", {
        "coordinates": [0, 0],
        "source_crs": "EPSG:4326",
        "target_crs": "EPSG:3857"
    })
    print(result)
```

## API Reference

### GISMCPClient

Main client for connecting to GIS MCP servers.

#### Methods

- `list_tools()` - List all available tools
- `call_tool(name, arguments)` - Call a remote tool
- `get_tool_info(name)` - Get information about a specific tool
- `connect_sse()` - Connect via Server-Sent Events

### RemoteStorage

Client for managing remote storage.

#### Methods

- `upload(local_path, remote_path)` - Upload a file
- `download(remote_path, local_path)` - Download a file
- `list_files(remote_path)` - List files in storage

## Examples

See the [examples directory](examples/) for comprehensive examples including:

- SSE connections with credentials
- Remote storage upload/download
- OpenAI integration
- Complete workflows

### Basic Example with Credentials

```python
from gis_mcp_client import GISMCPClient

# Connect with authentication
client = GISMCPClient(
    "https://remote-gis-mcp.com/mcp",
    credentials={"token": "your-access-token"}
)

# List available tools
tools = client.list_tools()

# Call a remote GIS operation
result = client.call_tool("transform_coordinates", {
    "coordinates": [-74.0060, 40.7128],
    "source_crs": "EPSG:4326",
    "target_crs": "EPSG:32633"
})
```

### Calculate Distance

```python
from gis_mcp_client import GISMCPClient

client = GISMCPClient("http://localhost:9010/mcp")

result = client.call_tool("calculate_geodetic_distance", {
    "point1": [0, 0],
    "point2": [1, 1],
    "ellps": "WGS84"
})
print(f"Distance: {result['distance']} meters")
```

### Transform Coordinates

```python
result = client.call_tool("transform_coordinates", {
    "coordinates": [-122.4194, 37.7749],  # San Francisco
    "source_crs": "EPSG:4326",
    "target_crs": "EPSG:3857"
})
print(f"Transformed: {result['coordinates']}")
```

### Create Buffer

```python
result = client.call_tool("buffer", {
    "geometry": "POINT(0 0)",
    "distance": 1000,
    "resolution": 16
})
print(f"Buffered geometry: {result['geometry']}")
```

## Requirements

- Python 3.10+
- `mcp` - MCP protocol client
- `requests` - HTTP client
- `sseclient-py` - Server-Sent Events support

## License

MIT License - see LICENSE file for details.

## Related Projects

- [GIS MCP Server](https://github.com/mahdin75/gis-mcp) - The server this client connects to
