#!/bin/bash
#
# Developer Environment Manager for MSN Weather Wrapper
# This script sets up a complete containerized development environment using Podman
#
# Usage: ./dev.sh [command]
# Commands:
#   setup     - Initial setup (build images, install dependencies)
#   start     - Start all development containers
#   stop      - Stop all containers
#   restart   - Restart all containers
#   clean     - Remove all containers, images, and volumes
#   test      - Run all tests (backend + frontend)
#   logs      - Show logs from all containers
#   shell-api - Open shell in API container
#   shell-frontend - Open shell in frontend container
#   rebuild   - Rebuild all containers from scratch
#   monitor   - DevSecOps dashboard with RAG status (Local env + GitHub workflows)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="msn-weather-wrapper"
COMPOSE_FILE="podman-compose.dev.yml"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

check_podman() {
    if ! command -v podman &> /dev/null; then
        log_error "Podman is not installed. Please install it first."
        echo "  Ubuntu/Debian: sudo apt-get install podman"
        echo "  Fedora: sudo dnf install podman"
        echo "  macOS: brew install podman"
        exit 1
    fi
    log_success "Podman is installed ($(podman --version))"
}

check_podman_compose() {
    if ! command -v podman-compose &> /dev/null; then
        log_warning "podman-compose is not installed. Installing..."
        pip3 install --user podman-compose
        log_success "podman-compose installed"
    else
        log_success "podman-compose is installed ($(podman-compose --version))"
    fi
}

setup_dev_env() {
    log_info "Setting up development environment..."

    # Check prerequisites
    check_podman
    check_podman_compose

    # Create development docker-compose file if it doesn't exist
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_info "Creating development compose file..."
        create_dev_compose
    fi

    # Build images
    log_info "Building container images..."
    podman-compose -f "$COMPOSE_FILE" build

    log_success "Development environment setup complete!"
    echo ""
    echo "Next steps:"
    echo "  ./dev.sh start    - Start the development environment"
    echo "  ./dev.sh logs     - View logs"
    echo "  ./dev.sh test     - Run tests"
}

start_dev() {
    log_info "Starting development containers..."

    # Check for port conflicts
    if ! check_port_conflicts; then
        exit 1
    fi

    podman-compose -f "$COMPOSE_FILE" up -d

    log_success "Containers started!"
    echo ""
    echo "Services available at:"
    echo "  Frontend:  http://localhost:5173"
    echo "  API:       http://localhost:5000"
    echo "  Health:    http://localhost:5000/api/v1/health"
    echo ""
    echo "View logs with: ./dev.sh logs"
    echo "Check status with: ./dev.sh status"
}

stop_dev() {
    log_info "Stopping development containers..."
    podman-compose -f "$COMPOSE_FILE" down
    log_success "Containers stopped"
}

restart_dev() {
    log_info "Restarting development containers..."
    stop_dev
    start_dev
}

clean_dev() {
    local clean_gitignore=false

    # Parse arguments
    if [[ "${1:-}" == "--gitignore" ]] || [[ "${1:-}" == "-g" ]]; then
        clean_gitignore=true
    fi

    if [ "$clean_gitignore" = true ]; then
        log_warning "This will remove all files matching patterns in .gitignore!"
        echo "Files to be removed:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        git clean -ndX | sed 's/^Would remove /  - /'
        echo ""
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Removing gitignored files..."
            git clean -fdX
            log_success "Gitignored files removed"
        else
            log_info "Cleanup cancelled"
        fi
    else
        log_warning "This will remove all containers, images, and volumes!"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Cleaning up containers..."
            podman-compose -f "$COMPOSE_FILE" down -v
            podman rmi $(podman images | grep $PROJECT_NAME | awk '{print $3}') 2>/dev/null || true
            log_success "Container cleanup complete"

            # Ask about gitignored files
            echo ""
            log_info "Would you also like to remove gitignored files?"
            read -p "Remove gitignored files? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Files to be removed:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                git clean -ndX | sed 's/^Would remove /  - /'
                echo ""
                read -p "Proceed with removal? (y/N) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    log_info "Removing gitignored files..."
                    git clean -fdX
                    log_success "Gitignored files removed"
                else
                    log_info "Gitignore cleanup skipped"
                fi
            else
                log_info "Gitignore cleanup skipped"
            fi
        else
            log_info "Cleanup cancelled"
        fi
    fi
}

