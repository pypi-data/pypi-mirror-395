# build rust extension in dev mode
dev:
    uvx maturin develop

# run tests
test: dev
    uv run pytest -v

# build release wheels
build:
    uvx maturin build --release

# lint
lint:
    uv run ruff check .
    uv run ruff format --check .

# format
fmt:
    uv run ruff check --fix .
    uv run ruff format .

# benchmark on atproto lexicons
bench: dev
    ./scripts/bench.py

# clean build artifacts
clean:
    rm -rf target dist *.egg-info
