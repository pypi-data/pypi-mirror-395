"""
XiaoShi AI Hub Python SDK

小时 AI Hub Python SDK，用于与小时 AI Hub 仓库进行交互。
支持模型和数据集的上传、下载，以及大型模型文件的透明加密。
"""

from .client import HubClient, DEFAULT_BASE_URL
from .download import (
    moha_hub_download,
    snapshot_download,
)
from .exceptions import (
    HubException,
    RepositoryNotFoundError,
    FileNotFoundError,
    AuthenticationError,
)
from .types import (
    Repository,
    Ref,
    GitContent,
    Commit,
)
from .auth import (
    login,
    save_token,
    load_token,
    delete_token,
)
from .envelope_crypto import (
    Algorithm,
    envelope_enc_file,
)

# Upload functionality (requires GitPython)
try:
    from .upload import (
        upload_file,
        upload_folder,
        UploadError,
    )
except ImportError:
    upload_file = None
    upload_folder = None
    UploadError = None

__version__ = "1.1.0"

__all__ = [
    # Client
    "HubClient",
    "DEFAULT_BASE_URL",
    # Download
    "moha_hub_download",
    "snapshot_download",
    # Upload
    "upload_file",
    "upload_folder",
    # Auth
    "login",
    "save_token",
    "load_token",
    "delete_token",
    # Encryption
    "Algorithm",
    "envelope_enc_file",
    # Exceptions
    "HubException",
    "RepositoryNotFoundError",
    "FileNotFoundError",
    "AuthenticationError",
    "UploadError",
    # Types
    "Repository",
    "Ref",
    "GitContent",
    "Commit",
]

