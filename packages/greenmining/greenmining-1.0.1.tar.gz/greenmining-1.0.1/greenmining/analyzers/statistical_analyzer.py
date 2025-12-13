"""Enhanced statistical analyzer for green software patterns."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy import stats


class EnhancedStatisticalAnalyzer:
    """
    Advanced statistical analyses for green software patterns.
    Based on Soliman et al. quantitative validation techniques.
    """

    def analyze_pattern_correlations(self, commit_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze correlations between patterns.

        Question: Do repositories that adopt caching also adopt resource limits?

        Args:
            commit_data: DataFrame with pattern columns

        Returns:
            Dictionary containing correlation matrix and significant pairs
        """
        # Create pattern co-occurrence matrix
        pattern_columns = [col for col in commit_data.columns if col.startswith("pattern_")]

        if not pattern_columns:
            return {
                "correlation_matrix": {},
                "significant_pairs": [],
                "interpretation": "No pattern columns found",
            }

        correlation_matrix = commit_data[pattern_columns].corr(method="pearson")

        # Identify significant correlations
        significant_pairs = []
        for i, pattern1 in enumerate(pattern_columns):
            for j, pattern2 in enumerate(pattern_columns[i + 1 :], start=i + 1):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:  # Strong correlation threshold
                    significant_pairs.append(
                        {
                            "pattern1": pattern1,
                            "pattern2": pattern2,
                            "correlation": corr_value,
                            "strength": "strong" if abs(corr_value) > 0.7 else "moderate",
                        }
                    )

        return {
            "correlation_matrix": correlation_matrix.to_dict(),
            "significant_pairs": significant_pairs,
            "interpretation": self._interpret_correlations(significant_pairs),
        }

    def temporal_trend_analysis(self, commits_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze temporal trends in green awareness.

        Techniques:
        - Mann-Kendall trend test (monotonic trend detection)
        - Seasonal decomposition (identify cyclical patterns)
        - Change point detection (identify sudden shifts)

        Args:
            commits_df: DataFrame with date and green_aware columns

        Returns:
            Dictionary containing trend analysis results
        """
        # Prepare time series data
        commits_df["date"] = pd.to_datetime(commits_df["date"])
        commits_df = commits_df.sort_values("date")

        # Monthly aggregation
        monthly = (
            commits_df.set_index("date")
            .resample("ME")
            .agg({"green_aware": "sum", "commit_hash": "count"})
        )
        monthly.columns = ["green_aware", "total_commits"]
        monthly["green_rate"] = monthly["green_aware"] / monthly["total_commits"]

        # Mann-Kendall trend test
        mk_result = stats.kendalltau(range(len(monthly)), monthly["green_rate"])
        trend_direction = "increasing" if mk_result.correlation > 0 else "decreasing"
        trend_significant = bool(mk_result.pvalue < 0.05)

        # Seasonal decomposition (requires at least 2 years of data)
        seasonal_pattern = None
        if len(monthly) >= 24:
            try:
                from statsmodels.tsa.seasonal import seasonal_decompose

                decomposition = seasonal_decompose(
                    monthly["green_rate"], model="additive", period=12
                )
                seasonal_pattern = decomposition.seasonal.to_dict()
            except Exception:
                seasonal_pattern = None

        # Change point detection (simple method: rolling window variance)
        window_size = 3
        monthly["rolling_var"] = monthly["green_rate"].rolling(window=window_size).var()
        change_points = monthly[
            monthly["rolling_var"]
            > monthly["rolling_var"].mean() + 2 * monthly["rolling_var"].std()
        ]

        return {
            "trend": {
                "direction": trend_direction,
                "significant": trend_significant,
                "correlation": mk_result.correlation,
                "p_value": mk_result.pvalue,
            },
            "seasonal_pattern": seasonal_pattern,
            "change_points": change_points.index.tolist() if not change_points.empty else [],
            "monthly_data": monthly.to_dict(),
        }

    def effect_size_analysis(self, group1: List[float], group2: List[float]) -> Dict[str, Any]:
        """
        Calculate effect size between two groups.

        Use case: Compare green awareness between:
        - Different programming languages
        - Different time periods
        - Different repository sizes

        Args:
            group1: First group values
            group2: Second group values

        Returns:
            Dictionary containing effect size metrics
        """
        # Cohen's d (effect size)
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        pooled_std = np.sqrt((std1**2 + std2**2) / 2)

        if pooled_std == 0:
            cohens_d = 0
        else:
            cohens_d = (mean1 - mean2) / pooled_std

        # Interpretation
        if abs(cohens_d) < 0.2:
            magnitude = "negligible"
        elif abs(cohens_d) < 0.5:
            magnitude = "small"
        elif abs(cohens_d) < 0.8:
            magnitude = "medium"
        else:
            magnitude = "large"

        # Statistical significance
        t_stat, p_value = stats.ttest_ind(group1, group2)

        return {
            "cohens_d": cohens_d,
            "magnitude": magnitude,
            "mean_difference": mean1 - mean2,
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": bool(p_value < 0.05),
        }

    def pattern_adoption_rate_analysis(self, commits_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze pattern adoption rates over repository lifetime.

        Metrics:
        - Time to first adoption (TTFA)
        - Adoption acceleration
        - Pattern stickiness (continued use after adoption)

        Args:
            commits_df: DataFrame with pattern and date columns

        Returns:
            Dictionary mapping patterns to adoption metrics
        """
        results = {}

        for pattern in commits_df["pattern"].unique():
            pattern_commits = commits_df[commits_df["pattern"] == pattern].sort_values("date")

            if len(pattern_commits) == 0:
                continue

            # Time to first adoption
            first_adoption = pattern_commits.iloc[0]["date"]
            repo_start = commits_df["date"].min()
            ttfa_days = (first_adoption - repo_start).days

            # Adoption frequency over time
            monthly_adoption = pattern_commits.set_index("date").resample("ME").size()

            # Pattern stickiness (months with at least one adoption)
            total_months = len(commits_df.set_index("date").resample("ME").size())
            active_months = len(monthly_adoption[monthly_adoption > 0])
            stickiness = active_months / total_months if total_months > 0 else 0

            results[pattern] = {
                "ttfa_days": ttfa_days,
                "total_adoptions": len(pattern_commits),
                "stickiness": stickiness,
                "monthly_adoption_rate": monthly_adoption.mean(),
            }

        return results

    def _interpret_correlations(self, significant_pairs: List[Dict[str, Any]]) -> str:
        """
        Generate interpretation of correlation results.

        Args:
            significant_pairs: List of significant correlation pairs

        Returns:
            Interpretation string
        """
        if not significant_pairs:
            return "No significant correlations found between patterns."

        interpretations = []
        for pair in significant_pairs[:5]:  # Top 5
            p1 = pair["pattern1"].replace("pattern_", "")
            p2 = pair["pattern2"].replace("pattern_", "")
            corr = pair["correlation"]
            if corr > 0:
                interpretations.append(f"{p1} and {p2} tend to be adopted together (r={corr:.2f})")
            else:
                interpretations.append(f"{p1} and {p2} rarely co-occur (r={corr:.2f})")

        return "; ".join(interpretations)
