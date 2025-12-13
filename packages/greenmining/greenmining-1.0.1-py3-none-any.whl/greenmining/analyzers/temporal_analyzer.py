"""
Temporal and Historical Analysis for Green Software Practices

Implements time-series analysis from Soliman et al. (2017):
- Adoption trend analysis (when practices emerged)
- Velocity analysis (commit frequency over time)
- Pattern evolution tracking (which practices dominated when)
- Temporal correlations (do practices cluster in time?)

Addresses research questions:
1. When did green practices emerge in software development?
2. Are green practices increasing or decreasing over time?
3. Which practices were early vs. late adopters?
4. Do green practices correlate with project maturity?
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import statistics


@dataclass
class TemporalMetrics:
    """Metrics for a specific time period"""

    period: str
    start_date: datetime
    end_date: datetime
    commit_count: int
    green_commit_count: int
    green_awareness_rate: float
    unique_patterns: int
    dominant_pattern: Optional[str]
    velocity: float  # commits per day


@dataclass
class TrendAnalysis:
    """Trend analysis results"""

    trend_direction: str  # 'increasing', 'decreasing', 'stable'
    slope: float
    r_squared: float
    start_rate: float
    end_rate: float
    change_percentage: float


class TemporalAnalyzer:
    """
    Analyze temporal patterns in green software adoption.

    Based on Soliman et al.: "Time-range filtering is standard practice"
    Extends with: trend detection, velocity analysis, evolution tracking
    """

    def __init__(self, granularity: str = "quarter"):
        """
        Initialize temporal analyzer.

        Args:
            granularity: Time period granularity ('day', 'week', 'month', 'quarter', 'year')
        """
        self.granularity = granularity

    def group_commits_by_period(
        self, commits: List[Dict], date_field: str = "date"
    ) -> Dict[str, List[Dict]]:
        """
        Group commits into time periods.

        Args:
            commits: List of commit dictionaries
            date_field: Field containing commit date

        Returns:
            Dictionary mapping period strings to commit lists
        """
        periods = defaultdict(list)

        for commit in commits:
            date_str = commit.get(date_field)
            if not date_str:
                continue

            # Parse date
            try:
                if isinstance(date_str, datetime):
                    date = date_str
                else:
                    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                continue

            # Determine period
            period_key = self._get_period_key(date)
            periods[period_key].append(commit)

        return dict(periods)

    def _get_period_key(self, date: datetime) -> str:
        """Get period key for a date based on granularity."""
        if self.granularity == "day":
            return date.strftime("%Y-%m-%d")
        elif self.granularity == "week":
            # ISO week number
            return f"{date.year}-W{date.isocalendar()[1]:02d}"
        elif self.granularity == "month":
            return date.strftime("%Y-%m")
        elif self.granularity == "quarter":
            quarter = (date.month - 1) // 3 + 1
            return f"{date.year}-Q{quarter}"
        elif self.granularity == "year":
            return str(date.year)
        else:
            return date.strftime("%Y-%m")

    def _parse_period_key(self, period_key: str) -> Tuple[datetime, datetime]:
        """Parse period key back to start and end dates."""
        if "W" in period_key:
            # Week format: 2024-W15
            year, week = period_key.split("-W")
            start = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
            end = start + timedelta(days=6)
        elif "Q" in period_key:
            # Quarter format: 2024-Q1
            year, quarter = period_key.split("-Q")
            quarter_num = int(quarter)
            start_month = (quarter_num - 1) * 3 + 1
            start = datetime(int(year), start_month, 1)
            # Calculate end of quarter
            end_month = start_month + 2
            if end_month == 12:
                end = datetime(int(year), 12, 31, 23, 59, 59)
            elif end_month > 12:
                end = datetime(int(year) + 1, 1, 1) - timedelta(seconds=1)
            else:
                # Get last day of end_month
                if end_month in [1, 3, 5, 7, 8, 10]:
                    end = datetime(int(year), end_month, 31, 23, 59, 59)
                elif end_month in [4, 6, 9, 11]:
                    end = datetime(int(year), end_month, 30, 23, 59, 59)
                else:  # February
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        end = datetime(int(year), end_month, 29, 23, 59, 59)
                    else:
                        end = datetime(int(year), end_month, 28, 23, 59, 59)
        elif len(period_key) == 4:
            # Year format: 2024
            start = datetime(int(period_key), 1, 1)
            end = datetime(int(period_key), 12, 31)
        elif len(period_key) == 7:
            # Month format: 2024-01
            start = datetime.strptime(period_key, "%Y-%m")
            next_month = start.month + 1 if start.month < 12 else 1
            next_year = start.year if start.month < 12 else start.year + 1
            end = datetime(next_year, next_month, 1) - timedelta(days=1)
        elif len(period_key) == 10:
            # Day format: 2024-01-15
            start = datetime.strptime(period_key, "%Y-%m-%d")
            end = start + timedelta(days=1) - timedelta(seconds=1)
        else:
            # Default: treat as month
            start = datetime.strptime(period_key[:7], "%Y-%m")
            end = start + timedelta(days=30)

        return start, end

    def calculate_period_metrics(
        self, period_key: str, commits: List[Dict], analysis_results: List[Dict]
    ) -> TemporalMetrics:
        """
        Calculate metrics for a time period.

        Args:
            period_key: Period identifier
            commits: Commits in this period
            analysis_results: Pattern analysis results for commits

        Returns:
            TemporalMetrics object
        """
        start_date, end_date = self._parse_period_key(period_key)

        # Count green commits
        commit_hashes = {c.get("hash", c.get("sha")) for c in commits}
        green_results = [
            r
            for r in analysis_results
            if r.get("commit_sha") in commit_hashes and r.get("is_green_aware", False)
        ]

        green_count = len(green_results)
        total_count = len(commits)
        green_rate = (green_count / total_count * 100) if total_count > 0 else 0

        # Count unique patterns
        all_patterns = set()
        for result in green_results:
            patterns = result.get("patterns_detected", [])
            all_patterns.update(patterns)

        # Find dominant pattern
        pattern_counts = defaultdict(int)
        for result in green_results:
            for pattern in result.get("patterns_detected", []):
                pattern_counts[pattern] += 1

        dominant = max(pattern_counts.items(), key=lambda x: x[1])[0] if pattern_counts else None

        # Calculate velocity (commits per day)
        days = (end_date - start_date).days + 1
        velocity = total_count / days if days > 0 else 0

        return TemporalMetrics(
            period=period_key,
            start_date=start_date,
            end_date=end_date,
            commit_count=total_count,
            green_commit_count=green_count,
            green_awareness_rate=round(green_rate, 2),
            unique_patterns=len(all_patterns),
            dominant_pattern=dominant,
            velocity=round(velocity, 2),
        )

    def analyze_trends(self, commits: List[Dict], analysis_results: List[Dict]) -> Dict:
        """
        Comprehensive temporal trend analysis.

        Args:
            commits: All commits to analyze
            analysis_results: Pattern analysis results

        Returns:
            Dictionary with:
            - periods: List of TemporalMetrics
            - trend: TrendAnalysis
            - adoption_curve: List of (period, cumulative_rate)
            - velocity_trend: Velocity change over time
        """
        # Group by periods
        grouped = self.group_commits_by_period(commits)

        # Calculate metrics per period
        periods = []
        for period_key in sorted(grouped.keys()):
            metrics = self.calculate_period_metrics(
                period_key, grouped[period_key], analysis_results
            )
            periods.append(metrics)

        # Analyze trend
        trend = self._calculate_trend(periods)

        # Calculate adoption curve (cumulative)
        adoption_curve = self._calculate_adoption_curve(periods)

        # Velocity trend
        velocity_trend = self._calculate_velocity_trend(periods)

        # Pattern evolution (which patterns emerged when)
        pattern_evolution = self._analyze_pattern_evolution(periods, analysis_results)

        return {
            "periods": [self._metrics_to_dict(m) for m in periods],
            "trend": self._trend_to_dict(trend),
            "adoption_curve": adoption_curve,
            "velocity_trend": velocity_trend,
            "pattern_evolution": pattern_evolution,
            "summary": {
                "total_periods": len(periods),
                "first_period": periods[0].period if periods else None,
                "last_period": periods[-1].period if periods else None,
                "overall_trend": trend.trend_direction if trend else "unknown",
                "average_green_rate": round(
                    statistics.mean([p.green_awareness_rate for p in periods]) if periods else 0, 2
                ),
            },
        }

    def _calculate_trend(self, periods: List[TemporalMetrics]) -> Optional[TrendAnalysis]:
        """Calculate linear trend using least squares regression."""
        if len(periods) < 2:
            return None

        # Simple linear regression
        n = len(periods)
        x = list(range(n))  # Period index
        y = [p.green_awareness_rate for p in periods]

        # Calculate slope and intercept
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean

        # Calculate R²
        y_pred = [slope * xi + intercept for xi in x]
        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Determine trend direction
        if abs(slope) < 0.1:
            direction = "stable"
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"

        # Calculate change
        start_rate = y[0]
        end_rate = y[-1]
        change = ((end_rate - start_rate) / start_rate * 100) if start_rate != 0 else 0

        return TrendAnalysis(
            trend_direction=direction,
            slope=round(slope, 4),
            r_squared=round(r_squared, 4),
            start_rate=round(start_rate, 2),
            end_rate=round(end_rate, 2),
            change_percentage=round(change, 2),
        )

    def _calculate_adoption_curve(self, periods: List[TemporalMetrics]) -> List[Tuple[str, float]]:
        """Calculate cumulative adoption over time."""
        cumulative_green = 0
        cumulative_total = 0
        curve = []

        for period in periods:
            cumulative_green += period.green_commit_count
            cumulative_total += period.commit_count
            cumulative_rate = (
                (cumulative_green / cumulative_total * 100) if cumulative_total > 0 else 0
            )
            curve.append((period.period, round(cumulative_rate, 2)))

        return curve

    def _calculate_velocity_trend(self, periods: List[TemporalMetrics]) -> Dict:
        """Analyze velocity changes over time."""
        if not periods:
            return {}

        velocities = [p.velocity for p in periods]

        return {
            "average_velocity": round(statistics.mean(velocities), 2),
            "velocity_std": round(statistics.stdev(velocities), 2) if len(velocities) > 1 else 0,
            "min_velocity": round(min(velocities), 2),
            "max_velocity": round(max(velocities), 2),
            "velocity_by_period": [(p.period, p.velocity) for p in periods],
        }

    def _analyze_pattern_evolution(
        self, periods: List[TemporalMetrics], analysis_results: List[Dict]
    ) -> Dict:
        """Track when different patterns emerged and dominated."""
        pattern_timeline = defaultdict(lambda: {"first_seen": None, "occurrences_by_period": {}})

        for period in periods:
            # Get commits in this period
            period_patterns = defaultdict(int)

            for result in analysis_results:
                commit_date_str = result.get("commit_date")
                if not commit_date_str:
                    continue

                try:
                    if isinstance(commit_date_str, datetime):
                        commit_date = commit_date_str
                    else:
                        commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))

                    if period.start_date <= commit_date <= period.end_date:
                        for pattern in result.get("patterns_detected", []):
                            period_patterns[pattern] += 1
                except (ValueError, AttributeError):
                    continue

            # Record occurrences
            for pattern, count in period_patterns.items():
                if pattern_timeline[pattern]["first_seen"] is None:
                    pattern_timeline[pattern]["first_seen"] = period.period
                pattern_timeline[pattern]["occurrences_by_period"][period.period] = count

        return {
            pattern: {
                "first_seen": data["first_seen"],
                "total_occurrences": sum(data["occurrences_by_period"].values()),
                "periods_active": len(data["occurrences_by_period"]),
                "timeline": data["occurrences_by_period"],
            }
            for pattern, data in pattern_timeline.items()
        }

    def _metrics_to_dict(self, metrics: TemporalMetrics) -> Dict:
        """Convert TemporalMetrics to dictionary."""
        return {
            "period": metrics.period,
            "start_date": metrics.start_date.isoformat(),
            "end_date": metrics.end_date.isoformat(),
            "commit_count": metrics.commit_count,
            "green_commit_count": metrics.green_commit_count,
            "green_awareness_rate": metrics.green_awareness_rate,
            "unique_patterns": metrics.unique_patterns,
            "dominant_pattern": metrics.dominant_pattern,
            "velocity": metrics.velocity,
        }

    def _trend_to_dict(self, trend: Optional[TrendAnalysis]) -> Dict:
        """Convert TrendAnalysis to dictionary."""
        if not trend:
            return {}

        return {
            "trend_direction": trend.trend_direction,
            "slope": trend.slope,
            "r_squared": trend.r_squared,
            "start_rate": trend.start_rate,
            "end_rate": trend.end_rate,
            "change_percentage": trend.change_percentage,
        }
