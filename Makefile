.PHONY: setup test lint format build clean ci

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"
	.venv/bin/pre-commit install

test:
	python3 -m pytest scripts/tests/ -v

lint:
	python3 -m ruff check scripts/

format:
	python3 -m ruff format scripts/

build:
	python3 scripts/update_emojis.py

clean:
	find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
	rm -rf .pytest_cache

ci: lint test build
