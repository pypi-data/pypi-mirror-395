# GitHub Actions Workflows

This directory contains the automated CI/CD workflows for the MSN Weather Wrapper project.

## 🚀 Auto-Versioning & Release Workflow

### How It Works

The project uses **automatic semantic versioning** that triggers on every merged PR:

1. **PR Merged to Main** → Triggers `auto-version-release.yml`
2. **Version Bump Determined** → Based on PR title, labels, or branch name
3. **Version Bump PR Created** → Automated PR updates version files
4. **Auto-Merge Enabled** → PR auto-merges when checks pass
5. **Tag Created** → Git tag `v X.Y.Z` is automatically created
6. **Release Published** → CI/CD builds and publishes to PyPI, Docker, and GitHub Releases

### Version Bump Rules

The bump type is determined by (in order of priority):

1. **PR Labels**:
   - `major` or `breaking` → Major version (X.0.0)
   - `minor`, `feature`, or `enhancement` → Minor version (0.X.0)
   - `patch`, `fix`, or `bugfix` → Patch version (0.0.X)

2. **PR Title** (Conventional Commits):
   - `feat!:` or `breaking:` → Major (X.0.0)
   - `feat:` or `feature:` → Minor (0.X.0)
   - `fix:`, `chore:`, `refactor:`, `perf:`, `docs:` → Patch (0.0.X - default)

3. **Branch Prefix**:
   - `breaking/` or `major/` → Major
   - `feat/` or `feature/` → Minor
   - `fix/` or `bugfix/` or `hotfix/` → Patch

**Default**: If no indicators are found, defaults to **patch** version bump.

### Example PR Titles

```text
feat: add weather alerts feature          → 0.X.0 (minor)
fix: correct temperature parsing          → 0.0.X (patch)
feat!: redesign API endpoints             → X.0.0 (major)
chore: update dependencies                → 0.0.X (patch)
docs: improve README                      → 0.0.X (patch)
refactor: simplify client logic           → 0.0.X (patch)
```

## 📋 Workflow Files

### Core Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **`auto-version-release.yml`** | PR merged to main | Automatic version bumping and tagging |
| **`ci.yml`** | Push, PR, tags | Full CI/CD pipeline (test, build, publish) |
| **`release.yml`** | Manual (workflow_dispatch) | Manual release creation with semantic-release |

### Supplementary Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **`security-scan.yml`** | Weekly schedule | Comprehensive security scanning (Trivy, Semgrep, Grype) |
| **`dependencies.yml`** | Weekly schedule | Dependency updates via Dependabot |
| **`performance.yml`** | PR to main | Performance benchmarking and regression testing |

## 🔄 CI/CD Pipeline (`ci.yml`)

The main CI/CD pipeline runs on:

- **Push to `main` or `develop`**
- **Pull Requests to `main` or `develop`**
- **Tag pushes** (`v*.*.*`)

### Pipeline Stages

1. **Smoke Tests** - Fast syntax and import validation
2. **Code Quality** - Ruff formatting and linting, mypy type checking
3. **Security** - Bandit, pip-audit, license scanning
4. **Unit Tests** - Pytest across Python 3.10-3.12 (matrix on main, 3.12 only on PRs)
5. **Coverage** - Test coverage reporting with Codecov
6. **Docker Build** - Build and test container images
7. **Integration Tests** - End-to-end API testing
8. **Frontend Tests** - React/TypeScript testing
9. **E2E Tests** - Playwright browser testing
10. **Build Package** - Build Python wheel and sdist
11. **SBOM Generation** - Software bill of materials (Syft, CycloneDX)
12. **📦 Publish to PyPI** - On tag push only
13. **🚀 Create GitHub Release** - On tag push only

### Publishing

- **PyPI**: Automatic on tag push (`v*.*.*`) using trusted publishing (OIDC)
- **Container Registry**: Automatic on main branch and tags to `ghcr.io`
- **GitHub Releases**: Automatic on tag push with all artifacts attached

## 🛡️ Security Workflows

### `security-scan.yml` (Weekly)

Comprehensive security scanning:

- **Trivy**: Vulnerability scanning for containers and dependencies
- **Semgrep**: Static application security testing (SAST)
- **Grype**: Vulnerability scanning for Docker images
- **SBOM**: Generate and scan software bill of materials

### `security` job in `ci.yml` (Every run)

Fast critical security checks:

- **Bandit**: Python security linting (fail on HIGH/CRITICAL)
- **pip-audit**: Check for known vulnerabilities in dependencies
- **License Compliance**: Generate license reports

## 🔧 Manual Release (`release.yml`)

For manual control over releases:

1. Go to **Actions** → **Automated Release**
2. Click **Run workflow**
3. Optionally force a specific bump level (patch/minor/major)
4. The workflow creates a release PR with changelog
5. Review and merge the PR
6. Auto-versioning workflow handles the rest

## 📊 Performance Testing (`performance.yml`)

Runs on PRs to main:

- API endpoint performance benchmarking
- Response time regression detection
- Load testing with locust
- Memory profiling

## 🔄 Dependency Management (`dependencies.yml`)

Weekly automated updates:

- Frontend dependencies (npm)
- Python dependencies (pip)
- GitHub Actions versions
- Security patches prioritized

## 🎯 Best Practices

### For Contributors

1. **Use Conventional Commits**: Start PR titles with `feat:`, `fix:`, etc.
2. **Add Labels**: Label PRs with `feature`, `bugfix`, `breaking` for clarity
3. **Review Auto-Generated PRs**: Version bump PRs are automated but reviewable
4. **Monitor CI/CD**: Check workflow runs for any failures

### For Maintainers

1. **Branch Protection**: Keep `main` protected (require PR reviews, status checks)
2. **Secrets Management**:
   - `PYPI_API_TOKEN`: For PyPI publishing (use trusted publishing instead)
   - GitHub token is auto-provided, no secrets needed
3. **Auto-Merge**: Version bump PRs use auto-merge for convenience
4. **Manual Override**: Use `release.yml` for controlled releases when needed

## 🐛 Troubleshooting

### Auto-versioning fails with "Protected branch" error

**Solution**: The new workflow creates a version bump PR instead of pushing directly. No branch protection bypass needed!

### Version bump PR not auto-merging

**Check**:

1. Branch protection requires PR reviews → Approve the PR
2. Required status checks failing → Fix the failures
3. Auto-merge not working → Manually merge the PR

### PyPI publishing fails

**Check**:

1. Version already exists on PyPI → Versions are immutable
2. Token expired → Set up trusted publishing (OIDC) instead
3. Package name conflicts → Ensure unique package name

### Tag already exists

**Solution**: The workflow checks for existing tags and skips if found. This is normal if re-running after a merge.

## 📚 Additional Documentation

- [CI/CD Pipeline Details](./README.md)
- [Security Scanning Guide](../../docs/SECURITY.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Versioning Guide](../../docs/VERSIONING.md)

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Python Semantic Release](https://python-semantic-release.readthedocs.io/)