show_status() {
    log_info "Checking container status..."
    echo ""

    # Check if containers exist
    if ! podman ps -a | grep -q "msn-weather"; then
        log_warning "No containers found. Run './dev.sh setup' first."
        return
    fi

    # Show container status
    echo "Container Status:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    podman ps -a --filter "name=msn-weather" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""

    # Check service health
    if podman ps | grep -q "msn-weather-api-dev"; then
        echo "Service Health:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        if curl -s http://localhost:5000/api/v1/health > /dev/null 2>&1; then
            log_success "API:       http://localhost:5000 - HEALTHY"
        else
            log_warning "API:       http://localhost:5000 - NOT RESPONDING"
        fi

        if curl -s http://localhost:5173 > /dev/null 2>&1; then
            log_success "Frontend:  http://localhost:5173 - HEALTHY"
        else
            log_warning "Frontend:  http://localhost:5173 - NOT RESPONDING"
        fi
    else
        log_info "Containers are not running. Start with: ./dev.sh start"
    fi
    echo ""
}

check_port_conflicts() {
    log_info "Checking for port conflicts..."
    local conflicts=0

    # Check port 5000 (API)
    if netstat -tuln 2>/dev/null | grep -q ":5000 " || ss -tuln 2>/dev/null | grep -q ":5000 "; then
        log_error "Port 5000 is already in use (required for API)"
        conflicts=$((conflicts + 1))
    fi

    # Check port 5173 (Frontend)
    if netstat -tuln 2>/dev/null | grep -q ":5173 " || ss -tuln 2>/dev/null | grep -q ":5173 "; then
        log_error "Port 5173 is already in use (required for Frontend)"
        conflicts=$((conflicts + 1))
    fi

    if [ $conflicts -gt 0 ]; then
        log_error "Found $conflicts port conflict(s). Please free the ports before starting."
        echo "  Tip: Use 'lsof -i :5000' or 'lsof -i :5173' to find the process using these ports"
        return 1
    fi

    log_success "No port conflicts detected"
    return 0
}

run_tests() {
    local watch_mode=false

    # Parse arguments
    if [[ "${1:-}" == "--watch" ]] || [[ "${1:-}" == "-w" ]]; then
        watch_mode=true
    fi

    # Check if containers are running
    if ! podman ps | grep -q "msn-weather-api-dev"; then
        log_error "Containers are not running. Start them with: ./dev.sh start"
        exit 1
    fi

    if [ "$watch_mode" = true ]; then
        log_info "Running tests in watch mode (Ctrl+C to stop)..."
        echo ""
        podman exec -it msn-weather-api-dev pytest -v --looponfail
    else
        log_info "Running backend tests..."
        podman exec msn-weather-api-dev pytest -v

        log_warning "Skipping frontend E2E tests in containerized dev environment"
        log_info "Frontend E2E tests require significant system resources and may fail in containers"
        log_info "To run E2E tests: cd frontend && npm run test:e2e (on host machine)"

        log_success "Backend tests completed!"
    fi
}

