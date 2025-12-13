"""Commit Model - Represents a Git commit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Commit:
    """Data model for a Git commit."""

    commit_id: str
    repo_name: str
    date: str
    author: str
    author_email: str
    message: str
    files_changed: list[str] = field(default_factory=list)
    lines_added: int = 0
    lines_deleted: int = 0
    insertions: int = 0
    deletions: int = 0
    is_merge: bool = False
    branches: list[str] = field(default_factory=list)
    in_main_branch: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "commit_id": self.commit_id,
            "repo_name": self.repo_name,
            "date": self.date,
            "author": self.author,
            "author_email": self.author_email,
            "message": self.message,
            "files_changed": self.files_changed,
            "lines_added": self.lines_added,
            "lines_deleted": self.lines_deleted,
            "insertions": self.insertions,
            "deletions": self.deletions,
            "is_merge": self.is_merge,
            "branches": self.branches,
            "in_main_branch": self.in_main_branch,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Commit":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    @classmethod
    def from_pydriller_commit(cls, commit, repo_name: str) -> "Commit":
        """Create from PyDriller commit object."""
        return cls(
            commit_id=commit.hash,
            repo_name=repo_name,
            date=(
                commit.committer_date.isoformat()
                if commit.committer_date
                else commit.author_date.isoformat()
            ),
            author=commit.author.name,
            author_email=commit.author.email,
            message=commit.msg,
            files_changed=[f.new_path or f.filename for f in commit.modified_files],
            lines_added=commit.insertions,
            lines_deleted=commit.deletions,
            insertions=commit.insertions,
            deletions=commit.deletions,
            is_merge=commit.merge,
            branches=commit.branches if hasattr(commit, "branches") else [],
            in_main_branch=commit.in_main_branch if hasattr(commit, "in_main_branch") else True,
        )
