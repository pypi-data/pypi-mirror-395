"""Utility functions for green microservices mining CLI."""

import json
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp in ISO 8601 format.

    Args:
        dt: Datetime object, defaults to now

    Returns:
        ISO formatted timestamp string
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json_file(path: Path) -> dict[str, Any]:
    """Load JSON data from file.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data: dict[str, Any], path: Path, indent: int = 2) -> None:
    """Save data to JSON file.

    Args:
        data: Data to save
        path: Output file path
        indent: JSON indentation level
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_csv_file(path: Path) -> pd.DataFrame:
    """Load CSV file as pandas DataFrame.

    Args:
        path: Path to CSV file

    Returns:
        DataFrame with CSV data

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)


def save_csv_file(df: pd.DataFrame, path: Path) -> None:
    """Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        path: Output file path
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")


def estimate_tokens(text: str) -> int:
    """Estimate number of tokens in text.

    Uses rough approximation: 1 token ≈ 4 characters

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    return len(text) // 4


def estimate_cost(tokens: int, model: str = "claude-sonnet-4-20250514") -> float:
    """Estimate API cost based on token usage.

    Args:
        tokens: Number of tokens
        model: Model name

    Returns:
        Estimated cost in USD
    """
    # Claude Sonnet 4 pricing (as of Dec 2024)
    # Input: $3 per million tokens
    # Output: $15 per million tokens
    # Average estimate: assume 50% input, 50% output

    if "sonnet" in model.lower():
        input_cost = 3.0 / 1_000_000  # per token
        output_cost = 15.0 / 1_000_000  # per token
        avg_cost = (input_cost + output_cost) / 2
        return tokens * avg_cost

    return 0.0


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 2.0,
    exponential_backoff: bool = True,
    exceptions: tuple = (Exception,),
) -> Callable:
    """Decorator to retry function on exception.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exponential_backoff: Use exponential backoff for delays
        exceptions: Tuple of exception types to catch

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise

                    colored_print(f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}", "yellow")
                    colored_print(f"Retrying in {current_delay:.1f} seconds...", "yellow")

                    time.sleep(current_delay)

                    if exponential_backoff:
                        current_delay *= 2

            return None

        return wrapper

    return decorator


def colored_print(text: str, color: str = "white") -> None:
    """Print colored text to console.

    Args:
        text: Text to print
        color: Color name (red, green, yellow, blue, magenta, cyan, white)
    """
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }

    color_code = color_map.get(color.lower(), Fore.WHITE)
    print(f"{color_code}{text}{Style.RESET_ALL}")


def handle_github_rate_limit(response) -> None:
    """Handle GitHub API rate limiting.

    Args:
        response: GitHub API response object

    Raises:
        Exception: If rate limit is exceeded
    """
    if hasattr(response, "status") and response.status == 403:
        colored_print("GitHub API rate limit exceeded!", "red")
        colored_print("Please wait or use an authenticated token.", "yellow")
        raise Exception("GitHub API rate limit exceeded")


def format_number(num: int) -> str:
    """Format large numbers with thousand separators.

    Args:
        num: Number to format

    Returns:
        Formatted string
    """
    return f"{num:,}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage value.

    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2h 15m")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length.

    Args:
        text: Input text
        max_length: Maximum length

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def create_checkpoint(checkpoint_file: Path, data: dict[str, Any]) -> None:
    """Create checkpoint file for resuming operations.

    Args:
        checkpoint_file: Path to checkpoint file
        data: Checkpoint data
    """
    save_json_file(data, checkpoint_file)
    colored_print(f"Checkpoint saved: {checkpoint_file}", "green")


def load_checkpoint(checkpoint_file: Path) -> Optional[dict[str, Any]]:
    """Load checkpoint data if exists.

    Args:
        checkpoint_file: Path to checkpoint file

    Returns:
        Checkpoint data or None if doesn't exist
    """
    if checkpoint_file.exists():
        try:
            return load_json_file(checkpoint_file)
        except Exception as e:
            colored_print(f"Failed to load checkpoint: {e}", "yellow")
    return None


def print_banner(title: str) -> None:
    """Print formatted banner.

    Args:
        title: Banner title
    """
    colored_print("\n" + "=" * 60, "cyan")
    colored_print(f"🔍 {title}", "cyan")
    colored_print("=" * 60 + "\n", "cyan")


def print_section(title: str) -> None:
    """Print section header.

    Args:
        title: Section title
    """
    colored_print(f"\n📌 {title}", "blue")
    colored_print("-" * 60, "blue")
