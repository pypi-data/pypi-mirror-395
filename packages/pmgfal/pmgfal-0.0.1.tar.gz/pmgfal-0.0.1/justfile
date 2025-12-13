# build rust extension
build:
    uv run maturin develop

# run tests (requires build first)
test: build
    uv run pytest

# lint python
lint:
    uv run ruff check
    uv run ruff format --check

# format python
fmt:
    uv run ruff format