generate_and_serve_docs() {
    log_info "Generating comprehensive documentation with reports..."

    # Check if containers are running
    if ! podman ps | grep -q "msn-weather-api-dev"; then
        log_warning "API container not running. Starting containers..."
        start_dev
        sleep 5  # Wait for containers to be ready
    fi

    # Check if mkdocs is installed
    if ! command -v mkdocs &> /dev/null; then
        log_warning "mkdocs not found. Installing..."
        pip3 install --user mkdocs mkdocs-material pymdown-extensions
    fi

    # Create reports directory
    mkdir -p docs/reports

    # Run backend tests with coverage and generate reports
    log_info "Running backend tests with coverage..."
    podman-compose -f "$COMPOSE_FILE" exec -T api pytest \
        --cov=msn_weather_wrapper \
        --cov-report=html:htmlcov \
        --cov-report=json:coverage.json \
        --cov-report=term \
        --junitxml=junit.xml \
        -v || true

    # Copy coverage reports from container
    log_info "Extracting coverage data..."
    API_CONTAINER=$(podman ps --filter "name=msn-weather-api-dev" --format "{{.Names}}" | head -1)
    if [ -n "$API_CONTAINER" ]; then
        podman cp "$API_CONTAINER:/app/coverage.json" ./coverage.json 2>/dev/null || true
        podman cp "$API_CONTAINER:/app/htmlcov" ./htmlcov 2>/dev/null || true
        podman cp "$API_CONTAINER:/app/junit.xml" ./junit.xml 2>/dev/null || true
    fi

    # Generate coverage report
    if [ -f coverage.json ]; then
        log_info "Generating coverage report..."
        python3 tools/generate_reports.py --type coverage --input . --output docs/reports/coverage-report.md
    fi

    # Generate test report
    if [ -f junit.xml ]; then
        log_info "Generating test report..."
        mkdir -p test-results
        mv junit.xml test-results/
        python3 tools/generate_reports.py --type test --input test-results --output docs/reports/test-report.md
    fi

    # Run security scan
    log_info "Running security scan..."
    podman-compose -f "$COMPOSE_FILE" exec -T api bash -c \
        "pip install bandit safety && bandit -r src/ -f json -o bandit-report.json || true" || true

    # Copy security report from container
    if [ -n "$API_CONTAINER" ]; then
        podman cp "$API_CONTAINER:/app/bandit-report.json" ./bandit-report.json 2>/dev/null || true
    fi

    if [ -f bandit-report.json ]; then
        log_info "Generating security report..."
        mkdir -p security-results
        mv bandit-report.json security-results/
        python3 tools/generate_reports.py --type security --input security-results --output docs/reports/security-report.md
    fi

    # Generate license report
    log_info "Generating license report..."
    podman-compose -f "$COMPOSE_FILE" exec -T api bash -c \
        "pip install pip-licenses && pip-licenses --format=json --output-file=licenses.json" || true

    # Copy license report from container
    if [ -n "$API_CONTAINER" ]; then
        podman cp "$API_CONTAINER:/app/licenses.json" ./licenses.json 2>/dev/null || true
    fi

    if [ -f licenses.json ]; then
        mkdir -p license-results
        mv licenses.json license-results/
        python3 tools/generate_reports.py --type license --input license-results --output docs/reports/license-report.md
    fi

    # Generate CI/CD report
    log_info "Generating CI/CD pipeline report..."
    python3 tools/generate_reports.py --type cicd --output docs/reports/ci-cd.md

    # Create reports index if it doesn't exist
    if [ ! -f docs/reports/index.md ]; then
        cat > docs/reports/index.md << 'INDEXEOF'
# Reports Overview

Automated reports generated from test execution, code coverage, security scans, and license compliance checks.

## 📊 Available Reports

- **[Test Report](test-report.md)** - Test execution results and statistics
- **[Coverage Report](coverage-report.md)** - Code coverage analysis
- **[Security Report](security-report.md)** - Security vulnerability scan results
- **[License Report](license-report.md)** - Dependency license compliance
- **[CI/CD Pipeline](ci-cd.md)** - Pipeline execution status

## 🔄 Report Generation

Reports are automatically generated during CI/CD pipeline execution and can be regenerated locally using:

```bash
./dev.sh docs
```

All reports are timestamped and reflect the current state of the codebase.
INDEXEOF
        log_success "Created reports index"
    fi

    # Update README in reports
    if [ ! -f docs/reports/README.md ]; then
        ln -sf index.md docs/reports/README.md
    fi

    log_success "All reports generated!"

    # Cleanup temporary files
    log_info "Cleaning up temporary files..."
    rm -f coverage.json junit.xml bandit-report.json licenses.json 2>/dev/null
    rm -rf test-results security-results license-results 2>/dev/null
    log_success "Temporary files cleaned up"

    # Start MkDocs server
    log_info "Starting documentation server..."
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 Documentation site will be available at:"
    echo "   http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    mkdocs serve
}

show_logs() {
    podman-compose -f "$COMPOSE_FILE" logs -f
}

shell_api() {
    log_info "Opening shell in API container..."
    podman exec -it msn-weather-api-dev /bin/bash
}

shell_frontend() {
    log_info "Opening shell in frontend container..."
    podman exec -it msn-weather-frontend-dev /bin/bash
}

rebuild_all() {
    log_info "Rebuilding all containers..."
    podman-compose -f "$COMPOSE_FILE" down
    podman-compose -f "$COMPOSE_FILE" build --no-cache
    log_success "Rebuild complete!"
}

