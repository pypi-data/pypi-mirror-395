# 🗺️ The Smart Roadmap

This is a visionary, integration-oriented plan that categorizes features from **"Core Essentials"** to **"God Level"** ambition.

---

## Phase 1: Foundation (CRITICALLY MUST HAVE)

**Focus**: Core functionality, stability, security, and basic usage.
**Status**: Mostly Completed (Q1)

- [x] **Branded Markdown Generation**: Auto TOC (list or tree), language-detected code blocks, Git metadata, timestamps.
- [x] **Async-First & Concurrent**: Built on `anyio` for high-throughput, non-blocking I/O.
- [x] **Flexible Archiving**: Automatically archive old dumps into ZIP, tar.gz, or tar.bz2 formats.
- [x] **Project Rollback & Restore**: Rehydrate a full project structure from a `.md` dump file.
- [x] **Git-Native Collection**: Use `git ls-files` for fast, accurate file discovery.
- [x] **Live Watch Mode**: Automatically re-run the dump on any file change.
- [x] **Secret Scanning**: Integrates `detect-secrets` to scan files during processing.
- [x] **Safety & Integrity**: SHA256 hashing for all dumps and atomic writes.
- [x] **Observability**: Prometheus metrics for monitoring.
- [x] **TODO/FIXME Scanning**: Scan for `TODO` or `FIXME` tags in code.
- [x] **Push Notifications**: Get notified on dump completion via `ntfy.sh`.
- [x] **Per-Project Config Discovery**: Enhance `batch` mode to detect and use project-specific `create_dump.toml` files in a monorepo.
- [x] **Dump Header Statistics**: Add total lines of code and file count to the dump header for quick context.
- [x] **Custom Secret Scanning Rules**: Allow users to define custom regex patterns for secret scanning.
- [x] **Configuration Profiles**: Merge configuration profiles for different environments (e.g., `local`, `ci`) from `pyproject.toml`.

---

## Phase 2: The Standard (MUST HAVE)

**Focus**: Feature parity with top competitors, user experience improvements, and robust error handling.
**Timeline**: Q2

- [x] **"Diff-Only" Dump Format**: Output a `.diff` or `.patch` file instead of the full file content when using `--diff-since`.
- [x] **Smart Caching Strategy**: Implement persistent hashing to avoid reprocessing unchanged files in `--watch` mode (beyond basic re-runs).
- [x] **Database Dump Integration**: Add flags to execute `pg_dump` or `mysqldump` and embed the SQL output in the dump.
- [x] **ChatOps Expansion**: Native integration for sending notifications to Slack, Discord, and Telegram (beyond `ntfy.sh`).
- [ ] **Enhanced Error Reporting**: Human-friendly error messages with suggested fixes for common configuration/permissions issues.
- [ ] **Docker Container Support**: Ability to target a running Docker container to dump its filesystem.

---

## Phase 3: The Ecosystem (INTEGRATION & SHOULD HAVE)

**Focus**: Webhooks, API exposure, 3rd party plugins, SDK generation, and extensibility.
**Timeline**: Q3

- [ ] **Cloud Storage Uploads**: Native support for uploading dumps to AWS S3, Google Cloud Storage, and Azure Blob Storage.
- [ ] **Persistent Server Mode**: A `create-dump serve` command launching a lightweight FastAPI server for webhook-triggered dumps.
- [ ] **Official GitHub Action**: A verified GitHub Action to generate dumps on Pull Requests or commits.
- [ ] **Plugin Architecture**: A dynamic plugin system to allow users to write custom collectors, scanners, and writers.
- [ ] **SDK Generation**: Refactor core logic into a stable library so other Python applications can `import create_dump`.
- [ ] **Pre-commit Hook Integration**: Provide a standard `.pre-commit-hooks.yaml` for easy adoption.

---

## Phase 4: The Vision (GOD LEVEL)

**Focus**: **"Futuristic"** features, AI integration, advanced automation, and industry-disrupting capabilities.
**Timeline**: Q4 / Future

- [ ] **RAG-Ready Dumps (Vector Embeddings)**: Automatically generate and embed vector representations of the code alongside the dump for instant LLM ingestion.
- [ ] **AI-Powered Dump Analysis**: Integrate with LLMs to automatically generate summaries, architectural insights, and "Code Health" reports.
- [ ] **Interactive TUI Explorer**: A `create-dump explore` command launching a Terminal UI to browse/search a dump without extracting it.
- [ ] **Direct-to-Archive Streaming**: High-performance mode writing directly to a compressed archive stream, bypassing disk I/O for massive repos.
- [ ] **Centralized Config Policy**: Allow SRE teams to enforce a master configuration policy fetched from a remote URL.
- [ ] **GitHub App / PR Bot**: A fully-fledged bot that listens to PR events and comments with a dump summary or "diff" analysis.

---

## The Sandbox (OUT OF THE BOX / OPTIONAL)

**Focus**: Wild, creative, experimental ideas that set the project apart.

- [ ] **Code Archeology**: Analyze git history to visualize code churn, heatmaps of activity, and authorship evolution in the dump.
- [ ] **Dependency Tree Analysis**: Generate and embed a visual dependency graph (pip/npm/cargo) within the Markdown dump.
- [ ] **IaC / Terraform Mode**: Specialized dumping for Infrastructure-as-Code with built-in validation and resource visualization.
- [ ] **Jupyter Notebook Integration**: "Magic" commands to snapshot and restore Jupyter notebook states effortlessly.
- [ ] **Context-Aware Sampling**: Use static analysis to dump only the "Call Graph" relevant to a specific function or feature.
