from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class SourceType(str, Enum):
    SOURCE_FILE = "source_file"
    COMMIT = "commit"
    PULL_REQUEST = "pull_request"
    ISSUE = "issue"


@dataclass
class Chunk:
    # Content
    content: str                        # The actual text that gets embedded
    summary: str                        # One-line human-readable description

    # Provenance
    source_type: SourceType             # Where this chunk came from
    repo: str                           # e.g. "owner/repo-name"
    file_path: Optional[str] = None     # Relative path for source files
    start_line: Optional[int] = None    # For source file chunks
    end_line: Optional[int] = None      # For source file chunks
    commit_sha: Optional[str] = None    # For commit chunks
    pr_number: Optional[int] = None     # For PR/issue chunks
    author: Optional[str] = None        # Commit author or PR author
    timestamp: Optional[str] = None     # ISO 8601 string

    # Identity
    chunk_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "summary": self.summary,
            "source_type": self.source_type.value,
            "repo": self.repo,
            "file_path": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "commit_sha": self.commit_sha,
            "pr_number": self.pr_number,
            "author": self.author,
            "timestamp": self.timestamp,
        }