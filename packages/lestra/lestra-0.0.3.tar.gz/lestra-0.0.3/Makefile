export PYTHONPATH=src


lint:
	uvx ruff check --no-fix
	uvx ruff format --check


.PHONY: tests
tests:
	 uv run --group tests pytest --cov=src tests/*


format:
	uvx ruff format
	uvx ruff check --fix



docs-serve:
	uv run --group docs mkdocs serve


docs-build:
	uv run --group docs mkdocs build


