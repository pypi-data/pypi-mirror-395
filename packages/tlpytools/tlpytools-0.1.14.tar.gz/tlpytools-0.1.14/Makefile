# Makefile for TLPyTools development

.PHONY: help install install-dev install-all test lint format type-check clean build

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install core dependencies
	uv sync

install-dev:  ## Install development dependencies
	uv sync --extra dev

install-orca:  ## Install ORCA dependencies
	uv sync --extra orca

install-activitysim:  ## Install ActivitySim dependencies (development only)
	uv sync --group activitysim

install-all:  ## Install all dependencies (dev + orca + activitysim group)
	uv sync --extra dev --extra orca --group activitysim

test:  ## Run tests
	uv run pytest

test-cov:  ## Run tests with coverage
	uv run pytest --cov=tests --cov-report=html --cov-report=term

lint:  ## Run linting with ruff
	uv run ruff check src/

lint-fix:  ## Run linting with auto-fix
	uv run ruff check --fix src/

format:  ## Format code with black
	uv run black src/

format-check:  ## Check code formatting
	uv run black --check src/

type-check:  ## Run type checking with mypy
	uv run mypy src/

pre-commit:  ## Install pre-commit hooks
	uv run pre-commit install

pre-commit-run:  ## Run pre-commit on all files
	uv run pre-commit run --all-files

clean:  ## Clean build artifacts
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	uv build

lock:  ## Update lock file
	uv lock

sync:  ## Sync dependencies from lock file
	uv sync

upgrade:  ## Upgrade all dependencies
	uv lock --upgrade

check-all: lint format-check type-check test  ## Run all checks

dev-setup: install-all pre-commit  ## Complete development setup (includes all extras)
	@echo "Development environment setup complete!"
