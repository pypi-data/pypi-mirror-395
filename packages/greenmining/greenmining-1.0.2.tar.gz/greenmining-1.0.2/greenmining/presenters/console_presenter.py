"""Console Presenter - Handles console output formatting."""

from __future__ import annotations

from typing import Any, Dict, List

from tabulate import tabulate

from greenmining.utils import colored_print


class ConsolePresenter:
    """Presenter for console/terminal output."""

    @staticmethod
    def show_banner():
        """Display application banner."""
        banner = """
╔══════════════════════════════════════════════════════════╗
║           Green Microservices Mining                     ║
╚══════════════════════════════════════════════════════════╝
        """
        colored_print(banner, "green")

    @staticmethod
    def show_repositories(repositories: list[dict], limit: int = 10):
        """Display repository table."""
        if not repositories:
            colored_print("No repositories to display", "yellow")
            return

        colored_print(f"\n📊 Top {min(limit, len(repositories))} Repositories:\n", "cyan")

        table_data = []
        for repo in repositories[:limit]:
            table_data.append(
                [
                    repo.get("full_name", "N/A"),
                    repo.get("language", "N/A"),
                    f"{repo.get('stars', 0):,}",
                    (
                        repo.get("description", "")[:50] + "..."
                        if len(repo.get("description", "")) > 50
                        else repo.get("description", "")
                    ),
                ]
            )

        headers = ["Repository", "Language", "Stars", "Description"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    @staticmethod
    def show_commit_stats(stats: dict[str, Any]):
        """Display commit statistics."""
        colored_print("\n📈 Commit Statistics:\n", "cyan")

        table_data = [
            ["Total Commits", f"{stats.get('total_commits', 0):,}"],
            ["Repositories", stats.get("total_repos", 0)],
            ["Avg per Repo", f"{stats.get('avg_per_repo', 0):.1f}"],
            ["Date Range", stats.get("date_range", "N/A")],
        ]

        print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))

    @staticmethod
    def show_analysis_results(results: dict[str, Any]):
        """Display analysis results."""
        colored_print("\n🔬 Analysis Results:\n", "cyan")

        summary = results.get("summary", {})
        table_data = [
            ["Total Commits Analyzed", f"{summary.get('total_commits', 0):,}"],
            ["Green-Aware Commits", f"{summary.get('green_commits', 0):,}"],
            ["Green Rate", f"{summary.get('green_commit_rate', 0):.1%}"],
            ["Patterns Detected", len(results.get("known_patterns", {}))],
        ]

        print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))

    @staticmethod
    def show_pattern_distribution(patterns: dict[str, Any], limit: int = 10):
        """Display pattern distribution."""
        if not patterns:
            colored_print("No patterns to display", "yellow")
            return

        colored_print(f"\n🎯 Top {limit} Green Patterns:\n", "cyan")

        # Sort by count
        sorted_patterns = sorted(
            patterns.items(), key=lambda x: x[1].get("count", 0), reverse=True
        )[:limit]

        table_data = []
        for pattern_name, data in sorted_patterns:
            table_data.append(
                [
                    pattern_name,
                    data.get("count", 0),
                    f"{data.get('percentage', 0):.1f}%",
                    data.get("confidence_distribution", {}).get("HIGH", 0),
                ]
            )

        headers = ["Pattern", "Count", "Percentage", "High Confidence"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    @staticmethod
    def show_pipeline_status(status: dict[str, Any]):
        """Display pipeline status."""
        colored_print("\n⚙️  Pipeline Status:\n", "cyan")

        table_data = []
        for phase, info in status.items():
            status_icon = "✅" if info.get("completed") else "⏳"
            table_data.append(
                [status_icon, phase, info.get("file", "N/A"), info.get("size", "N/A")]
            )

        headers = ["Status", "Phase", "Output File", "Size"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    @staticmethod
    def show_progress_message(phase: str, current: int, total: int):
        """Display progress message."""
        percentage = (current / total * 100) if total > 0 else 0
        colored_print(f"[{phase}] Progress: {current}/{total} ({percentage:.1f}%)", "cyan")

    @staticmethod
    def show_error(message: str):
        """Display error message."""
        colored_print(f"❌ Error: {message}", "red")

    @staticmethod
    def show_success(message: str):
        """Display success message."""
        colored_print(f"✅ {message}", "green")

    @staticmethod
    def show_warning(message: str):
        """Display warning message."""
        colored_print(f"⚠️  Warning: {message}", "yellow")
