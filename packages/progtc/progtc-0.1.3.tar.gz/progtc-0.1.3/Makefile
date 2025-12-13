.PHONY: lint check test ci

lint:
	uv run ruff check --fix
	uv run ruff format
	uv run mypy .

check:
	uv run ruff check
	uv run ruff format --check
	uv run mypy .

test:
	uv run pytest

ci: check test
