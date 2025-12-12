"""Type definitions for Pierre Git Storage SDK."""

from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Dict, Iterable, List, Literal, Optional, Protocol, Union

from typing_extensions import NotRequired, TypedDict


class DiffFileState(str, Enum):
    """File state in a diff."""

    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    RENAMED = "renamed"
    COPIED = "copied"
    TYPE_CHANGED = "type_changed"
    UNMERGED = "unmerged"
    UNKNOWN = "unknown"


class GitFileMode(str, Enum):
    """Git file modes."""

    REGULAR = "100644"
    EXECUTABLE = "100755"
    SYMLINK = "120000"
    SUBMODULE = "160000"


# Configuration types
class GitStorageOptions(TypedDict, total=False):
    """Options for GitStorage client."""

    name: str  # required
    key: str  # required
    api_base_url: Optional[str]
    storage_base_url: Optional[str]
    api_version: Optional[int]
    default_ttl: Optional[int]


class BaseRepo(TypedDict, total=False):
    """Base repository configuration for GitHub sync."""

    provider: Literal["github"]  # required
    owner: str  # required
    name: str  # required
    default_branch: Optional[str]


class DeleteRepoResult(TypedDict):
    """Result from deleting a repository."""

    repo_id: str
    message: str


# Removed: GetRemoteURLOptions - now uses **kwargs
# Removed: CreateRepoOptions - now uses **kwargs
# Removed: FindOneOptions - now uses **kwargs


# File and branch types
# Removed: GetFileOptions - now uses **kwargs
# Removed: ListFilesOptions - now uses **kwargs


class ListFilesResult(TypedDict):
    """Result from listing files."""

    paths: List[str]
    ref: str


# Removed: ListBranchesOptions - now uses **kwargs


class BranchInfo(TypedDict):
    """Information about a branch."""

    cursor: str
    name: str
    head_sha: str
    created_at: str


class ListBranchesResult(TypedDict):
    """Result from listing branches."""

    branches: List[BranchInfo]
    next_cursor: Optional[str]
    has_more: bool


class CreateBranchResult(TypedDict):
    """Result from creating a branch."""

    message: str
    target_branch: str
    target_is_ephemeral: bool
    commit_sha: NotRequired[str]


# Removed: ListCommitsOptions - now uses **kwargs


class CommitInfo(TypedDict):
    """Information about a commit."""

    sha: str
    message: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    date: datetime
    raw_date: str


class ListCommitsResult(TypedDict):
    """Result from listing commits."""

    commits: List[CommitInfo]
    next_cursor: Optional[str]
    has_more: bool


# Diff types
class DiffStats(TypedDict):
    """Statistics about a diff."""

    files: int
    additions: int
    deletions: int
    changes: int


class FileDiff(TypedDict):
    """A file diff entry."""

    path: str
    state: DiffFileState
    raw_state: str
    old_path: Optional[str]
    raw: str
    bytes: int
    is_eof: bool


class FilteredFile(TypedDict):
    """A filtered file entry."""

    path: str
    state: DiffFileState
    raw_state: str
    old_path: Optional[str]
    bytes: int
    is_eof: bool


# Removed: GetBranchDiffOptions - now uses **kwargs


class GetBranchDiffResult(TypedDict):
    """Result from getting branch diff."""

    branch: str
    base: str
    stats: DiffStats
    files: List[FileDiff]
    filtered_files: List[FilteredFile]


# Removed: GetCommitDiffOptions - now uses **kwargs


class GetCommitDiffResult(TypedDict):
    """Result from getting commit diff."""

    sha: str
    stats: DiffStats
    files: List[FileDiff]
    filtered_files: List[FilteredFile]


# Commit types
class CommitSignature(TypedDict):
    """Git commit signature."""

    name: str
    email: str


class CreateCommitOptions(TypedDict, total=False):
    """Options for creating a commit."""

    target_branch: str  # required
    commit_message: str  # required
    author: CommitSignature  # required
    expected_head_sha: Optional[str]
    base_branch: Optional[str]
    ephemeral: bool
    ephemeral_base: bool
    committer: Optional[CommitSignature]
    ttl: int


# Removed: CommitFileOptions - now uses **kwargs with explicit mode parameter


class RefUpdate(TypedDict):
    """Information about a ref update."""

    branch: str
    old_sha: str
    new_sha: str


class CommitResult(TypedDict):
    """Result from creating a commit."""

    commit_sha: str
    tree_sha: str
    target_branch: str
    pack_bytes: int
    blob_count: int
    ref_update: RefUpdate


# Removed: RestoreCommitOptions - now uses **kwargs


class RestoreCommitResult(TypedDict):
    """Result from restoring a commit."""

    commit_sha: str
    tree_sha: str
    target_branch: str
    pack_bytes: int
    ref_update: RefUpdate


# Removed: PullUpstreamOptions - now uses **kwargs


# File source types for commits
FileSource = Union[
    str,
    bytes,
    bytearray,
    memoryview,
    Iterable[bytes],
    AsyncIterator[bytes],
]


