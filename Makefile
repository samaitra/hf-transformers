# Makefile for HF Transformers

.PHONY: help install install-dev test test-cov lint format type-check clean run-example build dist

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with Black"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  clean        - Clean up generated files"
	@echo "  run-example  - Run the example application"
	@echo "  build        - Build the package"
	@echo "  dist         - Create distribution files"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Run linting
lint:
	flake8 src/ tests/ main.py

# Format code
format:
	black src/ tests/ main.py

# Type checking
type-check:
	mypy src/

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -f *.log
	rm -f *.json
	rm -f *.csv
	rm -f *.txt

# Run the example application
run-example:
	python main.py

# Build the package
build:
	python setup.py build

# Create distribution files
dist:
	python setup.py sdist bdist_wheel

# Check code quality (format, lint, type-check)
check: format lint type-check

# Full development setup
setup: install-dev format lint type-check test

# Quick development cycle
dev: format lint test 