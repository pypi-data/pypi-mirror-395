.PHONY: help build check clean fix format format-check install lint publish release test test-cov

help:
	@echo "Available targets:"
	@echo "  make build        - Build the project with uv"
	@echo "  make check        - Run all checks (lint, format-check, test)"
	@echo "  make clean        - Remove build artifacts and caches"
	@echo "  make fix          - Auto-fix linting issues and format code"
	@echo "  make format       - Format code with ruff"
	@echo "  make format-check - Check code formatting without changes"
	@echo "  make install      - Install or upgrade the package with pipx"
	@echo "  make lint         - Run ruff linter"
	@echo "  make publish      - Publish the built artifacts to PyPI"
	@echo "  make release      - Performs a full build and release for this project"
	@echo "  make test         - Run pytest"
	@echo "  make test-cov     - Run pytest with coverage report"

build:
	uv build

check: lint format-check test
	@echo ""
	@echo "✅ All checks passed!"

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fix:
	uv run ruff check --fix .
	uv run ruff format .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

install: build
	@VERSION=$$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"); \
	if pipx list | grep -q spotcrates; then \
		pipx install --force dist/spotcrates-$$VERSION-py3-none-any.whl; \
	else \
		pipx install dist/spotcrates-$$VERSION-py3-none-any.whl; \
	fi

lint:
	uv run ruff check .

publish:
	uv publish

release: test build
	@VERSION=$$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"); \
	git tag -a "v$$VERSION" -m "Release v$$VERSION" -f && \
	git push origin "v$$VERSION" -f && \
	uv version --bump patch
	@NEW_VERSION=$$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"); \
	git add pyproject.toml uv.lock && \
	git commit -m "[release] Bumped spotcrates to version $$NEW_VERSION"

test:
	uv run pytest

test-cov:
	uv run pytest --cov=spotcrates --cov-report=term-missing