# Quick Start: Automatic Versioning

## 🎯 TL;DR

Use conventional commits → Push to main → Automatic release!

```bash
# Add feature (minor version bump)
git commit -m "feat: add weather alerts"
git push origin main
# → v1.2.0 → v1.3.0

# Fix bug (patch version bump)
git commit -m "fix: handle null values"
git push origin main
# → v1.3.0 → v1.3.1

# Breaking change (major version bump)
git commit -m "feat!: redesign API"
git push origin main
# → v1.3.1 → v2.0.0
```

## 📝 Commit Format

```
<type>: <description>
```

**Types that trigger releases:**
- `feat:` - New feature → MINOR bump (0.X.0)
- `fix:` - Bug fix → PATCH bump (0.0.X)
- `perf:` - Performance → PATCH bump (0.0.X)
- `feat!:` or `BREAKING CHANGE:` → MAJOR bump (X.0.0)

**Types that don't trigger releases:**
- `docs:`, `style:`, `refactor:`, `test:`, `build:`, `ci:`, `chore:`

## 🚀 What Happens Automatically

1. ✅ Version bumped in `pyproject.toml` and `__init__.py`
2. 📝 CHANGELOG.md updated
3. 🏷️ Git tag created (e.g., `v1.3.0`)
4. 📦 Package built and published to PyPI
5. 🐳 Container images built and pushed to ghcr.io
6. 📋 GitHub Release created with artifacts

## 📚 Full Documentation

See [AUTOMATIC_VERSIONING.md](AUTOMATIC_VERSIONING.md) for complete guide.

## 🔧 Manual Release (if needed)

```bash
# Force a release via GitHub Actions UI or:
gh workflow run release.yml -f force-level=minor
```
