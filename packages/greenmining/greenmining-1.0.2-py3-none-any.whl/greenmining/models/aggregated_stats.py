"""Aggregated Statistics Model - Represents aggregated analysis data."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AggregatedStats:
    """Data model for aggregated statistics."""

    summary: dict = field(default_factory=dict)
    known_patterns: dict = field(default_factory=dict)
    repositories: list[dict] = field(default_factory=list)
    languages: dict = field(default_factory=dict)
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "summary": self.summary,
            "known_patterns": self.known_patterns,
            "repositories": self.repositories,
            "languages": self.languages,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AggregatedStats":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
