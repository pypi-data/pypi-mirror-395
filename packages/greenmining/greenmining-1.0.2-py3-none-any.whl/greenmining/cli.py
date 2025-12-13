"""Green Microservices Mining CLI"""

import click

from greenmining.config import Config
from greenmining.controllers.repository_controller import RepositoryController
from greenmining.presenters.console_presenter import ConsolePresenter
from greenmining.utils import colored_print, load_json_file

# Initialize configuration
config = Config()

# Initialize presenter
presenter = ConsolePresenter()


@click.group()
@click.option("--config-file", default=".env", help="Path to configuration file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def cli(config_file, verbose):
    """Green Microservices Mining"""
    if verbose:
        config.VERBOSE = True


@cli.command()
@click.option("--max-repos", default=100, type=int, help="Maximum repositories to fetch")
@click.option("--min-stars", default=100, type=int, help="Minimum stars required")
@click.option(
    "--languages", default="Python,Java,Go,JavaScript,TypeScript", help="Comma-separated languages"
)
@click.option(
    "--keywords",
    default="microservices",
    type=str,
    help="Search keywords (e.g., 'kubernetes', 'docker', 'cloud-native')",
)
@click.option("--created-after", type=str, help="Repository created after (YYYY-MM-DD)")
@click.option("--created-before", type=str, help="Repository created before (YYYY-MM-DD)")
@click.option("--pushed-after", type=str, help="Repository pushed after (YYYY-MM-DD)")
@click.option("--pushed-before", type=str, help="Repository pushed before (YYYY-MM-DD)")
def fetch(
    max_repos,
    min_stars,
    languages,
    keywords,
    created_after,
    created_before,
    pushed_after,
    pushed_before,
):
    """Fetch repositories from GitHub based on custom search keywords."""
    presenter.show_banner()
    colored_print(f"\n🎯 Target: {max_repos} repositories\n", "cyan")

    controller = RepositoryController(config)
    lang_list = [lang.strip() for lang in languages.split(",")]

    try:
        repositories = controller.fetch_repositories(
            max_repos=max_repos,
            min_stars=min_stars,
            languages=lang_list,
            keywords=keywords,
            created_after=created_after,
            created_before=created_before,
            pushed_after=pushed_after,
            pushed_before=pushed_before,
        )

        # Show results
        repo_dicts = [r.to_dict() for r in repositories]
        presenter.show_repositories(repo_dicts, limit=10)

        stats = controller.get_repository_stats(repositories)
        colored_print(f"\n📊 Total Stars: {stats.get('total_stars', 0):,}", "green")
        colored_print(f"📈 Average Stars: {stats.get('avg_stars', 0):.0f}", "green")

        presenter.show_success(f"Fetched {len(repositories)} repositories successfully!")

    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


@cli.command()
@click.option("--max-commits", default=50, type=int, help="Max commits per repository")
@click.option("--skip-merges", is_flag=True, default=True, help="Skip merge commits")
@click.option("--days-back", default=730, type=int, help="Days to look back (default: 2 years)")
@click.option("--timeout", default=60, type=int, help="Timeout per repo in seconds (default: 60)")
def extract(max_commits, skip_merges, days_back, timeout):
    """Extract commits from fetched repositories."""
    presenter.show_banner()

    from greenmining.services.commit_extractor import CommitExtractor

    try:
        # Load repositories
        controller = RepositoryController(config)
        repositories = controller.load_repositories()

        colored_print(f"\n📝 Extracting commits from {len(repositories)} repositories...\n", "cyan")
        colored_print(
            f"   Settings: max={max_commits}/repo, skip_merges={skip_merges}, days_back={days_back}\n",
            "cyan",
        )

        # Extract commits
        extractor = CommitExtractor(
            max_commits=max_commits, skip_merges=skip_merges, days_back=days_back, timeout=timeout
        )
        commits = extractor.extract_from_repositories(
            repositories=[r.to_dict() for r in repositories]
        )

        # Save commits
        from greenmining.utils import save_json_file

        save_json_file(commits, config.COMMITS_FILE)
        colored_print(f"   Saved to: {config.COMMITS_FILE}", "cyan")

        # Show stats
        stats = {
            "total_commits": len(commits),
            "total_repos": len(repositories),
            "avg_per_repo": len(commits) / len(repositories) if repositories else 0,
        }

        presenter.show_commit_stats(stats)
        presenter.show_success(f"Extracted {len(commits)} commits successfully!")

    except FileNotFoundError as e:
        presenter.show_error(str(e))
        colored_print("💡 Run 'fetch' command first to get repositories", "yellow")
        raise click.Abort() from e
    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


@cli.command()
@click.option("--batch-size", default=10, type=int, help="Batch size for processing")
@click.option("--enable-diff-analysis", is_flag=True, help="Enable code diff analysis (slower)")
@click.option("--enable-nlp", is_flag=True, help="Enable NLP-enhanced pattern detection")
@click.option("--enable-ml-features", is_flag=True, help="Enable ML feature extraction")
def analyze(batch_size, enable_diff_analysis, enable_nlp, enable_ml_features):
    """Analyze commits for green software patterns."""
    presenter.show_banner()

    from greenmining.services.data_analyzer import DataAnalyzer
    from greenmining.utils import save_json_file

    try:
        # Load commits
        if not config.COMMITS_FILE.exists():
            raise FileNotFoundError("No commits file found. Run 'extract' first.")

        commits = load_json_file(config.COMMITS_FILE)
        colored_print(f"\n🔬 Analyzing {len(commits)} commits for green patterns...\n", "cyan")

        # Show enabled methods
        methods = ["Keyword"]
        if enable_diff_analysis:
            methods.append("Code Diff")
        if enable_nlp:
            methods.append("NLP")
        if enable_ml_features:
            methods.append("ML Features")

        colored_print(f"   Methods: {' + '.join(methods)}\n", "cyan")
        colored_print(f"   Batch size: {batch_size}\n", "cyan")

        # Analyze
        analyzer = DataAnalyzer(
            batch_size=batch_size,
            enable_diff_analysis=enable_diff_analysis,
            enable_nlp=enable_nlp,
            enable_ml_features=enable_ml_features,
        )
        results = analyzer.analyze_commits(commits)

        # Save results
        save_json_file(results, config.ANALYSIS_FILE)

        # Show results
        green_count = sum(1 for r in results if r.get("green_aware", False))
        green_rate = (green_count / len(results)) if results else 0

        results_dict = {
            "summary": {
                "total_commits": len(results),
                "green_commits": green_count,
                "green_commit_rate": green_rate,
            },
            "known_patterns": {},
        }

        presenter.show_analysis_results(results_dict)
        presenter.show_success(f"Analysis complete! Results saved to {config.ANALYSIS_FILE}")

    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


@cli.command()
@click.option("--enable-enhanced-stats", is_flag=True, help="Enable enhanced statistical analysis")
@click.option("--enable-temporal", is_flag=True, help="Enable temporal trend analysis")
@click.option(
    "--temporal-granularity",
    default="quarter",
    type=click.Choice(["day", "week", "month", "quarter", "year"]),
    help="Temporal analysis granularity",
)
def aggregate(enable_enhanced_stats, enable_temporal, temporal_granularity):
    """Aggregate analysis results and generate statistics."""
    presenter.show_banner()

    from greenmining.services.data_aggregator import DataAggregator
    from greenmining.utils import save_json_file

    try:
        # Load data
        if not config.ANALYSIS_FILE.exists():
            raise FileNotFoundError("No analysis file found. Run 'analyze' first.")

        results = load_json_file(config.ANALYSIS_FILE)
        repos = load_json_file(config.REPOS_FILE) if config.REPOS_FILE.exists() else []

        colored_print(f"\n📊 Aggregating results from {len(results)} commits...\n", "cyan")

        # Show enabled features
        if enable_enhanced_stats:
            colored_print("   Enhanced statistics: Enabled\n", "cyan")
        if enable_temporal:
            colored_print(
                f"   Temporal analysis: Enabled (granularity: {temporal_granularity})\n", "cyan"
            )

        # Aggregate
        aggregator = DataAggregator(
            enable_enhanced_stats=enable_enhanced_stats,
            enable_temporal=enable_temporal,
            temporal_granularity=temporal_granularity,
        )
        aggregated = aggregator.aggregate(results, repos)

        # Save
        save_json_file(aggregated, config.AGGREGATED_FILE)

        # Show results
        presenter.show_analysis_results(aggregated)

        if aggregated.get("known_patterns"):
            # Convert list format to dict format expected by presenter
            patterns_dict = {}
            for pattern in aggregated["known_patterns"]:
                patterns_dict[pattern["pattern_name"]] = {
                    "count": pattern["count"],
                    "percentage": pattern["percentage"],
                    "confidence_distribution": pattern.get("confidence_breakdown", {}),
                }
            presenter.show_pattern_distribution(patterns_dict, limit=10)

        presenter.show_success(f"Aggregation complete! Results saved to {config.AGGREGATED_FILE}")

    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


@cli.command()
@click.option("--output", default="green_microservices_analysis.md", help="Output filename")
def report(output):
    """Generate comprehensive markdown report."""
    presenter.show_banner()

    from greenmining.services.reports import ReportGenerator

    try:
        # Load aggregated data
        if not config.AGGREGATED_FILE.exists():
            raise FileNotFoundError("No aggregated data found. Run 'aggregate' first.")

        # Load analysis results
        if not config.ANALYSIS_FILE.exists():
            raise FileNotFoundError("No analysis results found. Run 'analyze' first.")

        # Load repository data
        if not config.REPOS_FILE.exists():
            raise FileNotFoundError("No repository data found. Run 'fetch' first.")

        aggregated = load_json_file(config.AGGREGATED_FILE)
        analysis_results = load_json_file(config.ANALYSIS_FILE)
        repos_data = load_json_file(config.REPOS_FILE)

        # Wrap analysis results if it's a list
        if isinstance(analysis_results, list):
            analysis = {"results": analysis_results, "total": len(analysis_results)}
        else:
            analysis = analysis_results

        # Wrap repos data if it's a list
        if isinstance(repos_data, list):
            repos = {"repositories": repos_data, "total": len(repos_data)}
        else:
            repos = repos_data

        colored_print("\n📄 Generating comprehensive report...\n", "cyan")

        # Generate report
        generator = ReportGenerator()
        report_content = generator.generate_report(aggregated, analysis, repos)

        # Save report
        from pathlib import Path

        report_path = Path(output)
        report_path.write_text(report_content)

        presenter.show_success(f"Report generated: {report_path}")
        colored_print("\n📖 The report includes:", "cyan")
        colored_print("   • Executive Summary", "white")
        colored_print("   • Methodology", "white")
        colored_print("   • Results & Statistics", "white")
        colored_print("   • Pattern Analysis", "white")
        colored_print("   • Per-Repository Breakdown", "white")
        colored_print("   • Discussion & Conclusions", "white")

    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


@cli.command()
def status():
    """Show current pipeline status."""
    presenter.show_banner()

    phases = {
        "1. Fetch Repositories": {
            "file": str(config.REPOS_FILE),
            "completed": config.REPOS_FILE.exists(),
            "size": (
                f"{config.REPOS_FILE.stat().st_size / 1024:.1f} KB"
                if config.REPOS_FILE.exists()
                else "N/A"
            ),
        },
        "2. Extract Commits": {
            "file": str(config.COMMITS_FILE),
            "completed": config.COMMITS_FILE.exists(),
            "size": (
                f"{config.COMMITS_FILE.stat().st_size / 1024:.1f} KB"
                if config.COMMITS_FILE.exists()
                else "N/A"
            ),
        },
        "3. Analyze Commits": {
            "file": str(config.ANALYSIS_FILE),
            "completed": config.ANALYSIS_FILE.exists(),
            "size": (
                f"{config.ANALYSIS_FILE.stat().st_size / 1024:.1f} KB"
                if config.ANALYSIS_FILE.exists()
                else "N/A"
            ),
        },
        "4. Aggregate Results": {
            "file": str(config.AGGREGATED_FILE),
            "completed": config.AGGREGATED_FILE.exists(),
            "size": (
                f"{config.AGGREGATED_FILE.stat().st_size / 1024:.1f} KB"
                if config.AGGREGATED_FILE.exists()
                else "N/A"
            ),
        },
        "5. Generate Report": {
            "file": str(config.REPORT_FILE),
            "completed": config.REPORT_FILE.exists(),
            "size": (
                f"{config.REPORT_FILE.stat().st_size / 1024:.1f} KB"
                if config.REPORT_FILE.exists()
                else "N/A"
            ),
        },
    }

    presenter.show_pipeline_status(phases)

    # Show next step
    for phase_name, info in phases.items():
        if not info["completed"]:
            colored_print(f"\n💡 Next step: {phase_name}", "yellow")
            break
    else:
        colored_print("\n✅ All phases complete!", "green")


@cli.command()
@click.option("--max-repos", default=100, type=int, help="Maximum repositories to analyze")
@click.option("--skip-fetch", is_flag=True, help="Skip fetch phase if data exists")
def pipeline(max_repos, skip_fetch):
    """Run full pipeline: fetch → extract → analyze → aggregate → report."""
    presenter.show_banner()

    colored_print("\n🚀 Starting Full Pipeline...\n", "green")
    colored_print(f"   Target: {max_repos} repositories", "cyan")
    colored_print("   Phases: fetch → extract → analyze → aggregate → report\n", "cyan")

    try:
        # Phase 1: Fetch
        if not skip_fetch or not config.REPOS_FILE.exists():
            colored_print("\n[1/5] 🔍 Fetching repositories...", "cyan")
            controller = RepositoryController(config)
            controller.fetch_repositories(max_repos=max_repos)
        else:
            colored_print("\n[1/5] ⏭️  Skipping fetch (using existing data)", "yellow")

        # Phase 2: Extract
        colored_print("\n[2/5] 📝 Extracting commits...", "cyan")
        from greenmining.services.commit_extractor import CommitExtractor
        from greenmining.utils import save_json_file

        controller = RepositoryController(config)
        repos = controller.load_repositories()
        extractor = CommitExtractor()
        commits = extractor.extract_from_repositories([r.to_dict() for r in repos])
        save_json_file(commits, config.COMMITS_FILE)
        colored_print(f"   Saved {len(commits)} commits to: {config.COMMITS_FILE}", "green")

        # Phase 3: Analyze
        colored_print("\n[3/5] 🔬 Analyzing commits...", "cyan")
        from greenmining.services.data_analyzer import DataAnalyzer

        commits = load_json_file(config.COMMITS_FILE)
        analyzer = DataAnalyzer()
        results = analyzer.analyze_commits_batch(commits)
        save_json_file(results, config.ANALYSIS_FILE)
        colored_print(
            f"   Analyzed {len(results)} commits, saved to: {config.ANALYSIS_FILE}", "green"
        )

        # Phase 4: Aggregate
        colored_print("\n[4/5] 📊 Aggregating results...", "cyan")
        from greenmining.services.data_aggregator import DataAggregator

        aggregator = DataAggregator()
        aggregated = aggregator.aggregate(results, [r.to_dict() for r in repos])
        save_json_file(aggregated, config.AGGREGATED_FILE)

        # Phase 5: Report
        colored_print("\n[5/5] 📄 Generating report...", "cyan")
        from greenmining.services.reports import ReportGenerator

        generator = ReportGenerator()
        generator.generate_report(aggregated)

        colored_print("\n" + "=" * 60, "green")
        colored_print("✅ Pipeline Complete!", "green")
        colored_print("=" * 60, "green")

        presenter.show_success(f"All results saved to {config.OUTPUT_DIR}")
        colored_print(f"\n📖 View report: {config.REPORT_FILE}", "cyan")

    except Exception as e:
        presenter.show_error(str(e))
        raise click.Abort() from e


if __name__ == "__main__":
    cli()
