.PHONY: test lint format type-check clean check-style all

test:
	pytest

lint:
	ruff check --fix src/beautils

format:
	ruff format --fix src/beautils
	black src/beautils
	isort src/beautils

type-check:
	mypy src/beautils

clean: lint format

check: test lint format type-check

install-dev:
	pip install -e .[dev]

build:
	pip install --upgrade build
	python -m build

cleanup:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +