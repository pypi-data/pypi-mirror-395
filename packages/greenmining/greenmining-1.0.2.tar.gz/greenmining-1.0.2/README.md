# greenmining

Green mining for microservices repositories.

[![PyPI](https://img.shields.io/pypi/v/greenmining)](https://pypi.org/project/greenmining/)
[![Python](https://img.shields.io/pypi/pyversions/greenmining)](https://pypi.org/project/greenmining/)
[![License](https://img.shields.io/github/license/adam-bouafia/greenmining)](LICENSE)

## Overview

`greenmining` is a Python library and CLI tool for analyzing GitHub repositories to identify green software engineering practices and energy-efficient patterns. It detects sustainable software patterns across cloud, web, AI, database, networking, and general categories.

## Installation

### Via pip

```bash
pip install greenmining
```

### From source

```bash
git clone https://github.com/adam-bouafia/greenmining.git
cd greenmining
pip install -e .
```

### With Docker

```bash
docker pull adambouafia/greenmining:latest
```

## Quick Start

### CLI Usage

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_github_token"

# Run full analysis pipeline
greenmining pipeline --max-repos 100

# Fetch repositories with custom keywords
greenmining fetch --max-repos 100 --min-stars 100 --keywords "kubernetes docker cloud-native"

# Fetch with default (microservices)
greenmining fetch --max-repos 100 --min-stars 100

# Extract commits
greenmining extract --max-commits 50

# Analyze for green patterns
greenmining analyze

# Analyze with advanced features
greenmining analyze --enable-nlp --enable-ml-features --enable-diff-analysis

# Aggregate results with temporal analysis
greenmining aggregate --enable-temporal --temporal-granularity quarter --enable-enhanced-stats

# Generate report
greenmining report
```

### Python API

#### Basic Pattern Detection

```python
from greenmining import GSF_PATTERNS, is_green_aware, get_pattern_by_keywords

# Check available patterns
print(f"Total patterns: {len(GSF_PATTERNS)}")  # 122 patterns across 15 categories

# Detect green awareness in commit messages
commit_msg = "Optimize Redis caching to reduce energy consumption"
if is_green_aware(commit_msg):
    patterns = get_pattern_by_keywords(commit_msg)
    print(f"Matched patterns: {patterns}")
    # Output: ['Cache Static Data', 'Use Efficient Cache Strategies']
```

#### Fetch Repositories with Custom Keywords (NEW)

```python
from greenmining import fetch_repositories

# Fetch repositories with custom search keywords
repos = fetch_repositories(
    github_token="your_github_token",  # Required: GitHub personal access token
    max_repos=50,                      # Maximum number of repositories to fetch
    min_stars=500,                     # Minimum star count filter
    keywords="kubernetes cloud-native", # Search keywords (space-separated)
    languages=["Python", "Go"],        # Programming language filters
    created_after="2020-01-01",        # Filter by creation date (YYYY-MM-DD)
    created_before="2024-12-31",       # Filter by creation date (YYYY-MM-DD)
    pushed_after="2023-01-01",         # Filter by last push date (YYYY-MM-DD)
    pushed_before="2024-12-31"         # Filter by last push date (YYYY-MM-DD)
)

print(f"Found {len(repos)} repositories")
for repo in repos[:5]:
    print(f"- {repo.full_name} ({repo.stars} stars)")
```

**Parameters:**
- `github_token` (str, required): GitHub personal access token for API authentication
- `max_repos` (int, default=100): Maximum number of repositories to fetch
- `min_stars` (int, default=100): Minimum GitHub stars filter
- `keywords` (str, default="microservices"): Space-separated search keywords
- `languages` (list[str], optional): Programming language filters (e.g., ["Python", "Go", "Java"])
- `created_after` (str, optional): Filter repos created after date (format: "YYYY-MM-DD")
- `created_before` (str, optional): Filter repos created before date (format: "YYYY-MM-DD")
- `pushed_after` (str, optional): Filter repos pushed after date (format: "YYYY-MM-DD")
- `pushed_before` (str, optional): Filter repos pushed before date (format: "YYYY-MM-DD")

#### Analyze Repository Commits

```python
from greenmining.services.commit_extractor import CommitExtractor
from greenmining.services.data_analyzer import DataAnalyzer
from greenmining.analyzers.nlp_analyzer import NLPAnalyzer
from greenmining.analyzers.ml_feature_extractor import MLFeatureExtractor
from greenmining import fetch_repositories

# Fetch repositories with custom keywords
repos = fetch_repositories(
    github_token="your_token",
    max_repos=10,
    keywords="serverless edge-computing"
)

# Initialize commit extractor with parameters
extractor = CommitExtractor(
    exclude_merge_commits=True,      # Skip merge commits (default: True)
    exclude_bot_commits=True,        # Skip bot commits (default: True)
    min_message_length=10            # Minimum commit message length (default: 10)
)

# Initialize analyzer with advanced features
analyzer = DataAnalyzer(
    enable_diff_analysis=False,      # Enable code diff analysis (slower but more accurate)
    enable_nlp=True,                 # Enable NLP-enhanced pattern detection
    enable_ml_features=True,         # Enable ML feature extraction
    patterns=None,                   # Custom pattern dict (default: GSF_PATTERNS)
    batch_size=10                    # Batch processing size (default: 10)
)

# Optional: Configure NLP analyzer separately
nlp_analyzer = NLPAnalyzer(
    enable_stemming=True,            # Enable morphological analysis (optimize→optimizing)
    enable_synonyms=True             # Enable semantic synonym matching (cache→buffer)
)

# Optional: Configure ML feature extractor
ml_extractor = MLFeatureExtractor(
    green_keywords=None              # Custom keyword list (default: built-in 19 keywords)
)

# Extract commits from first repo
commits = extractor.extract_commits(
    repository=repos[0],             # PyGithub Repository object
    max_commits=50,                  # Maximum commits to extract per repository
    since=None,                      # Start date filter (datetime object, optional)
    until=None                       # End date filter (datetime object, optional)
)

**CommitExtractor Parameters:**
- `exclude_merge_commits` (bool, default=True): Skip merge commits during extraction
- `exclude_bot_commits` (bool, default=True): Skip commits from bot accounts
- `min_message_length` (int, default=10): Minimum length for commit message to be included

**DataAnalyzer Parameters:**
- `enable_diff_analysis` (bool, default=False): Enable code diff analysis (slower)
- `enable_nlp` (bool, default=False): Enable NLP-enhanced pattern detection
- `enable_ml_features` (bool, default=False): Enable ML feature extraction
- `patterns` (dict, optional): Custom pattern dictionary (default: GSF_PATTERNS)
- `batch_size` (int, default=10): Number of commits to process in each batch

**NLPAnalyzer Parameters:**
- `enable_stemming` (bool, default=True): Enable morphological variant matching
- `enable_synonyms` (bool, default=True): Enable semantic synonym expansion

**MLFeatureExtractor Parameters:**
- `green_keywords` (list[str], optional): Custom green keywords list

# Analyze commits for green patterns
results = []
for commit in commits:
    result = analyzer.analyze_commit(commit)
    if result['green_aware']:
        results.append(result)
        print(f"Green commit found: {commit.message[:50]}...")
        print(f"  Patterns: {result['known_pattern']}")
        
        # Access NLP analysis results (NEW)
        if 'nlp_analysis' in result:
            nlp = result['nlp_analysis']
            print(f"  NLP: {nlp['morphological_count']} morphological matches, "
                  f"{nlp['semantic_count']} semantic matches")
        
        # Access ML features (NEW)
        if 'ml_features' in result:
            ml = result['ml_features']['text']
            print(f"  ML Features: {ml['word_count']} words, "
                  f"keyword density: {ml['keyword_density']:.2f}")
```

#### Access Sustainability Patterns Data

```python
from greenmining import GSF_PATTERNS

# Get all patterns by category
cloud_patterns = {
    pid: pattern for pid, pattern in GSF_PATTERNS.items()
    if pattern['category'] == 'cloud'
}
print(f"Cloud patterns: {len(cloud_patterns)}")  # 40 patterns

ai_patterns = {
    pid: pattern for pid, pattern in GSF_PATTERNS.items()
    if pattern['category'] == 'ai'
}
print(f"AI/ML patterns: {len(ai_patterns)}")  # 19 patterns

# Get pattern details
cache_pattern = GSF_PATTERNS['gsf_001']
print(f"Pattern: {cache_pattern['name']}")
print(f"Category: {cache_pattern['category']}")
print(f"Keywords: {cache_pattern['keywords']}")
print(f"Impact: {cache_pattern['sci_impact']}")

# List all available categories
categories = set(p['category'] for p in GSF_PATTERNS.values())
print(f"Available categories: {sorted(categories)}")
# Output: ['ai', 'async', 'caching', 'cloud', 'code', 'data', 
#          'database', 'general', 'infrastructure', 'microservices',
#          'monitoring', 'network', 'networking', 'resource', 'web']
```

#### Advanced Analysis: Temporal Trends (NEW)

```python
from greenmining.services.data_aggregator import DataAggregator
from greenmining.analyzers.temporal_analyzer import TemporalAnalyzer
from greenmining.analyzers.qualitative_analyzer import QualitativeAnalyzer

# Initialize aggregator with all advanced features
aggregator = DataAggregator(
    config=None,                        # Config object (optional)
    enable_enhanced_stats=True,         # Enable statistical analysis (correlations, trends)
    enable_temporal=True,               # Enable temporal trend analysis
    temporal_granularity="quarter"      # Time granularity: day/week/month/quarter/year
)

# Optional: Configure temporal analyzer separately
temporal_analyzer = TemporalAnalyzer(
    granularity="quarter"               # Time period granularity for grouping commits
)

# Optional: Configure qualitative analyzer for validation sampling
qualitative_analyzer = QualitativeAnalyzer(
    sample_size=30,                     # Number of samples for manual validation
    stratify_by="pattern"               # Stratification method: pattern/repository/time/random
)

# Aggregate results with temporal insights
aggregated = aggregator.aggregate(
    analysis_results=analysis_results,  # List of analysis result dictionaries
    repositories=repositories           # List of PyGithub repository objects
)

**DataAggregator Parameters:**
- `config` (Config, optional): Configuration object
- `enable_enhanced_stats` (bool, default=False): Enable pattern correlations and effect size analysis
- `enable_temporal` (bool, default=False): Enable temporal trend analysis over time
- `temporal_granularity` (str, default="quarter"): Time granularity (day/week/month/quarter/year)

**TemporalAnalyzer Parameters:**
- `granularity` (str, default="quarter"): Time period for grouping (day/week/month/quarter/year)

**QualitativeAnalyzer Parameters:**
- `sample_size` (int, default=30): Number of commits to sample for validation
- `stratify_by` (str, default="pattern"): Stratification method (pattern/repository/time/random)

# Access temporal analysis results
temporal = aggregated['temporal_analysis']
print(f"Time periods analyzed: {len(temporal['periods'])}")

# View pattern adoption trends over time
for period_data in temporal['periods']:
    print(f"{period_data['period']}: {period_data['commit_count']} commits, "
          f"{period_data['green_awareness_rate']:.1%} green awareness")

# Access pattern evolution insights
evolution = temporal.get('pattern_evolution', {})
print(f"Emerging patterns: {evolution.get('emerging', [])}")
print(f"Stable patterns: {evolution.get('stable', [])}")
```

#### Generate Custom Reports

```python
from greenmining.services.data_aggregator import DataAggregator
from greenmining.config import Config

config = Config()
aggregator = DataAggregator(config)

# Load analysis results
results = aggregator.load_analysis_results()

# Generate statistics
stats = aggregator.calculate_statistics(results)
print(f"Total commits analyzed: {stats['total_commits']}")
print(f"Green-aware commits: {stats['green_aware_count']}")
print(f"Top patterns: {stats['top_patterns'][:5]}")

# Export to CSV
aggregator.export_to_csv(results, "output.csv")
```

#### Batch Analysis

```python
from greenmining.controllers.repository_controller import RepositoryController
from greenmining.config import Config

config = Config()
controller = RepositoryController(config)

# Run full pipeline programmatically
controller.fetch_repositories(max_repos=50)
controller.extract_commits(max_commits=100)
controller.analyze_commits()
controller.aggregate_results()
controller.generate_report()

print("Analysis complete! Check data/ directory for results.")
```

### Docker Usage

```bash
# Run analysis pipeline
docker run -v $(pwd)/data:/app/data \
           adambouafia/greenmining:latest --help

# With custom configuration
docker run -v $(pwd)/.env:/app/.env:ro \
           -v $(pwd)/data:/app/data \
           adambouafia/greenmining:latest pipeline --max-repos 50

# Interactive shell
docker run -it adambouafia/greenmining:latest /bin/bash
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
GITHUB_TOKEN=your_github_personal_access_token

# Optional - Repository Fetching
MAX_REPOS=100
MIN_STARS=100
SUPPORTED_LANGUAGES=Python,Java,Go,JavaScript,TypeScript
SEARCH_KEYWORDS=microservices

# Optional - Commit Extraction
COMMITS_PER_REPO=50
EXCLUDE_MERGE_COMMITS=true
EXCLUDE_BOT_COMMITS=true

# Optional - Analysis Features
ENABLE_DIFF_ANALYSIS=false
ENABLE_NLP=true
ENABLE_ML_FEATURES=true
BATCH_SIZE=10

# Optional - Temporal Analysis
ENABLE_TEMPORAL=true
TEMPORAL_GRANULARITY=quarter
ENABLE_ENHANCED_STATS=true

# Optional - Output
OUTPUT_DIR=./data
REPORT_FORMAT=markdown
```

### Config Object Parameters

```python
from greenmining.config import Config

config = Config(
    # GitHub API
    github_token="your_token",              # GitHub personal access token (required)
    
    # Repository Fetching
    max_repos=100,                          # Maximum repositories to fetch
    min_stars=100,                          # Minimum star threshold
    supported_languages=["Python", "Go"],   # Language filters
    search_keywords="microservices",        # Default search keywords
    
    # Commit Extraction
    max_commits=50,                         # Commits per repository
    exclude_merge_commits=True,             # Skip merge commits
    exclude_bot_commits=True,               # Skip bot commits
    min_message_length=10,                  # Minimum commit message length
    
    # Analysis Options
    enable_diff_analysis=False,             # Enable code diff analysis
    enable_nlp=True,                        # Enable NLP features
    enable_ml_features=True,                # Enable ML feature extraction
    batch_size=10,                          # Batch processing size
    
    # Temporal Analysis
    enable_temporal=True,                   # Enable temporal trend analysis
    temporal_granularity="quarter",         # day/week/month/quarter/year
    enable_enhanced_stats=True,             # Enable statistical analysis
    
    # Output Configuration
    output_dir="./data",                    # Output directory path
    repos_file="repositories.json",         # Repositories filename
    commits_file="commits.json",            # Commits filename
    analysis_file="analysis_results.json",  # Analysis results filename
    stats_file="aggregated_statistics.json", # Statistics filename
    report_file="green_analysis.md"         # Report filename
)
```

## Features

### Core Capabilities

- **Pattern Detection**: Automatically identifies 122 sustainability patterns across 15 categories
- **Keyword Analysis**: Scans commit messages using 321 green software keywords
- **Custom Repository Fetching**: Fetch repositories with custom search keywords (not limited to microservices)
- **Repository Analysis**: Analyzes repositories from GitHub with flexible filtering
- **Batch Processing**: Analyze hundreds of repositories and thousands of commits
- **Multi-format Output**: Generates Markdown reports, CSV exports, and JSON data
- **Statistical Analysis**: Calculates green-awareness metrics, pattern distribution, and trends
- **Docker Support**: Pre-built images for containerized analysis
- **Programmatic API**: Full Python API for custom workflows and integrations
- **Clean Architecture**: Modular design with services layer (Fetcher, Extractor, Analyzer, Aggregator, Reports)

### Pattern Database

**122 green software patterns based on:**
- Green Software Foundation (GSF) Patterns Catalog
- VU Amsterdam 2024 research on ML system sustainability
- ICSE 2024 conference papers on sustainable software

### Detection Performance

- **Coverage**: 67% of patterns actively detect in real-world commits
- **Accuracy**: 100% true positive rate for green-aware commits
- **Categories**: 15 distinct sustainability domains covered
- **Keywords**: 321 detection terms across all patterns

## GSF Pattern Categories

**122 patterns across 15 categories:**

### 1. Cloud (40 patterns)
Auto-scaling, serverless computing, right-sizing instances, region selection for renewable energy, spot instances, idle resource detection, cloud-native architectures

### 2. Web (17 patterns)
CDN usage, caching strategies, lazy loading, asset compression, image optimization, minification, code splitting, tree shaking, prefetching

### 3. AI/ML (19 patterns)
Model optimization, pruning, quantization, edge inference, batch optimization, efficient training, model compression, hardware acceleration, green ML pipelines

### 4. Database (5 patterns)
Indexing strategies, query optimization, connection pooling, prepared statements, database views, denormalization for efficiency

### 5. Networking (8 patterns)
Protocol optimization, connection reuse, HTTP/2, gRPC, efficient serialization, compression, persistent connections

### 6. Network (6 patterns)
Request batching, GraphQL optimization, API gateway patterns, circuit breakers, rate limiting, request deduplication

### 7. Caching (2 patterns)
Multi-level caching, cache invalidation strategies, data deduplication, distributed caching

### 8. Resource (2 patterns)
Resource limits, dynamic allocation, memory management, CPU throttling

### 9. Data (3 patterns)
Efficient serialization formats, pagination, streaming, data compression

### 10. Async (3 patterns)
Event-driven architecture, reactive streams, polling elimination, non-blocking I/O

### 11. Code (4 patterns)
Algorithm optimization, code efficiency, garbage collection tuning, memory profiling

### 12. Monitoring (3 patterns)
Energy monitoring, performance profiling, APM tools, observability patterns

### 13. Microservices (4 patterns)
Service decomposition, colocation strategies, graceful shutdown, service mesh optimization

### 14. Infrastructure (4 patterns)
Alpine containers, Infrastructure as Code, renewable energy regions, container optimization

### 15. General (8 patterns)
Feature flags, incremental processing, precomputation, background jobs, workflow optimization

## CLI Commands

| Command | Description | Key Options |
|---------|-------------|-------------|
| `fetch` | Fetch repositories from GitHub with custom keywords | `--max-repos`, `--min-stars`, `--languages`, `--keywords` |
| `extract` | Extract commit history from repositories | `--max-commits` per repository |
| `analyze` | Analyze commits for green patterns | `--enable-nlp`, `--enable-ml-features`, `--enable-diff-analysis` |
| `aggregate` | Aggregate analysis results | `--enable-temporal`, `--temporal-granularity`, `--enable-enhanced-stats` |
| `report` | Generate comprehensive report | Creates Markdown and CSV outputs |
| `pipeline` | Run complete analysis pipeline | `--max-repos`, `--max-commits` (all-in-one) |
| `status` | Show current analysis status | Displays progress and file statistics |

### Command Details

#### Fetch Repositories
```bash
# Fetch with custom search keywords
greenmining fetch --max-repos 100 --min-stars 50 --languages Python --keywords "kubernetes docker"

# Fetch microservices (default)
greenmining fetch --max-repos 100 --min-stars 50 --languages Python
```
Options:
- `--max-repos`: Maximum repositories to fetch (default: 100)
- `--min-stars`: Minimum GitHub stars (default: 100)
- `--languages`: Filter by programming languages (default: "Python,Java,Go,JavaScript,TypeScript")
- `--keywords`: Custom search keywords (default: "microservices")

#### Extract Commits
```bash
greenmining extract --max-commits 50
```
Options:
- `--max-commits`: Maximum commits per repository (default: 50)

#### Analyze Commits (with Advanced Features)
```bash
# Basic analysis
greenmining analyze

# Advanced analysis with all features
greenmining analyze --enable-nlp --enable-ml-features --enable-diff-analysis --batch-size 20
```
Options:
- `--batch-size`: Batch size for processing (default: 10)
- `--enable-diff-analysis`: Enable code diff analysis (slower but more accurate)
- `--enable-nlp`: Enable NLP-enhanced pattern detection with morphological variants and synonyms
- `--enable-ml-features`: Enable ML feature extraction for model training

#### Aggregate Results (with Temporal Analysis)
```bash
# Basic aggregation
greenmining aggregate

# Advanced aggregation with temporal trends
greenmining aggregate --enable-temporal --temporal-granularity quarter --enable-enhanced-stats
```
Options:
- `--enable-enhanced-stats`: Enable enhanced statistical analysis (correlations, effect sizes)
- `--enable-temporal`: Enable temporal trend analysis
- `--temporal-granularity`: Time period granularity (choices: day, week, month, quarter, year)

#### Run Pipeline
```bash
greenmining pipeline --max-repos 50 --max-commits 100
```
Options:
- `--max-repos`: Repositories to analyze
- `--max-commits`: Commits per repository
- Executes: fetch → extract → analyze → aggregate → report

## Output Files

All outputs are saved to the `data/` directory:

- `repositories.json` - Repository metadata
- `commits.json` - Extracted commit data
- `analysis_results.json` - Pattern analysis results
- `aggregated_statistics.json` - Summary statistics
- `green_analysis_results.csv` - CSV export for spreadsheets
- `green_microservices_analysis.md` - Final report

## Development

```bash
# Clone repository
git clone https://github.com/adam-bouafia/greenmining.git
cd greenmining

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=greenmining tests/

# Format code
black greenmining/ tests/
ruff check greenmining/ tests/
```

## Requirements

- Python 3.9+
- PyGithub >= 2.1.1
- PyDriller >= 2.5
- pandas >= 2.2.0
- click >= 8.1.7

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Links

- **GitHub**: https://github.com/adam-bouafia/greenmining
- **PyPI**: https://pypi.org/project/greenmining/
- **Docker Hub**: https://hub.docker.com/r/adambouafia/greenmining
- **Documentation**: https://github.com/adam-bouafia/greenmining#readme


