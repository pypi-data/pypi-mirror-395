"""GIS MCP Client for connecting to remote GIS MCP servers."""

import json
from typing import Optional, Dict, Any, List

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import sseclient
    SSE_AVAILABLE = True
except ImportError:
    SSE_AVAILABLE = False


class GISMCPClient:
    """Client for connecting to GIS MCP servers via HTTP or SSE."""

    SUPPORTED_TRANSPORTS = {"http", "sse", "auto"}

    def __init__(
        self,
        server_url: str,
        transport: str = "http",
        credentials: Optional[Dict[str, str]] = None
    ):
        """
        Initialize a GIS MCP client.
        
        Args:
            server_url: URL of the GIS MCP server (e.g., "http://localhost:9010/mcp")
            transport: Transport type - "http" or "sse" (default: "http")
            credentials: Optional authentication credentials
                        (e.g., {'token': 'token'} or {'username': 'user', 'password': 'pass'})
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests is required. Install with: pip install gis-mcp-client"
            )
        
        self.server_url = server_url.rstrip('/')
        self.transport = transport.lower().strip()
        if self.transport not in self.SUPPORTED_TRANSPORTS:
            raise ValueError(
                f"Unsupported transport '{transport}'. "
                f"Use one of: {', '.join(sorted(self.SUPPORTED_TRANSPORTS))}"
            )
        self.credentials = credentials or {}
        self.session = requests.Session()
        self._tools_cache: Optional[List[Dict[str, Any]]] = None
        self.rpc_url = self._derive_rpc_url()
        
        # Set up authentication
        if self.credentials:
            if 'token' in self.credentials:
                self.session.headers.update({
                    'Authorization': f"Bearer {self.credentials['token']}"
                })
            elif 'username' in self.credentials and 'password' in self.credentials:
                self.session.auth = (
                    self.credentials['username'],
                    self.credentials['password']
                )
    def _derive_rpc_url(self) -> str:
        """
        Derive the HTTP JSON-RPC endpoint from the provided URL.
        If the user passes an SSE URL, swap it for /mcp so HTTP calls still work.
        """
        if self.server_url.endswith('/sse'):
            return self.server_url[:-4] + '/mcp'
        if '/sse' in self.server_url:
            return self.server_url.replace('/sse', '/mcp')
        return self.server_url

    def _post_rpc(self, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
        """
        Internal helper to POST a JSON-RPC request and return JSON.
        Adds clearer messaging when users pass an SSE-only endpoint.
        """
        try:
            response = self.session.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            # Hint to users who pointed us at an SSE-only server.
            if self.transport in {"sse", "auto"} and '/sse' in self.server_url:
                raise ConnectionError(
                    "HTTP JSON-RPC call failed. If your server is SSE-only, "
                    "use connect_sse() or hand as_mcp_tool() to your agentic "
                    "library so it manages the SSE stream."
                ) from e
            raise ConnectionError(f"Failed to connect to GIS MCP server: {str(e)}") from e

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the GIS MCP server.
        
        Returns:
            List of tool definitions
        """
        if self._tools_cache is not None:
            return self._tools_cache
        
        result = self._post_rpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            },
            timeout=30,
        )

        if "result" in result and "tools" in result["result"]:
            self._tools_cache = result["result"]["tools"]
            return self._tools_cache
        return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the remote GIS MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
        
        Returns:
            Tool execution result
        
        Example:
            >>> client = GISMCPClient("http://localhost:9010/mcp")
            >>> result = client.call_tool("buffer", {
            ...     "geometry": "POINT(0 0)",
            ...     "distance": 10
            ... })
        """
        result = self._post_rpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=300,  # 5 minute timeout for long operations
        )

        if "error" in result:
            raise RuntimeError(f"Tool execution error: {result['error']}")

        if "result" in result:
            return result["result"]
        return result
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific tool.
        
        Args:
            tool_name: Name of the tool
        
        Returns:
            Tool definition or None if not found
        """
        tools = self.list_tools()
        for tool in tools:
            if tool.get("name") == tool_name:
                return tool
        return None
    
    def get_sse_url(self) -> str:
        """
        Get the SSE URL for this server.
        
        This constructs the URL for FastMCP's native SSE transport endpoint.
        FastMCP handles SSE natively when the server runs with transport="sse".
        
        Returns:
            SSE endpoint URL (typically at /sse)
        """
        if '/mcp' in self.server_url:
            return self.server_url.replace('/mcp', '/sse')
        else:
            return f"{self.server_url}/sse"
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for this client.
        
        Returns:
            Dictionary with authentication headers
        """
        headers = {}
        if self.credentials:
            if 'token' in self.credentials:
                headers['Authorization'] = f"Bearer {self.credentials['token']}"
            elif 'username' in self.credentials and 'password' in self.credentials:
                # For basic auth, requests handles it via session.auth
                # But we can still provide headers if needed
                pass
        return headers

    def as_mcp_tool(
        self,
        server_label: str = "gis-mcp",
        server_description: str = "Remote GIS MCP server",
        require_approval: str = "never"
    ) -> Dict[str, Any]:
        """
        Build an MCP tool spec compatible with OpenAI, LangChain MCP adapters,
        and other agentic libraries that accept MCP tool dictionaries.
        """
        return {
            "type": "mcp",
            "server_label": server_label,
            "server_description": server_description,
            "server_url": self.get_sse_url(),
            "server_headers": self.get_auth_headers(),
            "require_approval": require_approval,
        }
    
    def connect_sse(self):
        """
        Connect to the server via Server-Sent Events (SSE).
        
        Returns:
            SSE client connection
        """
        if not SSE_AVAILABLE:
            raise ImportError(
                "sseclient-py is required for SSE connections. "
                "Install with: pip install gis-mcp-client"
            )
        
        headers = self.get_auth_headers()
        sse_url = self.get_sse_url()
        
        response = self.session.get(
            sse_url,
            headers=headers,
            stream=True,
            timeout=None
        )
        response.raise_for_status()
        
        return sseclient.SSEClient(response)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()


# Convenience functions for common GIS operations

def create_client(
    server_url: str,
    transport: str = "http",
    credentials: Optional[Dict[str, str]] = None
) -> GISMCPClient:
    """
    Create a GIS MCP client instance.
    
    Args:
        server_url: URL of the GIS MCP server
        transport: Transport type ("http" or "sse")
        credentials: Optional authentication credentials
    
    Returns:
        GISMCPClient instance
    
    Example:
        >>> from gis_mcp_client import create_client
        >>> client = create_client("http://localhost:9010/mcp")
        >>> result = client.call_tool("buffer", {"geometry": "POINT(0 0)", "distance": 10})
    """
    return GISMCPClient(server_url, transport, credentials)

