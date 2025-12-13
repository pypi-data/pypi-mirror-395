"""
Upload utilities for XiaoShi AI Hub SDK using HTTP API
"""

import base64
import hashlib
import os
import tempfile
from pathlib import Path
from typing import List, Optional, Union, Dict

import requests

from xiaoshiai_hub.client import DEFAULT_BASE_URL, HubClient
from xiaoshiai_hub.envelope_crypto import Algorithm, DataKey, envelope_enc_file
from .exceptions import HubException, AuthenticationError, RepositoryNotFoundError



try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None


# File extensions that require encryption
ENCRYPTABLE_EXTENSIONS = {".safetensors", ".bin", ".pt", ".pth", ".ckpt"}


class UploadError(HubException):
    """Raised when an upload operation fails."""
    pass


def _build_api_url(
    base_url: Optional[str],
    organization: str,
    repo_type: str,
    repo_name: str,
) -> str:
    """Build API upload URL."""
    base_url = (base_url or DEFAULT_BASE_URL).rstrip('/')
    return f"{base_url}/moha/{organization}/{repo_type}/{repo_name}/api/upload"


def _create_session(
    token: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> requests.Session:
    """Create HTTP session with authentication."""
    session = requests.Session()
    
    if token:
        session.headers.update({'Authorization': f'Bearer {token}'})
    elif username and password:
        from requests.auth import HTTPBasicAuth
        session.auth = HTTPBasicAuth(username, password)  # type: ignore
    
    session.headers.update({'Content-Type': 'application/json'})
    return session


def _calculate_file_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


class _TqdmUploadWrapper:
    """Wrapper to add tqdm progress bar to file upload."""

    def __init__(self, file_obj, total_size, desc=None):
        self.file_obj = file_obj
        self.total_size = total_size
        self.pbar = None
        if tqdm:
            self.pbar = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=desc,
            )

    def read(self, size=-1):
        """Read data and update progress bar."""
        data = self.file_obj.read(size)
        if self.pbar is not None and data:
            self.pbar.update(len(data))
        return data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore[no-untyped-def]
        del exc_type, exc_val, exc_tb  # Unused but required by context manager protocol
        if self.pbar is not None:
            self.pbar.close()
        self.file_obj.close()


def _upload_file_with_progress(
    upload_url: str,
    file_path: Path,
    desc: Optional[str] = None,
) -> None:
    """Upload file to URL with progress bar."""
    file_size = file_path.stat().st_size

    with open(file_path, 'rb') as f:
        with _TqdmUploadWrapper(f, file_size, desc=desc) as wrapped_file:
            upload_response = requests.put(
                upload_url,
                data=wrapped_file,
                headers={'Content-Type': 'application/octet-stream'}
            )
            upload_response.raise_for_status()


def _encrypt_file_if_needed(
    file_path: Path,
    encryption_password: Optional[str] = None,
    data_key: Optional[DataKey] = None,
    algorithm: Optional[Algorithm] = None,
) -> tuple[Optional[Path], Optional[Path]]:
    """
    Encrypt file if encryption_password is provided, file is large enough, and file extension is encryptable.

    Args:
        file_path: Path to the file to encrypt
        encryption_password: Password for encryption
        data_key: DataKey for encryption (required if encryption_password is provided)
        algorithm: Encryption algorithm (default: AES-256-CTR)

    Returns:
        Tuple of (encrypted_file_path, temp_dir_path)
        If no encryption, returns (None, None)
    """
    if not encryption_password or not data_key:
        return None, None

    # Check file size first (only encrypt files >= 5MB)
    file_size = file_path.stat().st_size
    if file_size < 5 * 1024 * 1024:
        return None, None

    # Check if file extension requires encryption
    if file_path.suffix.lower() not in ENCRYPTABLE_EXTENSIONS:
        return None, None

    temp_dir = Path(tempfile.mkdtemp())
    encrypted_file = temp_dir / file_path.name

    # Encrypt the file
    enc_kwargs = {
        "source": file_path,
        "data_key": data_key,
        "dest": encrypted_file,
        "chunked": True,
    }
    if algorithm:
        enc_kwargs["algorithm"] = algorithm
    envelope_enc_file(**enc_kwargs)
    print(f"Encrypted file path: {encrypted_file}")

    return encrypted_file, temp_dir


