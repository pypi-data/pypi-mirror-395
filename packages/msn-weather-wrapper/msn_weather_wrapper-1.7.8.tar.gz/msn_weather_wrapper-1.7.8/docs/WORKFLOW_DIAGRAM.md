# Workflow Architecture Diagram

This document provides a comprehensive UML diagram showing all GitHub Actions workflows and their interactions.

## Workflow Flow Diagram

```mermaid
sequenceDiagram
    autonumber

    actor Dev as Developer
    participant PR as Pull Request
    participant CI as CI/CD Pipeline
    participant Perf as Performance Testing
    participant Sec as Security Scanning
    participant Main as Main Branch
    participant Auto as Auto Version & Release
    participant Pub as Publish Release
    participant PyPI as PyPI Registry
    participant GH as GitHub Releases
    participant Pages as GitHub Pages
    participant Dep as Dependency Update

    %% Pull Request Flow
    Note over Dev,Sec: Pull Request Workflow
    Dev->>PR: Create PR to main
    activate PR

    par Run in parallel on PR
        PR->>CI: Trigger CI/CD Pipeline
        activate CI
        CI->>CI: Smoke Tests (fast fail)
        CI->>CI: Code Quality & Linting
        CI->>CI: Unit Tests (3.10, 3.11, 3.12)
        CI->>CI: Test Coverage (97%+)
        CI->>CI: Build Documentation
        CI->>CI: Build & Test Docker Images
        CI->>CI: Integration Tests
        CI->>CI: Security Scanning (internal)
        CI->>CI: Generate SBOM
        CI->>CI: Generate Report Documentation
        CI-->>PR: ✓ Tests Pass / ✗ Tests Fail
        deactivate CI
    and
        PR->>Perf: Trigger Performance Testing
        activate Perf
        Perf->>Perf: Benchmark Tests
        Perf->>Perf: Load Testing (Locust)
        Perf-->>PR: ✓ Performance OK / ✗ Performance Issue
        deactivate Perf
    and
        PR->>Sec: Trigger Security Scanning
        activate Sec
        Sec->>Sec: SAST (Bandit, Semgrep)
        Sec->>Sec: Dependency Scanning
        Sec->>Sec: Container Scanning (Trivy)
        Sec-->>PR: ✓ Security OK / ✗ Vulnerabilities Found
        deactivate Sec
    end

    Dev->>PR: Review and Merge
    PR->>Main: Merge to main
    deactivate PR

    %% Main Branch Flow
    Note over Main,Pages: Main Branch Push Workflow
    activate Main
    Main->>CI: Trigger CI/CD Pipeline
    activate CI

    CI->>CI: Run All Jobs
    Note right of CI: Smoke Tests<br/>Code Quality<br/>Unit Tests (3 versions)<br/>Test Coverage<br/>Security Scanning<br/>Docker Build & Push<br/>Integration Tests<br/>Generate SBOM<br/>Generate Reports

    CI->>Pages: Deploy Documentation
    activate Pages
    Pages-->>CI: ✓ Docs Deployed
    deactivate Pages

    CI->>Auto: Trigger Auto-Version-Release
    deactivate CI

    activate Auto
    Note right of Auto: Workflow Dispatch Trigger
    Auto->>Auto: Get Latest Merged PR Info
    Auto->>Auto: Determine Version Bump Type
    Note right of Auto: Analyze PR Title:<br/>feat: → minor<br/>fix: → patch<br/>BREAKING CHANGE: → major<br/>chore/docs: → patch

    Auto->>Auto: Calculate New Version
    Auto->>Auto: Check if Version Exists
    Auto->>Auto: Update pyproject.toml
    Auto->>Auto: Update __init__.py
    Auto->>Main: Create Version Bump PR
    Auto->>Main: Auto-merge PR
    Auto->>Main: Create Git Tag (v*.*.*)
    Note right of Auto: Tag triggers<br/>Publish Release

    Auto->>Pub: Trigger Publish Release
    deactivate Auto
    deactivate Main

    %% Publish Release Flow
    Note over Pub,GH: Publish Release Workflow
    activate Pub
    Pub->>Pub: Build Python Package
    Note right of Pub: Build wheel & sdist

    Pub->>PyPI: Publish to PyPI
    activate PyPI
    PyPI-->>Pub: ✓ Package Published
    deactivate PyPI

    Pub->>GH: Create GitHub Release
    activate GH
    Note right of GH: Attach wheel & tarball<br/>Generate release notes<br/>from commit history
    GH-->>Pub: ✓ Release Created
    deactivate GH

    Pub-->>Dev: ✓ Release v*.*.* Complete
    deactivate Pub

    %% Dependency Update Flow (Scheduled)
    Note over Dep,Main: Scheduled Dependency Updates
    Dep->>Dep: Weekly Cron Trigger
    activate Dep
    Dep->>Dep: Update Python Dependencies
    Dep->>Dep: Update Node Dependencies
    Dep->>Main: Create Update PR
    deactivate Dep
    Note right of Dep: PR triggers CI/CD<br/>and requires manual review
```

