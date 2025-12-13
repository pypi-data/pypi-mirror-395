"""Green Microservices Mining - GSF Pattern Analysis Tool."""

from greenmining.config import Config
from greenmining.controllers.repository_controller import RepositoryController
from greenmining.gsf_patterns import (
    GREEN_KEYWORDS,
    GSF_PATTERNS,
    get_pattern_by_keywords,
    is_green_aware,
)

__version__ = "0.1.12"


def fetch_repositories(
    github_token: str,
    max_repos: int = 100,
    min_stars: int = 100,
    languages: list = None,
    keywords: str = "microservices",
):
    """Fetch repositories from GitHub with custom search keywords.

    Args:
        github_token: GitHub personal access token
        max_repos: Maximum number of repositories to fetch (default: 100)
        min_stars: Minimum GitHub stars required (default: 100)
        languages: List of programming languages to filter (default: ["Python", "Java", "Go", "JavaScript", "TypeScript"])
        keywords: Search keywords (default: "microservices")

    Returns:
        List of Repository model instances

    Example:
        >>> from greenmining import fetch_repositories
        >>> repos = fetch_repositories(
        ...     github_token="your_token",
        ...     max_repos=50,
        ...     keywords="kubernetes cloud-native",
        ...     min_stars=500
        ... )
        >>> print(f"Found {len(repos)} repositories")
    """
    config = Config()
    config.GITHUB_TOKEN = github_token
    controller = RepositoryController(config)

    return controller.fetch_repositories(
        max_repos=max_repos, min_stars=min_stars, languages=languages, keywords=keywords
    )


__all__ = [
    "Config",
    "GSF_PATTERNS",
    "GREEN_KEYWORDS",
    "is_green_aware",
    "get_pattern_by_keywords",
    "fetch_repositories",
    "__version__",
]
