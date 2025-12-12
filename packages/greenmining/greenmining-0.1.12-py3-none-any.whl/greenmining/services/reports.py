"""Report generator for green microservices analysis."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import click

from greenmining.config import get_config
from greenmining.utils import (
    colored_print,
    format_number,
    format_percentage,
    load_json_file,
    print_banner,
)


class ReportGenerator:
    """Generates markdown report from aggregated statistics."""

    def __init__(self):
        """Initialize report generator."""
        pass

    def generate_report(
        self,
        aggregated_data: dict[str, Any],
        analysis_data: dict[str, Any],
        repos_data: dict[str, Any],
    ) -> str:
        """Generate comprehensive markdown report.

        Args:
            aggregated_data: Aggregated statistics
            analysis_data: Original analysis results
            repos_data: Repository metadata

        Returns:
            Markdown report content
        """
        report_sections = []

        # Title and metadata
        report_sections.append(self._generate_header())

        # Executive Summary
        report_sections.append(self._generate_executive_summary(aggregated_data))

        # 1. Methodology
        report_sections.append(self._generate_methodology(repos_data, analysis_data))

        # 2. Results
        report_sections.append(self._generate_results(aggregated_data))

        # 3. Discussion
        report_sections.append(self._generate_discussion(aggregated_data))

        # 4. Limitations
        report_sections.append(self._generate_limitations())

        # 5. Conclusion
        report_sections.append(self._generate_conclusion(aggregated_data))

        return "\n\n".join(report_sections)

    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""# Mining Software Repositories for Green Microservices
## Comprehensive Analysis Report

**Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Analysis Type:** Keyword and Heuristic-Based Pattern Detection

---"""

    def _generate_executive_summary(self, data: dict[str, Any]) -> str:
        """Generate executive summary."""
        summary = data["summary"]
        top_patterns = data["known_patterns"][:3] if data["known_patterns"] else []

        pattern_text = ""
        if top_patterns:
            pattern_list = ", ".join(
                [f"{p['pattern_name']} ({p['count']} occurrences)" for p in top_patterns]
            )
            pattern_text = f"The most common patterns detected include: {pattern_list}."

        return f"""### Executive Summary

This report presents findings from analyzing **{format_number(summary['total_commits'])} commits** across **{format_number(summary['total_repos'])} microservice-based repositories** to identify green software engineering practices.

**Key Findings:**

- **{format_percentage(summary['green_aware_percentage'])}** of commits ({format_number(summary['green_aware_count'])}) explicitly mention energy efficiency, performance optimization, or sustainability concerns
- **{format_number(summary['repos_with_green_commits'])}** out of {format_number(summary['total_repos'])} repositories contain at least one green-aware commit
- {pattern_text if pattern_text else "Various green software patterns were detected across the analyzed commits."}

**Implications:**

These findings suggest that while green software practices are present in microservices development, there is significant room for increased awareness and adoption of energy-efficient patterns. The relatively low percentage of green-aware commits indicates an opportunity for the software engineering community to emphasize sustainability in distributed systems."""

    def _generate_methodology(
        self, repos_data: dict[str, Any], analysis_data: dict[str, Any]
    ) -> str:
        """Generate methodology section."""
        metadata = repos_data.get("metadata", {})
        analysis_metadata = analysis_data.get("metadata", {})

        languages = ", ".join(metadata.get("languages", []))
        search_keywords = ", ".join(metadata.get("search_keywords", []))

        return f"""### 1. Methodology

#### 1.1 Repository Selection Criteria

Repositories were selected from GitHub based on the following criteria:

- **Keywords:** {search_keywords}
- **Programming Languages:** {languages}
- **Minimum Stars:** {metadata.get('min_stars', 100)} (to ensure established projects)
- **Sort Order:** Stars (descending)
- **Total Repositories:** {metadata.get('total_repos', 0)}

#### 1.2 Data Extraction Approach

Commit data was extracted using PyDriller library:

- **Commits Analyzed:** {analysis_metadata.get('total_commits_analyzed', 0)}
- **Time Window:** Last 2 years (730 days)
- **Merge Commits:** Excluded
- **Minimum Commit Message Length:** 10 characters

#### 1.3 Analysis Methodology

Commits were analyzed using a keyword and heuristic-based classification framework:

**Q1) Green Awareness Detection:**
- Searched for explicit mentions of energy, performance, sustainability, caching, optimization, and related keywords
- Analyzed file names for patterns (cache, performance, optimization)

**Q2) Known Pattern Detection:**
- Matched against predefined green software tactics:
  - Resource pooling (connection pools, thread pools)
  - Caching strategies (Redis, in-memory caches)
  - Lazy initialization
  - Database query optimization
  - Asynchronous processing
  - Code optimization
  - Event-driven architecture
  - Resource limits
  - Service decommissioning
  - Auto-scaling

**Q3) Emergent Pattern Detection:**
- Placeholder for manual review of novel microservice-specific patterns

#### 1.4 Limitations and Scope

- Analysis based on commit messages and file names only (no code inspection)
- Keyword matching may miss implicit green practices
- Limited to English language commit messages
- Focused on microservices architecture
- 2-year time window may not capture all historical practices"""

    def _generate_results(self, data: dict[str, Any]) -> str:
        """Generate results section."""
        sections = []

        # 2.1 Green Awareness
        sections.append(self._generate_green_awareness_section(data))

        # 2.2 Known Patterns
        sections.append(self._generate_known_patterns_section(data))

        # 2.3 Emerging Practices
        sections.append(self._generate_emergent_patterns_section(data))

        # 2.4 Per-Repository Analysis
        sections.append(self._generate_repo_analysis_section(data))

        return "### 2. Results\n\n" + "\n\n".join(sections)

    def _generate_green_awareness_section(self, data: dict[str, Any]) -> str:
        """Generate green awareness subsection."""
        summary = data["summary"]
        per_lang = data["per_language_stats"]
        per_repo = data["per_repo_stats"]

        # Top 10 repos table
        top_repos_table = "| Repository | Total Commits | Green Commits | Percentage |\n|------------|---------------|---------------|------------|\n"
        for repo in per_repo[:10]:
            top_repos_table += f"| {repo['repo_name'][:50]} | {repo['total_commits']} | {repo['green_commits']} | {format_percentage(repo['percentage'])} |\n"

        # Language table
        lang_table = "| Language | Total Commits | Green Commits | Percentage |\n|----------|---------------|---------------|------------|\n"
        for lang in per_lang:
            lang_table += f"| {lang['language']} | {format_number(lang['total_commits'])} | {format_number(lang['green_commits'])} | {format_percentage(lang['percentage'])} |\n"

        return f"""#### 2.1 Green Awareness in Commits

**Total commits analyzed:** {format_number(summary['total_commits'])}
**Commits with explicit green mention:** {format_number(summary['green_aware_count'])} ({format_percentage(summary['green_aware_percentage'])})

**Table: Top 10 Repositories with Highest Green Awareness**

{top_repos_table}

**Table: Green Awareness by Programming Language**

{lang_table}"""

    def _generate_known_patterns_section(self, data: dict[str, Any]) -> str:
        """Generate known patterns subsection."""
        patterns = data["known_patterns"]

        if not patterns:
            return "#### 2.2 Known Green Patterns & Tactics Applied\n\nNo known patterns were detected in the analyzed commits."

        # Patterns table
        patterns_table = (
            "| Pattern | Count | Percentage | High Conf. | Medium Conf. | Low Conf. |\n"
        )
        patterns_table += (
            "|---------|-------|------------|------------|--------------|----------|\n"
        )
        for pattern in patterns:
            conf = pattern["confidence_breakdown"]
            patterns_table += f"| {pattern['pattern_name']} | {format_number(pattern['count'])} | {format_percentage(pattern['percentage'])} | {conf['HIGH']} | {conf['MEDIUM']} | {conf['LOW']} |\n"

        # Pattern descriptions
        pattern_details = []
        for i, pattern in enumerate(patterns[:10], 1):
            pattern_details.append(
                f"""**{i}. {pattern['pattern_name']}**
- Frequency: {format_number(pattern['count'])} commits ({format_percentage(pattern['percentage'])})
- Confidence Distribution: HIGH={conf['HIGH']}, MEDIUM={conf['MEDIUM']}, LOW={conf['LOW']}
- Example Commits: {', '.join([c[:8] for c in pattern['example_commits'][:3]])}"""
            )

        return f"""#### 2.2 Known Green Patterns & Tactics Applied

The following table summarizes the known green software patterns detected in the dataset:

**Table: Known Patterns Ranked by Frequency**

{patterns_table}

**Detailed Pattern Analysis:**

{chr(10).join(pattern_details)}"""

    def _generate_emergent_patterns_section(self, data: dict[str, Any]) -> str:
        """Generate emergent patterns subsection."""
        emergent = data["emergent_patterns"]

        if not emergent:
            return """#### 2.3 Emerging Practices Discovered

No novel microservice-specific green practices were automatically detected. Manual review of high-impact commits may reveal emerging patterns not captured by keyword matching."""

        pattern_list = []
        for pattern in emergent:
            pattern_list.append(
                f"""**Pattern:** {pattern['pattern_name']}
- Occurrences: {pattern['count']}
- Description: {pattern['description']}
- Example Commits: {', '.join([c[:8] for c in pattern['example_commits'][:3]])}"""
            )

        return f"""#### 2.3 Emerging Practices Discovered

{chr(10).join(pattern_list)}"""

    def _generate_repo_analysis_section(self, data: dict[str, Any]) -> str:
        """Generate per-repository analysis subsection."""
        per_repo = data["per_repo_stats"]

        # Top 10 greenest
        top_10_table = (
            "| Repository | Total Commits | Green Commits | Percentage | Patterns Detected |\n"
        )
        top_10_table += (
            "|------------|---------------|---------------|------------|-------------------|\n"
        )
        for repo in per_repo[:10]:
            patterns_str = ", ".join(repo["patterns"][:3]) if repo["patterns"] else "None"
            top_10_table += f"| {repo['repo_name'][:50]} | {repo['total_commits']} | {repo['green_commits']} | {format_percentage(repo['percentage'])} | {patterns_str} |\n"

        # Repos with no green mentions
        no_green = [r for r in per_repo if r["green_commits"] == 0]
        no_green_count = len(no_green)

        return f"""#### 2.4 Per-Repository Analysis

**Top 10 Greenest Repositories (by % green-aware commits):**

{top_10_table}

**Repositories with No Green Mentions:** {no_green_count} out of {len(per_repo)} repositories had zero green-aware commits."""

    def _generate_discussion(self, data: dict[str, Any]) -> str:
        """Generate discussion section."""
        summary = data["summary"]
        green_pct = summary["green_aware_percentage"]

        interpretation = (
            "relatively low" if green_pct < 10 else "moderate" if green_pct < 20 else "high"
        )

        return f"""### 3. Discussion

#### 3.1 Interpretation of Findings

The analysis reveals that {format_percentage(green_pct)} of microservice commits explicitly address energy efficiency or sustainability concerns. This {interpretation} percentage suggests that:

1. **Green software practices exist but are not mainstream:** While developers are applying some energy-efficient patterns, sustainability is not yet a primary concern in microservices development.

2. **Implicit vs. Explicit practices:** Many optimizations (e.g., caching, async processing) may improve energy efficiency without explicitly mentioning it in commit messages.

3. **Domain-specific awareness:** Some repositories show significantly higher green awareness, suggesting that certain domains (e.g., cloud-native, high-scale systems) are more conscious of resource efficiency.

#### 3.2 How Microservice Developers Approach Energy Efficiency

Based on the detected patterns, microservice developers primarily focus on:

- **Performance optimization** as a proxy for energy efficiency
- **Caching strategies** to reduce redundant computations
- **Resource pooling** to minimize connection overhead
- **Asynchronous processing** to improve resource utilization

#### 3.3 Gap Analysis: Literature vs. Practice

**Literature Emphasis:**
- Formal green software engineering methodologies
- Energy measurement and profiling
- Carbon-aware computing

**Practice Emphasis:**
- Performance optimization (implicitly green)
- Cost reduction (aligned with energy efficiency)
- Scalability patterns (may or may not be green)

**Gap:** Explicit sustainability terminology is rare in commit messages, even when applying green patterns.

#### 3.4 Implications for Green Software Engineering in Distributed Systems

1. **Need for awareness:** Developers would benefit from education on how common optimizations contribute to sustainability
2. **Tooling opportunity:** IDE plugins or CI/CD checks could highlight energy implications of code changes
3. **Metrics integration:** Including energy/carbon metrics alongside performance metrics in monitoring dashboards
4. **Best practices dissemination:** Green microservices patterns should be documented and promoted in the community"""

    def _generate_limitations(self) -> str:
        """Generate limitations section."""
        return """### 4. Limitations

#### 4.1 Sample Size and Selection Bias

- Analysis limited to top-starred repositories, which may not represent typical microservices projects
- GitHub-centric sample excludes private enterprise repositories
- Selection based on keywords may miss relevant projects with different terminology

#### 4.2 Commit Message Analysis Limitations

- Commit messages may not fully describe code changes
- Keyword matching cannot detect implicit green practices in code
- English-only analysis excludes international projects
- Developers may not document energy implications in commit messages

#### 4.3 Scope Limitations

- 2-year time window may not capture long-term trends
- Focus on microservices excludes monolithic and other architectures
- No code-level analysis (only commit metadata)
- Heuristic classification may have false positives/negatives

#### 4.4 Future Work Suggestions

1. **AI-powered analysis:** Use Claude Sonnet or similar LLMs for deeper semantic understanding
2. **Code-level inspection:** Analyze actual code changes, not just commit messages
3. **Longitudinal study:** Track green practices evolution over time
4. **Developer surveys:** Complement automated analysis with developer perspectives
5. **Energy measurement:** Correlate detected patterns with actual energy consumption data"""

    def _generate_conclusion(self, data: dict[str, Any]) -> str:
        """Generate conclusion section."""
        summary = data["summary"]
        top_patterns = (
            [p["pattern_name"] for p in data["known_patterns"][:5]]
            if data["known_patterns"]
            else []
        )

        patterns_text = (
            ", ".join(top_patterns[:3]) if top_patterns else "various optimization patterns"
        )

        return f"""### 5. Conclusion

#### 5.1 Summary of Key Findings

This study analyzed {format_number(summary['total_commits'])} commits from {format_number(summary['total_repos'])} microservice repositories and found:

1. **{format_percentage(summary['green_aware_percentage'])}** of commits explicitly address energy/sustainability concerns
2. **{format_number(summary['repos_with_green_commits'])}** repositories demonstrate some level of green awareness
3. Common green patterns include: {patterns_text}

#### 5.2 Answers to Research Questions

**RQ1: What percentage of microservice commits explicitly mention energy efficiency?**
Answer: {format_percentage(summary['green_aware_percentage'])} of analyzed commits contain explicit mentions.

**RQ2: Which green software tactics are developers applying in practice?**
Answer: Developers primarily apply caching strategies, resource pooling, database optimization, and asynchronous processing patterns.

**RQ3: Are there novel microservice-specific green practices not yet documented?**
Answer: Automated keyword analysis found limited evidence of novel patterns. Manual review and AI-powered analysis may reveal more nuanced practices.

#### 5.3 Recommendations for Practitioners

1. **Adopt explicit green terminology:** Document energy implications in commit messages and PR descriptions
2. **Measure and monitor:** Integrate energy/carbon metrics into observability platforms
3. **Apply known patterns:** Systematically apply caching, pooling, and optimization patterns with sustainability in mind
4. **Education and training:** Incorporate green software engineering principles into team training

#### 5.4 Recommendations for Researchers

1. **Develop better detection tools:** Create AI-powered tools for identifying green practices in code
2. **Build pattern catalogs:** Document microservice-specific green patterns with examples
3. **Conduct empirical studies:** Measure actual energy savings from detected patterns
4. **Create benchmarks:** Establish baseline metrics for green microservices

---

**Report End**

*For questions or additional analysis, please refer to the accompanying data files: `green_analysis_results.csv` and `aggregated_statistics.json`*"""

    def save_report(self, report_content: str, output_file: Path):
        """Save report to markdown file."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        colored_print(f"Saved report to {output_file}", "green")


@click.command()
@click.option("--aggregated-file", default=None, help="Input aggregated statistics file")
@click.option("--analysis-file", default=None, help="Input analysis results file")
@click.option("--repos-file", default=None, help="Input repositories file")
@click.option(
    "--output-file",
    default=None,
    help="Output markdown file (default: data/green_microservices_analysis.md)",
)
@click.option("--config-file", default=".env", help="Path to .env configuration file")
def report(
    aggregated_file: Optional[str],
    analysis_file: Optional[str],
    repos_file: Optional[str],
    output_file: Optional[str],
    config_file: str,
):
    """Generate comprehensive markdown report."""
    print_banner("Report Generator")

    try:
        # Load configuration
        config = get_config(config_file)

        # Determine input/output files
        agg_input = Path(aggregated_file) if aggregated_file else config.AGGREGATED_FILE
        analysis_input = Path(analysis_file) if analysis_file else config.ANALYSIS_FILE
        repos_input = Path(repos_file) if repos_file else config.REPOS_FILE
        output = Path(output_file) if output_file else config.REPORT_FILE

        # Check if input files exist
        missing_files = []
        if not agg_input.exists():
            missing_files.append(str(agg_input))
        if not analysis_input.exists():
            missing_files.append(str(analysis_input))
        if not repos_input.exists():
            missing_files.append(str(repos_input))

        if missing_files:
            colored_print("Missing required input files:", "red")
            for f in missing_files:
                colored_print(f"  - {f}", "red")
            colored_print(
                "\nPlease run the full pipeline first: fetch → extract → analyze → aggregate",
                "yellow",
            )
            exit(1)

        # Load data
        colored_print("Loading data files...", "blue")
        aggregated_data = load_json_file(agg_input)
        analysis_data = load_json_file(analysis_input)
        repos_data = load_json_file(repos_input)
        colored_print("✓ Data loaded successfully", "green")

        # Generate report
        colored_print("\nGenerating report...", "blue")
        generator = ReportGenerator()
        report_content = generator.generate_report(aggregated_data, analysis_data, repos_data)

        # Save report
        generator.save_report(report_content, output)

        colored_print("\n✓ Report generated successfully!", "green")
        colored_print(f"Output: {output}", "green")
        colored_print(f"Report size: {len(report_content):,} characters", "white")

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
    report()
