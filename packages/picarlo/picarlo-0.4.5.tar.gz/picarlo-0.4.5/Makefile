# Make targets to abstract common project workflows
# Usage: `make <target>` (see `make help` for all targets)

.DEFAULT_GOAL := help

UV ?= uv
PACKAGE ?= picarlo

.PHONY: help uv-update sync install lint format typecheck test check build publish install-check precommit clean dev

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "Available targets:\n"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

uv-update: ## Update uv itself
	$(UV) self update

sync: ## Sync project with dev dependencies
	$(UV) sync --group dev

install: uv-update sync ## Install/update tooling and dependencies (incl. dev)

lint: ## Run lint checks (Ruff & Cargo)
	$(UV) run ruff check .
	cargo clippy

format: ## Apply formatting (Ruff & Cargo)
	$(UV) run ruff format .
	cargo fmt

typecheck: ## Run type checks via pyrefly
	$(UV) run pyrefly check

test: ## Run tests with coverage
	$(UV) run pytest

benchmark: ## Run benchmarks only
	$(UV) run pytest --benchmark-only

check: lint typecheck test ## Run lint, type checks, and tests

# Add 'dev' to install the package in editable mode with the Rust extension
dev: ## Build and install the package in development mode
	$(UV) run maturin develop

# Update 'build' to just focus on distribution artifacts
build: clean ## Build sdist and wheel for distribution
	$(UV) run maturin build --release --sdist
# Publishing:
# - Provide PYPI_TOKEN env var (and optionally PYPI_REPOSITORY) when invoking:
#   PYPI_TOKEN=... make publish
#   PYPI_TOKEN=... PYPI_REPOSITORY=testpypi make publish
publish: ## Publish package using uv (requires PYPI_TOKEN env var)
	$(UV) publish $(if $(PYPI_REPOSITORY),--repository $(PYPI_REPOSITORY),) $(if $(PYPI_TOKEN),--token $(PYPI_TOKEN),)

install-check: ## Verify the package can be imported in a clean interpreter
	$(UV) run --with $(PACKAGE) --no-project -- python -c "import $(PACKAGE)"

changelog: ## Generate CHANGELOG.md using git-cliff
	$(UV) tool run git-cliff --config cliff.toml --output CHANGELOG.md

precommit: ## Run all pre-commit hooks (if configured)
	$(UV) run pre-commit run --all-files

precommit-install: ## Install git hooks for pre-commit
	$(UV) run pre-commit install


docs-serve: ## Serve documentation locally
	$(UV) run mkdocs serve

docs-build: ## Build documentation site
	$(UV) run mkdocs build

## find src -name "*.so" -delete  # Remove compiled extension modules
clean:
	rm -rf dist build .pytest_cache .ruff_cache .pyrefly_cache *.egg-info target
	find . -type d -name "__pycache__" -exec rm -rf {} +
