"""Repository Model - Represents a GitHub repository."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Repository:
    """Data model for a GitHub repository."""

    repo_id: int
    name: str
    owner: str
    full_name: str
    url: str
    clone_url: str
    language: Optional[str]
    stars: int
    forks: int
    watchers: int
    open_issues: int
    last_updated: str
    created_at: str
    description: Optional[str]
    main_branch: str
    topics: list[str] = field(default_factory=list)
    size: int = 0
    has_issues: bool = True
    has_wiki: bool = True
    archived: bool = False
    license: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "repo_id": self.repo_id,
            "name": self.name,
            "owner": self.owner,
            "full_name": self.full_name,
            "url": self.url,
            "clone_url": self.clone_url,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "watchers": self.watchers,
            "open_issues": self.open_issues,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
            "description": self.description,
            "main_branch": self.main_branch,
            "topics": self.topics,
            "size": self.size,
            "has_issues": self.has_issues,
            "has_wiki": self.has_wiki,
            "archived": self.archived,
            "license": self.license,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Repository":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    @classmethod
    def from_github_repo(cls, repo, repo_id: int) -> "Repository":
        """Create from PyGithub repository object."""
        return cls(
            repo_id=repo_id,
            name=repo.name,
            owner=repo.owner.login,
            full_name=repo.full_name,
            url=repo.html_url,
            clone_url=repo.clone_url,
            language=repo.language,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            watchers=repo.watchers_count,
            open_issues=repo.open_issues_count,
            last_updated=repo.updated_at.isoformat() if repo.updated_at else None,
            created_at=repo.created_at.isoformat() if repo.created_at else None,
            description=repo.description,
            main_branch=repo.default_branch,
            topics=repo.topics or [],
            size=repo.size,
            has_issues=repo.has_issues,
            has_wiki=repo.has_wiki,
            archived=repo.archived,
            license=repo.license.key if repo.license else None,
        )
