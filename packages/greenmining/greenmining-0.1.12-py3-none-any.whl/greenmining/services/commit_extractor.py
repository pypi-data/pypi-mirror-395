"""Commit extractor for green microservices mining."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import click
from github import Github
from tqdm import tqdm

from greenmining.config import get_config
from greenmining.utils import (
    colored_print,
    format_timestamp,
    load_json_file,
    print_banner,
    retry_on_exception,
    save_json_file,
)


class CommitExtractor:
    """Extracts commit data from repositories using GitHub API."""

    def __init__(
        self,
        max_commits: int = 50,
        skip_merges: bool = True,
        days_back: int = 730,
        github_token: str | None = None,
    ):
        """Initialize commit extractor.

        Args:
            max_commits: Maximum commits per repository
            skip_merges: Skip merge commits
            days_back: Only analyze commits from last N days
            github_token: GitHub API token (optional)
        """
        self.max_commits = max_commits
        self.skip_merges = skip_merges
        self.days_back = days_back
        self.cutoff_date = datetime.now() - timedelta(days=days_back)
        self.github = Github(github_token) if github_token else None

    def extract_from_repositories(self, repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract commits from list of repositories.

        Args:
            repositories: List of repository metadata

        Returns:
            List of commit data dictionaries
        """
        all_commits = []
        failed_repos = []

        colored_print(f"\nExtracting commits from {len(repositories)} repositories...", "cyan")
        colored_print(
            f"Settings: max_commits={self.max_commits}, skip_merges={self.skip_merges}, days_back={self.days_back}",
            "cyan",
        )

        with tqdm(total=len(repositories), desc="Processing repositories", unit="repo") as pbar:
            for repo in repositories:
                try:
                    commits = self._extract_repo_commits(repo)
                    all_commits.extend(commits)
                    pbar.set_postfix({"commits": len(all_commits), "failed": len(failed_repos)})
                    pbar.update(1)
                except Exception as e:
                    colored_print(f"\nError processing {repo['full_name']}: {e}", "yellow")
                    failed_repos.append(repo["full_name"])
                    pbar.update(1)

        if failed_repos:
            colored_print(f"\nFailed to process {len(failed_repos)} repositories:", "yellow")
            for repo_name in failed_repos[:5]:
                colored_print(f"  - {repo_name}", "yellow")
            if len(failed_repos) > 5:
                colored_print(f"  ... and {len(failed_repos) - 5} more", "yellow")

        return all_commits

    @retry_on_exception(max_retries=2, delay=5.0, exceptions=(Exception,))
    def _extract_repo_commits(self, repo: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract commits from a single repository using GitHub API.

        Args:
            repo: Repository metadata dictionary

        Returns:
            List of commit dictionaries
        """
        commits = []
        repo_name = repo["full_name"]

        try:
            # Get repository from GitHub API
            if not self.github:
                config = get_config()
                self.github = Github(config.GITHUB_TOKEN)

            gh_repo = self.github.get_repo(repo_name)

            # Get recent commits (GitHub API returns in reverse chronological order)
            commit_count = 0

            for commit in gh_repo.get_commits():
                # Skip if reached max commits
                if commit_count >= self.max_commits:
                    break

                # Skip merge commits if requested
                if self.skip_merges and len(commit.parents) > 1:
                    continue

                # Skip trivial commits
                commit_msg = commit.commit.message
                if not commit_msg or len(commit_msg.strip()) < 10:
                    continue

                # Extract commit data
                commit_data = self._extract_commit_metadata_from_github(commit, repo_name)
                commits.append(commit_data)
                commit_count += 1

        except Exception as e:
            colored_print(f"Error extracting commits from {repo_name}: {e}", "yellow")
            raise

        return commits

    def _extract_commit_metadata(self, commit, repo_name: str) -> dict[str, Any]:
        """Extract metadata from commit object.

        Args:
            commit: PyDriller commit object
            repo_name: Repository name

        Returns:
            Dictionary with commit metadata
        """
        # Get modified files
        files_changed = []
        lines_added = 0
        lines_deleted = 0

        try:
            for modified_file in commit.modified_files:
                files_changed.append(modified_file.filename)
                lines_added += modified_file.added_lines
                lines_deleted += modified_file.deleted_lines
        except Exception:
            pass

        return {
            "commit_id": commit.hash,
            "repo_name": repo_name,
            "date": commit.committer_date.isoformat(),
            "author": commit.author.name,
            "author_email": commit.author.email,
            "message": commit.msg.strip(),
            "files_changed": files_changed[:20],  # Limit to 20 files
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "insertions": lines_added,
            "deletions": lines_deleted,
            "is_merge": commit.merge,
            "branches": (
                list(commit.branches) if hasattr(commit, "branches") and commit.branches else []
            ),
            "in_main_branch": commit.in_main_branch if hasattr(commit, "in_main_branch") else True,
        }

    def _extract_commit_metadata_from_github(self, commit, repo_name: str) -> dict[str, Any]:
        """Extract metadata from GitHub API commit object.

        Args:
            commit: GitHub API commit object
            repo_name: Repository name

        Returns:
            Dictionary with commit metadata
        """
        # Get modified files and stats
        files_changed = []
        lines_added = 0
        lines_deleted = 0

        try:
            for file in commit.files:
                files_changed.append(file.filename)
                lines_added += file.additions
                lines_deleted += file.deletions
        except Exception:
            pass

        return {
            "commit_id": commit.sha,
            "repo_name": repo_name,
            "date": commit.commit.committer.date.isoformat(),
            "author": commit.commit.author.name,
            "author_email": commit.commit.author.email,
            "message": commit.commit.message.strip(),
            "files_changed": files_changed[:20],  # Limit to 20 files
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "insertions": lines_added,
            "deletions": lines_deleted,
            "is_merge": len(commit.parents) > 1,
            "branches": [],
            "in_main_branch": True,
        }

    def save_results(self, commits: list[dict[str, Any]], output_file: Path, repos_count: int):
        """Save extracted commits to JSON file.

        Args:
            commits: List of commit data
            output_file: Output file path
            repos_count: Number of repositories processed
        """
        data = {
            "metadata": {
                "extracted_at": format_timestamp(),
                "total_commits": len(commits),
                "total_repos": repos_count,
                "max_commits_per_repo": self.max_commits,
                "skip_merges": self.skip_merges,
                "days_back": self.days_back,
                "cutoff_date": self.cutoff_date.isoformat(),
            },
            "commits": commits,
        }

        save_json_file(data, output_file)
        colored_print(f"Saved {len(commits)} commits to {output_file}", "green")


@click.command()
@click.option("--max-commits", default=50, help="Maximum commits per repository")
@click.option("--skip-merges/--include-merges", default=True, help="Skip merge commits")
@click.option("--days-back", default=730, help="Only analyze commits from last N days")
@click.option(
    "--repos-file", default=None, help="Input repositories file (default: data/repositories.json)"
)
@click.option("--output", default=None, help="Output file path (default: data/commits.json)")
@click.option("--config-file", default=".env", help="Path to .env configuration file")
def extract(
    max_commits: int,
    skip_merges: bool,
    days_back: int,
    repos_file: Optional[str],
    output: Optional[str],
    config_file: str,
):
    """Extract commits from fetched repositories."""
    print_banner("Commit Data Extractor")

    try:
        # Load configuration
        config = get_config(config_file)

        # Determine input/output files
        input_file = Path(repos_file) if repos_file else config.REPOS_FILE
        output_file = Path(output) if output else config.COMMITS_FILE

        # Check if input file exists
        if not input_file.exists():
            colored_print(f"Input file not found: {input_file}", "red")
            colored_print("Please run 'fetch' command first to fetch repositories", "yellow")
            exit(1)

        # Load repositories
        colored_print(f"Loading repositories from {input_file}...", "blue")
        data = load_json_file(input_file)
        repositories = data.get("repositories", [])

        if not repositories:
            colored_print("No repositories found in input file", "yellow")
            exit(1)

        colored_print(f"Loaded {len(repositories)} repositories", "green")

        # Initialize extractor
        extractor = CommitExtractor(
            max_commits=max_commits, skip_merges=skip_merges, days_back=days_back
        )

        # Extract commits
        commits = extractor.extract_from_repositories(repositories)

        if not commits:
            colored_print("No commits extracted", "yellow")
            exit(1)

        # Save results
        extractor.save_results(commits, output_file, len(repositories))

        # Display summary
        colored_print(f"\n✓ Successfully extracted {len(commits)} commits", "green")
        colored_print(f"Output saved to: {output_file}", "green")

        # Calculate statistics
        avg_commits = len(commits) / len(repositories)
        colored_print("\nStatistics:", "cyan")
        colored_print(f"  Total repositories: {len(repositories)}", "white")
        colored_print(f"  Total commits: {len(commits)}", "white")
        colored_print(f"  Average commits per repo: {avg_commits:.1f}", "white")

        # Show language breakdown
        from collections import Counter

        repo_languages = [repo["language"] for repo in repositories if repo.get("language")]
        language_counts = Counter(repo_languages)

        colored_print("\nLanguage breakdown:", "cyan")
        for lang, count in language_counts.most_common(5):
            colored_print(f"  {lang}: {count} repos", "white")

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
    extract()
