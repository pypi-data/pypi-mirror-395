# ============================================================
# pomo-i18n Makefile
#
# This Makefile provides a unified interface for:
#   - Installing development dependencies
#   - Running linters (flake8)
#   - Running type checks (mypy --strict)
#   - Running tests (pytest)
#   - Generating code coverage reports
#   - Auto-formatting the codebase (Black)
#
# Usage:
#   make init          # Install dev dependencies
#   make lint          # Run flake8
#   make typecheck     # Run mypy
#   make test          # Run pytest
#   make coverage      # Run coverage (+ report)
#   make coverage-html # Generate HTML coverage report
#   make format        # Run black formatter
#   make bench         # Run bench
#   make bench-pytest  # Run pytest-benchmark
#   make all           # Run lint + typecheck + test + coverage
#   make clean         # Remove caches and build artifacts
#
# Notes:
#   - All dev tools are installed through pyproject.toml `[project.optional-dependencies].dev`
#   - `make all` is ideal for pre-commit checking and CI
# ============================================================

.PHONY: init lint typecheck test coverage coverage-html format bench bench-pytesst all clean


# ------------------------------------------------------------
# Install development dependencies
# ------------------------------------------------------------
init:
	@echo ">>> Installing pomo-i18n development dependencies..."
	pip install -e .[dev]


# ------------------------------------------------------------
# Lint (flake8)
# ------------------------------------------------------------
lint:
	@echo ">>> Running flake8..."
	flake8 src/pypomo


# ------------------------------------------------------------
# Type checking (mypy strict mode)
# ------------------------------------------------------------
typecheck:
	@echo ">>> Running mypy (strict mode)..."
	mypy src/pypomo --strict


# ------------------------------------------------------------
# Run tests (pytest)
# ------------------------------------------------------------
test:
	@echo ">>> Running pytest..."
	pytest --maxfail=1 --disable-warnings


# ------------------------------------------------------------
# Coverage: CLI report
# ------------------------------------------------------------
coverage:
	@echo ">>> Running coverage..."
	coverage run -m pytest
	coverage report


# ------------------------------------------------------------
# Coverage: HTML report
# ------------------------------------------------------------
coverage-html:
	@echo ">>> Generating HTML coverage report..."
	coverage run -m pytest
	coverage html
	@echo "Open htmlcov/index.html in your browser."


# ------------------------------------------------------------
# Auto-code formatting (Black)
# ------------------------------------------------------------
format:
	@echo ">>> Formatting code with Black..."
	black src tests


# ------------------------------------------------------------
# Benchmark
# ------------------------------------------------------------
bench:
	@echo ">>> Benchmark "
	PYTHONPATH=src python bench/timeit_plural.py

bench-pytest:
	PYTHONPATH=src pytest --benchmark-only


# ------------------------------------------------------------
# Run everything: lint + typecheck + test + coverage
# ------------------------------------------------------------
all: lint typecheck test coverage
	@echo ">>> All checks completed successfully!"


# ------------------------------------------------------------
# Clean cache / build artifacts
# ------------------------------------------------------------
clean:
	@echo ">>> Cleaning build artifacts & caches..."
	rm -rf .coverage htmlcov/ __pycache__/ */__pycache__/ \
		build dist *.egg-info
