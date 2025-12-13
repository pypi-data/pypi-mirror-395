"""
Machine Learning Feature Extraction for Green Pattern Classification

Prepares data for ML-based pattern detection (Soliman et al.: 26/151 studies used ML).

Features extracted:
1. Text features: TF-IDF, word embeddings, n-grams
2. Code metrics: complexity, churn, file counts
3. Temporal features: time of day, day of week, commit velocity
4. Repository features: stars, contributors, language
5. Historical features: past green awareness, pattern history

Use case: Train ML classifier as complement to keyword matching
Goal: Higher recall while maintaining precision (De Martino 2025: 97.91% accuracy)
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import Counter
import math


@dataclass
class MLFeatures:
    """Feature vector for ML classification"""

    # Text features
    message_length: int
    word_count: int
    unique_word_ratio: float
    avg_word_length: float
    has_green_keywords: bool
    keyword_count: int
    keyword_density: float

    # Code metrics
    files_changed: int
    lines_added: int
    lines_deleted: int
    total_changes: int
    change_entropy: float  # Distribution of changes across files

    # Temporal features
    hour_of_day: int
    day_of_week: int
    is_weekend: bool
    commit_velocity: float  # Recent commit frequency

    # Repository features
    repo_stars: int
    repo_age_days: int
    primary_language: str

    # Historical features
    author_green_rate: float  # Author's historical green awareness
    repo_green_rate: float  # Repository's green awareness trend

    # Target label (for training)
    is_green_aware: Optional[bool] = None


class MLFeatureExtractor:
    """
    Extract features from commits for ML classification.

    Implements feature engineering based on:
    - Soliman et al. (2017): 26/151 studies used ML
    - De Martino et al. (2025): 97.91% accuracy with ML classifier

    Features are designed to be:
    1. Informative (capture green patterns)
    2. Discriminative (separate green from non-green)
    3. Robust (work across repositories/languages)
    """

    def __init__(self, green_keywords: Optional[List[str]] = None):
        """
        Initialize feature extractor.

        Args:
            green_keywords: List of green-related keywords for text features
        """
        self.green_keywords = green_keywords or self._default_keywords()
        self._author_history = {}
        self._repo_history = {}

    def _default_keywords(self) -> List[str]:
        """Default green keywords for feature extraction."""
        return [
            "cache",
            "optimize",
            "performance",
            "efficient",
            "reduce",
            "compress",
            "lazy",
            "async",
            "parallel",
            "batch",
            "pool",
            "scale",
            "memory",
            "cpu",
            "resource",
            "green",
            "sustainable",
            "energy",
            "power",
        ]

    def extract_text_features(self, text: str) -> Dict:
        """
        Extract text-based features from commit message.

        Args:
            text: Commit message text

        Returns:
            Dictionary with text features
        """
        words = re.findall(r"\b\w+\b", text.lower())
        unique_words = set(words)

        # Keyword matching
        keyword_matches = [w for w in words if w in self.green_keywords]

        return {
            "message_length": len(text),
            "word_count": len(words),
            "unique_word_ratio": len(unique_words) / len(words) if words else 0,
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "has_green_keywords": len(keyword_matches) > 0,
            "keyword_count": len(keyword_matches),
            "keyword_density": len(keyword_matches) / len(words) if words else 0,
        }

    def extract_code_metrics(self, commit: Dict) -> Dict:
        """
        Extract code change metrics.

        Args:
            commit: Commit dictionary with file changes

        Returns:
            Dictionary with code metrics
        """
        files = commit.get("files", [])

        files_changed = len(files)
        lines_added = sum(f.get("additions", 0) for f in files)
        lines_deleted = sum(f.get("deletions", 0) for f in files)
        total_changes = lines_added + lines_deleted

        # Change entropy (distribution of changes)
        if files_changed > 1:
            file_changes = [f.get("additions", 0) + f.get("deletions", 0) for f in files]
            total = sum(file_changes)
            if total > 0:
                probabilities = [c / total for c in file_changes]
                entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
            else:
                entropy = 0
        else:
            entropy = 0

        return {
            "files_changed": files_changed,
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "total_changes": total_changes,
            "change_entropy": round(entropy, 4),
        }

    def extract_temporal_features(self, commit: Dict, repo_commits: List[Dict]) -> Dict:
        """
        Extract temporal features.

        Args:
            commit: Current commit
            repo_commits: All commits in repository (for velocity calculation)

        Returns:
            Dictionary with temporal features
        """
        date_str = commit.get("date")

        if not date_str:
            return {
                "hour_of_day": 12,
                "day_of_week": 3,
                "is_weekend": False,
                "commit_velocity": 0,
            }

        # Parse date
        try:
            if isinstance(date_str, datetime):
                date = date_str
            else:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return {
                "hour_of_day": 12,
                "day_of_week": 3,
                "is_weekend": False,
                "commit_velocity": 0,
            }

        # Calculate velocity (commits in past 7 days)
        week_ago = date.timestamp() - (7 * 24 * 60 * 60)
        recent_commits = [
            c for c in repo_commits if self._parse_date(c.get("date")).timestamp() > week_ago
        ]
        velocity = len(recent_commits) / 7  # commits per day

        return {
            "hour_of_day": date.hour,
            "day_of_week": date.weekday(),
            "is_weekend": date.weekday() >= 5,
            "commit_velocity": round(velocity, 2),
        }

    def extract_repository_features(self, repository: Dict) -> Dict:
        """
        Extract repository-level features.

        Args:
            repository: Repository metadata

        Returns:
            Dictionary with repository features
        """
        created_at = repository.get("created_at")

        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                now = datetime.now(created_date.tzinfo)
                age_days = (now - created_date).days
            except (ValueError, AttributeError):
                age_days = 365  # Default
        else:
            age_days = 365

        return {
            "repo_stars": repository.get("stars", 0),
            "repo_age_days": age_days,
            "primary_language": repository.get("language", "Unknown"),
        }

    def extract_historical_features(
        self,
        commit: Dict,
        author_commits: List[Dict],
        repo_commits: List[Dict],
        analysis_results: List[Dict],
    ) -> Dict:
        """
        Extract historical features (past green awareness).

        Args:
            commit: Current commit
            author_commits: All commits by this author
            repo_commits: All commits in repository
            analysis_results: Pattern detection results

        Returns:
            Dictionary with historical features
        """
        # Author's historical green rate
        author_email = commit.get("author_email")
        author_green = [
            r
            for r in analysis_results
            if r.get("author_email") == author_email and r.get("is_green_aware", False)
        ]
        author_total = len([c for c in author_commits if c.get("author_email") == author_email])
        author_green_rate = len(author_green) / author_total if author_total > 0 else 0

        # Repository's historical green rate
        repo_name = commit.get("repository")
        repo_green = [
            r
            for r in analysis_results
            if r.get("repository") == repo_name and r.get("is_green_aware", False)
        ]
        repo_total = len([c for c in repo_commits if c.get("repository") == repo_name])
        repo_green_rate = len(repo_green) / repo_total if repo_total > 0 else 0

        return {
            "author_green_rate": round(author_green_rate, 4),
            "repo_green_rate": round(repo_green_rate, 4),
        }

    def extract_features(
        self,
        commit: Dict,
        repository: Dict,
        all_commits: List[Dict],
        analysis_results: List[Dict],
        ground_truth: Optional[bool] = None,
    ) -> MLFeatures:
        """
        Extract complete feature vector for a commit.

        Args:
            commit: Commit to extract features from
            repository: Repository metadata
            all_commits: All commits (for temporal/historical features)
            analysis_results: Pattern detection results (for historical features)
            ground_truth: Optional true label for supervised learning

        Returns:
            MLFeatures object
        """
        message = commit.get("message", "")

        # Extract feature groups
        text_features = self.extract_text_features(message)
        code_features = self.extract_code_metrics(commit)
        temporal_features = self.extract_temporal_features(commit, all_commits)
        repo_features = self.extract_repository_features(repository)
        historical_features = self.extract_historical_features(
            commit, all_commits, all_commits, analysis_results
        )

        # Combine into MLFeatures object
        return MLFeatures(
            # Text
            message_length=text_features["message_length"],
            word_count=text_features["word_count"],
            unique_word_ratio=text_features["unique_word_ratio"],
            avg_word_length=text_features["avg_word_length"],
            has_green_keywords=text_features["has_green_keywords"],
            keyword_count=text_features["keyword_count"],
            keyword_density=text_features["keyword_density"],
            # Code
            files_changed=code_features["files_changed"],
            lines_added=code_features["lines_added"],
            lines_deleted=code_features["lines_deleted"],
            total_changes=code_features["total_changes"],
            change_entropy=code_features["change_entropy"],
            # Temporal
            hour_of_day=temporal_features["hour_of_day"],
            day_of_week=temporal_features["day_of_week"],
            is_weekend=temporal_features["is_weekend"],
            commit_velocity=temporal_features["commit_velocity"],
            # Repository
            repo_stars=repo_features["repo_stars"],
            repo_age_days=repo_features["repo_age_days"],
            primary_language=repo_features["primary_language"],
            # Historical
            author_green_rate=historical_features["author_green_rate"],
            repo_green_rate=historical_features["repo_green_rate"],
            # Target
            is_green_aware=ground_truth,
        )

    def extract_features_batch(
        self,
        commits: List[Dict],
        repositories: List[Dict],
        analysis_results: List[Dict],
        ground_truth: Optional[List[bool]] = None,
    ) -> List[MLFeatures]:
        """
        Extract features for multiple commits.

        Args:
            commits: List of commits
            repositories: List of repository metadata
            analysis_results: Pattern detection results
            ground_truth: Optional list of true labels

        Returns:
            List of MLFeatures objects
        """
        # Build repository lookup
        repo_lookup = {r["name"]: r for r in repositories}

        features = []
        for i, commit in enumerate(commits):
            repo_name = commit.get("repository")
            repository = repo_lookup.get(repo_name, {})

            label = ground_truth[i] if ground_truth and i < len(ground_truth) else None

            feature = self.extract_features(commit, repository, commits, analysis_results, label)
            features.append(feature)

        return features

    def export_to_csv(self, features: List[MLFeatures], output_path: str) -> None:
        """
        Export features to CSV for ML training.

        Args:
            features: List of MLFeatures
            output_path: Path to output CSV file
        """
        import csv

        # Get all field names
        field_names = [
            "message_length",
            "word_count",
            "unique_word_ratio",
            "avg_word_length",
            "has_green_keywords",
            "keyword_count",
            "keyword_density",
            "files_changed",
            "lines_added",
            "lines_deleted",
            "total_changes",
            "change_entropy",
            "hour_of_day",
            "day_of_week",
            "is_weekend",
            "commit_velocity",
            "repo_stars",
            "repo_age_days",
            "primary_language",
            "author_green_rate",
            "repo_green_rate",
            "is_green_aware",
        ]

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()

            for feature in features:
                row = {
                    "message_length": feature.message_length,
                    "word_count": feature.word_count,
                    "unique_word_ratio": feature.unique_word_ratio,
                    "avg_word_length": feature.avg_word_length,
                    "has_green_keywords": int(feature.has_green_keywords),
                    "keyword_count": feature.keyword_count,
                    "keyword_density": feature.keyword_density,
                    "files_changed": feature.files_changed,
                    "lines_added": feature.lines_added,
                    "lines_deleted": feature.lines_deleted,
                    "total_changes": feature.total_changes,
                    "change_entropy": feature.change_entropy,
                    "hour_of_day": feature.hour_of_day,
                    "day_of_week": feature.day_of_week,
                    "is_weekend": int(feature.is_weekend),
                    "commit_velocity": feature.commit_velocity,
                    "repo_stars": feature.repo_stars,
                    "repo_age_days": feature.repo_age_days,
                    "primary_language": feature.primary_language,
                    "author_green_rate": feature.author_green_rate,
                    "repo_green_rate": feature.repo_green_rate,
                    "is_green_aware": (
                        int(feature.is_green_aware) if feature.is_green_aware is not None else ""
                    ),
                }
                writer.writerow(row)

    def get_feature_importance_guide(self) -> Dict:
        """
        Guide for interpreting feature importance in ML models.

        Returns:
            Dictionary describing each feature and expected importance
        """
        return {
            "text_features": {
                "keyword_density": "HIGH - Direct indicator of green awareness",
                "keyword_count": "HIGH - Number of green terms",
                "has_green_keywords": "MEDIUM - Binary presence indicator",
                "message_length": "LOW - General text characteristic",
                "unique_word_ratio": "LOW - Vocabulary diversity",
            },
            "code_features": {
                "total_changes": "MEDIUM - Refactoring indicator",
                "change_entropy": "LOW - Change distribution",
                "files_changed": "LOW - Scope of change",
            },
            "temporal_features": {
                "commit_velocity": "LOW - Development pace",
                "hour_of_day": "VERY_LOW - Time of commit",
                "day_of_week": "VERY_LOW - Day of commit",
            },
            "repository_features": {
                "repo_stars": "LOW - Project popularity",
                "repo_age_days": "LOW - Project maturity",
                "primary_language": "MEDIUM - Language-specific patterns",
            },
            "historical_features": {
                "author_green_rate": "HIGH - Author green awareness history",
                "repo_green_rate": "HIGH - Repository green culture",
            },
        }

    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string to datetime."""
        if not date_str:
            return datetime.now()

        try:
            if isinstance(date_str, datetime):
                return date_str
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.now()
