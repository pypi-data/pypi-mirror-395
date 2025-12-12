.PHONY: help setup test test-fast test-integration lint format ruff ruff-fix build clean dev check all black mypy deptree

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: ## Setup development environment
	@./scripts/setup.sh

dev: setup ## Setup development environment (alias)

test: ## Run all tests with coverage
	@./scripts/test.sh

test-fast: ## Run fast tests only (skip slow and integration)
	@./scripts/test.sh --fast

test-integration: ## Run integration tests only
	@./scripts/test.sh --integration

test-no-cov: ## Run tests without coverage
	@./scripts/test.sh --no-cov

lint: ## Run all linting checks (black, ruff, mypy)
	@./scripts/lint.sh

ruff: ## Run ruff linter
	@./scripts/ruff.sh

ruff-fix: ## Run ruff with auto-fix
	@./scripts/ruff.sh --fix

format: ## Format code with black and ruff
	@./scripts/format.sh

black: ## Format code with black only
	@source .venv/bin/activate && black src/ tests/

mypy: ## Run type checking with mypy
	@source .venv/bin/activate && mypy src/

build: ## Build the package
	@./scripts/build.sh

clean: ## Clean build artifacts and cache files
	@./scripts/clean.sh

deptree: ## Show dependency tree
	@./scripts/deptree.sh

check: lint test ## Run all checks (lint + test)

all: clean format lint test build ## Run complete CI workflow
	@echo ""
	@echo "✅ All checks passed and package built successfully!"
