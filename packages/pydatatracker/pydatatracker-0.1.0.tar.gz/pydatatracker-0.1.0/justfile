set shell := ["bash", "-lc"]
UV_CACHE_DIR := "/tmp/uv-cache"

# Default target prints available recipes
default:
	@just --list

install:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv venv --seed
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv pip install -e '.[dev]'

lint:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run ruff check src tests

format:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run ruff format src tests

format-check:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run ruff format --check src tests

test:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run pytest

coverage:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run pytest --cov=pydatatracker --cov-report=term-missing

check: lint format-check test

clean:
	rm -rf .ruff_cache .pytest_cache htmlcov .coverage*

benchmark:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run python scripts/benchmark.py

build:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv build

publish:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv build
	PYPI_TOKEN=${PYPI_TOKEN:?set PYPI_TOKEN} UV_CACHE_DIR={{UV_CACHE_DIR}} uv publish --token "$PYPI_TOKEN"

cli:
	UV_CACHE_DIR={{UV_CACHE_DIR}} uv run python scripts/cli.py demo
