# DevSecOps Monitor - Quick Reference Card

## Command

```bash
./dev.sh monitor
```

## RAG Status Legend

| Symbol | Color | Status | Meaning |
|--------|-------|--------|---------|
| ✅ | Green | Healthy/Passing | Everything is good |
| ⚠️ | Amber | Warning | Needs attention soon |
| ❌ | Red | Critical | Immediate action required |
| ○ | Grey | Unknown | Data not available |

## Monitored Categories

### 🐳 Local Development Environment

| Item | Green | Amber | Red | Grey |
|------|-------|-------|-----|------|
| **Container Services** | Both healthy | Partial/Unhealthy | Services stopped | Podman disabled |
| **Python Virtual Env** | Active | Exists but inactive | Not configured | - |
| **Git Working Directory** | Clean | Dirty (uncommitted) | - | - |

### ✅ Code Quality & Testing

| Item | Green | Amber | Red | Grey |
|------|-------|-------|-----|------|
| **Test Execution** | All passing | - | Any failures | No report |
| **Code Coverage** | ≥80% | 60-79% | <60% | No report |

### 🔒 Security & Compliance

| Item | Green | Amber | Red | Grey |
|------|-------|-------|-----|------|
| **SAST Security Scan** | No critical vulns | - | Critical issues | No report |
| **Dependency Scan** | No vulnerabilities | Minor vulns | Critical vulns | Not scanned |
| **License Compliance** | Tracked | - | - | No report |

### 🚀 GitHub CI/CD Workflows

| Workflow | Green | Amber | Red | Grey |
|----------|-------|-------|-----|------|
| **CI Pipeline** | Success | - | Failure | No recent runs |
| **Security Scans** | Success | - | Failure | No recent runs |
| **Build & Push** | Success | - | Failure | No recent runs |
| **Deploy to Production** | Success | - | Failure | No recent runs |

## Key Features

- ⏱️ **Auto-refresh**: Every 60 seconds
- 🌐 **GitHub Integration**: Public API (no auth needed)
- 📊 **13 Metrics**: Across 4 categories
- 💾 **Smart Caching**: 30s cache for GitHub data
- ⌨️ **Simple Control**: Ctrl+C to exit

## Prerequisites

### Required

- `bash`, `curl`, `jq`, `git`

### Optional

- `podman` - Container monitoring
- `pip-audit` - Dependency scanning
- Generated reports (via `./dev.sh test` and `./dev.sh docs`)

## Quick Workflow

1. **Generate Reports**

   ```bash
   ./dev.sh test      # Run tests, generate coverage
   ./dev.sh docs      # Generate all reports
   ```

2. **Launch Monitor**

   ```bash
   ./dev.sh monitor
   ```

3. **Verify Status**

   - All green? Ready to push!
   - Any amber/red? Fix before pushing

4. **Monitor Post-Push**

   - GitHub workflows appear automatically
   - Watch CI/CD status in real-time

## API Rate Limits

- **GitHub**: 60 requests/hour (unauthenticated)
- **Cache**: 30-second cache = ~2 calls/minute
- **Runtime**: Can run continuously for hours

## Troubleshooting

### No GitHub data

- Check internet connectivity
- Verify: `curl -s https://api.github.com/repos/jim-wyatt/msn-weather-wrapper/actions/runs`

### Missing local data

- Run: `./dev.sh test` and `./dev.sh docs`
- Check: `htmlcov/`, `junit.xml`, `artifacts/security-reports/`

### Container status disabled

- Install Podman: `sudo apt-get install podman` (Ubuntu/Debian)

## Example Interpretation

```text
Container Services:      ✅  Both services healthy
Python Virtual Env:      ⚠️  Exists but not activated
Git Working Directory:   ✅  No uncommitted changes
Test Execution:          ✅  168 tests passed
Code Coverage:           ✅  97% (Excellent)
SAST Security Scan:      ✅  No critical vulnerabilities
Dependency Scan:         ○   Not scanned (install pip-audit)
License Compliance:      ✅  142 dependencies tracked
CI Pipeline:             ✅  Passed
Security Scans:          ✅  Passed
Build & Push:            ✅  Passed
Deploy to Production:    ✅  Passed
```

**Status**: Mostly green! Two minor items:

- ⚠️ Activate venv: `source venv/bin/activate`
- ○ Install pip-audit: `pip install pip-audit`

**Action**: Safe to push, but activate venv for better development experience.

## See Full Documentation

```bash
# View comprehensive guide
cat docs/MONITOR_DASHBOARD.md

# View in browser (with mkdocs)
./dev.sh docs
# Navigate to: http://localhost:8000/MONITOR_DASHBOARD/
```
