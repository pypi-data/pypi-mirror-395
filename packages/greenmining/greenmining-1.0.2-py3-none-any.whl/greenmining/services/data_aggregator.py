"""Data aggregator for green microservices analysis results."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import pandas as pd

from greenmining.analyzers import (
    EnhancedStatisticalAnalyzer,
    TemporalAnalyzer,
    QualitativeAnalyzer,
)
from greenmining.config import get_config
from greenmining.models.repository import Repository
from greenmining.utils import (
    colored_print,
    format_number,
    format_percentage,
    load_json_file,
    print_banner,
    save_csv_file,
    save_json_file,
)


class DataAggregator:
    """Aggregates analysis results and generates statistics."""

    def __init__(
        self,
        enable_enhanced_stats: bool = False,
        enable_temporal: bool = False,
        temporal_granularity: str = "quarter",
    ):
        """Initialize aggregator.

        Args:
            enable_enhanced_stats: Enable enhanced statistical analysis
            enable_temporal: Enable temporal trend analysis
            temporal_granularity: Granularity for temporal analysis (day/week/month/quarter/year)
        """
        self.enable_enhanced_stats = enable_enhanced_stats
        self.enable_temporal = enable_temporal

        if self.enable_enhanced_stats:
            self.statistical_analyzer = EnhancedStatisticalAnalyzer()
            colored_print("Enhanced statistical analysis enabled", "cyan")
        else:
            self.statistical_analyzer = None

        if self.enable_temporal:
            self.temporal_analyzer = TemporalAnalyzer(granularity=temporal_granularity)
            colored_print(
                f"Temporal analysis enabled (granularity: {temporal_granularity})", "cyan"
            )
        else:
            self.temporal_analyzer = None

    def aggregate(
        self, analysis_results: list[dict[str, Any]], repositories: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Aggregate analysis results into summary statistics.

        Args:
            analysis_results: List of commit analysis results
            repositories: List of repository metadata

        Returns:
            Aggregated statistics dictionary
        """
        colored_print("\nAggregating analysis results...", "cyan")

        # Summary statistics
        summary = self._generate_summary(analysis_results, repositories)

        # Known patterns analysis
        known_patterns = self._analyze_known_patterns(analysis_results)

        # Emergent patterns (placeholder)
        emergent_patterns = self._analyze_emergent_patterns(analysis_results)

        # Per-repository statistics
        per_repo_stats = self._generate_repo_stats(analysis_results, repositories)

        # Per-language statistics
        per_language_stats = self._generate_language_stats(analysis_results, repositories)

        # Enhanced statistical analysis (if enabled)
        enhanced_stats = None
        if self.enable_enhanced_stats and len(analysis_results) > 0:
            try:
                enhanced_stats = self._generate_enhanced_statistics(analysis_results)
                colored_print("✅ Enhanced statistical analysis complete", "green")
            except Exception as e:
                colored_print(f"⚠️  Enhanced statistics failed: {e}", "yellow")
                enhanced_stats = {"error": str(e)}

        # Temporal trend analysis (if enabled)
        temporal_analysis = None
        if self.enable_temporal and len(analysis_results) > 0:
            try:
                # Convert analysis results to commits format for temporal analyzer
                commits = [
                    {
                        "hash": r.get("commit_hash", "unknown"),
                        "date": r.get("date"),
                        "message": r.get("message", ""),
                        "repository": r.get("repository", "unknown"),
                    }
                    for r in analysis_results
                ]

                temporal_analysis = self.temporal_analyzer.analyze_trends(commits, analysis_results)
                colored_print("✅ Temporal trend analysis complete", "green")
            except Exception as e:
                colored_print(f"⚠️  Temporal analysis failed: {e}", "yellow")
                temporal_analysis = {"error": str(e)}

        result = {
            "summary": summary,
            "known_patterns": known_patterns,
            "emergent_patterns": emergent_patterns,
            "per_repo_stats": per_repo_stats,
            "per_language_stats": per_language_stats,
        }

        if enhanced_stats:
            result["enhanced_statistics"] = enhanced_stats

        if temporal_analysis:
            result["temporal_analysis"] = temporal_analysis

        return result

    def _generate_summary(
        self, results: list[dict[str, Any]], repos: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Generate overall summary statistics."""
        total_commits = len(results)
        green_aware_count = sum(1 for r in results if r.get("green_aware", False))

        # Count repos with at least one green commit
        repos_with_green = len({r["repository"] for r in results if r.get("green_aware", False)})

        return {
            "total_commits": total_commits,
            "green_aware_count": green_aware_count,
            "green_aware_percentage": (
                round(green_aware_count / total_commits * 100, 2) if total_commits > 0 else 0
            ),
            "repos_with_green_commits": repos_with_green,
            "total_repos": len(repos),
        }

    def _analyze_known_patterns(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Analyze known green software patterns."""
        pattern_data = defaultdict(
            lambda: {"count": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "example_commits": []}
        )

        for result in results:
            # Handle both gsf_patterns_matched (list) and known_pattern (string)
            patterns = result.get("gsf_patterns_matched", [])
            if not patterns:  # Fallback to old format
                pattern = result.get("known_pattern")
                if pattern and pattern != "NONE DETECTED":
                    patterns = [pattern]

            confidence = result.get("confidence", result.get("pattern_confidence", "low")).upper()

            for pattern in patterns:
                pattern_data[pattern]["count"] += 1
                if confidence in ["HIGH", "MEDIUM", "LOW"]:
                    pattern_data[pattern][confidence] += 1

                # Store example commits (max 3)
                if len(pattern_data[pattern]["example_commits"]) < 3:
                    commit_id = result.get("commit_hash", result.get("commit_id", "unknown"))
                    pattern_data[pattern]["example_commits"].append(commit_id)

        # Convert to list format
        patterns_list = []
        total_patterns = sum(p["count"] for p in pattern_data.values())

        for pattern_name, data in sorted(
            pattern_data.items(), key=lambda x: x[1]["count"], reverse=True
        ):
            patterns_list.append(
                {
                    "pattern_name": pattern_name,
                    "count": data["count"],
                    "percentage": (
                        round(data["count"] / total_patterns * 100, 1) if total_patterns > 0 else 0
                    ),
                    "confidence_breakdown": {
                        "HIGH": data["HIGH"],
                        "MEDIUM": data["MEDIUM"],
                        "LOW": data["LOW"],
                    },
                    "example_commits": data["example_commits"],
                }
            )

        return patterns_list

    def _analyze_emergent_patterns(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Analyze emergent patterns (placeholder for manual review)."""
        emergent = []

        for result in results:
            if result.get("emergent_pattern") and result["emergent_pattern"] != "NONE":
                emergent.append(
                    {
                        "pattern_name": "Novel pattern detected",
                        "count": 1,
                        "description": result["emergent_pattern"],
                        "example_commits": [result["commit_id"]],
                    }
                )

        return emergent

    def _generate_repo_stats(
        self, results: list[dict[str, Any]], repos: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Generate per-repository statistics."""
        repo_commits = defaultdict(list)

        # Group commits by repository
        for result in results:
            repo_commits[result["repository"]].append(result)

        # Calculate stats for each repo
        repo_stats = []
        for repo_name, commits in repo_commits.items():
            green_commits = [c for c in commits if c.get("green_aware", False)]
            # Get all patterns from commits (gsf_patterns_matched is a list)
            patterns = []
            for c in commits:
                patterns_list = c.get("gsf_patterns_matched", [])
                if not patterns_list:  # Fallback
                    pattern = c.get("known_pattern")
                    if pattern and pattern != "NONE DETECTED":
                        patterns_list = [pattern]
                patterns.extend(patterns_list)
            unique_patterns = list(set(patterns))

            repo_stats.append(
                {
                    "repo_name": repo_name,
                    "total_commits": len(commits),
                    "green_commits": len(green_commits),
                    "percentage": (
                        round(len(green_commits) / len(commits) * 100, 1) if commits else 0
                    ),
                    "patterns": unique_patterns,
                }
            )

        # Sort by percentage descending
        repo_stats.sort(key=lambda x: x["percentage"], reverse=True)

        return repo_stats

    def _generate_language_stats(
        self, results: list[dict[str, Any]], repos: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Generate per-language statistics."""
        # Create repo name to language mapping (handle both Repository objects and dicts)
        repo_language_map = {}
        for repo in repos:
            if isinstance(repo, Repository):
                repo_language_map[repo.full_name] = repo.language or "Unknown"
            else:
                repo_language_map[repo["full_name"]] = repo.get("language", "Unknown")

        # Group commits by language
        language_commits = defaultdict(list)
        for result in results:
            language = repo_language_map.get(result["repository"], "Unknown")
            language_commits[language].append(result)

        # Calculate stats for each language
        language_stats = []
        for language, commits in language_commits.items():
            green_commits = [c for c in commits if c.get("green_aware", False)]

            language_stats.append(
                {
                    "language": language,
                    "total_commits": len(commits),
                    "green_commits": len(green_commits),
                    "percentage": (
                        round(len(green_commits) / len(commits) * 100, 1) if commits else 0
                    ),
                }
            )

        # Sort by total commits descending
        language_stats.sort(key=lambda x: x["total_commits"], reverse=True)

        return language_stats

    def _generate_enhanced_statistics(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate enhanced statistical analysis.

        Args:
            results: List of commit analysis results

        Returns:
            Dictionary with enhanced statistical analysis
        """
        # Prepare DataFrame
        df = pd.DataFrame(results)

        # Ensure required columns exist
        if "date" not in df.columns or "green_aware" not in df.columns:
            return {"error": "Missing required columns for enhanced statistics"}

        enhanced_stats = {}

        # 1. Temporal Trend Analysis
        if len(df) >= 8:  # Need at least 8 data points
            try:
                df_copy = df.copy()
                df_copy["commit_hash"] = df_copy.get("commit_hash", df_copy.index)
                trends = self.statistical_analyzer.temporal_trend_analysis(df_copy)
                enhanced_stats["temporal_trends"] = {
                    "trend_direction": trends["trend"]["direction"],
                    "correlation": float(trends["trend"]["correlation"]),
                    "p_value": float(trends["trend"]["p_value"]),
                    "significant": trends["trend"]["significant"],
                    "monthly_data_points": len(trends.get("monthly_data", {})),
                }
            except Exception as e:
                enhanced_stats["temporal_trends"] = {"error": str(e)}

        # 2. Pattern Correlation Analysis (if pattern columns exist)
        pattern_cols = [col for col in df.columns if col.startswith("pattern_")]
        if pattern_cols and len(pattern_cols) >= 2:
            try:
                correlations = self.statistical_analyzer.analyze_pattern_correlations(df)
                enhanced_stats["pattern_correlations"] = {
                    "significant_pairs_count": len(correlations["significant_pairs"]),
                    "significant_pairs": correlations["significant_pairs"][:5],  # Top 5
                    "interpretation": correlations["interpretation"],
                }
            except Exception as e:
                enhanced_stats["pattern_correlations"] = {"error": str(e)}

        # 3. Effect Size Analysis by Repository
        if "repository" in df.columns:
            try:
                # Group by repository
                green_rates_by_repo = df.groupby("repository")["green_aware"].mean()
                if len(green_rates_by_repo) >= 2:
                    # Compare top vs bottom half
                    sorted_rates = sorted(green_rates_by_repo.values)
                    mid_point = len(sorted_rates) // 2
                    group1 = sorted_rates[:mid_point]
                    group2 = sorted_rates[mid_point:]

                    if len(group1) > 0 and len(group2) > 0:
                        effect = self.statistical_analyzer.effect_size_analysis(
                            list(group1), list(group2)
                        )
                        enhanced_stats["effect_size"] = {
                            "cohens_d": float(effect["cohens_d"]),
                            "magnitude": effect["magnitude"],
                            "mean_difference": float(effect["mean_difference"]),
                            "significant": effect["significant"],
                            "comparison": "high_green_vs_low_green_repos",
                        }
            except Exception as e:
                enhanced_stats["effect_size"] = {"error": str(e)}

        # 4. Basic descriptive statistics
        enhanced_stats["descriptive"] = {
            "total_commits": len(df),
            "green_commits": int(df["green_aware"].sum()),
            "green_rate_mean": float(df["green_aware"].mean()),
            "green_rate_std": float(df["green_aware"].std()) if len(df) > 1 else 0.0,
            "unique_repositories": (
                int(df["repository"].nunique()) if "repository" in df.columns else 0
            ),
        }

        return enhanced_stats

    def save_results(
        self,
        aggregated_data: dict[str, Any],
        json_file: Path,
        csv_file: Path,
        analysis_results: list[dict[str, Any]],
    ):
        """Save aggregated results to JSON and CSV files.

        Args:
            aggregated_data: Aggregated statistics
            json_file: JSON output file path
            csv_file: CSV output file path
            analysis_results: Original analysis results for CSV
        """
        # Save JSON
        save_json_file(aggregated_data, json_file)
        colored_print(f"Saved aggregated statistics to {json_file}", "green")

        # Create CSV with one row per commit
        csv_data = []
        for result in analysis_results:
            csv_data.append(
                {
                    "commit_hash": result.get("commit_hash", result.get("commit_id", "")),
                    "repo_name": result.get("repository", ""),
                    "date": result.get("date", ""),
                    "message": result.get("message", "")[:200],  # Truncate
                    "green_aware": result.get("green_aware", False),
                    "gsf_patterns": ", ".join(result.get("gsf_patterns_matched", [])),
                    "pattern_count": result.get("pattern_count", 0),
                    "confidence": result.get("confidence", ""),
                    "lines_added": result.get("lines_added", 0),
                    "lines_deleted": result.get("lines_deleted", 0),
                }
            )

        df = pd.DataFrame(csv_data)
        save_csv_file(df, csv_file)
        colored_print(f"Saved detailed results to {csv_file}", "green")

    def print_summary(self, aggregated_data: dict[str, Any]):
        """Print summary to console."""
        from tabulate import tabulate

        summary = aggregated_data["summary"]

        colored_print("\n" + "=" * 60, "cyan")
        colored_print("📊 AGGREGATED STATISTICS SUMMARY", "cyan")
        colored_print("=" * 60, "cyan")

        # Overall summary
        colored_print("\n📈 Overall Statistics:", "blue")
        summary_table = [
            ["Total Commits Analyzed", format_number(summary["total_commits"])],
            [
                "Green-Aware Commits",
                f"{format_number(summary['green_aware_count'])} ({format_percentage(summary['green_aware_percentage'])})",
            ],
            ["Total Repositories", format_number(summary["total_repos"])],
            ["Repos with Green Commits", format_number(summary["repos_with_green_commits"])],
        ]
        print(tabulate(summary_table, tablefmt="simple"))

        # Top patterns
        if aggregated_data["known_patterns"]:
            colored_print("\n🎯 Top Green Patterns Detected:", "blue")
            pattern_table = []
            for pattern in aggregated_data["known_patterns"][:10]:
                pattern_table.append(
                    [
                        pattern["pattern_name"],
                        format_number(pattern["count"]),
                        format_percentage(pattern["percentage"]),
                        f"H:{pattern['confidence_breakdown']['HIGH']} M:{pattern['confidence_breakdown']['MEDIUM']} L:{pattern['confidence_breakdown']['LOW']}",
                    ]
                )
            print(
                tabulate(
                    pattern_table,
                    headers=["Pattern", "Count", "%", "Confidence"],
                    tablefmt="simple",
                )
            )

        # Top repositories
        if aggregated_data["per_repo_stats"]:
            colored_print("\n🏆 Top 10 Greenest Repositories:", "blue")
            repo_table = []
            for repo in aggregated_data["per_repo_stats"][:10]:
                repo_table.append(
                    [
                        repo["repo_name"][:50],
                        format_number(repo["total_commits"]),
                        format_number(repo["green_commits"]),
                        format_percentage(repo["percentage"]),
                    ]
                )
            print(
                tabulate(
                    repo_table, headers=["Repository", "Total", "Green", "%"], tablefmt="simple"
                )
            )

        # Language breakdown
        if aggregated_data["per_language_stats"]:
            colored_print("\n💻 Language Breakdown:", "blue")
            lang_table = []
            for lang in aggregated_data["per_language_stats"]:
                lang_table.append(
                    [
                        lang["language"],
                        format_number(lang["total_commits"]),
                        format_number(lang["green_commits"]),
                        format_percentage(lang["percentage"]),
                    ]
                )
            print(
                tabulate(lang_table, headers=["Language", "Total", "Green", "%"], tablefmt="simple")
            )


@click.command()
@click.option(
    "--analysis-file",
    default=None,
    help="Input analysis file (default: data/analysis_results.json)",
)
@click.option(
    "--repos-file", default=None, help="Input repositories file (default: data/repositories.json)"
)
@click.option(
    "--output-json",
    default=None,
    help="Output JSON file (default: data/aggregated_statistics.json)",
)
@click.option(
    "--output-csv", default=None, help="Output CSV file (default: data/green_analysis_results.csv)"
)
@click.option("--config-file", default=".env", help="Path to .env configuration file")
def aggregate(
    analysis_file: Optional[str],
    repos_file: Optional[str],
    output_json: Optional[str],
    output_csv: Optional[str],
    config_file: str,
):
    """Aggregate analysis results and generate statistics."""
    print_banner("Data Aggregator")

    try:
        # Load configuration
        config = get_config(config_file)

        # Determine input/output files
        analysis_input = Path(analysis_file) if analysis_file else config.ANALYSIS_FILE
        repos_input = Path(repos_file) if repos_file else config.REPOS_FILE
        json_output = Path(output_json) if output_json else config.AGGREGATED_FILE
        csv_output = Path(output_csv) if output_csv else config.CSV_FILE

        # Check if input files exist
        if not analysis_input.exists():
            colored_print(f"Analysis file not found: {analysis_input}", "red")
            colored_print("Please run 'analyze' command first", "yellow")
            exit(1)

        if not repos_input.exists():
            colored_print(f"Repositories file not found: {repos_input}", "red")
            colored_print("Please run 'fetch' command first", "yellow")
            exit(1)

        # Load data
        colored_print(f"Loading analysis results from {analysis_input}...", "blue")
        analysis_data = load_json_file(analysis_input)
        analysis_results = analysis_data.get("results", [])

        colored_print(f"Loading repositories from {repos_input}...", "blue")
        repos_data = load_json_file(repos_input)
        repositories = repos_data.get("repositories", [])

        if not analysis_results:
            colored_print("No analysis results found", "yellow")
            exit(1)

        colored_print(
            f"Loaded {len(analysis_results)} analysis results and {len(repositories)} repositories",
            "green",
        )

        # Initialize aggregator
        aggregator = DataAggregator()

        # Aggregate data
        aggregated_data = aggregator.aggregate(analysis_results, repositories)

        # Save results
        aggregator.save_results(aggregated_data, json_output, csv_output, analysis_results)

        # Print summary
        aggregator.print_summary(aggregated_data)

        colored_print("\n✓ Aggregation complete!", "green")
        colored_print(f"JSON output: {json_output}", "green")
        colored_print(f"CSV output: {csv_output}", "green")

    except FileNotFoundError as e:
        colored_print(f"File not found: {e}", "red")
        exit(1)
    except json.JSONDecodeError as e:
        colored_print(f"Invalid JSON: {e}", "red")
        exit(1)
    except Exception as e:
        colored_print(f"Error: {e}", "red")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    aggregate()
