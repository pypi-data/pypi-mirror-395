"""
Qualitative Analysis Framework for Pattern Validation

Implements qualitative validation from Soliman et al. (2017):
- Stratified random sampling for manual validation
- Precision/recall calculation framework
- Inter-rater reliability support
- False positive/negative tracking

Based on Soliman et al.: 42/151 studies used qualitative analysis
Critical for: validating IR-based approaches, calculating accuracy metrics
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json


@dataclass
class ValidationSample:
    """Represents a single validation sample"""

    commit_sha: str
    commit_message: str
    code_diff: Optional[str]
    repository: str
    detected_patterns: List[str]
    detection_method: str  # 'keyword', 'nlp', 'code_diff'
    validation_status: Optional[str] = None  # 'pending', 'validated', 'rejected'
    true_label: Optional[bool] = None  # Ground truth after manual review
    reviewer: Optional[str] = None
    review_notes: Optional[str] = None


@dataclass
class ValidationMetrics:
    """Precision/recall metrics for validation"""

    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    precision: float
    recall: float
    f1_score: float
    accuracy: float


class QualitativeAnalyzer:
    """
    Framework for manual validation and qualitative analysis.

    Implements:
    1. Stratified sampling (ensure representation across categories)
    2. Validation workflow (export → review → import → calculate metrics)
    3. Precision/recall calculation
    4. Inter-rater reliability (if multiple reviewers)

    Based on Soliman et al.: "42 studies used qualitative analysis for validation"
    """

    def __init__(self, sample_size: int = 30, stratify_by: str = "pattern"):
        """
        Initialize qualitative analyzer.

        Args:
            sample_size: Number of commits to sample for validation
            stratify_by: Stratification method ('pattern', 'repository', 'time', 'random')
        """
        self.sample_size = sample_size
        self.stratify_by = stratify_by
        self.samples: List[ValidationSample] = []

    def generate_validation_samples(
        self, commits: List[Dict], analysis_results: List[Dict], include_negatives: bool = True
    ) -> List[ValidationSample]:
        """
        Generate stratified validation samples.

        Args:
            commits: All commits
            analysis_results: Pattern detection results
            include_negatives: Include non-green commits for false negative detection

        Returns:
            List of ValidationSample objects
        """
        # Build commit lookup
        commit_lookup = {c.get("hash", c.get("sha")): c for c in commits}

        # Separate positives (detected as green) and negatives
        positives = [r for r in analysis_results if r.get("is_green_aware", False)]
        negatives = [r for r in analysis_results if not r.get("is_green_aware", False)]

        samples = []

        # Calculate sample distribution
        if include_negatives:
            # 80% positives, 20% negatives (to check false negatives)
            pos_sample_size = int(self.sample_size * 0.8)
            neg_sample_size = self.sample_size - pos_sample_size
        else:
            pos_sample_size = self.sample_size
            neg_sample_size = 0

        # Sample positives (stratified by pattern or repository)
        if self.stratify_by == "pattern":
            pos_samples = self._stratified_sample_by_pattern(positives, pos_sample_size)
        elif self.stratify_by == "repository":
            pos_samples = self._stratified_sample_by_repo(positives, commit_lookup, pos_sample_size)
        else:
            pos_samples = random.sample(positives, min(pos_sample_size, len(positives)))

        # Sample negatives (random)
        if include_negatives and negatives:
            neg_samples = random.sample(negatives, min(neg_sample_size, len(negatives)))
        else:
            neg_samples = []

        # Create ValidationSample objects
        for result in pos_samples + neg_samples:
            commit_sha = result.get("commit_sha")
            commit = commit_lookup.get(commit_sha, {})

            sample = ValidationSample(
                commit_sha=commit_sha,
                commit_message=commit.get("message", result.get("commit_message", "")),
                code_diff=result.get("code_diff"),
                repository=commit.get("repository", result.get("repository", "")),
                detected_patterns=result.get("patterns_detected", []),
                detection_method=result.get("detection_method", "keyword"),
                validation_status="pending",
            )
            samples.append(sample)

        self.samples = samples
        return samples

    def _stratified_sample_by_pattern(self, results: List[Dict], sample_size: int) -> List[Dict]:
        """Stratified sampling ensuring each pattern category is represented."""
        # Group by dominant pattern
        pattern_groups = defaultdict(list)
        for result in results:
            patterns = result.get("patterns_detected", [])
            if patterns:
                # Use first pattern as primary
                primary_pattern = patterns[0]
                pattern_groups[primary_pattern].append(result)

        # Calculate samples per pattern (proportional)
        total = len(results)
        samples = []

        for pattern, group in pattern_groups.items():
            proportion = len(group) / total
            pattern_sample_size = max(1, int(sample_size * proportion))
            pattern_samples = random.sample(group, min(pattern_sample_size, len(group)))
            samples.extend(pattern_samples)

        # If we have fewer than sample_size, add random extras
        if len(samples) < sample_size and len(samples) < len(results):
            remaining = [r for r in results if r not in samples]
            extra_needed = min(sample_size - len(samples), len(remaining))
            samples.extend(random.sample(remaining, extra_needed))

        return samples[:sample_size]

    def _stratified_sample_by_repo(
        self, results: List[Dict], commit_lookup: Dict, sample_size: int
    ) -> List[Dict]:
        """Stratified sampling ensuring each repository is represented."""
        # Group by repository
        repo_groups = defaultdict(list)
        for result in results:
            commit_sha = result.get("commit_sha")
            commit = commit_lookup.get(commit_sha, {})
            repo = commit.get("repository", result.get("repository", "unknown"))
            repo_groups[repo].append(result)

        # Sample proportionally from each repo
        samples = []
        total = len(results)

        for repo, group in repo_groups.items():
            proportion = len(group) / total
            repo_sample_size = max(1, int(sample_size * proportion))
            repo_samples = random.sample(group, min(repo_sample_size, len(group)))
            samples.extend(repo_samples)

        return samples[:sample_size]

    def export_samples_for_review(self, output_path: str) -> None:
        """
        Export validation samples to JSON for manual review.

        Args:
            output_path: Path to output JSON file
        """
        samples_data = []
        for i, sample in enumerate(self.samples, 1):
            samples_data.append(
                {
                    "sample_id": i,
                    "commit_sha": sample.commit_sha,
                    "repository": sample.repository,
                    "commit_message": sample.commit_message,
                    "detected_patterns": sample.detected_patterns,
                    "detection_method": sample.detection_method,
                    "code_diff_preview": sample.code_diff[:500] if sample.code_diff else None,
                    "validation_status": sample.validation_status,
                    "true_label": sample.true_label,
                    "reviewer": sample.reviewer,
                    "review_notes": sample.review_notes,
                    "___INSTRUCTIONS___": "Set true_label to true/false, add reviewer name, add review_notes",
                }
            )

        with open(output_path, "w") as f:
            json.dump(samples_data, f, indent=2)

    def import_validated_samples(self, input_path: str) -> None:
        """
        Import manually validated samples from JSON.

        Args:
            input_path: Path to JSON file with validated samples
        """
        with open(input_path, "r") as f:
            samples_data = json.load(f)

        # Update samples with validation results
        for data in samples_data:
            commit_sha = data["commit_sha"]

            # Find matching sample
            for sample in self.samples:
                if sample.commit_sha == commit_sha:
                    sample.true_label = data.get("true_label")
                    sample.reviewer = data.get("reviewer")
                    sample.review_notes = data.get("review_notes")
                    sample.validation_status = (
                        "validated" if sample.true_label is not None else "pending"
                    )
                    break

    def calculate_metrics(self) -> ValidationMetrics:
        """
        Calculate precision, recall, F1, and accuracy.

        Returns:
            ValidationMetrics object
        """
        # Count outcomes
        tp = 0  # True positive: detected as green, truly green
        fp = 0  # False positive: detected as green, not green
        tn = 0  # True negative: not detected, truly not green
        fn = 0  # False negative: not detected, but is green

        for sample in self.samples:
            if sample.true_label is None:
                continue  # Skip unvalidated samples

            detected_as_green = len(sample.detected_patterns) > 0
            truly_green = sample.true_label

            if detected_as_green and truly_green:
                tp += 1
            elif detected_as_green and not truly_green:
                fp += 1
            elif not detected_as_green and not truly_green:
                tn += 1
            elif not detected_as_green and truly_green:
                fn += 1

        # Calculate metrics
        total = tp + fp + tn + fn
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / total if total > 0 else 0

        return ValidationMetrics(
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            accuracy=round(accuracy, 4),
        )

    def get_validation_report(self) -> Dict:
        """
        Generate comprehensive validation report.

        Returns:
            Dictionary with validation statistics and metrics
        """
        validated_count = sum(1 for s in self.samples if s.validation_status == "validated")
        pending_count = sum(1 for s in self.samples if s.validation_status == "pending")

        metrics = self.calculate_metrics() if validated_count > 0 else None

        # Analyze false positives and false negatives
        false_positives = [
            {
                "commit_sha": s.commit_sha,
                "detected_patterns": s.detected_patterns,
                "review_notes": s.review_notes,
            }
            for s in self.samples
            if s.true_label is not None and len(s.detected_patterns) > 0 and not s.true_label
        ]

        false_negatives = [
            {
                "commit_sha": s.commit_sha,
                "commit_message": s.commit_message[:100],
                "review_notes": s.review_notes,
            }
            for s in self.samples
            if s.true_label is not None and len(s.detected_patterns) == 0 and s.true_label
        ]

        # Pattern accuracy breakdown
        pattern_accuracy = self._analyze_pattern_accuracy()

        return {
            "sampling": {
                "total_samples": len(self.samples),
                "validated_samples": validated_count,
                "pending_samples": pending_count,
                "validation_progress": (
                    round(validated_count / len(self.samples) * 100, 1) if self.samples else 0
                ),
                "stratification_method": self.stratify_by,
            },
            "metrics": {
                "precision": metrics.precision if metrics else None,
                "recall": metrics.recall if metrics else None,
                "f1_score": metrics.f1_score if metrics else None,
                "accuracy": metrics.accuracy if metrics else None,
                "true_positives": metrics.true_positives if metrics else None,
                "false_positives": metrics.false_positives if metrics else None,
                "true_negatives": metrics.true_negatives if metrics else None,
                "false_negatives": metrics.false_negatives if metrics else None,
            },
            "error_analysis": {
                "false_positive_count": len(false_positives),
                "false_negative_count": len(false_negatives),
                "false_positives": false_positives[:5],  # Top 5
                "false_negatives": false_negatives[:5],  # Top 5
            },
            "pattern_accuracy": pattern_accuracy,
        }

    def _analyze_pattern_accuracy(self) -> Dict:
        """Analyze accuracy per pattern category."""
        pattern_stats = defaultdict(lambda: {"tp": 0, "fp": 0})

        for sample in self.samples:
            if sample.true_label is None:
                continue

            for pattern in sample.detected_patterns:
                if sample.true_label:
                    pattern_stats[pattern]["tp"] += 1
                else:
                    pattern_stats[pattern]["fp"] += 1

        # Calculate precision per pattern
        pattern_accuracy = {}
        for pattern, stats in pattern_stats.items():
            total = stats["tp"] + stats["fp"]
            precision = stats["tp"] / total if total > 0 else 0
            pattern_accuracy[pattern] = {
                "true_positives": stats["tp"],
                "false_positives": stats["fp"],
                "precision": round(precision, 4),
            }

        return pattern_accuracy

    def get_inter_rater_reliability(
        self,
        samples_from_reviewer_a: List[ValidationSample],
        samples_from_reviewer_b: List[ValidationSample],
    ) -> Dict:
        """
        Calculate inter-rater reliability (Cohen's Kappa).

        Args:
            samples_from_reviewer_a: Samples validated by reviewer A
            samples_from_reviewer_b: Samples validated by reviewer B (same commits)

        Returns:
            Dictionary with Cohen's Kappa and agreement statistics
        """
        # Match samples by commit_sha
        matched_samples = []
        for sample_a in samples_from_reviewer_a:
            for sample_b in samples_from_reviewer_b:
                if sample_a.commit_sha == sample_b.commit_sha:
                    matched_samples.append((sample_a, sample_b))
                    break

        if not matched_samples:
            return {"error": "No matching samples between reviewers"}

        # Calculate agreement
        agreements = 0
        for sample_a, sample_b in matched_samples:
            if sample_a.true_label == sample_b.true_label:
                agreements += 1

        observed_agreement = agreements / len(matched_samples)

        # Calculate expected agreement (by chance)
        a_positive = sum(1 for s, _ in matched_samples if s.true_label)
        b_positive = sum(1 for _, s in matched_samples if s.true_label)
        n = len(matched_samples)

        p_a_yes = a_positive / n
        p_b_yes = b_positive / n
        expected_agreement = (p_a_yes * p_b_yes) + ((1 - p_a_yes) * (1 - p_b_yes))

        # Cohen's Kappa
        kappa = (
            (observed_agreement - expected_agreement) / (1 - expected_agreement)
            if expected_agreement < 1
            else 1
        )

        return {
            "cohens_kappa": round(kappa, 4),
            "observed_agreement": round(observed_agreement, 4),
            "expected_agreement": round(expected_agreement, 4),
            "sample_count": n,
            "interpretation": self._interpret_kappa(kappa),
        }

    def _interpret_kappa(self, kappa: float) -> str:
        """Interpret Cohen's Kappa value."""
        if kappa < 0:
            return "Poor (less than chance)"
        elif kappa < 0.20:
            return "Slight"
        elif kappa < 0.40:
            return "Fair"
        elif kappa < 0.60:
            return "Moderate"
        elif kappa < 0.80:
            return "Substantial"
        else:
            return "Almost perfect"
