.PHONY: help install test test-cov test-fast clean lint format docs

help:
	@echo "Available commands:"
	@echo "  make install     Install package in editable mode with dev dependencies"
	@echo "  make test        Run all tests"
	@echo "  make test-cov    Run tests with coverage report"
	@echo "  make test-fast   Run tests without slow tests"
	@echo "  make clean       Remove build artifacts and cache files"
	@echo "  make lint        Run code quality checks"
	@echo "  make format      Format code with black"
	@echo "  make docs        Build documentation"

install:
	uv pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=cesiumjs_anywidget --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-fast:
	pytest -m "not slow"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

lint:
	ruff check src/ tests/ || true
	mypy src/ || true

format:
	ruff check --fix src/ tests/ || true
	ruff format src/ tests/ || true

docs:
	@echo "Documentation building not yet configured"

.DEFAULT_GOAL := help
