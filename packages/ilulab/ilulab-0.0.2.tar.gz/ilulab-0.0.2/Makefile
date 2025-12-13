.PHONY: clean
clean:
	rm -rf dist/ build/ *.egg-info/ .venv/ .mypy_cache/ .pytest_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

.PHONY: build
build: clean
	uv run --frozen --extra dev python -m build

.PHONY: publish-test
publish-test: build
	uv run --frozen --extra dev python -m twine upload --repository testpypi dist/* --verbose

.PHONY: publish
publish: build
	uv run --frozen --extra dev python -m twine upload dist/*

.PHONY: lint
lint:
	uv run --frozen --extra dev ruff check .

.PHONY: format
format:
	uv run --frozen --extra dev ruff format .
	uv run --frozen --extra dev ruff check --fix .

.PHONY: typecheck
typecheck:
	uv run --frozen --extra dev ty check ilulab

.PHONY: check
check: lint typecheck

.PHONY: test
test:
	uv run --frozen --extra dev pytest tests/