def _upload_files_via_api(
    session: requests.Session,
    api_url: str,
    files: List[Dict],
    message: str,
    branch: str,
    author: Optional[Dict] = None,
) -> Dict:
    """Upload files via HTTP API."""
    payload = {
        "files": files,
        "message": message,
        "branch": branch,
    }
    if author:
        payload["author"] = author
    
    try:
        response = session.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {e}")
        elif e.response.status_code == 404:
            raise RepositoryNotFoundError(f"Repository not found: {e}")
        else:
            raise UploadError(f"Upload failed: {e}")
    except requests.exceptions.RequestException as e:
        raise UploadError(f"Request failed: {e}")


def _upload_small_file(
    session: requests.Session,
    api_url: str,
    local_path: Path,
    remote_path: str,
    message: str,
    branch: str,
) -> Dict:
    """Upload small file (< 5MB) with base64 encoding."""
    file_size = local_path.stat().st_size

    # Show progress bar for reading file
    pbar = None
    if tqdm and file_size > 0:
        pbar = tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Uploading {local_path.name}",
        )

    try:
        with open(local_path, 'rb') as f:
            content = f.read()
            if pbar is not None:
                pbar.update(file_size)

        content_b64 = base64.b64encode(content).decode('utf-8')

        files = [{
            "path": remote_path,
            "content": content_b64,
            "size": len(content),
        }]

        result = _upload_files_via_api(session, api_url, files, message, branch)

        if pbar is not None:
            pbar.close()

        return result
    except Exception:
        if pbar is not None:
            pbar.close()
        raise


def _upload_large_file(
    session: requests.Session,
    api_url: str,
    local_path: Path,
    remote_path: str,
    message: str,
    branch: str,
) -> Dict:
    """Upload large file (≥ 5MB) using LFS."""
    file_size = os.path.getsize(local_path)
    sha256 = _calculate_file_sha256(local_path)
    
    files = [{
        "path": remote_path,
        "size": file_size,
        "sha256": sha256,
    }]
    
    # Step 1: Request upload URL
    result = _upload_files_via_api(session, api_url, files, message, branch)
    
    # Step 2: Upload to S3 if needed
    if result.get('needUpload'):
        upload_url = result['uploadUrls'].get(remote_path)
        if upload_url:
            _upload_file_with_progress(
                upload_url,
                local_path,
                desc=f"Uploading {local_path.name}"
            )
            print(f"Upload completed: {remote_path}")
    
    return result


