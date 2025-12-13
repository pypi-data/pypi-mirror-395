# scikit-lite

⚠️ **PRE-ALPHA** - This package is in very early development. APIs will change.

A simple machine learning library built for educational purposes.

## Installation

For users:

```bash
pip install scikit-lite
```

## Development Installation

### Prerequisites
- Python >= 3.11
- Rust and Cargo (install from https://rustup.rs)
- uv (install with `pip install uv`)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kowanietz/scikit-lite.git
   cd scikit-lite
   ```

2. Install dependencies and build Rust extensions:
   ```bash
   uv sync --extra dev
   uv run maturin develop
   ```

3. Verify installation:
   ```bash
   python -c "import sklite; print(sklite.rust_health_check())"
   ```


## Development Workflow

### Rebuilding After Changes

When you modify Rust code in `src/`:
```bash
# Quick rebuild (debug mode)
uv run maturin develop

# Optimized rebuild (release mode, slower build but faster runtime)
uv run maturin develop --release
```

### Code Quality
```bash
# Install pre-commit hooks (one-time setup)
uv run pre-commit install

# Run all checks manually
uv run pre-commit run --all-files
```

## Publishing to PyPI

### Prerequisites

1. Ensure versions match in both:
   - `pyproject.toml`: `version = "x.y.z"`
   - `Cargo.toml`: `version = "x.y.z"`

2. Set PyPI token:
   ```bash
   export MATURIN_PYPI_TOKEN="your-pypi-token"
   ```

### Publish

```bash
# Build and publish in one command
uv run maturin publish --release
```

Maturin will automatically:
- Build optimized wheels for your platform
- Upload to PyPI

TODO: Migrate release workflow to GitHub Actions for multiplatform builds.

## Contributing

This project is in early development. Contributions are welcome but please note the API is unstable.

## License

MIT License - See LICENSE file for details.

## Acknowledgments

Inspired by scikit-learn's excellent API design and educational resources.
