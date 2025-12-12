# TLPyTools Developer Guide

This guide provides information for developers contributing to and maintaining the TLPyTools package.

## Table of Contents

- [Development Setup](#development-setup)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Release Process](#release-process)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Contributing](#contributing)

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Quick Start with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/TransLinkForecasting/tlpytools.git
cd tlpytools

# Install uv if not already installed
pip install uv

# Set up development environment
make dev-setup

# Or manually:
uv sync --extra dev --extra orca --group activitysim
# Note: ActivitySim and PopulationSim are included via --group activitysim
```

More detailed installation instruction is available on [conda_env repository](https://github.com/TransLinkForecasting/conda_env?tab=readme-ov-file#installations).

### Manual Setup with pip

```bash
# Clone the repository
git clone https://github.com/TransLinkForecasting/tlpytools.git
cd tlpytools

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode (without ActivitySim - use uv for that)
pip install -e .[dev,orca]
```

### Development Dependencies

The development environment includes:

- **Testing**: pytest, pytest-cov
- **Code Quality**: black, ruff, mypy, pre-commit
- **Transportation Modeling**: ActivitySim, PopulationSim (via `activitysim` extra)
- **Geospatial**: geopandas, Shapely, Fiona, etc.
- **Visualization**: plotly, dash, panel, folium
- **Documentation**: jupyter, notebook

### Dependency Management with uv

TLPyTools uses `uv.lock` to ensure reproducible builds and consistent dependency versions across environments.

#### Updating Dependencies

```bash
# Update all dependencies to their latest compatible versions
uv lock --upgrade

# Sync the environment after updating the lockfile
uv sync --extra dev --extra orca --group activitysim
```

#### When to Update Dependencies

- **Regularly**: Update dependencies monthly or before major releases
- **Security**: Update immediately when security vulnerabilities are discovered
- **Features**: Update when you need new features from dependencies
- **Bug fixes**: Update when dependencies fix critical bugs

**Note**: Always test thoroughly after updating dependencies, especially before releases.

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test categories
uv run pytest tests/test_basic.py -v          # Core functionality
uv run pytest tests/test_orca_unit.py -v           # ORCA unit tests
uv run pytest tests/test_orca_integration.py -v    # ORCA integration tests

# Run with coverage
make test-cov
# Or manually:
uv run pytest --cov=tests --cov-report=html --cov-report=term
```

### Test Structure

- `tests/test_basic.py` - Core TLPyTools functionality tests
- `tests/test_orca_unit.py` - ORCA orchestrator unit tests
- `tests/test_orca_integration.py` - ORCA integration tests
- `tests/test_core.py` - Comprehensive core feature tests (requires additional dependencies)

### Writing Tests

When adding new features:

1. Add unit tests for individual functions/classes
2. Add integration tests for complex workflows
3. Ensure tests are isolated and don't depend on external services
4. Use mocking for external dependencies (ADLS, SQL Server, etc.)

## Code Quality

### Linting and Formatting

```bash
# Format code
make format
# Or manually:
uv run black src/ tests/
uv run ruff check src/ tests/ --fix

# Check code quality
make lint
# Or manually:
uv run black --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/

# Run all quality checks
make check-all
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run hooks manually
uv run pre-commit run --all-files
```

### Code Style Guidelines

- Follow PEP 8 (enforced by black)
- Use type hints where possible
- Write docstrings for public functions and classes
- Keep functions focused and modular
- Handle errors gracefully with appropriate logging

## Release Process

### Overview

TLPyTools uses a manual release process triggered through GitHub Actions. This ensures quality control and allows for proper testing before releases.

### Step-by-Step Release Process

#### 1. Prepare for Release

```bash
# Ensure you're on the main branch and up to date
git checkout main
git pull origin main

# Update dependencies to latest versions (optional, but recommended)
uv lock --upgrade
uv sync --extra dev --extra orca --group activitysim

# Run all tests locally
make test
make check-all

# Verify documentation is up to date
# Update CHANGELOG.md if you maintain one
```

#### 2. Trigger the Release Workflow

1. Go to the GitHub repository: https://github.com/TransLinkForecasting/tlpytools
2. Navigate to **Actions** tab
3. Select **"Deploy to PyPI"** workflow from the left sidebar
4. Click **"Run workflow"** button
5. Fill in the required information:
   - **Branch**: Select `main` (or your release branch)
   - **Version number**: Enter the new version (e.g., `0.1.14`)
   - **Is this a pre-release?**: Check if this is a pre-release version

#### 3. Monitor the Release

The workflow will automatically:

1. **Run Tests**: Execute the full test suite to ensure quality
2. **Update Version**: Update version numbers in `pyproject.toml` and `__init__.py`
3. **Build Package**: Create wheel and source distributions
4. **Deploy to PyPI**: Upload the package to PyPI
5. **Create GitHub Release**: Tag the release and create release notes

#### 4. Post-Release Verification

After the workflow completes:

```bash
# Verify the package is available on PyPI
pip install tlpytools==0.1.14  # Replace with your version

# Test installation in a fresh environment
python -c "import tlpytools; print(tlpytools.__version__)"
```

### Version Numbering

TLPyTools follows semantic versioning (SemVer):

- **Major** (x.0.0): Breaking changes
- **Minor** (0.x.0): New features, backwards compatible
- **Patch** (0.0.x): Bug fixes, backwards compatible

Examples:
- `0.1.7` → `0.1.8` (patch release)
- `0.1.8` → `0.2.0` (minor release)
- `0.2.0` → `1.0.0` (major release)

### Pre-releases

For testing purposes, you can create pre-release versions:

- `0.1.8-alpha.1`
- `0.1.8-beta.1`
- `0.1.8-rc.1`

Check the "Is this a pre-release?" option when running the workflow.

## GitHub Actions Workflows

### Test Workflow (`.github/workflows/test.yml`)

**Trigger**: Automatic on push/PR to main branches

**Purpose**: Ensures code quality and functionality

**Features**:
- Tests on multiple Python versions (3.10, 3.11, 3.12)
- Tests on both Ubuntu and Windows
- Runs core functionality tests
- Runs ORCA-specific tests
- Verifies package imports and installation

**Runs on**: Every commit and pull request

### Deploy Workflow (`.github/workflows/deploy.yml`)

**Trigger**: Manual workflow dispatch

**Purpose**: Releases new versions to PyPI

**Workflow Steps**:

1. **Test**: Run full test suite
2. **Update Version**: Automatically update version numbers
3. **Build**: Create distribution packages
4. **Deploy**: Upload to PyPI
5. **Release**: Create GitHub release with notes

**Required Secrets**:
- `PYPI_API_TOKEN`: PyPI API token for package upload

### Setting Up PyPI Deployment

#### For Repository Maintainers

1. **Create PyPI API Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with scope limited to the `tlpytools` project
   - Copy the token (starts with `pypi-`)

2. **Add Secret to GitHub**:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste the PyPI token

3. **Test with Test PyPI** (Optional):
   - Create token at https://test.pypi.org
   - Update workflow to use test PyPI temporarily
   - Test the release process

## Contributing

### Workflow for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch**: `git checkout -b feature/my-new-feature`
4. **Make your changes** and add tests
5. **Run tests and quality checks**: `make check-all`
6. **Commit your changes**: `git commit -am 'Add some feature'`
7. **Push to the branch**: `git push origin feature/my-new-feature`
8. **Create a Pull Request** on GitHub

### Pull Request Guidelines

- Include a clear description of the changes
- Add tests for new functionality
- Ensure all tests pass
- Update documentation if needed
- Follow the existing code style
- Link to any relevant issues

### Development Workflow

```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Test changes
make test
make lint

# Commit and push
git add .
git commit -m "Add my feature"
git push origin feature/my-feature

# Create PR on GitHub
```

## Troubleshooting

### Common Issues

#### GDAL Installation on Windows

GDAL can be problematic on Windows. If you encounter issues:

```bash
# Skip GDAL for development
uv sync --extra orca  # Skip dev extras with GDAL

# Or install from conda-forge
conda install -c conda-forge gdal
```

#### Test Failures

If tests fail locally:

```bash
# Run specific test with verbose output
uv run pytest tests/test_basic.py::TestBasicFunctionality::test_data_validation -v -s

# Check imports
uv run python -c "from tlpytools import data; print('OK')"

# Clean and reinstall
rm -rf .venv/
uv sync --extra orca
```

#### Package Import Issues

```bash
# Reinstall in development mode
uv pip install -e .

# Check Python path
uv run python -c "import sys; print(sys.path)"
```

#### Dependency Issues

```bash
# Update and sync dependencies
uv lock --upgrade
uv sync --extra dev --extra orca --group activitysim

# Check for dependency conflicts
uv pip check

# Reset virtual environment if needed
rm -rf .venv/
uv sync --extra dev --extra orca --group activitysim
```

### Getting Help

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/TransLinkForecasting/tlpytools/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/TransLinkForecasting/tlpytools/discussions) for questions
- **Email**: Contact the TransLink Forecasting Team at forecasting@translink.ca

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Semantic Versioning](https://semver.org/)

```bash
pip install tlpytools --upgrade
```

### Method 2: build from source

Build and install from source allow you to access the latest version or a specific version without any available precompiled wheels:

```bash
git clone https://github.com/TransLinkForecasting/tlpytools.git --depth=1
cd tlpytools
python -m pip install --upgrade build
python -m build
pip install dist/tlpytools-X.X.X-py3-none-any.whl --upgrade --force-reinstall
```

### Method 3: editable install for development

If you are developing and testing tlpytools to work with downstream code, you may install the package as an [editable install](https://pip.pypa.io/en/stable/cli/pip_install/?highlight=edit%20mode#editable-installs). This allows you to continuously make changes to the `tlpytools` package in your local development folder, while integrating these changes in real time with your downstream code.

```bash
git clone https://github.com/TransLinkForecasting/tlpytools.git --depth=1
cd tlpytools
pip install -e ./
```

Note that after this installation, any code changes you make within the `tlpytools` folder will take effect immeidately witin your development environment.

## Usage

After installation, you can access the `tlpytools` namespace within your data project and importing parts of the package in your python script:

```python
from tlpytools.log import logger
from tlpytools.config import run_yaml
```

## Build and Distribution Process

1. Review `pyproject.toml` to ensure dependencies and versions are up to date.
2. Generate distribution archives
```
conda activate base
python -m pip install --upgrade build
python -m build
```
3. Upload to PyPI
```
python -m pip install --upgrade twine
python -m twine upload dist/*
```
Review the newly upload package on `https://test.pypi.org/project/tlpytools/`

If you are having problem authenticating to PyPI, you should register on [PyPI](https://pypi.org/account/register/) and create a new token. Set up the token in `~/.pypirc` by following [package distribution guide](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#create-an-account)