def upload_folder(
    folder_path: Union[str, Path],
    repo_id: str,
    repo_type: str = "models",
    revision: str = "main",
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    encryption_password: Optional[str] = None,
    ignore_patterns: Optional[List[str]] = None,
    temp_dir: Optional[Union[str, Path]] = None,
    algorithm: Optional[str] = None,
) -> Dict:
    """
    Upload a folder to a repository using HTTP API.

    Args:
        folder_path: Path to the folder to upload
        repo_id: Repository ID in the format "organization/repo_name"
        repo_type: Type of repository ("models" or "datasets")
        revision: Branch to upload to (default: "main")
        commit_message: Commit message
        commit_description: Additional commit description
        base_url: Base URL of the Hub API
        username: Username for authentication
        password: Password for authentication
        token: Token for authentication (preferred)
        encryption_password: Password for file encryption (optional)
        ignore_patterns: List of patterns to ignore
        temp_dir: Temporary directory for encrypted files (optional, auto-created if not specified)
        algorithm: Encryption algorithm ("AES-256-CTR" or "SM4-CTR", default: AES-256-CTR)

    Returns:
        Upload response
    """
    import fnmatch
    import shutil

    # Parse repo_id
    parts = repo_id.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid repo_id format: {repo_id}. Expected 'organization/repo_name'")
    organization, repo_name = parts

    # Check if repository exists
    client = HubClient(base_url=base_url, username=username, password=password, token=token)
    try:
        client.get_repository_info(organization, repo_type, repo_name)
    except RepositoryNotFoundError:
        raise RepositoryNotFoundError(
            f"Repository not found: {organization}/{repo_type}/{repo_name}. "
            f"Please create the repository first."
        )

    # Validate folder
    folder_path = Path(folder_path)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    if not folder_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")

    # Setup ignore patterns
    if ignore_patterns is None:
        ignore_patterns = []
    if '.git' not in ignore_patterns and '.git/' not in ignore_patterns:
        ignore_patterns.append('.git')
    ignore_patterns.append('.gitattributes')
    # Create or use temporary directory for encrypted files
    temp_dir_path: Optional[Path] = None
    data_key: Optional[DataKey] = None
    if encryption_password:
        if temp_dir:
            # Use user-specified temp directory
            temp_dir_path = Path(temp_dir)
            temp_dir_path.mkdir(parents=True, exist_ok=True)
        else:
            # Auto-create temp directory
            temp_dir_path = Path(tempfile.mkdtemp())
        # Generate data key for encryption
        data_key = client.generate_data_key(algorithm,encryption_password)

    try:
        # Create session and API URL
        session = _create_session(token, username, password)
        api_url = _build_api_url(base_url, organization, repo_type, repo_name)

        # Prepare commit message
        if commit_message is None:
            commit_message = f"Upload folder from {folder_path.name}"
        if commit_description:
            commit_message = f"{commit_message}\n\n{commit_description}"

        # Collect all files
        files_to_upload = []
        large_files = []  # Files >= 5MB
        small_files = []  # Files < 5MB
        has_encrypted_files = False  # Track if any file was encrypted
        for root, dirs, files in os.walk(folder_path):
            # Filter directories
            dirs[:] = [d for d in dirs if not any(
                fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns
            )]

            rel_root = os.path.relpath(root, folder_path)

            for file in files:
                # Construct relative file path
                if rel_root == '.':
                    rel_file_path = file
                else:
                    rel_file_path = os.path.join(rel_root, file)

                # Check if file matches ignore pattern
                if any(fnmatch.fnmatch(rel_file_path, pattern) for pattern in ignore_patterns):
                    continue

                local_file = Path(root) / file
                file_size = local_file.stat().st_size

                # Encrypt file if needed (only for large files with specific extensions)
                actual_file = local_file
                if (encryption_password and temp_dir_path and data_key and
                    file_size >= 5 * 1024 * 1024 and  # Only encrypt files >= 5MB
                    local_file.suffix.lower() in ENCRYPTABLE_EXTENSIONS):
                    # Preserve directory structure in temp dir
                    encrypted_file = temp_dir_path / rel_file_path
                    encrypted_file.parent.mkdir(parents=True, exist_ok=True)
                    # Build encryption kwargs
                    enc_kwargs = {
                        "source": local_file,
                        "data_key": data_key,
                        "dest": encrypted_file,
                        "chunked": True,
                    }
                    if algorithm:
                        enc_kwargs["algorithm"] = Algorithm(algorithm)
                    envelope_enc_file(**enc_kwargs)
                    print(f"Encrypted file path: {encrypted_file}")
                    # 加密后重新计算大小，避免被huggingface下载的时候大小一致性检查不通过
                    file_size = encrypted_file.stat().st_size
                    actual_file = encrypted_file

                    has_encrypted_files = True

                # Determine upload method based on size
                if file_size >= 5 * 1024 * 1024:  # 5MB
                    # Large file - use LFS
                    sha256 = _calculate_file_sha256(actual_file)
                    files_to_upload.append({
                        "path": rel_file_path,
                        "size": file_size,
                        "sha256": sha256,
                    })
                    large_files.append((actual_file, rel_file_path))
                else:
                    # Small file - use base64
                    with open(actual_file, 'rb') as f:
                        content = f.read()
                    content_b64 = base64.b64encode(content).decode('utf-8')
                    files_to_upload.append({
                        "path": rel_file_path,
                        "content": content_b64,
                        "size": file_size,
                    })
                    small_files.append((rel_file_path, file_size))

        print(f"Found {len(files_to_upload)} files to upload ({len(large_files)} large files, {len(small_files)} small files)")
        # Show progress for small files upload
        small_files_pbar = None
        if small_files and tqdm:
            total_small_size = sum(size for _, size in small_files)
            small_files_pbar = tqdm(
                total=total_small_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc="Uploading small files",
            )

        # Upload files via API
        try:
            result = _upload_files_via_api(session, api_url, files_to_upload, commit_message, revision)
            # Update progress bar for small files
            if small_files_pbar is not None:
                for _, size in small_files:
                    small_files_pbar.update(size)
                small_files_pbar.close()
        except Exception:
            if small_files_pbar is not None:
                small_files_pbar.close()
            raise

        # Upload large files to S3 if needed
        if result.get('needUpload') and large_files:
            upload_urls = result.get('uploadUrls', {})
            for local_file, remote_path in large_files:
                upload_url = upload_urls.get(remote_path)
                if upload_url:
                    _upload_file_with_progress(
                        upload_url,
                        local_file,
                        desc=f"Uploading {local_file.name}"
                    )
                    print(f"Upload completed: {remote_path}")

        # Set repository encrypted flag if any file was encrypted
        if has_encrypted_files:
            try:
                client.set_repository_encrypted(organization, repo_type, repo_name)
                print(f"Set repository encrypted flag for {repo_id}")
            except Exception as e:
                print(f"Warning: Failed to set repository encrypted flag: {e}")

        print(f"Successfully uploaded to {repo_id}")
        return result
    finally:
        if temp_dir_path and temp_dir_path.exists():
            shutil.rmtree(temp_dir_path)


