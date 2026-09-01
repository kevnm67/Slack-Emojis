.PHONY: setup test lint format build fetch clean ci

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"
	.venv/bin/pre-commit install

test:
	python3 -m pytest tests/ -v

lint:
	python3 -m ruff check src/ tests/

format:
	python3 -m ruff format src/ tests/

build:
	python3 -m slack_emojis.update_emojis

fetch:
	python3 -m slack_emojis.fetch_slack_emojis

clean:
	find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache *.egg-info

ci: lint test build
