# umpyre

Code analysis and quality metrics tracking system for CI/CD pipelines.

## Overview

`umpyre` provides automated code metrics collection and tracking for Python projects, designed to integrate seamlessly with GitHub Actions CI/CD pipelines. Track code quality trends over time with minimal overhead.

**Key Features:**
- 🎯 **Pluggable collectors**: Workflow status, complexity (wily), coverage, code statistics
- 📊 **Git-based storage**: Metrics stored in separate branch, no external dependencies
- ⚙️ **Config-driven**: Customize via YAML configuration
- 🚀 **Fast & lightweight**: Limited history tracking for speed
- 🔌 **GitHub Action**: Drop-in integration for existing workflows

## Installation

```bash
pip install umpyre
```

## Quick Start

### 1. Create Configuration

Create `.github/umpyre-config.yml`:

```yaml
schema_version: "1.0"

collectors:
  workflow_status:
    enabled: true
    lookback_runs: 10
  
  coverage:
    enabled: true
    source: pytest-cov
  
  umpyre_stats:
    enabled: true
    exclude_dirs: [tests, examples, scrap]

storage:
  branch: code-metrics
  formats: [json, csv]
```

### 2. Add to GitHub Actions

In your `.github/workflows/ci.yml` (after successful PyPI publish):

```yaml
- name: Track Code Metrics
  if: success()  # Only track metrics after successful publish
  uses: i2mint/umpyre/actions/track-metrics@master
  continue-on-error: true  # Never fails CI - see FAILURE_PROTECTION.md
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    config-path: .github/umpyre-config.yml  # Optional: defaults to this path
```

**Important**: Metrics collection has **triple-layer failure protection** and will never break your CI pipeline. See [FAILURE_PROTECTION.md](FAILURE_PROTECTION.md) for details.

### 3. View Metrics

Metrics are stored in the `code-metrics` branch:
- `metrics.json` - Latest snapshot
- `metrics.csv` - Flat format for analysis
- `history/` - Flat historical records (filename format: `YYYY_MM_DD_HH_MM_SS__commit__version.json`)

See [STORAGE_STRUCTURE.md](STORAGE_STRUCTURE.md) for full details on storage design and querying.

## CLI Usage

```bash
# Collect and store metrics
python -m umpyre.cli collect

# Collect with custom config
python -m umpyre.cli collect --config my-config.yml

# Dry run (don't store)
python -m umpyre.cli collect --no-store

# Validate against thresholds (coming soon)
python -m umpyre.cli validate
```

## Querying Stored Metrics

Metrics are stored in a flat structure with parseable filenames: `YYYY_MM_DD_HH_MM_SS__shahash__version.json`

### Shell Queries

```bash
# Switch to metrics branch
git checkout code-metrics

# Get all metrics from November 14
ls history/2025_11_14_*

# Find metrics for specific commit
ls history/*__700e012__*

# Find all v0.1.0 metrics
ls history/*__0.1.0.json

# Get latest 10 metrics
ls -t history/ | head -10

# Exclude metrics without version
ls history/ | grep -v "__none.json"
```

### Python Queries

```python
from pathlib import Path
from umpyre.storage import (
    parse_metric_filename,
    find_metrics_by_commit,
    find_metrics_by_version,
    get_latest_metric_for_version,
    get_all_versions,
)

history_dir = Path("history")

# Parse filename
info = parse_metric_filename("2025_11_14_22_45_00__700e012__0.1.0.json")
print(info['commit_sha'])    # '700e012'
print(info['pypi_version'])  # '0.1.0'
print(info['timestamp'])     # datetime object

# Find by commit
metrics = find_metrics_by_commit(history_dir, "700e012")

# Find all metrics for a version
all_v0_1_0 = find_metrics_by_version(history_dir, "0.1.0")

# Get latest metric for a version
latest = get_latest_metric_for_version(history_dir, "0.1.0")

# List all versions
versions = get_all_versions(history_dir)
print(versions)  # ['0.1.0', '0.1.1', '0.2.0']
```