def upload_file(
    path_file: Union[str, Path],
    path_in_repo: str,
    repo_id: str,
    repo_type: str = "models",
    revision: str = "main",
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    encryption_password: Optional[str] = None,
    algorithm: Optional[str] = None,
) -> Dict:
    """
    Upload a single file to a repository using HTTP API.

    Args:
        path_file: Path to the local file
        path_in_repo: Path in the repository
        repo_id: Repository ID in the format "organization/repo_name"
        repo_type: Type of repository ("models" or "datasets")
        revision: Branch to upload to (default: "main")
        commit_message: Commit message
        commit_description: Additional commit description
        base_url: Base URL of the Hub API
        username: Username for authentication
        password: Password for authentication
        token: Token for authentication (preferred)
        encryption_password: Password for file encryption (optional)
        algorithm: Encryption algorithm ("AES" or "SM4", default: AES)

    Returns:
        Upload response
    """
    import shutil

    # Parse repo_id
    parts = repo_id.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid repo_id format: {repo_id}. Expected 'organization/repo_name'")
    organization, repo_name = parts

    # Check if repository exists
    client = HubClient(base_url=base_url, username=username, password=password, token=token)
    try:
        client.get_repository_info(organization, repo_type, repo_name)
    except RepositoryNotFoundError:
        raise RepositoryNotFoundError(
            f"Repository not found: {organization}/{repo_type}/{repo_name}. "
            f"Please create the repository first."
        )

    # Validate file
    path_file = Path(path_file)
    if not path_file.exists():
        raise FileNotFoundError(f"File not found: {path_file}")
    if not path_file.is_file():
        raise ValueError(f"Path is not a file: {path_file}")

    # Generate data key if encryption is needed
    data_key: Optional[DataKey] = None
    if encryption_password:
        data_key = client.generate_data_key(algorithm,encryption_password)

    # Encrypt file if needed
    algo = Algorithm(algorithm) if algorithm else None
    encrypted_file, temp_dir = _encrypt_file_if_needed(path_file, encryption_password, data_key, algo)
    actual_file = encrypted_file if encrypted_file else path_file
    file_was_encrypted = encrypted_file is not None

    try:
        # Create session and API URL
        session = _create_session(token, username, password)
        api_url = _build_api_url(base_url, organization, repo_type, repo_name)

        # Prepare commit message
        if commit_message is None:
            commit_message = f"Upload {path_in_repo}"
        if commit_description:
            commit_message = f"{commit_message}\n\n{commit_description}"

        # Check file size
        file_size = actual_file.stat().st_size
        # Upload main file
        if file_size >= 5 * 1024 * 1024:  # 5MB
            # Large file
            result = _upload_large_file(session, api_url, actual_file, path_in_repo, commit_message, revision)
        else:
            # Small file
            result = _upload_small_file(session, api_url, actual_file, path_in_repo, commit_message, revision)

        # Set repository encrypted flag if file was encrypted
        if file_was_encrypted:
            try:
                client.set_repository_encrypted(organization, repo_type, repo_name)
                print(f"Set repository encrypted flag for {repo_id}")
            except Exception as e:
                print(f"Warning: Failed to set repository encrypted flag: {e}")

        print(f"Successfully uploaded {path_in_repo} to {repo_id}")
        return result
    finally:
        # Clean up temporary encrypted file
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)

