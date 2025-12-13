.PHONY: help
.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

lint: ## Run linting with ruff
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

typecheck: ## Run type checking with mypy
	uv run python -m mypy elevenlabs_tts_tool

test: ## Run tests
	uv run python -m pytest tests/

security-bandit: ## Run bandit security linter
	uv run bandit -r elevenlabs_tts_tool -c pyproject.toml

security-pip-audit: ## Run pip-audit for dependency vulnerabilities
	uv run pip-audit

security-gitleaks: ## Run gitleaks secret scanner
	@command -v gitleaks >/dev/null 2>&1 || { echo "❌ gitleaks not found. Install: brew install gitleaks"; exit 1; }
	gitleaks detect --source . --config .gitleaks.toml --verbose

security: security-bandit security-pip-audit security-gitleaks ## Run all security checks

check: lint typecheck test security ## Run all checks (lint, typecheck, test, security)

pipeline: format lint typecheck test security build install-global ## Run full pipeline (format, lint, typecheck, test, security, build, install-global)

clean: ## Remove build artifacts and cache
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

run: ## Run elevenlabs-tts-tool (usage: make run ARGS="...")
	uv run elevenlabs-tts-tool $(ARGS)

build: ## Build package
	uv build --force-pep517

install-global: ## Install globally with uv tool
	uv tool uninstall elevenlabs-tts-tool || true
	uv build --force-pep517
	uv tool install .

uninstall-global: ## Uninstall global installation
	uv tool uninstall elevenlabs-tts-tool
