"""
XiaoShi AI Hub Client
"""

import base64
import os
from typing import Dict, List, Optional


import requests
from xiaoshiai_hub.envelope_crypto import DEFAULT_ALGORITHM, Algorithm, DataKey

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None

from .exceptions import (
    AuthenticationError,
    HTTPError,
    RepositoryNotFoundError,
)
from .types import  Repository, Ref, GitContent


# 默认基础 URL，可通过环境变量 MOHA_ENDPOINT 覆盖
DEFAULT_BASE_URL = os.environ.get(
    "MOHA_ENDPOINT",
    "https://rune-api.develop.xiaoshiai.cn"
)



class HubClient:
    """Client for interacting with XiaoShi AI Hub API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):
        """
        Initialize the Hub client.

        Args:
            base_url: Base URL of the Hub API (default: from MOHA_ENDPOINT env var)
            username: Username for authentication
            password: Password for authentication
            token: Token for authentication (alternative to username/password)
        """
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip('/')
        self.username = username
        self.password = password
        self.token = token
        self.session = requests.Session()
        
        # Set up authentication
        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'
        elif username and password:
            auth_string = f"{username}:{password}"
            encoded = base64.b64encode(auth_string.encode()).decode()
            self.session.headers['Authorization'] = f'Basic {encoded}'
    
    def _make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """Make an HTTP request with error handling."""
        try:
            response = self.session.request(method, url, **kwargs)
            
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed")
            elif response.status_code == 404:
                raise RepositoryNotFoundError("Resource not found")
            elif response.status_code >= 400:
                raise HTTPError(
                    f"HTTP {response.status_code}: {response.reason}",
                    status_code=response.status_code
                )
            
            return response
        except requests.RequestException as e:
            raise HTTPError(f"Request failed: {str(e)}")
        
    def cancel_repository_encrypted(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
    ) -> None:
        """Cancel repository encrypted flag."""
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/encryption/cancel"
        response = self._make_request("PUT", url)
        if response.status_code != 200:
            raise HTTPError(f"Failed to cancel repository encrypted flag: {response.text}")
        
    def set_repository_encrypted(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
    ) -> None:
        """Set repository encrypted flag."""
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/encryption/set"
        response = self._make_request("PUT", url)
        if response.status_code != 200:
            raise HTTPError(f"Failed to set repository encrypted flag: {response.text}")    
    
    def get_repository_info(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
    ) -> Repository:
        """
        Get repository information.

        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name

        Returns:
            Repository information
        """
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}"
        response = self._make_request("GET", url)
        data = response.json()

        # Parse annotations if present
        annotations: Dict[str, str] = {}
        if 'annotations' in data and isinstance(data['annotations'], dict):
            annotations = data['annotations']

        # Parse metadata if present
        metadata: Dict[str, List[str]] = {}
        if 'metadata' in data and isinstance(data['metadata'], dict):
            metadata = data['metadata']

        return Repository(
            name=data.get('name', repo_name),
            organization=organization,
            type=repo_type,
            description=data.get('description'),
            metadata=metadata,
            annotations=annotations,
        )
    
    def get_repository_refs(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
    ) -> List[Ref]:
        """
        Get repository references (branches and tags).

        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name

        Returns:
            List of references
        """
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/refs"
        response = self._make_request("GET", url)
        data = response.json()

        refs = []
        for ref_data in data:
            refs.append(Ref(
                name=ref_data.get('name', ''),
                ref=ref_data.get('ref', ''),
                type=ref_data.get('type', ''),
                hash=ref_data.get('hash', ''),
                is_default=ref_data.get('isDefault', False),
            ))

        return refs

    def get_default_branch(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
    ) -> str:
        """
        Get the default branch name for a repository.

        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name

        Returns:
            Default branch name (defaults to "main" if not found)
        """
        refs = self.get_repository_refs(organization, repo_type, repo_name)
        for ref in refs:
            if ref.is_default and ref.type == "branch":
                return ref.name
        return "main"
    
    def get_repository_content(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
        branch: str,
        path: str = "",
    ) -> GitContent:
        """
        Get repository content at a specific path.
        
        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name
            branch: Branch name
            path: Path within the repository (empty for root)
            
        Returns:
            Git content information
        """
        if path:
            url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/contents/{branch}/{path}"
        else:
            url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/contents/{branch}"
        
        response = self._make_request("GET", url)
        data = response.json()
        
        return self._parse_git_content(data)
    
    def _parse_git_content(self, data: dict) -> GitContent:
        """Parse GitContent from API response."""
        entries = None
        if 'entries' in data and data['entries']:
            entries = [self._parse_git_content(entry) for entry in data['entries']]
        
        return GitContent(
            name=data.get('name', ''),
            path=data.get('path', ''),
            type=data.get('type', 'file'),
            size=data.get('size', 0),
            hash=data.get('hash'),
            content_type=data.get('contentType'),
            content=data.get('content'),
            content_omitted=data.get('contentOmitted', False),
            entries=entries,
        )
    
    def add_download_count(self, organization: str, repo_type: str, repo_name: str) -> None:
        """
        Add download count for a repository.
        
        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name
        """
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/downloads"
        response = self._make_request("POST", url)
        # 检查http code
        if response.status_code != 200:
            raise HTTPError(f"Failed to add download count: {response.text}")
    
    def download_file(
        self,
        organization: str,
        repo_type: str,
        repo_name: str,
        branch: str,
        file_path: str,
        local_path: str,
        show_progress: bool = True,
    ) -> None:
        """
        Download a single file from the repository.

        Args:
            organization: Organization name
            repo_type: Repository type ("models" or "datasets")
            repo_name: Repository name
            branch: Branch name
            file_path: Path to the file in the repository
            local_path: Local path to save the file
            show_progress: Whether to show download progress bar
        """
        url = f"{self.base_url}/moha/v1/organizations/{organization}/{repo_type}/{repo_name}/resolve/{branch}/{file_path}"
        response = self._make_request("GET", url, stream=True)

        # Get file size from headers
        total_size = int(response.headers.get('content-length', 0))

        # Create parent directories if needed
        import os
        os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else '.', exist_ok=True)

        # Prepare progress bar
        progress_bar = None
        if show_progress and tqdm is not None and total_size > 0:
            # Get filename for display
            filename = os.path.basename(file_path)
            progress_bar = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=filename,
                leave=True,
            )

        # Write file with progress
        try:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        # Ensure chunk is bytes for type safety
                        if isinstance(chunk, str):
                            chunk_bytes = chunk.encode('utf-8')
                        elif isinstance(chunk, bytes):
                            chunk_bytes = chunk
                        else:
                            chunk_bytes = bytes(chunk)
                        f.write(chunk_bytes)
                        if progress_bar is not None:
                            progress_bar.update(len(chunk_bytes))
        finally:
            if progress_bar is not None:
                progress_bar.close()


    def generate_data_key(
            self, 
            algorithm : Optional[str]  = DEFAULT_ALGORITHM,
            password: Optional[str] = None) -> DataKey:
        url = f"{self.base_url}/api/kms/generate-data-key"
        try:
            resp = requests.post(
                url,
                json={
                    "algorithm": algorithm,
                    "password": password,
                },
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            plaintext_key = base64.b64decode(data["plaintextKey"])
            encrypted_key = data["encryptedKey"]
            
            return DataKey(
                plaintext_key=plaintext_key,
                encrypted_key=encrypted_key
            )
            
        except requests.RequestException as e:
            raise e