# Protocol for commit builder
class CommitBuilder(Protocol):
    """Protocol for commit builder."""

    def add_file(
        self,
        path: str,
        source: FileSource,
        *,
        mode: Optional[GitFileMode] = None,
    ) -> "CommitBuilder":
        """Add a file to the commit."""
        ...

    def add_file_from_string(
        self,
        path: str,
        contents: str,
        *,
        encoding: str = "utf-8",
        mode: Optional[GitFileMode] = None,
    ) -> "CommitBuilder":
        """Add a file from a string."""
        ...

    def delete_path(self, path: str) -> "CommitBuilder":
        """Delete a path from the commit."""
        ...

    async def send(self) -> CommitResult:
        """Send the commit to the server."""
        ...


# Protocol for repository
class Repo(Protocol):
    """Protocol for repository."""

    @property
    def id(self) -> str:
        """Get the repository ID."""
        ...

    async def get_remote_url(
        self,
        *,
        permissions: Optional[list[str]] = None,
        ttl: Optional[int] = None,
    ) -> str:
        """Get the remote URL for the repository."""
        ...

    async def get_file_stream(
        self,
        *,
        path: str,
        ref: Optional[str] = None,
        ephemeral: Optional[bool] = None,
        ttl: Optional[int] = None,
    ) -> Any:  # httpx.Response
        """Get a file as a stream."""
        ...

    async def list_files(
        self,
        *,
        ref: Optional[str] = None,
        ephemeral: Optional[bool] = None,
        ttl: Optional[int] = None,
    ) -> ListFilesResult:
        """List files in the repository."""
        ...

    async def list_branches(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        ttl: Optional[int] = None,
    ) -> ListBranchesResult:
        """List branches in the repository."""
        ...

    async def create_branch(
        self,
        *,
        base_branch: str,
        target_branch: str,
        base_is_ephemeral: bool = False,
        target_is_ephemeral: bool = False,
        ttl: Optional[int] = None,
    ) -> CreateBranchResult:
        """Create or promote a branch."""
        ...

    async def promote_ephemeral_branch(
        self,
        *,
        base_branch: str,
        target_branch: Optional[str] = None,
        ttl: Optional[int] = None,
    ) -> CreateBranchResult:
        """Promote an ephemeral branch to a persistent target branch."""
        ...

    async def list_commits(
        self,
        *,
        branch: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        ttl: Optional[int] = None,
    ) -> ListCommitsResult:
        """List commits in the repository."""
        ...

    async def get_branch_diff(
        self,
        *,
        branch: str,
        base: Optional[str] = None,
        ephemeral: Optional[bool] = None,
        ephemeral_base: Optional[bool] = None,
        ttl: Optional[int] = None,
    ) -> GetBranchDiffResult:
        """Get diff between branches."""
        ...

    async def get_commit_diff(
        self,
        *,
        sha: str,
        base_sha: Optional[str] = None,
        ttl: Optional[int] = None,
    ) -> GetCommitDiffResult:
        """Get diff for a commit."""
        ...

    async def pull_upstream(
        self,
        *,
        ref: Optional[str] = None,
        ttl: Optional[int] = None,
    ) -> None:
        """Pull from upstream repository."""
        ...

    async def restore_commit(
        self,
        *,
        target_branch: str,
        target_commit_sha: str,
        author: CommitSignature,
        commit_message: Optional[str] = None,
        expected_head_sha: Optional[str] = None,
        committer: Optional[CommitSignature] = None,
        ttl: Optional[int] = None,
    ) -> RestoreCommitResult:
        """Restore a previous commit."""
        ...

    def create_commit(
        self,
        *,
        target_branch: str,
        commit_message: str,
        author: CommitSignature,
        expected_head_sha: Optional[str] = None,
        base_branch: Optional[str] = None,
        ephemeral: Optional[bool] = None,
        ephemeral_base: Optional[bool] = None,
        committer: Optional[CommitSignature] = None,
        ttl: Optional[int] = None,
    ) -> CommitBuilder:
        """Create a new commit builder."""
        ...

    async def create_commit_from_diff(
        self,
        *,
        target_branch: str,
        commit_message: str,
        diff: FileSource,
        author: CommitSignature,
        expected_head_sha: Optional[str] = None,
        base_branch: Optional[str] = None,
        ephemeral: Optional[bool] = None,
        ephemeral_base: Optional[bool] = None,
        committer: Optional[CommitSignature] = None,
        ttl: Optional[int] = None,
    ) -> CommitResult:
        """Create a commit by applying a diff."""
        ...


# Webhook types
class WebhookValidationOptions(TypedDict, total=False):
    """Options for webhook validation."""

    max_age_seconds: int


class WebhookPushEvent(TypedDict):
    """Webhook push event."""

    type: Literal["push"]
    repository: Dict[str, str]
    ref: str
    before: str
    after: str
    customer_id: str
    pushed_at: datetime
    raw_pushed_at: str


class ParsedWebhookSignature(TypedDict):
    """Parsed webhook signature."""

    timestamp: str
    signature: str


class WebhookUnknownEvent(TypedDict):
    """Fallback webhook event for unknown types."""

    type: str
    raw: Any


WebhookEventPayload = Union[WebhookPushEvent, WebhookUnknownEvent]


class WebhookValidationResult(TypedDict, total=False):
    """Result from webhook validation."""

    valid: bool
    error: Optional[str]
    event_type: Optional[str]
    timestamp: Optional[int]
    payload: WebhookEventPayload
