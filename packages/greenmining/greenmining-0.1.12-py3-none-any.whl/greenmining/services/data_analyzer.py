"""Data analyzer for green microservices commits using GSF patterns."""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

import click
from tqdm import tqdm

from greenmining.config import get_config
from greenmining.gsf_patterns import (
    GREEN_KEYWORDS,
    GSF_PATTERNS,
    get_pattern_by_keywords,
    is_green_aware,
)
from greenmining.utils import (
    colored_print,
    create_checkpoint,
    format_timestamp,
    load_checkpoint,
    load_json_file,
    print_banner,
    save_json_file,
)


class DataAnalyzer:
    """Analyzes commits for green software patterns using GSF (Green Software Foundation) patterns."""

    def __init__(self, batch_size: int = 10):
        """Initialize analyzer with GSF patterns.

        Args:
            batch_size: Number of commits to process in each batch
        """
        # Use GSF patterns from gsf_patterns.py
        self.gsf_patterns = GSF_PATTERNS
        self.green_keywords = GREEN_KEYWORDS
        self.batch_size = batch_size

    def analyze_commits(
        self, commits: list[dict[str, Any]], resume_from: int = 0
    ) -> list[dict[str, Any]]:
        """Analyze commits for green software practices.

        Args:
            commits: List of commit dictionaries
            resume_from: Index to resume from

        Returns:
            List of analysis results
        """
        results = []

        colored_print(f"\nAnalyzing {len(commits)} commits for green practices...", "cyan")

        with tqdm(
            total=len(commits), initial=resume_from, desc="Analyzing commits", unit="commit"
        ) as pbar:
            for _idx, commit in enumerate(commits[resume_from:], start=resume_from):
                try:
                    analysis = self._analyze_commit(commit)
                    results.append(analysis)
                    pbar.update(1)
                except Exception as e:
                    colored_print(
                        f"\nError analyzing commit {commit.get('commit_id', 'unknown')}: {e}",
                        "yellow",
                    )
                    pbar.update(1)

        return results

    def _analyze_commit(self, commit: dict[str, Any]) -> dict[str, Any]:
        """Analyze a single commit using GSF patterns.

        Args:
            commit: Commit dictionary

        Returns:
            Analysis result with GSF pattern matching
        """
        message = commit.get("message", "")

        # Q1: GREEN AWARENESS - Check using GSF keywords
        green_aware = is_green_aware(message)

        # Q2: KNOWN GSF PATTERNS - Match against Green Software Foundation patterns
        matched_patterns = get_pattern_by_keywords(message)

        # Get detailed pattern info
        pattern_details = []
        for _pattern_id, pattern in self.gsf_patterns.items():
            if pattern["name"] in matched_patterns:
                pattern_details.append(
                    {
                        "name": pattern["name"],
                        "category": pattern["category"],
                        "description": pattern["description"],
                        "sci_impact": pattern["sci_impact"],
                    }
                )

        # Calculate confidence based on number of patterns matched
        confidence = (
            "high"
            if len(matched_patterns) >= 2
            else "medium" if len(matched_patterns) == 1 else "low"
        )

        return {
            "commit_hash": commit.get("hash", commit.get("commit_id", "unknown")),
            "repository": commit.get("repository", commit.get("repo_name", "unknown")),
            "author": commit.get("author", commit.get("author_name", "unknown")),
            "date": commit.get("date", commit.get("author_date", "unknown")),
            "message": message,
            # Research Question 1: Green awareness
            "green_aware": green_aware,
            # Research Question 2: Known GSF patterns
            "gsf_patterns_matched": matched_patterns,
            "pattern_count": len(matched_patterns),
            "pattern_details": pattern_details,
            "confidence": confidence,
            # Additional metadata
            "files_modified": commit.get("files_changed", commit.get("modified_files", [])),
            "insertions": commit.get("lines_added", commit.get("insertions", 0)),
            "deletions": commit.get("lines_deleted", commit.get("deletions", 0)),
        }

    def _check_green_awareness(self, message: str, files: list[str]) -> tuple[bool, Optional[str]]:
        """Check if commit explicitly mentions green/energy concerns.

        Args:
            message: Commit message (lowercase)
            files: List of changed files (lowercase)

        Returns:
            Tuple of (is_green_aware, evidence_text)
        """
        # Check message for green keywords
        for keyword in self.GREEN_KEYWORDS:
            if keyword in message:
                # Extract context around keyword
                pattern = rf".{{0,30}}{re.escape(keyword)}.{{0,30}}"
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    evidence = match.group(0).strip()
                    return True, f"Keyword '{keyword}': {evidence}"

        # Check file names for patterns
        cache_files = [f for f in files if "cache" in f or "redis" in f]
        if cache_files:
            return True, f"Modified cache-related file: {cache_files[0]}"

        perf_files = [f for f in files if "performance" in f or "optimization" in f]
        if perf_files:
            return True, f"Modified performance file: {perf_files[0]}"

        return False, None

    def _detect_known_pattern(self, message: str, files: list[str]) -> tuple[Optional[str], str]:
        """Detect known green software pattern.

        Args:
            message: Commit message (lowercase)
            files: List of changed files (lowercase)

        Returns:
            Tuple of (pattern_name, confidence_level)
        """
        matches = []

        # Check each pattern
        for pattern_name, keywords in self.GREEN_PATTERNS.items():
            for keyword in keywords:
                if keyword in message:
                    # Calculate confidence based on specificity
                    confidence = "HIGH" if len(keyword) > 10 else "MEDIUM"
                    matches.append((pattern_name, confidence, len(keyword)))

        # Check file names for pattern hints
        all_files = " ".join(files)
        for pattern_name, keywords in self.GREEN_PATTERNS.items():
            for keyword in keywords:
                if keyword in all_files:
                    matches.append((pattern_name, "MEDIUM", len(keyword)))

        if not matches:
            return "NONE DETECTED", "NONE"

        # Return most specific match (longest keyword)
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches[0][0], matches[0][1]

    def save_results(self, results: list[dict[str, Any]], output_file: Path):
        """Save analysis results to JSON file.

        Args:
            results: List of analysis results
            output_file: Output file path
        """
        # Calculate summary statistics
        green_aware_count = sum(1 for r in results if r["green_aware"])

        # Count all matched patterns (results have gsf_patterns_matched which is a list)
        all_patterns = []
        for r in results:
            patterns = r.get("gsf_patterns_matched", [])
            if patterns:  # If there are matched patterns
                all_patterns.extend(patterns)

        pattern_counts = Counter(all_patterns)

        data = {
            "metadata": {
                "analyzed_at": format_timestamp(),
                "total_commits_analyzed": len(results),
                "green_aware_commits": green_aware_count,
                "green_aware_percentage": (
                    round(green_aware_count / len(results) * 100, 2) if results else 0
                ),
                "analyzer_type": "keyword_heuristic",
                "note": "This analysis uses keyword and heuristic matching. For AI-powered analysis, use Claude API.",
            },
            "results": results,
        }

        save_json_file(data, output_file)
        colored_print(f"Saved analysis for {len(results)} commits to {output_file}", "green")

        # Display summary
        colored_print("\n📊 Analysis Summary:", "cyan")
        colored_print(
            f"  Green-aware commits: {green_aware_count} ({data['metadata']['green_aware_percentage']}%)",
            "white",
        )
        if pattern_counts:
            colored_print("\n  Top patterns detected:", "cyan")
            for pattern, count in pattern_counts.most_common(5):
                colored_print(f"    - {pattern}: {count}", "white")