## Workflow Descriptions

### 1. **CI/CD Pipeline** (`ci.yml`)
**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Manual dispatch

**Jobs:**
1. **Smoke Tests** - Fast validation (imports, syntax)
2. **Code Quality & Linting** - Ruff format check, linting, mypy type checking
3. **Unit Tests** - Runs on Python 3.10, 3.11, 3.12
4. **Test Coverage** - Generates coverage reports (target: 97%+)
5. **Security Scanning** - Bandit, pip-audit, license checks
6. **Build Documentation** - MkDocs build validation
7. **Build & Test Docker Images** - Multi-stage container build
8. **Integration Tests** - Tests against containerized API
9. **Generate SBOM** - Software Bill of Materials with Syft
10. **Generate Report Documentation** - Consolidated test/coverage/security reports
11. **Deploy Documentation** - Push to GitHub Pages (main branch only)
12. **Trigger Auto-Version-Release** - Starts versioning workflow (main branch only)

### 2. **Performance Testing** (`performance.yml`)
**Triggers:**
- Pull requests to `main`

**Jobs:**
1. **Benchmark Tests** - Performance baseline measurements
2. **Load Testing** - Locust-based load testing (20 concurrent users, 10 req/s)
   - Health check endpoint testing
   - Weather endpoint testing
   - Rate limiting validation (accepts 429 responses)

### 3. **Security Scanning** (`security-scan.yml`)
**Triggers:**
- Pull requests to `main`
- Manual dispatch

**Jobs:**
1. **SAST** - Bandit and Semgrep static analysis
2. **Dependency Scanning** - pip-audit vulnerability checks
3. **Container Scanning** - Trivy image scanning

### 4. **Auto Version and Release** (`auto-version-release.yml`)
**Triggers:**
- Workflow dispatch from CI/CD Pipeline (after successful main branch build)

**Process:**
1. Analyzes merged PR title to determine version bump type:
   - `feat:` → minor version bump
   - `fix:` → patch version bump
   - `BREAKING CHANGE:` → major version bump
   - `chore:`, `docs:` → patch version bump
2. Calculates new version
3. Updates `pyproject.toml` and `src/msn_weather_wrapper/__init__.py`
4. Creates version bump PR
5. Auto-merges the PR
6. Creates git tag (format: `v*.*.*`)
7. Triggers Publish Release workflow

### 5. **Publish Release** (`publish-release.yml`)
**Triggers:**
- Git tag push (pattern: `v*.*.*`)
- Manual dispatch with tag input

**Jobs:**
1. **Build Package** - Creates wheel and source distribution
2. **Publish to PyPI** - Uploads package to PyPI registry
3. **Create GitHub Release** - Creates release with artifacts and generated notes

### 6. **Dependency Update** (`dependencies.yml`)
**Triggers:**
- Weekly cron schedule
- Manual dispatch

**Process:**
1. Updates Python dependencies in `pyproject.toml`
2. Updates Node.js dependencies in `frontend/package.json`
3. Creates PR with updates
4. PR triggers CI/CD Pipeline for validation

