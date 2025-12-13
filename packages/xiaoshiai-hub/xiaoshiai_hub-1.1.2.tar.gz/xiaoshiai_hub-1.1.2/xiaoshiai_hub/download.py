"""
Download utilities for XiaoShi AI Hub SDK
"""

import fnmatch
import os
from pathlib import Path
from typing import List, Optional, Union

from .exceptions import RepositoryNotFoundError

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None

from .client import HubClient



def _match_pattern(name: str, pattern: str) -> bool:
    """
    Match a filename against a pattern.
    
    Supports wildcards:
    - * matches any characters
    - *.ext matches files with extension
    - prefix* matches files starting with prefix
    
    Args:
        name: Filename to match
        pattern: Pattern to match against
        
    Returns:
        True if the name matches the pattern
    """
    return fnmatch.fnmatch(name, pattern)


def _should_download_file(
    file_path: str,
    allow_patterns: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
) -> bool:
    """
    Determine if a file should be downloaded based on patterns.
    
    Args:
        file_path: Path of the file
        allow_patterns: List of patterns to allow (if None, allow all)
        ignore_patterns: List of patterns to ignore
        
    Returns:
        True if the file should be downloaded
    """
    filename = os.path.basename(file_path)
    
    # Check ignore patterns first
    if ignore_patterns:
        for pattern in ignore_patterns:
            if _match_pattern(filename, pattern) or _match_pattern(file_path, pattern):
                return False
    
    # If no allow patterns, allow all (except ignored)
    if not allow_patterns:
        return True
    
    # Check allow patterns
    for pattern in allow_patterns:
        if _match_pattern(filename, pattern) or _match_pattern(file_path, pattern):
            return True
    
    return False


def _count_files_to_download(
    client: HubClient,
    organization: str,
    repo_type: str,
    repo_name: str,
    branch: str,
    path: str,
    allow_patterns: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
) -> int:
    """
    Count total number of files to download.

    Args:
        client: Hub client instance
        organization: Organization name
        repo_type: Repository type
        repo_name: Repository name
        branch: Branch name
        path: Current path in the repository
        allow_patterns: Patterns to allow
        ignore_patterns: Patterns to ignore

    Returns:
        Total number of files to download
    """
    content = client.get_repository_content(
        organization=organization,
        repo_type=repo_type,
        repo_name=repo_name,
        branch=branch,
        path=path,
    )

    count = 0
    if content.entries:
        for entry in content.entries:
            if entry.type == "file":
                if _should_download_file(entry.path, allow_patterns, ignore_patterns):
                    count += 1
            elif entry.type == "dir":
                count += _count_files_to_download(
                    client=client,
                    organization=organization,
                    repo_type=repo_type,
                    repo_name=repo_name,
                    branch=branch,
                    path=entry.path,
                    allow_patterns=allow_patterns,
                    ignore_patterns=ignore_patterns,
                )

    return count


def _download_repository_recursively(
    client: HubClient,
    organization: str,
    repo_type: str,
    repo_name: str,
    branch: str,
    path: str,
    local_dir: str,
    allow_patterns: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
    progress_bar = None,
) -> None:
    """
    Recursively download repository contents.

    Args:
        client: Hub client instance
        organization: Organization name
        repo_type: Repository type
        repo_name: Repository name
        branch: Branch name
        path: Current path in the repository
        local_dir: Local directory to save files
        allow_patterns: Patterns to allow
        ignore_patterns: Patterns to ignore
        progress_bar: Optional tqdm progress bar for overall progress
    """
    content = client.get_repository_content(
        organization=organization,
        repo_type=repo_type,
        repo_name=repo_name,
        branch=branch,
        path=path,
    )

    # Process entries
    if content.entries:
        for entry in content.entries:
            if entry.type == "file":
                # 检查文件是否应该被下载
                if _should_download_file(entry.path, allow_patterns, ignore_patterns):
                    print(f"Downloading file: {entry.path}")
                    local_path = os.path.join(local_dir, entry.path)

                    # Update progress bar description if available
                    if progress_bar is not None:
                        progress_bar.set_description(f"Downloading {entry.path}")

                    client.download_file(
                        organization=organization,
                        repo_type=repo_type,
                        repo_name=repo_name,
                        branch=branch,
                        file_path=entry.path,
                        local_path=local_path,
                        show_progress=progress_bar is None,  # Show individual progress only if no overall progress
                    )

                    if progress_bar is not None:
                        progress_bar.update(1)
                else:
                    print(f"Skipping file: {entry.path}")

            elif entry.type == "dir":
                print(f"Entering directory: {entry.path}")
                # 递归下载
                _download_repository_recursively(
                    client=client,
                    organization=organization,
                    repo_type=repo_type,
                    repo_name=repo_name,
                    branch=branch,
                    path=entry.path,
                    local_dir=local_dir,
                    allow_patterns=allow_patterns,
                    ignore_patterns=ignore_patterns,
                    progress_bar=progress_bar,
                )
            else:
                print(f"Skipping {entry.type}: {entry.path}")