@click.command()
@click.option("--batch-size", default=10, help="Batch size for processing")
@click.option("--resume", is_flag=True, help="Resume from checkpoint")
@click.option(
    "--commits-file", default=None, help="Input commits file (default: data/commits.json)"
)
@click.option(
    "--output", default=None, help="Output file path (default: data/analysis_results.json)"
)
@click.option("--config-file", default=".env", help="Path to .env configuration file")
def analyze(
    batch_size: int,
    resume: bool,
    commits_file: Optional[str],
    output: Optional[str],
    config_file: str,
):
    """Analyze commits for green software practices."""
    print_banner("Data Analyzer")

    try:
        # Load configuration
        config = get_config(config_file)

        # Determine input/output files
        input_file = Path(commits_file) if commits_file else config.COMMITS_FILE
        output_file = Path(output) if output else config.ANALYSIS_FILE

        # Check if input file exists
        if not input_file.exists():
            colored_print(f"Input file not found: {input_file}", "red")
            colored_print("Please run 'extract' command first to extract commits", "yellow")
            exit(1)

        # Load commits
        colored_print(f"Loading commits from {input_file}...", "blue")
        data = load_json_file(input_file)
        commits = data.get("commits", [])

        if not commits:
            colored_print("No commits found in input file", "yellow")
            exit(1)

        colored_print(f"Loaded {len(commits)} commits", "green")

        # Check for resume
        resume_from = 0
        if resume:
            checkpoint_data = load_checkpoint(config.CHECKPOINT_FILE)
            if checkpoint_data:
                resume_from = checkpoint_data.get("processed_count", 0)
                colored_print(
                    f"Resuming from checkpoint: {resume_from} commits processed", "yellow"
                )

        # Initialize analyzer
        analyzer = DataAnalyzer(batch_size=batch_size)

        # Analyze commits
        results = analyzer.analyze_commits(commits, resume_from=resume_from)

        if not results:
            colored_print("No analysis results generated", "yellow")
            exit(1)

        # Save results
        analyzer.save_results(results, output_file)

        # Save checkpoint
        create_checkpoint(
            config.CHECKPOINT_FILE,
            {"processed_count": len(results), "timestamp": format_timestamp()},
        )

        colored_print(f"\n✓ Successfully analyzed {len(results)} commits", "green")
        colored_print(f"Output saved to: {output_file}", "green")

    except FileNotFoundError as e:
        colored_print(f"File not found: {e}", "red")
        exit(1)
    except json.JSONDecodeError:
        colored_print(f"Invalid JSON in input file: {input_file}", "red")
        exit(1)
    except Exception as e:
        colored_print(f"Error: {e}", "red")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    analyze()