## Workflow Dependencies

```mermaid
graph TB
    subgraph "Pull Request"
        PR[Pull Request Created]
        PR --> CI_PR[CI/CD Pipeline]
        PR --> PERF[Performance Testing]
        PR --> SEC[Security Scanning]
        CI_PR --> APPROVE{All Checks Pass?}
        PERF --> APPROVE
        SEC --> APPROVE
        APPROVE -->|Yes| MERGE[Merge to Main]
        APPROVE -->|No| FIX[Fix Issues]
        FIX --> PR
    end

    subgraph "Main Branch"
        MERGE --> CI_MAIN[CI/CD Pipeline]
        CI_MAIN --> DEPLOY[Deploy Docs to Pages]
        CI_MAIN --> TRIGGER[Trigger Auto-Version]
    end

    subgraph "Release Process"
        TRIGGER --> AUTO[Auto Version & Release]
        AUTO --> VERSION[Calculate Version]
        VERSION --> BUMP_PR[Create Version Bump PR]
        BUMP_PR --> AUTO_MERGE[Auto-merge PR]
        AUTO_MERGE --> TAG[Create Git Tag]
        TAG --> PUBLISH[Publish Release]
        PUBLISH --> PYPI[PyPI Package]
        PUBLISH --> GH_RELEASE[GitHub Release]
    end

    subgraph "Scheduled"
        CRON[Weekly Cron] --> DEP_UPDATE[Dependency Update]
        DEP_UPDATE --> DEP_PR[Create Update PR]
        DEP_PR --> PR
    end

    style PR fill:#e1f5ff
    style MERGE fill:#c8e6c9
    style TAG fill:#fff9c4
    style PYPI fill:#ffccbc
    style GH_RELEASE fill:#ffccbc
    style CRON fill:#f3e5f5
```

## Key Features

### Automatic Version Management
- **Convention-based:** PR titles determine version bump type
- **Semantic Versioning:** Follows semver (MAJOR.MINOR.PATCH)
- **Automated:** No manual version updates required
- **Consistent:** Version synced across all files

### Quality Gates
- **Fast Fail:** Smoke tests run first to catch obvious issues
- **Comprehensive Testing:** Unit, integration, and performance tests
- **Security First:** Multiple security scanning layers
- **Coverage Requirements:** Maintains 97%+ code coverage

### Deployment Pipeline
- **Automated Publishing:** PyPI and GitHub Releases
- **Documentation:** Auto-deployed to GitHub Pages
- **Container Images:** Built and pushed to registry
- **SBOM Generation:** Software Bill of Materials for compliance

### Concurrency Control
- **Cancel in Progress:** Only latest run per PR
- **Resource Efficient:** Prevents duplicate workflow runs
- **Fast Feedback:** Cancels obsolete runs immediately

## Workflow Triggers Summary

| Workflow | PR | Push to Main | Tag Push | Manual | Cron |
|----------|----|-----------------|----------|--------|------|
| CI/CD Pipeline | ✓ | ✓ | ✓ | ✓ | - |
| Performance Testing | ✓ | - | - | - | - |
| Security Scanning | ✓ | - | - | ✓ | - |
| Auto Version & Release | - | ✓ (via workflow_dispatch) | - | ✓ | - |
| Publish Release | - | - | ✓ | ✓ | - |
| Dependency Update | - | - | - | ✓ | ✓ (weekly) |

## Environment Variables

All workflows use consistent environment configuration:

```yaml
env:
  PYTHON_VERSION: '3.12'
  NODE_VERSION: '20'
  REPORTS_DIR: 'docs/reports'
```

## Secrets Required

- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `PYPI_API_TOKEN` - PyPI upload authentication (stored in repository secrets)

## Cache Strategy

Workflows leverage GitHub Actions caching for:
- Python dependencies (pip cache)
- Node.js dependencies (npm/yarn cache)
- Docker layer caching
- Build artifacts between jobs
