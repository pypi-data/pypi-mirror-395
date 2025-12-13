"""GitHub repository fetcher for green microservices mining."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from github import Github, GithubException, RateLimitExceededException
from tqdm import tqdm

from greenmining.config import get_config
from greenmining.utils import (
    colored_print,
    format_timestamp,
    print_banner,
    save_json_file,
)


class GitHubFetcher:
    """Fetches microservice repositories from GitHub."""

    def __init__(
        self,
        token: str,
        max_repos: int = 100,
        min_stars: int = 100,
        languages: Optional[list[str]] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        pushed_after: Optional[str] = None,
        pushed_before: Optional[str] = None,
    ):
        """Initialize GitHub fetcher.

        Args:
            token: GitHub personal access token
            max_repos: Maximum number of repositories to fetch
            min_stars: Minimum number of stars required
            languages: List of programming languages to filter
            created_after: Repository created after date (YYYY-MM-DD)
            created_before: Repository created before date (YYYY-MM-DD)
            pushed_after: Repository pushed after date (YYYY-MM-DD)
            pushed_before: Repository pushed before date (YYYY-MM-DD)
        """
        self.github = Github(token)
        self.max_repos = max_repos
        self.min_stars = min_stars
        self.languages = languages or [
            "Java",
            "Python",
            "Go",
            "JavaScript",
            "TypeScript",
            "C#",
            "Rust",
        ]
        self.created_after = created_after
        self.created_before = created_before
        self.pushed_after = pushed_after
        self.pushed_before = pushed_before

    def search_repositories(self) -> list[dict[str, Any]]:
        """Search for microservice repositories.

        Returns:
            List of repository metadata dictionaries
        """
        repositories = []
        keywords = ["microservices", "microservice-architecture", "cloud-native"]

        colored_print(f"Searching for repositories with keywords: {', '.join(keywords)}", "cyan")
        colored_print(
            f"Filters: min_stars={self.min_stars}, languages={', '.join(self.languages)}", "cyan"
        )

        # Build search query with temporal filters
        query = self._build_temporal_query(keywords)

        try:
            # Execute search
            search_results = self.github.search_repositories(
                query=query, sort="stars", order="desc"
            )

            total_found = search_results.totalCount
            colored_print(f"Found {total_found} repositories matching criteria", "green")

            # Fetch repository details with progress bar
            with tqdm(
                total=min(self.max_repos, total_found), desc="Fetching repositories", unit="repo"
            ) as pbar:
                for idx, repo in enumerate(search_results):
                    if idx >= self.max_repos:
                        break

                    try:
                        repo_data = self._extract_repo_metadata(repo, idx + 1)
                        repositories.append(repo_data)
                        pbar.update(1)
                    except GithubException as e:
                        colored_print(f"Error fetching {repo.full_name}: {e}", "yellow")
                        continue
                    except RateLimitExceededException:
                        colored_print("Rate limit exceeded. Waiting...", "red")
                        self._handle_rate_limit()
                        continue

            return repositories

        except GithubException as e:
            colored_print(f"GitHub API error: {e}", "red")
            raise
        except Exception as e:
            colored_print(f"Unexpected error: {e}", "red")
            raise

    def _extract_repo_metadata(self, repo, repo_id: int) -> dict[str, Any]:
        """Extract metadata from repository object.

        Args:
            repo: GitHub repository object
            repo_id: Sequential repository ID

        Returns:
            Dictionary with repository metadata
        """
        return {
            "repo_id": repo_id,
            "name": repo.name,
            "owner": repo.owner.login,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "last_updated": repo.updated_at.isoformat() if repo.updated_at else None,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "description": repo.description or "",
            "main_branch": repo.default_branch,
            "topics": repo.get_topics() if hasattr(repo, "get_topics") else [],
            "size": repo.size,
            "has_issues": repo.has_issues,
            "has_wiki": repo.has_wiki,
            "archived": repo.archived,
            "license": repo.license.name if repo.license else None,
        }

    def _build_temporal_query(self, keywords: list[str]) -> str:
        """
        Build GitHub search query with temporal constraints.

        Args:
            keywords: List of search keywords

        Returns:
            Complete search query string
        """
        query_parts = []

        # Keywords
        keyword_query = " OR ".join(keywords)
        query_parts.append(f"({keyword_query})")

        # Languages
        language_query = " OR ".join([f"language:{lang}" for lang in self.languages])
        query_parts.append(f"({language_query})")

        # Stars
        query_parts.append(f"stars:>={self.min_stars}")

        # Archived filter
        query_parts.append("archived:false")

        # Temporal filters
        if self.created_after and self.created_before:
            query_parts.append(f"created:{self.created_after}..{self.created_before}")
        elif self.created_after:
            query_parts.append(f"created:>={self.created_after}")
        elif self.created_before:
            query_parts.append(f"created:<={self.created_before}")

        if self.pushed_after and self.pushed_before:
            query_parts.append(f"pushed:{self.pushed_after}..{self.pushed_before}")
        elif self.pushed_after:
            query_parts.append(f"pushed:>={self.pushed_after}")
        elif self.pushed_before:
            query_parts.append(f"pushed:<={self.pushed_before}")

        query = " ".join(query_parts)
        colored_print(f"Query: {query}", "cyan")
        return query

    def _handle_rate_limit(self):
        """Handle GitHub API rate limiting."""
        rate_limit = self.github.get_rate_limit()
        reset_time = rate_limit.core.reset
        wait_seconds = (reset_time - datetime.now()).total_seconds()

        if wait_seconds > 0:
            colored_print(f"Rate limit will reset in {wait_seconds:.0f} seconds", "yellow")
            import time

            time.sleep(min(wait_seconds + 10, 60))  # Wait with max 60 seconds

    def save_results(self, repositories: list[dict[str, Any]], output_file: Path):
        """Save fetched repositories to JSON file.

        Args:
            repositories: List of repository metadata
            output_file: Output file path
        """
        data = {
            "metadata": {
                "fetched_at": format_timestamp(),
                "total_repos": len(repositories),
                "min_stars": self.min_stars,
                "languages": self.languages,
                "search_keywords": ["microservices", "microservice-architecture", "cloud-native"],
            },
            "repositories": repositories,
        }

        save_json_file(data, output_file)
        colored_print(f"Saved {len(repositories)} repositories to {output_file}", "green")


@click.command()
@click.option("--max-repos", default=100, help="Maximum number of repositories to fetch")
@click.option("--min-stars", default=100, help="Minimum stars required")
@click.option(
    "--languages",
    default="java,python,go,javascript,typescript,csharp,rust",
    help="Comma-separated list of languages",
)
@click.option("--output", default=None, help="Output file path (default: data/repositories.json)")
@click.option("--config-file", default=".env", help="Path to .env configuration file")
def fetch(max_repos: int, min_stars: int, languages: str, output: Optional[str], config_file: str):
    """Fetch top microservice repositories from GitHub."""
    print_banner("GitHub Repository Fetcher")

    try:
        # Load configuration
        config = get_config(config_file)

        # Parse languages
        language_list = [lang.strip().title() for lang in languages.split(",")]

        # Map common language names
        language_map = {"Nodejs": "JavaScript", "Csharp": "C#", "Typescript": "TypeScript"}
        language_list = [language_map.get(lang, lang) for lang in language_list]

        # Determine output file
        output_file = Path(output) if output else config.REPOS_FILE

        colored_print(f"Fetching up to {max_repos} repositories...", "blue")

        # Initialize fetcher
        fetcher = GitHubFetcher(
            token=config.GITHUB_TOKEN,
            max_repos=max_repos,
            min_stars=min_stars,
            languages=language_list,
        )

        # Search and fetch repositories
        repositories = fetcher.search_repositories()

        if not repositories:
            colored_print("No repositories found matching criteria", "yellow")
            return

        # Save results
        fetcher.save_results(repositories, output_file)

        # Display summary
        colored_print(f"\n✓ Successfully fetched {len(repositories)} repositories", "green")
        colored_print(f"Output saved to: {output_file}", "green")

        # Show top 5 repos
        colored_print("\nTop 5 repositories by stars:", "cyan")
        from tabulate import tabulate

        top_repos = sorted(repositories, key=lambda x: x["stars"], reverse=True)[:5]
        table_data = [
            [
                repo["full_name"],
                repo["language"],
                f"{repo['stars']:,}",
                repo["description"][:50] + "...",
            ]
            for repo in top_repos
        ]
        print(
            tabulate(
                table_data,
                headers=["Repository", "Language", "Stars", "Description"],
                tablefmt="simple",
            )
        )

    except ValueError as e:
        colored_print(f"Configuration error: {e}", "red")
        colored_print("Please check your .env file and ensure GITHUB_TOKEN is set", "yellow")
        exit(1)
    except GithubException as e:
        colored_print(f"GitHub API error: {e}", "red")
        exit(1)
    except Exception as e:
        colored_print(f"Error: {e}", "red")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    fetch()
