"""Analysis Result Model - Represents commit analysis output."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AnalysisResult:
    """Data model for commit analysis results."""

    commit_id: str
    repo_name: str
    date: str
    commit_message: str
    green_aware: bool
    green_evidence: Optional[str] = None
    known_pattern: Optional[str] = None
    pattern_confidence: Optional[str] = None
    emergent_pattern: Optional[str] = None
    files_changed: list = None
    lines_added: int = 0
    lines_deleted: int = 0

    def __post_init__(self):
        if self.files_changed is None:
            self.files_changed = []

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "commit_id": self.commit_id,
            "repo_name": self.repo_name,
            "date": self.date,
            "commit_message": self.commit_message,
            "green_aware": self.green_aware,
            "green_evidence": self.green_evidence,
            "known_pattern": self.known_pattern,
            "pattern_confidence": self.pattern_confidence,
            "emergent_pattern": self.emergent_pattern,
            "files_changed": self.files_changed,
            "lines_added": self.lines_added,
            "lines_deleted": self.lines_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisResult":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
