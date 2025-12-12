SPHINX_DIR := sphinx
BUILD_DIR := docs/reference
DOCTREE_DIR := $(SPHINX_DIR)/doctrees

.PHONY: docs-clean
docs-clean: ## Remove generated docs, doctrees, and .rst files (except index.rst)
	@echo "Cleaning docs..."
	@rm -rf $(BUILD_DIR) $(DOCTREE_DIR)
	@find $(SPHINX_DIR) -maxdepth 1 -type f -name "wriftai*.rst" -delete

.PHONY: docs
docs: docs-clean ## Build markdown documentation
	@echo "Building markdown documentation..."
	@uv run sphinx-apidoc -o $(SPHINX_DIR) wriftai -e -T --force
	@uv run sphinx-build -b markdown $(SPHINX_DIR) $(BUILD_DIR) -d $(DOCTREE_DIR)
	@echo "Adding custom frontmatter..."
	@uv run python $(SPHINX_DIR)/_custom_frontmatter.py

.PHONY: install
install: ## Setup virtual environment with dependencies
	@echo "Setting up virtual environment using uv"
	@uv sync

.PHONY: format
format: ## Auto format code
	@echo "Auto formatting with Ruff"
	@uv run ruff format .

.PHONY: format-check
format-check: ## Check that code is properly formatted (no changes made)
	@echo "Checking formatting with Ruff"
	@uv run ruff format --check .

.PHONY: lint
lint: ## Lint code
	@echo "Linting code with Ruff"
	@uv run ruff check .

.PHONY: type-check
type-check: ## Type checking
	@echo "Running mypy"
	@uv run mypy wriftai/ tests/

.PHONY: dep-check
dep-check: ## Check for unused/obsolete deps
	@echo "Running deptry"
	@uv run deptry .

.PHONY: lock-check
lock-check: ## Verify lock file consistency
	@echo "Checking lock file consistency with pyproject.toml"
	@uv lock --locked

.PHONY: check
check: lock-check format-check lint type-check dep-check ## Run all quality control checks.

.PHONY: unit-test
unit-test: ## Run unit tests
	@echo "Running unit tests"
	@uv run python -m pytest --cov --cov-config=pyproject.toml ./tests/unit/

.PHONY: integration-test
integration-test: ## Run integration tests
	@echo "Running integration tests"
	@uv run python -m pytest ./tests/integration/

.PHONY: test
test: unit-test integration-test ## Run all tests

.PHONY: build
build: clean # Build package
	@echo "Building wheel and sdist with uv"
	@uv build

.PHONY: clean
clean: # Clean up build artifacts
	@echo "Removing build artifacts"
	@rm -rf dist

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
