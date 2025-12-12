"""
Type definitions for XiaoShi AI Hub SDK
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal, Dict


@dataclass
class Repository:
    """Repository information."""
    name: str
    organization: str
    type: str  # "models" or "datasets"
    description: Optional[str] = None
    metadata: Dict[str, List[str]] = field(default_factory=dict)  # Repository metadata
    annotations: Dict[str, str] = field(default_factory=dict)  # Repository annotations/metadata



@dataclass
class Signature:
    """Git signature (author/committer)."""
    name: str
    email: str
    when: datetime


@dataclass
class Commit:
    """Git commit information."""
    hash: str
    message: str
    author: Signature
    committer: Signature
    timestamp: datetime
    tree_hash: Optional[str] = None
    parents: Optional[List[str]] = None


@dataclass
class Ref:
    """Git reference (branch/tag)."""
    name: str
    ref: str
    type: str  # "branch" or "tag"
    hash: str
    is_default: bool = False
    last_commit: Optional[Commit] = None


@dataclass
class GitLFSMeta:
    """Git LFS metadata."""
    oid: str
    size: int


@dataclass
class Symlink:
    """Symlink information."""
    target: str


@dataclass
class Submodule:
    """Submodule information."""
    url: str
    path: str
    branch: str


FileType = Literal["file", "dir", "symlink", "submodule"]


@dataclass
class GitContent:
    """Git content (file or directory)."""
    name: str
    path: str
    type: FileType
    size: int = 0
    hash: Optional[str] = None
    content_type: Optional[str] = None
    content: Optional[str] = None
    content_omitted: bool = False
    last_commit: Optional[Commit] = None
    symlink: Optional[Symlink] = None
    submodule: Optional[Submodule] = None
    lfs: Optional[GitLFSMeta] = None
    entries: Optional[List['GitContent']] = None

