.PHONY: help install install-dev sync lock lint lint-fix format format-check type-check test test-verbose test-coverage run dev clean build check all

help: ## Show this help message
	@echo "HomeStock Backend - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ======================================================================
# Installation & Dependencies
# ======================================================================

install: ## Install dependencies using uv
	uv sync

install-dev: ## Install dependencies including dev tools
	uv sync --extra dev --extra build

sync: ## Sync dependencies with pyproject.toml
	uv sync

lock: ## Update lock file
	uv lock

# ======================================================================
# Code Quality
# ======================================================================

lint: ## Run ruff linter
	uv run ruff check app tests

lint-fix: ## Run ruff linter and auto-fix issues
	uv run ruff check --fix app tests

format: ## Format code with ruff
	uv run ruff format app tests

format-check: ## Check if code is formatted correctly
	uv run ruff format --check app tests

type-check: ## Run pyright type checker
	uv run pyright app tests

check: lint type-check ## Run all checks (lint + type-check)

# ======================================================================
# Testing
# ======================================================================

test: ## Run tests with pytest
	uv run pytest

test-verbose: ## Run tests with verbose output
	uv run pytest -v

test-coverage: ## Run tests with coverage report
	uv run pytest --cov=app --cov-report=term-missing --cov-report=html

# ======================================================================
# Development & Running
# ======================================================================

run: ## Run the FastAPI server (production mode)
	uv run python start_server.py

dev: ## Run the FastAPI server in development mode with auto-reload
	uv run uvicorn app.main:app --host 127.0.0.1 --port 5001 --reload

# ======================================================================
# Building & Distribution
# ======================================================================

build: ## Build backend executable with PyInstaller
	uv run pyinstaller build_backend.spec

# ======================================================================
# Cleanup
# ======================================================================

clean: ## Clean build artifacts and cache
	rm -rf dist build *.egg-info .pytest_cache .ruff_cache htmlcov .coverage .pyright_cache
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# ======================================================================
# Meta Commands
# ======================================================================

all: clean install-dev check test ## Clean, install, check, and test