def moha_hub_download(
    repo_id: str,
    filename: str,
    *,
    repo_type: str = "models",
    revision: Optional[str] = None,
    local_dir: Optional[Union[str, Path]] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    show_progress: bool = True,
) -> Union[str, bytes]:
    """
    Download a single file from a repository.

    Similar to huggingface_hub.hf_hub_download().

    Note: This function does not support decryption. If you need to download encrypted files,
    use xpai-enc CLI tool to decrypt them after download.

    Args:
        repo_id: Repository ID in the format "organization/repo_name"
        filename: Path to the file in the repository
        repo_type: Type of repository ("models" or "datasets")
        revision: Branch/tag/commit to download from (default: main branch)
        local_dir: Directory to save the file (if not using cache)
        base_url: Base URL of the Hub API (default: from MOHA_ENDPOINT env var)
        username: Username for authentication
        password: Password for authentication
        token: Token for authentication
        show_progress: Whether to show download progress bar

    Returns:
        File path (str) or file content (bytes) based on return_content parameter

    Example:
        >>> file_path = moha_hub_download(
        ...     repo_id="demo/demo",
        ...     filename="data/config.yaml",
        ...     username="your-username",
        ...     password="your-password",
        ... )
    """
    parts = repo_id.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid repo_id format: {repo_id}. Expected 'organization/repo_name'")
    organization, repo_name = parts
    client = HubClient(
        base_url=base_url,
        username=username,
        password=password,
        token=token,
    )

    try:
        client.get_repository_info(organization, repo_type, repo_name)
    except RepositoryNotFoundError:
        raise RepositoryNotFoundError(
            f"Repository not found: {organization}/{repo_type}/{repo_name}. "
            f"Please create the repository first."
        )


    # 获取默认分支
    if revision is None:
        revision = client.get_default_branch(organization, repo_type, repo_name)

    if local_dir:
        local_path = os.path.join(local_dir, filename)
    else:
        local_path = filename

    # 下载文件
    client.download_file(
        organization=organization,
        repo_type=repo_type,
        repo_name=repo_name,
        branch=revision,
        file_path=filename,
        local_path=local_path,
        show_progress=show_progress,
    )
    return local_path


def snapshot_download(
    repo_id: str,
    repo_type: str = "models",
    revision: Optional[str] = None,
    local_dir: Optional[Union[str, Path]] = None,
    allow_patterns: Optional[Union[List[str], str]] = None,
    ignore_patterns: Optional[Union[List[str], str]] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    show_progress: bool = True,
) -> str:
    """
    Download an entire repository snapshot.

    Similar to huggingface_hub.snapshot_download().

    Note: This function does not support decryption. If you need to download encrypted repositories,
    use xpai-enc CLI tool to decrypt them after download.

    Args:
        repo_id: Repository ID in the format "organization/repo_name"
        repo_type: Type of repository ("models" or "datasets")
        revision: Branch/tag/commit to download from (default: main branch)
        local_dir: Directory to save files (if not using cache)
        allow_patterns: Pattern or list of patterns to allow (e.g., "*.yaml", "*.yml")
        ignore_patterns: Pattern or list of patterns to ignore (e.g., ".git*")
        base_url: Base URL of the Hub API (default: from MOHA_ENDPOINT env var)
        username: Username for authentication
        password: Password for authentication
        token: Token for authentication
        show_progress: Whether to show overall progress bar

    Returns:
        Path to the downloaded repository

    Example:
        >>> repo_path = snapshot_download(
        ...     repo_id="demo/demo",
        ...     repo_type="models",
        ...     allow_patterns=["*.yaml", "*.yml"],
        ...     ignore_patterns=[".git*"],
        ...     username="your-username",
        ...     password="your-password",
        ... )
    """
    parts = repo_id.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid repo_id format: {repo_id}. Expected 'organization/repo_name'")

    organization, repo_name = parts

    if isinstance(allow_patterns, str):
        allow_patterns = [allow_patterns]
    if isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]
    client = HubClient(
        base_url=base_url,
        username=username,
        password=password,
        token=token,
    )
    try:
        client.get_repository_info(organization, repo_type, repo_name)
    except RepositoryNotFoundError:
        raise RepositoryNotFoundError(
            f"Repository not found: {organization}/{repo_type}/{repo_name}. "
            f"Please create the repository first."
        )
    if revision is None:
        revision = client.get_default_branch(organization, repo_type, repo_name)

    # Determine local directory
    if local_dir:
        download_dir = str(local_dir)
    else:
        # Default to downloads directory
        download_dir = f"./downloads/{organization}_{repo_type}_{repo_name}"

    progress_bar = None
    if show_progress and tqdm is not None:
        # 计算需要下载的文件总数
        total_files = _count_files_to_download(
            client=client,
            organization=organization,
            repo_type=repo_type,
            repo_name=repo_name,
            branch=revision,
            path="",
            allow_patterns=allow_patterns,
            ignore_patterns=ignore_patterns,
        )

        if total_files > 0:
            progress_bar = tqdm(
                total=total_files,
                unit='file',
                desc=f"Downloading {repo_id}",
                leave=True,
            )

    # 递归下载，不是使用git的方式
    try:
        _download_repository_recursively(
            client=client,
            organization=organization,
            repo_type=repo_type,
            repo_name=repo_name,
            branch=revision,
            path="",
            local_dir=download_dir,
            allow_patterns=allow_patterns,
            ignore_patterns=ignore_patterns,
            progress_bar=progress_bar,
        )
    finally:
        if progress_bar is not None:
            progress_bar.close()

    if show_progress:
        print(f"Download completed to: {download_dir}")

    # Add download count
    try:
        client.add_download_count(
            organization=organization,
            repo_type=repo_type,
            repo_name=repo_name,
        )
    except Exception as e:
        # Don't fail the download if adding count fails
        print(f"Warning: Failed to add download count: {e}")

    return download_dir




