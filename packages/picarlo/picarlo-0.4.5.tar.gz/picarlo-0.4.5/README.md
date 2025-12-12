# Calculating Pi with Modern Tooling

[![image](https://img.shields.io/pypi/v/picarlo)](https://pypi.org/project/picarlo/)
[![image](https://img.shields.io/pypi/l/picarlo)](https://pypi.org/project/picarlo/)
[![image](https://img.shields.io/pypi/pyversions/picarlo)](https://pypi.org/project/picarlo/)

We need a few things:
1. a CLI tool to specify the number of iterations and the number of cores it runs on:
`picarlo --cores 4 --iterations 10000`
2. a library that can be imported in a notebook

> [!CAUTION]
> The CLI requires a few more dependencies like `typer`

## Tooling setup (runs on each commit)
* [x] `uv self update` & `uv sync --group dev`
* [x] linting/format checking: `uv run ruff check`
* [x] auto-formatting: `uv run ruff format`
* [x] type checking: `uv run pyrefly check`
* [x] testing: `uv run pytest`
* [x] integrate into pre-commit `pre-commit run --all-files`
* [ ] use maturin framework to run MC via Rust
* [ ] build a GitHub actions pipeline to run prior to merge into `main` (and post to publish to PyPi)
* [ ] run tests in parallel
* [x] split between dev and prod dependencies: `uv add --group dev`
* [x] add a build system, hatchling in [pyproject.toml](pyproject.toml)
* [x] run a build `uv build`

## Checks
1. Check that the package can be installed: `uv run --with picarlo --no-project -- python -c "import picarlo"`

## Goal
1. [x] run from command-line (uvx)
2. [x] import lib into notebook (either via PyPi or from local dist)
3. [x] published module

## Useful stuff
1. Create docstrings via LLM
2. Create docs from docstrings
3. Calculate test coverage
4. Tracing
5. [server-sent event via starlette](https://github.com/sysid/sse-starlette)

## More interesting stuff
* parallelism, e.g. [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) (see prime number example)
* bulk python version testing through tox

## Release preparation
1. **Generate Changelog:** `make changelog` (requires [Conventional Commits](https://www.conventionalcommits.org/))
2. **Bump Version:** Update `pyproject.toml` and `Cargo.toml`
3. **Build:** `make build`
4. **Publish:** `make publish`

## Commit Convention
This project uses Conventional Commits to automate changelog generation.
* `feat: ...` for new features
* `fix: ...` for bug fixes
* `docs: ...` for documentation
* `perf: ...` for performance improvements

Example: `git commit -m "feat: add parallel processing support"`

# [vscode extensions](.vscode/extensions.json)
1. Ruff
2. TOML syntax highlighting
