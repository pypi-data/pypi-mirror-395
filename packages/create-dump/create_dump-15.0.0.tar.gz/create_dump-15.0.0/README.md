<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/create-dump/main/create-dump_logo.png" alt="create-dump logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/create-dump.svg)](https://pypi.org/project/create-dump/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/create-dump.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/create-dump/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/create-dump/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/create-dump/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/create-dump/graph/badge.svg)](https://codecov.io/gh/dhruv13x/create-dump)
[![Test Coverage](https://img.shields.io/badge/coverage-85%25%2B-brightgreen.svg)](https://github.com/dhruv13x/create-dump/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/create-dump.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/create-dump.svg)](https://pypi.org/project/create-dump/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

# create-dump

**Enterprise-Grade Code Dump Utility for Monorepos**

`create-dump` is a production-ready CLI tool for automated code archival in large-scale monorepos. It generates branded Markdown dumps with Git metadata, integrity checksums, flexible archiving, retention policies, path safety, full concurrency, and SRE-grade observability.

Designed for SRE-heavy environments (Telegram bots, microservices, monorepos), it ensures **reproducible snapshots for debugging, forensics, compliance audits, and CI/CD pipelines**. It also includes a `rollback` command to restore a project from a dump file.

Built for Python 3.11+, leveraging **AnyIO**, Pydantic, Typer, Rich, and Prometheus metrics.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git (optional, for metadata and `git ls-files` support)
- PostgreSQL / MySQL client tools (optional, for database dumping)

### Installation

**PyPI (Recommended):**
```bash
pip install create-dump
```

**From Source:**
```bash
git clone https://github.com/dhruv13x/create-dump.git
cd create-dump
pip install -e .[dev]
```

### Usage Examples

**Interactive Setup (Recommended for first-time users):**
```bash
create-dump --init
```

**Single Mode (Default):**
```bash
# Dump current directory to a markdown file
create-dump single --dest ./dumps/my-snapshot.md

# Dump with Git file listing, watch mode, and secret redaction
create-dump single --git-ls-files --watch --scan-secrets --hide-secrets
```

**Database Snapshotting:**
```bash
# Dump code AND a PostgreSQL database schema/data
create-dump single --db-provider postgres --db-name mydb --db-user postgres --db-pass-env DB_PASSWORD
```

**Batch Mode (Monorepos):**
```bash
# Dump specific directories (src, tests) and keep only the last 5 dumps
create-dump batch run --root ./monorepo --dirs src,tests --archive --keep-last 5
```

**Rollback & Restore:**
```bash
# Restore project from a dump file
create-dump rollback --file ./dumps/my-snapshot.md
```

**Output Example:**
```text
dumps/my-snapshot_all_create_dump_20250101_121045.md
dumps/my-snapshot_all_create_dump_20250101_121045.md.sha256
archives/my-snapshot_20250101_121045.zip
```

---

## ✨ Key Features

*   **Branded Markdown Generation**: Auto TOC (list or tree), language-detected code blocks, Git metadata, timestamps.
*   **Async-First & Concurrent**: Built on `anyio` for high-throughput, non-blocking I/O. Parallel file processing (16+ workers), timeouts, and progress bars (Rich).
*   **Flexible Archiving**: Automatically archive old dumps into **ZIP, tar.gz, or tar.bz2** formats. Includes integrity validation and retention policies (e.g., "keep last N").
*   **Project Rollback & Restore**: Includes a `rollback` command to rehydrate a full project structure from a `.md` dump file, with SHA256 integrity verification.
*   **Git-Native Collection**: Use `git ls-files` for fast, accurate file discovery (`--git-ls-files`) or dump only changed files (`--diff-since <ref>`).
*   **Live Watch Mode & Smart Caching**: Run in a persistent state (`--watch`) that automatically re-runs the dump on any file change. Includes **Smart Caching** to avoid reprocessing unchanged files for blazing fast updates.
*   **Secret Scanning**: Integrates `detect-secrets` to scan files during processing. Can fail the dump (`--scan-secrets`), redact secrets in-place (`--hide-secrets`), or use custom patterns (`--secret-patterns`).
*   **Database Snapshotting**: Dump **PostgreSQL or MySQL** schemas and data alongside your code (`--db-provider`). Supports env-var password security (`--db-pass-env`).
*   **ChatOps & Notifications**: Push notifications via **ntfy.sh, Slack, Discord, and Telegram** on dump completion.
*   **Safety & Integrity**: SHA256 hashing for all dumps, atomic writes, async-safe path guards (prevents traversal & Zip-Slip), and orphan quarantine.
*   **Observability**: Prometheus metrics (e.g., `create_dump_duration_seconds`, `create_dump_files_total`).
*   **TODO/FIXME Scanning**: Scan for `TODO` or `FIXME` tags in code and append a summary to the dump (`--scan-todos`).

| Feature | Single Mode | Batch Mode |
| :--- | :--- | :--- |
| **Scope** | Current dir/files | Recursive subdirs |
| **Archiving** | Optional | Enforced retention |
| **Concurrency** | Up to **16** workers | Parallel subdirs |
| **Git Metadata** | ✔️ | Per-subdir ✔️ |
| **Database Dumps** | ✔️ | ❌ |

---

## ⚙️ Configuration & Advanced Usage

### Environment Variables & Config File
You can configure `create-dump` using a `create_dump.toml` file or `pyproject.toml`.

**Example `pyproject.toml`:**
```toml
[tool.create-dump]
dest = "/path/to/dumps"
use_gitignore = true
git_meta = true
max_file_size_kb = 5000
dump_pattern = ".*_all_create_dump_\\d{8}_\\d{6}\\.(md(\\.gz)?|sha256)$"
excluded_dirs = ["__pycache__", ".git", ".venv", "node_modules"]
metrics_port = 8000
# git_ls_files = true
# scan_secrets = true
# hide_secrets = true
# notify_slack = "https://hooks.slack.com/services/..."
```

### CLI Arguments

#### Main / Single Mode (`create-dump single`)

| Argument | Shorthand | Description | Default |
| :--- | :--- | :--- | :--- |
| `--version` | `-V` | Show version and exit. | `false` |
| `--init` | | Run interactive wizard to create `create_dump.toml`. | `false` |
| `--config` | | Path to TOML config file. | `null` |
| `--profile` | | Config profile to merge from `pyproject.toml`. | `null` |
| `--dest` | | Destination dir for output. | `.` |
| `--no-toc` | | Omit table of contents. | `false` |
| `--tree-toc` | | Render Table of Contents as a file tree. | `false` |
| `--format` | | Output format (md or json). | `md` |
| `--compress` | `-c` | Gzip the output file. | `false` |
| `--progress` / `--no-progress` | `-p` | Show processing progress. | `true` |
| `--allow-empty` | | Succeed on 0 files. | `false` |
| `--metrics-port` | | Prometheus export port. | `8000` |
| `--exclude` | | Comma-separated exclude patterns. | `""` |
| `--include` | | Comma-separated include patterns. | `""` |
| `--max-file-size` | | Max file size in KB. | `null` |
| `--use-gitignore` / `--no-use-gitignore` | | Incorporate .gitignore excludes. | `true` |
| `--git-meta` / `--no-git-meta` | | Include Git branch/commit. | `true` |
| `--max-workers` | | Concurrency level. | `16` |
| `--watch` | | Run in live-watch mode. | `false` |
| `--git-ls-files` | | Use 'git ls-files' for file collection. | `false` |
| `--diff-since` | | Generate a git diff/patch file for changes since a specific git ref. | `null` |
| `--scan-secrets` | | Scan files for secrets. Fails dump if secrets are found. | `false` |
| `--hide-secrets` | | Redact found secrets (requires --scan-secrets). | `false` |
| `--secret-patterns` | | Custom regex patterns for secret scanning. | `null` |
| `--scan-todos` | | Scan files for TODO/FIXME tags and append a summary. | `false` |
| `--archive` | `-a` | Archive prior dumps into ZIP. | `false` |
| `--archive-all` | | Archive dumps grouped by prefix. | `false` |
| `--archive-search` | | Search project-wide for dumps. | `false` |
| `--archive-include-current` / `--no-archive-include-current` | | Include this run in archive. | `true` |
| `--archive-no-remove` | | Preserve originals post-archiving. | `false` |
| `--archive-keep-latest` / `--no-archive-keep-latest` | | Keep latest dump live or archive all. | `true` |
| `--archive-keep-last` | | Keep last N archives. | `null` |
| `--archive-clean-root` | | Clean root post-archive. | `false` |
| `--archive-format` | | Archive format (zip, tar.gz, tar.bz2). | `zip` |
| **ChatOps** | | | |
| `--notify-topic` | | ntfy.sh topic for push notification. | `null` |
| `--notify-slack` | | Slack webhook URL. | `null` |
| `--notify-discord` | | Discord webhook URL. | `null` |
| `--notify-telegram-chat` | | Telegram chat ID. | `null` |
| `--notify-telegram-token` | | Telegram bot token. | `null` |
| **Database** | | | |
| `--db-provider` | | Database provider (postgres, mysql). | `null` |
| `--db-name` | | Database name. | `null` |
| `--db-host` | | Database host. | `localhost` |
| `--db-port` | | Database port. | `null` |
| `--db-user` | | Database user. | `null` |
| `--db-pass-env` | | Env var containing database password. | `null` |
| **Controls** | | | |
| `--yes` | `-y` | Assume yes for prompts and deletions. | `false` |
| `--dry-run` | `-d` | Simulate without writing files. | `false` |
| `--no-dry-run` | `-nd` | Run for real (disables simulation). | `false` |
| `--verbose` | `-v` | Enable debug logging. | `false` |
| `--quiet` | `-q` | Suppress output (CI mode). | `false` |

#### Batch Mode (`create-dump batch run`)
*Runs dumps across subdirectories.*

| Argument | Description | Default |
| :--- | :--- | :--- |
| `root` | Root project path. | `.` |
| `--dirs` | Subdirectories to process (comma-separated). | `.,packages,services` |
| `--pattern` | Regex to identify dump files. | (Canonical Pattern) |
| `--archive-all` | Archive dumps grouped by prefix into separate ZIPs. | `false` |
| `--archive-keep-last` | Keep last N archives. | `null` |
| `--max-workers` | Workers per subdir dump. | `4` |

#### Rollback (`create-dump rollback`)
*Rehydrates a project from a dump file.*

| Argument | Description |
| :--- | :--- |
| `root` | Project root to scan for dumps and write rollback to. |
| `--file` | Specify a dump file to use (e.g., `my_dump.md`). |

---

## 🏗️ Architecture

```
┌─────────────────┐
│   CLI (Typer)   │
│ (single, batch, │
│  init, rollback)│
└────────┬────────┘
         │
┌────────▼────────┐
│ Config / Models │
│    (core.py)    │
└─────────────────┘
         │
┌─────────────────┴─────────────────┐
│                                   │
▼                                   ▼
┌─────────────────┐               ┌───────────────────┐
│   DUMP FLOW     │               │   RESTORE FLOW    │
│ (Collect)       │               │   (Verify SHA256) │
│      │          │               │         │         │
│      ▼          │               │         ▼         │
│ (Process/Scan)  │               │   (Parse .md)     │
│      │          │               │         ▼         │
│      ▼          │               │   (Rehydrate Files) │
│ (Write MD/JSON) │               │   (Rehydrate Files) │
│      │          │               │                   │
│      ▼          │               └───────────────────┘
│ (Archive/Prune) │
│      │          │
│      ▼          │
│(Notify/Database)│
└─────────────────┘
```

**Core Components:**
- **Collector**: Gathers files using glob patterns or `git ls-files`.
- **Processor**: Reads files, detects binary content, scans for secrets/todos.
- **Writer**: Generates the Markdown or JSON output with TOC and headers.
- **Archiver**: Manages retention policies and compression of old dumps.
- **DatabaseDumper**: Connects to DBs (Postgres/MySQL) and dumps schemas/data.
- **Rollback Engine**: Parses dump files and reconstructs the file system safely.

---

## 🗺️ Roadmap

- [x] Single & Batch Dumps
- [x] Git Metadata & `ls-files` Integration
- [x] Secret Scanning & Redaction
- [x] Rollback / Restore Capability
- [x] Multi-Channel Notifications (Slack, Discord, Telegram, ntfy)
- [x] Database Dumping (Postgres/MySQL)
- [x] Differential Dumps (Git Diff)
- [ ] Remote Storage Support (S3, GCS)
- [ ] PDF Export

---

## 🤝 Contributing

We welcome contributions! Please see the [Contributing Guide](CONTRIBUTING.md) (if available) or follow these steps:

1.  Fork the repo.
2.  Create a feature branch.
3.  Install dev dependencies: `pip install -e .[dev]`
4.  Run tests: `pytest`
5.  Submit a Pull Request.

**License**: MIT