See `STORAGE_STRUCTURE.md` for detailed storage design documentation.

## Available Collectors

### WorkflowStatusCollector
Tracks GitHub CI/CD health via API:
- Last run status (success/failure)
- Recent failure count
- Last successful run timestamp

### CoverageCollector
Extracts test coverage from pytest-cov or coverage.py:
- Line coverage %
- Branch coverage %
- Supports JSON and XML formats

### WilyCollector
Complexity metrics using wily (requires installation):
- Cyclomatic complexity
- Maintainability index
- Limited to recent commits for speed

### UmpyreCollector
Code statistics using built-in analyzer:
- Function/class counts
- Line metrics (total, empty, comments, docs)
- Code ratios and averages

## Configuration Reference

See `.github/umpyre-config.yml` for full options:

```yaml
schema_version: "1.0"  # Required

collectors:
  workflow_status:
    enabled: true
    lookback_runs: 10  # Number of recent runs to analyze
  
  wily:
    enabled: true
    max_revisions: 5  # Limit for performance
    operators: [cyclomatic, maintainability]
  
  coverage:
    enabled: true
    source: pytest-cov  # or 'coverage'
  
  umpyre_stats:
    enabled: true
    exclude_dirs: [tests, examples, scrap]

storage:
  branch: code-metrics  # Branch name for metrics
  formats: [json, csv]  # Output formats
  retention:
    strategy: all  # or: last_n_days, last_n_commits

visualization:  # Coming in Phase 2
  generate_plots: true
  generate_readme: true
  plot_metrics: [maintainability, coverage, loc]

thresholds:  # Coming in Phase 3
  enabled: false

aggregation:  # Coming in Phase 2
  enabled: false
```

## Architecture

```
umpyre/
├── collectors/          # Metric collectors (pluggable)
│   ├── base.py         # Abstract Collector with Mapping interface
│   ├── workflow_status.py
│   ├── wily_collector.py
│   ├── coverage_collector.py
│   └── umpyre_collector.py
├── storage/            # Persistence layer
│   ├── git_branch.py  # Git-based storage
│   └── formats.py     # JSON/CSV serialization
├── config.py           # YAML config loading
├── schema.py           # Versioned metric schema
└── cli.py              # Command-line interface
```

## Metric Schema (v1.0)

```json
{
  "schema_version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "commit_sha": "abc123...",
  "commit_message": "Fix bug in parser",
  "python_version": "3.10",
  "workflow_status": {
    "last_run_status": "success",
    "recent_failure_count": 0
  },
  "metrics": {
    "complexity": {
      "cyclomatic_avg": 3.2,
      "maintainability_index": 75.3
    },
    "coverage": {
      "line_coverage": 87.5,
      "branch_coverage": 82.1
    },
    "code_stats": {
      "num_functions": 342,
      "num_classes": 28
    }
  },
  "collection_duration_seconds": 12.3
}
```

## Roadmap

**Phase 1 (✅ Complete)**: Core tracking system
- Config-driven collectors
- Git branch storage
- CLI and GitHub Action

**Phase 2 (Planned)**: Visualization & Aggregation
- Plot generation (matplotlib/plotly)
- Auto-generated README with charts
- Cross-repository aggregation
- Organization-wide dashboards

**Phase 3 (Planned)**: Advanced Features
- Security metrics (bandit)
- Docstring coverage (interrogate)
- Threshold validation with custom validators
- Data pruning and compression
- Schema migration utilities

## Contributing

Contributions welcome! See `misc/CHANGELOG.md` for recent changes.

## Original Code Statistics Feature

Get stats about packages (existing functionality preserved):

```python
from umpyre import modules_info_df, stats_of
import collections

# Analyze a single package
modules_info_df(collections)

# Compare multiple packages
stats_of(['urllib', 'json', 'collections'])
```

See original README examples above for detailed usage.

## License

Apache-2.0
