"""Configuration management for green microservices mining CLI."""

import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """Configuration class for loading and validating environment variables."""

    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment file.

        Args:
            env_file: Path to .env file
        """
        # Load environment variables
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # Load from system environment

        # GitHub API Configuration
        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not self.GITHUB_TOKEN or self.GITHUB_TOKEN == "your_github_pat_here":
            raise ValueError("GITHUB_TOKEN not set. Please set it in .env file or environment.")

        # Analysis Type - Using GitHub Copilot for AI-powered analysis
        self.ANALYSIS_TYPE = "keyword_heuristic"

        # Search and Processing Configuration
        self.GITHUB_SEARCH_KEYWORDS = ["microservices", "microservice-architecture", "cloud-native"]

        self.SUPPORTED_LANGUAGES = [
            "Java",
            "Python",
            "Go",
            "JavaScript",
            "TypeScript",
            "C#",
            "Rust",
        ]

        # Repository and Commit Limits
        self.MIN_STARS = int(os.getenv("MIN_STARS", "100"))
        self.MAX_REPOS = int(os.getenv("MAX_REPOS", "100"))
        self.COMMITS_PER_REPO = int(os.getenv("COMMITS_PER_REPO", "50"))
        self.DAYS_BACK = int(os.getenv("DAYS_BACK", "730"))  # 2 years

        # Analysis Configuration
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))

        # Processing Configuration
        self.TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.RETRY_DELAY = 2  # seconds
        self.EXPONENTIAL_BACKOFF = True

        # Output Configuration
        self.OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./data"))
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # File Paths
        self.REPOS_FILE = self.OUTPUT_DIR / "repositories.json"
        self.COMMITS_FILE = self.OUTPUT_DIR / "commits.json"
        self.ANALYSIS_FILE = self.OUTPUT_DIR / "analysis_results.json"
        self.AGGREGATED_FILE = self.OUTPUT_DIR / "aggregated_statistics.json"
        self.CSV_FILE = self.OUTPUT_DIR / "green_analysis_results.csv"
        self.REPORT_FILE = self.OUTPUT_DIR / "green_microservices_analysis.md"
        self.CHECKPOINT_FILE = self.OUTPUT_DIR / "checkpoint.json"

        # Logging
        self.VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
        self.LOG_FILE = self.OUTPUT_DIR / "mining.log"

    def validate(self) -> bool:
        """Validate that all required configuration is present.

        Returns:
            True if configuration is valid
        """
        required_attrs = ["GITHUB_TOKEN", "CLAUDE_API_KEY", "MAX_REPOS", "COMMITS_PER_REPO"]

        for attr in required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(f"Missing required configuration: {attr}")

        return True

    def __repr__(self) -> str:
        """String representation of configuration (hiding sensitive data)."""
        return (
            f"Config("
            f"MAX_REPOS={self.MAX_REPOS}, "
            f"COMMITS_PER_REPO={self.COMMITS_PER_REPO}, "
            f"BATCH_SIZE={self.BATCH_SIZE}, "
            f"OUTPUT_DIR={self.OUTPUT_DIR}"
            f")"
        )


# Global config instance
_config_instance = None


def get_config(env_file: str = ".env") -> Config:
    """Get or create global configuration instance.

    Args:
        env_file: Path to .env file

    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(env_file)
    return _config_instance