monitor_workflows() {
    # Add CYAN color for running status
    local CYAN='\033[0;36m'
    local MAGENTA='\033[0;35m'

    # GitHub API configuration
    local GITHUB_OWNER="jim-wyatt"
    local GITHUB_REPO="msn-weather-wrapper"
    local GITHUB_API_BASE="https://api.github.com"

    # Function to get RAG status color and symbol
    get_rag_status() {
        local status="$1"
        local percentage="$2"

        # If percentage provided, use thresholds
        if [ -n "$percentage" ]; then
            if [ "$percentage" -ge 80 ]; then
                echo "GREEN|✅"
            elif [ "$percentage" -ge 60 ]; then
                echo "AMBER|⚠️"
            else
                echo "RED|❌"
            fi
            return
        fi

        # Otherwise use status string
        case "$status" in
            pass|success|clean|healthy|completed) echo "GREEN|✅" ;;
            warn|warning|amber|in_progress|queued) echo "AMBER|⚠️" ;;
            fail|failure|error|stopped|down|unhealthy) echo "RED|❌" ;;
            skip|skipped|cancelled|disabled|unknown) echo "GREY|⊘" ;;
            *) echo "GREY|○" ;;
        esac
    }

    # Function to format RAG output
    format_rag() {
        local rag_output="$1"
        local color="${rag_output%%|*}"
        local symbol="${rag_output##*|}"

        case "$color" in
            GREEN) printf "%b%s%b" "${GREEN}" "$symbol" "${NC}" ;;
            AMBER) printf "%b%s%b" "${YELLOW}" "$symbol" "${NC}" ;;
            RED) printf "%b%s%b" "${RED}" "$symbol" "${NC}" ;;
            GREY) printf "%b%s%b" "${BLUE}" "$symbol" "${NC}" ;;
            *) printf "%s" "$symbol" ;;
        esac
    }

    # Function to get local build status
    get_local_status() {
        local item="$1"
        case "$item" in
            coverage)
                if [ -f "htmlcov/index.html" ]; then
                    local pct=$(grep -oP 'pc_cov">\K[0-9]+(?=%)' htmlcov/index.html 2>/dev/null | head -1)
                    if [ -n "$pct" ]; then
                        echo "$pct"
                    else
                        echo "unknown"
                    fi
                else
                    echo "none"
                fi
                ;;
            tests)
                if [ -f "junit.xml" ]; then
                    local fail=$(grep -oP 'failures="\K[0-9]+' junit.xml 2>/dev/null | head -1)
                    if [ "${fail:-0}" -eq 0 ] 2>/dev/null; then
                        echo "pass"
                    else
                        echo "fail"
                    fi
                else
                    echo "none"
                fi
                ;;
            security)
                if [ -f "artifacts/security-reports/bandit-report.json" ]; then
                    local issues=$(jq '[.results[] | select(.issue_severity == "HIGH" or .issue_severity == "CRITICAL")] | length' "artifacts/security-reports/bandit-report.json" 2>/dev/null || echo "0")
                    if [ "${issues:-0}" -eq 0 ] 2>/dev/null; then
                        echo "pass"
                    else
                        echo "fail|$issues"
                    fi
                else
                    echo "none"
                fi
                ;;
            containers)
                if ! command -v podman &> /dev/null; then
                    echo "disabled"
                    return
                fi

                local api_up=$(podman ps --filter "name=msn-weather-api-dev" --format "{{.Status}}" 2>/dev/null)
                local fe_up=$(podman ps --filter "name=msn-weather-frontend-dev" --format "{{.Status}}" 2>/dev/null)

                if [ -n "$api_up" ] && [ -n "$fe_up" ]; then
                    # Check API health
                    if curl -s -f --max-time 2 http://localhost:5000/api/v1/health > /dev/null 2>&1; then
                        echo "healthy"
                    else
                        echo "unhealthy"
                    fi
                elif [ -n "$api_up" ] || [ -n "$fe_up" ]; then
                    echo "partial"
                else
                    echo "stopped"
                fi
                ;;
            git)
                local staged=$(git diff --cached --numstat 2>/dev/null | wc -l || echo "0")
                local unstaged=$(git diff --numstat 2>/dev/null | wc -l || echo "0")
                local untracked=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l || echo "0")

                if [ "$staged" -gt 0 ] || [ "$unstaged" -gt 0 ] || [ "$untracked" -gt 0 ]; then
                    echo "dirty|$staged+$unstaged+$untracked"
                else
                    echo "clean"
                fi
                ;;
            python_env)
                if [ -d "venv" ]; then
                    if [ -n "$VIRTUAL_ENV" ]; then
                        echo "active"
                    else
                        echo "inactive"
                    fi
                else
                    echo "none"
                fi
                ;;
            dependencies)
                if [ -f "pyproject.toml" ] && command -v pip &> /dev/null; then
                    # Check if pip-audit is available
                    if command -v pip-audit &> /dev/null 2>&1 || pip list 2>/dev/null | grep -q "pip-audit"; then
                        local vuln_count=$(pip-audit --desc on --format json 2>/dev/null | jq '.dependencies | length' 2>/dev/null || echo "0")
                        if [ "${vuln_count:-0}" -eq 0 ] 2>/dev/null; then
                            echo "pass"
                        else
                            echo "warn|$vuln_count"
                        fi
                    else
                        echo "unchecked"
                    fi
                else
                    echo "none"
                fi
                ;;
            *)
                echo "unknown"
                ;;
        esac
    }

    # Function to fetch GitHub workflow status
    get_github_workflows() {
        local cache_file="/tmp/gh_workflows_${GITHUB_OWNER}_${GITHUB_REPO}.json"
        local cache_age=0

        # Check cache age (refresh every 30 seconds)
        if [ -f "$cache_file" ]; then
            cache_age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo "0")))
        fi

        # Fetch if cache is old or doesn't exist
        if [ ! -f "$cache_file" ] || [ "$cache_age" -gt 30 ]; then
            curl -s --max-time 5 \
                "${GITHUB_API_BASE}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runs?per_page=5&status=completed" \
                > "$cache_file" 2>/dev/null || echo '{"workflow_runs":[]}' > "$cache_file"
        fi

        cat "$cache_file"
    }

    # Function to get latest workflow run status for a specific workflow
    get_workflow_status() {
        local workflow_name="$1"
        local workflows_json="$2"

        # Extract the latest run for this workflow
        local status=$(echo "$workflows_json" | jq -r --arg name "$workflow_name" \
            '.workflow_runs[] | select(.name == $name) | .conclusion' 2>/dev/null | head -1)

        if [ -z "$status" ] || [ "$status" = "null" ]; then
            echo "unknown"
        else
            echo "$status"
        fi
    }

    # Function to draw the monitor display
    draw_monitor() {
        clear
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

        # Fetch GitHub workflow data
        local workflows_json=$(get_github_workflows)

        printf "%b\n" "${BLUE}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
        printf "%b║%b ${YELLOW}DevSecOps Dashboard${NC}%-45s %b║${NC}\n" "${BLUE}" "${NC}" "" "${BLUE}"
        printf "%b║%b ${CYAN}${GITHUB_OWNER}/${GITHUB_REPO}${NC} @ ${MAGENTA}${branch}${NC}%-30s %b║${NC}\n" "${BLUE}" "${NC}" "" "${BLUE}"
        printf "%b║%b ${BLUE}${timestamp}${NC}%-49s %b║${NC}\n" "${BLUE}" "${NC}" "" "${BLUE}"
        printf "%b╚═══════════════════════════════════════════════════════════════════════════╝${NC}\n" "${BLUE}"
        echo ""

        # ═══════════════════════════════════════════════════════════════════════════
        # LOCAL DEVELOPMENT ENVIRONMENT
        # ═══════════════════════════════════════════════════════════════════════════
        printf "%b┌─ Local Development Environment ─────────────────────────────────────────────┐${NC}\n" "${YELLOW}"

        # Container Services
        local cont_status=$(get_local_status containers)
        local cont_rag=$(get_rag_status "$cont_status")
        local cont_text=""
        case "$cont_status" in
            healthy) cont_text="Both services healthy" ;;
            partial) cont_text="Partial (1 service down)" ;;
            unhealthy) cont_text="API unhealthy" ;;
            stopped) cont_text="Services stopped" ;;
            disabled) cont_text="Podman not available" ;;
        esac
        printf "%b│${NC} %-25s " "${YELLOW}" "Container Services:"
        format_rag "$cont_rag"
        printf "  %-45s %b│${NC}\n" "$cont_text" "${YELLOW}"

        # Python Virtual Environment
        local pyenv_status=$(get_local_status python_env)
        local pyenv_rag=$(get_rag_status "$pyenv_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "Python Virtual Env:"
        format_rag "$pyenv_rag"
        case "$pyenv_status" in
            active) printf "  %bActive (venv/)%b" "${GREEN}" "${NC}" ;;
            inactive) printf "  %bExists but not activated%b" "${YELLOW}" "${NC}" ;;
            none) printf "  %bNot configured%b" "${RED}" "${NC}" ;;
        esac
        printf "%32s%b│${NC}\n" "" "${YELLOW}"

        # Git Working Directory
        local git_status=$(get_local_status git)
        local git_rag=$(get_rag_status "${git_status%%|*}")
        printf "%b│${NC} %-25s " "${YELLOW}" "Git Working Directory:"
        format_rag "$git_rag"
        case "${git_status%%|*}" in
            clean) printf "  %bNo uncommitted changes%b" "${GREEN}" "${NC}" ;;
            dirty)
                local changes="${git_status##*|}"
                printf "  %bChanges: %s%b" "${YELLOW}" "$changes" "${NC}" ;;
        esac
        printf "%30s%b│${NC}\n" "" "${YELLOW}"

        printf "%b└─────────────────────────────────────────────────────────────────────────────┘${NC}\n" "${YELLOW}"
        echo ""

        # ═══════════════════════════════════════════════════════════════════════════
        # CODE QUALITY & TESTING
        # ═══════════════════════════════════════════════════════════════════════════
        printf "%b┌─ Code Quality & Testing ────────────────────────────────────────────────────┐${NC}\n" "${YELLOW}"

        # Test Results
        local test_status=$(get_local_status tests)
        local test_rag=$(get_rag_status "$test_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "Test Execution:"
        format_rag "$test_rag"
        if [ "$test_status" = "pass" ]; then
            if [ -f "junit.xml" ]; then
                local tot=$(grep -oP 'tests="\K[0-9]+' junit.xml 2>/dev/null | head -1)
                printf "  %b%d tests passed%b" "${GREEN}" "${tot:-0}" "${NC}"
            else
                printf "  %bAll tests passed%b" "${GREEN}" "${NC}"
            fi
        elif [ "$test_status" = "fail" ]; then
            if [ -f "junit.xml" ]; then
                local tot=$(grep -oP 'tests="\K[0-9]+' junit.xml 2>/dev/null | head -1)
                local fail=$(grep -oP 'failures="\K[0-9]+' junit.xml 2>/dev/null | head -1)
                printf "  %b%d/%d tests failed%b" "${RED}" "${fail:-0}" "${tot:-0}" "${NC}"
            else
                printf "  %bTests failed%b" "${RED}" "${NC}"
            fi
        else
            printf "  %bNo test report available%b" "${BLUE}" "${NC}"
        fi
        printf "%21s%b│${NC}\n" "" "${YELLOW}"

        # Code Coverage
        local cov_status=$(get_local_status coverage)
        if [ "$cov_status" != "none" ] && [ "$cov_status" != "unknown" ]; then
            local cov_rag=$(get_rag_status "" "$cov_status")
            printf "%b│${NC} %-25s " "${YELLOW}" "Code Coverage:"
            format_rag "$cov_rag"
            if [ "$cov_status" -ge 80 ]; then
                printf "  %b%d%% (Excellent)%b" "${GREEN}" "$cov_status" "${NC}"
            elif [ "$cov_status" -ge 60 ]; then
                printf "  %b%d%% (Good)%b" "${YELLOW}" "$cov_status" "${NC}"
            else
                printf "  %b%d%% (Needs improvement)%b" "${RED}" "$cov_status" "${NC}"
            fi
        else
            local cov_rag="GREY|○"
            printf "%b│${NC} %-25s " "${YELLOW}" "Code Coverage:"
            format_rag "$cov_rag"
            printf "  %bNo coverage report%b" "${BLUE}" "${NC}"
        fi
        printf "%27s%b│${NC}\n" "" "${YELLOW}"

        printf "%b└─────────────────────────────────────────────────────────────────────────────┘${NC}\n" "${YELLOW}"
        echo ""

        # ═══════════════════════════════════════════════════════════════════════════
        # SECURITY & COMPLIANCE
        # ═══════════════════════════════════════════════════════════════════════════
        printf "%b┌─ Security & Compliance ─────────────────────────────────────────────────────┐${NC}\n" "${YELLOW}"

        # SAST Security Scan
        local sec_status=$(get_local_status security)
        local sec_rag=$(get_rag_status "${sec_status%%|*}")
        printf "%b│${NC} %-25s " "${YELLOW}" "SAST Security Scan:"
        format_rag "$sec_rag"
        if [ "${sec_status%%|*}" = "pass" ]; then
            printf "  %bNo critical vulnerabilities%b" "${GREEN}" "${NC}"
        elif [ "${sec_status%%|*}" = "fail" ]; then
            local issues="${sec_status##*|}"
            printf "  %b%s critical issues found%b" "${RED}" "$issues" "${NC}"
        else
            printf "  %bNo security report%b" "${BLUE}" "${NC}"
        fi
        printf "%26s%b│${NC}\n" "" "${YELLOW}"

        # Dependency Vulnerabilities
        local dep_status=$(get_local_status dependencies)
        local dep_rag=$(get_rag_status "${dep_status%%|*}")
        printf "%b│${NC} %-25s " "${YELLOW}" "Dependency Scan:"
        format_rag "$dep_rag"
        case "${dep_status%%|*}" in
            pass) printf "  %bNo known vulnerabilities%b" "${GREEN}" "${NC}" ;;
            warn)
                local vuln_count="${dep_status##*|}"
                printf "  %b%s vulnerable packages%b" "${YELLOW}" "$vuln_count" "${NC}" ;;
            unchecked) printf "  %bNot scanned (install pip-audit)%b" "${BLUE}" "${NC}" ;;
            none) printf "  %bUnavailable%b" "${BLUE}" "${NC}" ;;
        esac
        printf "%34s%b│${NC}\n" "" "${YELLOW}"

        # License Compliance
        if [ -f "artifacts/security-reports/licenses.json" ]; then
            local pkgs=$(jq 'length' "artifacts/security-reports/licenses.json" 2>/dev/null)
            printf "%b│${NC} %-25s " "${YELLOW}" "License Compliance:"
            format_rag "GREEN|✅"
            printf "  %b%s dependencies tracked%b" "${GREEN}" "$pkgs" "${NC}"
        else
            printf "%b│${NC} %-25s " "${YELLOW}" "License Compliance:"
            format_rag "GREY|○"
            printf "  %bNo license report%b" "${BLUE}" "${NC}"
        fi
        printf "%28s%b│${NC}\n" "" "${YELLOW}"

        printf "%b└─────────────────────────────────────────────────────────────────────────────┘${NC}\n" "${YELLOW}"
        echo ""

        # ═══════════════════════════════════════════════════════════════════════════
        # GITHUB CI/CD WORKFLOWS
        # ═══════════════════════════════════════════════════════════════════════════
        printf "%b┌─ GitHub CI/CD Workflows (Latest Runs) ──────────────────────────────────────┐${NC}\n" "${YELLOW}"

        # CI Pipeline
        local ci_status=$(get_workflow_status "CI Pipeline" "$workflows_json")
        local ci_rag=$(get_rag_status "$ci_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "CI Pipeline:"
        format_rag "$ci_rag"
        case "$ci_status" in
            success) printf "  %bPassed%b" "${GREEN}" "${NC}" ;;
            failure) printf "  %bFailed%b" "${RED}" "${NC}" ;;
            cancelled) printf "  %bCancelled%b" "${BLUE}" "${NC}" ;;
            *) printf "  %bNo recent runs%b" "${BLUE}" "${NC}" ;;
        esac
        printf "%31s%b│${NC}\n" "" "${YELLOW}"

        # Security Scans
        local sec_wf_status=$(get_workflow_status "Security Scans" "$workflows_json")
        local sec_wf_rag=$(get_rag_status "$sec_wf_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "Security Scans:"
        format_rag "$sec_wf_rag"
        case "$sec_wf_status" in
            success) printf "  %bPassed%b" "${GREEN}" "${NC}" ;;
            failure) printf "  %bFailed%b" "${RED}" "${NC}" ;;
            cancelled) printf "  %bCancelled%b" "${BLUE}" "${NC}" ;;
            *) printf "  %bNo recent runs%b" "${BLUE}" "${NC}" ;;
        esac
        printf "%31s%b│${NC}\n" "" "${YELLOW}"

        # Build & Push
        local build_status=$(get_workflow_status "Build & Push" "$workflows_json")
        local build_rag=$(get_rag_status "$build_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "Build & Push:"
        format_rag "$build_rag"
        case "$build_status" in
            success) printf "  %bPassed%b" "${GREEN}" "${NC}" ;;
            failure) printf "  %bFailed%b" "${RED}" "${NC}" ;;
            cancelled) printf "  %bCancelled%b" "${BLUE}" "${NC}" ;;
            *) printf "  %bNo recent runs%b" "${BLUE}" "${NC}" ;;
        esac
        printf "%31s%b│${NC}\n" "" "${YELLOW}"

        # Deploy to Production
        local deploy_status=$(get_workflow_status "Deploy to Production" "$workflows_json")
        local deploy_rag=$(get_rag_status "$deploy_status")
        printf "%b│${NC} %-25s " "${YELLOW}" "Deploy to Production:"
        format_rag "$deploy_rag"
        case "$deploy_status" in
            success) printf "  %bPassed%b" "${GREEN}" "${NC}" ;;
            failure) printf "  %bFailed%b" "${RED}" "${NC}" ;;
            cancelled) printf "  %bCancelled%b" "${BLUE}" "${NC}" ;;
            *) printf "  %bNo recent runs%b" "${BLUE}" "${NC}" ;;
        esac
        printf "%31s%b│${NC}\n" "" "${YELLOW}"

        printf "%b└─────────────────────────────────────────────────────────────────────────────┘${NC}\n" "${YELLOW}"
        echo ""

        printf "%b─────────────────────────────────────────────────────────────────────────────${NC}\n" "${BLUE}"
        printf " ${GREEN}●${NC} Press Ctrl+C to exit  ${BLUE}•${NC}  Updates every 60s  ${BLUE}•${NC}  GitHub API via public endpoint\n"
        printf "%b─────────────────────────────────────────────────────────────────────────────${NC}\n" "${BLUE}"
    }

    log_info "Starting DevOps monitor (Ctrl+C to exit)..."
    sleep 1

    # Trap Ctrl+C to clean up
    trap 'clear; echo -e "${GREEN}Monitor stopped${NC}"; exit 0' INT TERM

    while true; do
        draw_monitor
        sleep 60
    done
}

