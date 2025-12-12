.PHONY: help install test test-examples test-all lint format clean

help:
	@echo "synqed-python Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Install package and dependencies"
	@echo "  test           - Run core tests"
	@echo "  test-examples  - Run example tests"
	@echo "  test-all       - Run all tests (core + examples)"
	@echo "  lint           - Run linters"
	@echo "  format         - Format code"
	@echo "  clean          - Clean build artifacts"

install:
	pip install -e .
	pip install pytest pytest-asyncio pytest-cov aiohttp anthropic openai python-dotenv

test:
	pytest tests/ -v --ignore=tests/examples/

test-examples:
	./scripts/run_example_tests.sh

test-all:
	pytest tests/ -v --cov=src/synqed --cov-report=term-missing --cov-report=html

test-integration:
	./scripts/run_example_tests.sh --integration

lint:
	@echo "Running linters..."
	ruff check src/ tests/ || true
	mypy src/ || true

format:
	@echo "Formatting code..."
	ruff format src/ tests/
	ruff check --fix src/ tests/ || true

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	rm -rf htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

