"""Remote storage client for GIS MCP servers."""

from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class RemoteStorage:
    """Client for managing remote storage on GIS MCP servers."""
    
    def __init__(
        self,
        storage_endpoint: str,
        credentials: Optional[Dict[str, str]] = None
    ):
        """
        Initialize a remote storage client.
        
        Args:
            storage_endpoint: URL of the storage endpoint
                            (e.g., "http://localhost:9010/storage")
            credentials: Optional authentication credentials
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests is required. Install with: pip install gis-mcp-client"
            )
        
        self.storage_endpoint = storage_endpoint.rstrip('/')
        self.credentials = credentials or {}
        self.session = requests.Session()
        
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
    
    def upload(self, local_path: str, remote_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to remote storage.
        
        Args:
            local_path: Path to local file
            remote_path: Optional remote path (defaults to filename)
        
        Returns:
            Upload result dictionary
        """
        local_file = Path(local_path)
        
        if not local_file.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")
        
        if not local_file.is_file():
            raise ValueError(f"Path is not a file: {local_path}")
        
        if remote_path is None:
            remote_path = local_file.name
        
        remote_path = remote_path.lstrip('/')
        upload_url = f"{self.storage_endpoint}/upload"
        
        try:
            with open(local_file, 'rb') as f:
                files = {'file': (local_file.name, f, 'application/octet-stream')}
                data = {'path': remote_path}
                
                response = self.session.post(
                    upload_url,
                    files=files,
                    data=data,
                    timeout=300
                )
                response.raise_for_status()
                
                result = response.json() if response.content else {}
                # Use remote_path from server response (in case server modified it)
                server_remote_path = result.get('remote_path', remote_path)
                return {
                    'success': True,
                    'remote_path': server_remote_path,
                    'local_path': str(local_path),
                    'size': result.get('size'),
                    'message': result.get('message', f"File uploaded successfully to {server_remote_path}"),
                    'response': result
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to upload file: {str(e)}"
            }
    
    def download(self, remote_path: str, local_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Download a file from remote storage.
        
        Args:
            remote_path: Path to remote file
            local_path: Optional local path (defaults to filename)
        
        Returns:
            Download result dictionary
        """
        remote_path = remote_path.lstrip('/')
        download_url = f"{self.storage_endpoint}/download"
        
        try:
            params = {'path': remote_path}
            response = self.session.get(
                download_url,
                params=params,
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            if local_path is None:
                local_path = Path(remote_path).name
            
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                'success': True,
                'remote_path': remote_path,
                'local_path': str(local_path),
                'message': f"File downloaded successfully to {local_path}",
                'size': local_file.stat().st_size
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to download file: {str(e)}"
            }
    
    def list_files(self, remote_path: Optional[str] = None) -> Dict[str, Any]:
        """
        List files in remote storage.
        
        Args:
            remote_path: Optional path to list (defaults to root)
        
        Returns:
            Dictionary with list of files
        """
        list_url = f"{self.storage_endpoint}/list"
        
        try:
            params = {}
            if remote_path:
                params['path'] = remote_path.lstrip('/')
            
            response = self.session.get(list_url, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json() if response.content else {}
            return {
                'success': True,
                'files': result.get('files', []),
                'path': remote_path or '/',
                'response': result
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list files: {str(e)}"
            }
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()

