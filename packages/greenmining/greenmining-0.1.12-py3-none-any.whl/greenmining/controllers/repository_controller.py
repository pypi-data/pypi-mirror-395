"""Repository Controller - Handles repository fetching operations."""

from github import Github, GithubException
from tqdm import tqdm

from greenmining.config import Config
from greenmining.models.repository import Repository
from greenmining.utils import colored_print, load_json_file, save_json_file


class RepositoryController:
    """Controller for GitHub repository operations."""

    def __init__(self, config: Config):
        """Initialize controller with configuration."""
        self.config = config
        self.github = Github(config.GITHUB_TOKEN)

    def fetch_repositories(
        self,
        max_repos: int = None,
        min_stars: int = None,
        languages: list[str] = None,
        keywords: str = None,
    ) -> list[Repository]:
        """Fetch repositories from GitHub.

        Args:
            max_repos: Maximum number of repositories to fetch
            min_stars: Minimum stars filter
            languages: List of programming languages to filter
            keywords: Custom search keywords (default: "microservices")

        Returns:
            List of Repository model instances
        """
        max_repos = max_repos or self.config.MAX_REPOS
        min_stars = min_stars or self.config.MIN_STARS
        languages = languages or self.config.SUPPORTED_LANGUAGES
        keywords = keywords or "microservices"

        colored_print(f"🔍 Fetching up to {max_repos} repositories...", "cyan")
        colored_print(f"   Keywords: {keywords}", "cyan")
        colored_print(f"   Filters: min_stars={min_stars}", "cyan")

        # Build search query with custom keywords
        query = f"{keywords} stars:>={min_stars}"

        try:
            # Execute search
            search_results = self.github.search_repositories(
                query=query, sort="stars", order="desc"
            )

            total_found = search_results.totalCount
            colored_print(f"   Found {total_found} repositories", "green")

            # Fetch repositories
            repositories = []
            with tqdm(total=min(max_repos, total_found), desc="Fetching", unit="repo") as pbar:
                for idx, repo in enumerate(search_results):
                    if idx >= max_repos:
                        break

                    try:
                        repo_model = Repository.from_github_repo(repo, idx + 1)
                        repositories.append(repo_model)
                        pbar.update(1)
                    except GithubException as e:
                        colored_print(f"   Error: {repo.full_name}: {e}", "yellow")
                        continue

            # Save to file
            repo_dicts = [r.to_dict() for r in repositories]
            save_json_file(repo_dicts, self.config.REPOS_FILE)

            colored_print(f"✅ Fetched {len(repositories)} repositories", "green")
            colored_print(f"   Saved to: {self.config.REPOS_FILE}", "cyan")

            return repositories

        except Exception as e:
            colored_print(f"❌ Error fetching repositories: {e}", "red")
            raise

    def load_repositories(self) -> list[Repository]:
        """Load repositories from file.

        Returns:
            List of Repository model instances
        """
        if not self.config.REPOS_FILE.exists():
            raise FileNotFoundError(f"No repositories file found at {self.config.REPOS_FILE}")

        repo_dicts = load_json_file(self.config.REPOS_FILE)
        return [Repository.from_dict(r) for r in repo_dicts]

    def get_repository_stats(self, repositories: list[Repository]) -> dict:
        """Get statistics about fetched repositories.

        Args:
            repositories: List of Repository instances

        Returns:
            Dictionary with statistics
        """
        if not repositories:
            return {}

        return {
            "total": len(repositories),
            "by_language": self._count_by_language(repositories),
            "total_stars": sum(r.stars for r in repositories),
            "avg_stars": sum(r.stars for r in repositories) / len(repositories),
            "top_repo": max(repositories, key=lambda r: r.stars).full_name,
        }

    def _count_by_language(self, repositories: list[Repository]) -> dict:
        """Count repositories by language."""
        counts = {}
        for repo in repositories:
            lang = repo.language or "Unknown"
            counts[lang] = counts.get(lang, 0) + 1
        return counts
