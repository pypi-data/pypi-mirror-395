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

See the examples for runnable code.

## Examples

### `upload_only.py` (RemoteStorage upload)

```python
import os
from pathlib import Path
from gis_mcp_client import RemoteStorage

def main() -> None:
    base = os.getenv("GIS_MCP_BASE", "http://localhost:9010").rstrip("/")
    storage_url = os.getenv("GIS_STORAGE_URL", f"{base}/storage")
    token = os.getenv("GIS_MCP_TOKEN")

    local_file = os.getenv("GIS_INPUT_FILE")
    if not local_file:
        raise SystemExit("Set GIS_INPUT_FILE to the local path you want to upload.")

    remote_name = os.getenv("GIS_REMOTE_OUTPUT") or Path(local_file).name

    storage = RemoteStorage(
        storage_endpoint=storage_url,
        credentials={"token": token} if token else None,
    )

    result = storage.upload(local_file, remote_name)
    if not result.get("success"):
        raise SystemExit(f"Upload failed: {result.get('message')}")

    print(f"Uploaded '{local_file}' -> remote path '{result['remote_path']}'")

if __name__ == "__main__":
    main()
```

### `langchain_openrouter_buffer_simple.py` (LangChain + OpenRouter buffer)

```python
import asyncio, os
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from gis_mcp_client import GISMCPClient

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:9010/sse")
GIS_MCP_TOKEN = os.getenv("GIS_MCP_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek/deepseek-chat-v3.1")
SYSTEM_PROMPT = "You are a helpful GIS agent using remote MCP tools."

def init_llm() -> ChatOpenAI:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is required.")
    return ChatOpenAI(model=MODEL_NAME, api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, temperature=0.2)

def init_mcp() -> MultiServerMCPClient:
    gis_client = GISMCPClient(
        server_url=MCP_SERVER_URL,
        transport="auto",
        credentials={"token": GIS_MCP_TOKEN} if GIS_MCP_TOKEN else None,
    )
    tool_spec = gis_client.as_mcp_tool(server_label="gis-mcp")
    return MultiServerMCPClient({
        "gis": {
            "transport": "sse",
            "url": tool_spec["server_url"],
            "headers": tool_spec["server_headers"],
        }
    })

async def main() -> None:
    llm = init_llm()
    mcp_client = init_mcp()
    tools = await mcp_client.get_tools()

    agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
    user_prompt = (
        "Call the GIS MCP 'buffer' tool and return the buffered geometry. "
        f"Use geometry POINT(0 0), distance 1000, resolution 16."
    )

    res = await agent.ainvoke({"messages": [{"role": "user", "content": user_prompt}]})
    msgs = res.get("messages", [])
    final = next(
        (m.content for m in reversed(msgs) if isinstance(m, AIMessage)),
        msgs[-1].content if msgs else "No response",
    )
    print("Agent response:\n", final)

if __name__ == "__main__":
    asyncio.run(main())
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

## Requirements

- Python 3.10+
- `mcp` - MCP protocol client
- `requests` - HTTP client
- `sseclient-py` - Server-Sent Events support

## License

MIT License - see LICENSE file for details.

## Related Projects

- [GIS MCP Server](https://github.com/mahdin75/gis-mcp) - The server this client connects to
- See `examples/agentic_any_library.py` for an end-to-end agent bridge example.
