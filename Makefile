# Makefile for vibe-coding-handson-20250823

.PHONY: help test test-chapter4 test-chapter5 run-fizzbuzz run-pong clean install

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	uv sync

# Testing
test: ## Run all tests
	@echo "Running chapter4 tests..."
	@cd chapter4 && uv run --with pytest -m pytest -v || echo "No tests in chapter4"
	@echo "Running chapter5 tests..."
	@cd chapter5 && uv run --with pytest --with pygame -m pytest -v

test-chapter4: ## Run chapter4 lambda expression tests
	@echo "Chapter4 exercises use Jupyter notebooks - run cells directly"
	@cd chapter4 && uv run -m jupyter nbconvert --execute level1.ipynb --to notebook --inplace

test-chapter5: ## Run chapter5 TDD tests (FizzBuzz and Pong)
	cd chapter5 && uv run --with pytest --with pygame -m pytest -v

test-fizzbuzz: ## Run FizzBuzz tests only
	cd chapter5 && uv run --with pytest -m pytest -v test_fizzbuzz.py

test-pong: ## Run Pong game tests only
	cd chapter5 && uv run --with pytest --with pygame -m pytest -v test_pong.py

# Execution
run-fizzbuzz: ## Run FizzBuzz demo (1-100)
	cd chapter5 && uv run run_fizzbuzz.py

run-pong: ## Run Pong game (requires display)
	cd chapter5 && uv run --with pygame pong.py

# Development
notebook: ## Start Jupyter notebook server
	uv run --with jupyter -m jupyter notebook

lab: ## Start JupyterLab server  
	uv run --with jupyterlab -m jupyter lab

# Maintenance
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} + 2>/dev/null || true

lint: ## Run linting (if available)
	@echo "No linter configured - add ruff or flake8 if needed"

format: ## Format code (if available)
	@echo "No formatter configured - add black or ruff format if needed"

# Git shortcuts
commit: ## Stage all changes and commit with message
	git add .
	git status
	@echo "Files staged. Use 'git commit -m \"your message\"' to commit"

push: ## Push changes to remote
	git push

status: ## Show git status
	git status