create_dev_compose() {
    cat > "$COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Containerfile.dev
    container_name: msn-weather-api-dev
    ports:
      - "5000:5000"
    volumes:
      - ./src:/app/src:z
      - ./api.py:/app/api.py:z
      - ./tests:/app/tests:z
      - ./pyproject.toml:/app/pyproject.toml:z
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - PYTHONUNBUFFERED=1
    command: python api.py
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Containerfile.dev
    container_name: msn-weather-frontend-dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend/src:/app/src:z
      - ./frontend/tests:/app/tests:z
      - ./frontend/public:/app/public:z
    environment:
      - NODE_ENV=development
    command: npm run dev -- --host 0.0.0.0
    depends_on:
      - api

  test-runner:
    build:
      context: .
      dockerfile: Containerfile.dev
    container_name: msn-weather-test-runner
    volumes:
      - ./src:/app/src:z
      - ./api.py:/app/api.py:z
      - ./tests:/app/tests:z
      - ./pyproject.toml:/app/pyproject.toml:z
    environment:
      - PYTHONUNBUFFERED=1
    command: pytest --cov=msn_weather_wrapper --cov-report=term-missing --cov-report=html
    profiles:
      - test
EOF
    log_success "Development compose file created: $COMPOSE_FILE"
}

show_usage() {
    cat << EOF
Developer Environment Manager for MSN Weather Wrapper

Usage: ./dev.sh [command] [options]

Commands:
  setup             Initial setup (build images, install dependencies)
  start             Start all development containers
  stop              Stop all containers
  restart           Restart all containers
  status            Show container status and health checks
  clean [--gitignore]
                    Remove all containers, images, and volumes
                    --gitignore, -g: Remove only gitignored files
  test [--watch]    Run all tests (backend + frontend)
                    --watch, -w: Run tests in watch mode
  docs              Generate all reports and serve documentation site
  logs              Show logs from all containers
  shell-api         Open shell in API container
  shell-frontend    Open shell in frontend container
  rebuild           Rebuild all containers from scratch
  monitor           Real-time DevSecOps dashboard with RAG status indicators
                    • Local: containers, tests, coverage, security, dependencies
                    • GitHub: CI/CD workflow status (public API, no auth required)
                    • Updates every 60 seconds
  help              Show this help message

Examples:
  ./dev.sh setup              # First-time setup
  ./dev.sh start              # Start development
  ./dev.sh status             # Check container status
  ./dev.sh monitor            # Launch comprehensive DevSecOps dashboard
  ./dev.sh logs               # Watch logs
  ./dev.sh test               # Run tests once
  ./dev.sh test --watch       # Run tests in watch mode
  ./dev.sh clean              # Remove containers and optionally gitignored files
  ./dev.sh clean --gitignore  # Remove only gitignored files
  ./dev.sh docs               # Generate reports & serve docs

Monitor Dashboard Features:
  ✅ Green   - Healthy/Passing (80%+ coverage, 0 critical issues, all tests pass)
  ⚠️  Amber   - Warning (60-79% coverage, minor issues, partial services)
  ❌ Red     - Critical (< 60% coverage, failed tests, critical vulnerabilities)
  ○  Grey    - Unknown/Not Available

EOF
}

# Main script logic
case "${1:-help}" in
    setup)
        setup_dev_env
        ;;
    start)
        start_dev
        ;;
    stop)
        stop_dev
        ;;
    restart)
        restart_dev
        ;;
    status)
        show_status
        ;;
    clean)
        shift  # Remove 'clean' from arguments
        clean_dev "$@"
        ;;
    test)
        shift  # Remove 'test' from arguments
        run_tests "$@"
        ;;
    docs)
        generate_and_serve_docs
        ;;
    logs)
        show_logs
        ;;
    shell-api)
        shell_api
        ;;
    shell-frontend)
        shell_frontend
        ;;
    rebuild)
        rebuild_all
        ;;
    monitor)
        monitor_workflows
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
