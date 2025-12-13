# PyPI Publishing Guide for myjaconv

This guide explains how to publish myjaconv to PyPI (Python Package Index).

## Prerequisites

### 1. PyPI Account

1. Create an account at https://pypi.org/account/register/
2. (Optional) Create a TestPyPI account at https://test.pypi.org/account/register/

### 2. API Token

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token with scope "Entire account" or project-specific
3. Save the token securely (it starts with `pypi-`)

### 3. Required Tools

```bash
# Install build tools
pip install build twine

# Or with uv
uv pip install build twine
```

## pyproject.toml Configuration

The current `pyproject.toml` needs additional metadata for PyPI:

```toml
[project]
name = "myjaconv"
version = "0.1.0"
description = "Japanese character converter extending jaconv with pydomino phoneme conversion"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["japanese", "converter", "hiragana", "katakana", "phoneme", "domino", "lyrics"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Text Processing :: Linguistic",
    "Natural Language :: Japanese",
]
dependencies = ["jaconv>=0.4.0"]

[project.urls]
Homepage = "https://github.com/yourusername/myjaconv"
Repository = "https://github.com/yourusername/myjaconv"
Documentation = "https://github.com/yourusername/myjaconv#readme"
Issues = "https://github.com/yourusername/myjaconv/issues"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["myjaconv"]
```

### Required Fields for PyPI

| Field | Description | Status |
|-------|-------------|--------|
| `name` | Package name | Required |
| `version` | Package version | Required |
| `description` | Short description | Required |
| `readme` | README file path | Recommended |
| `requires-python` | Python version requirement | Recommended |
| `license` | License type | Recommended |
| `authors` | Author information | Recommended |
| `classifiers` | PyPI classifiers | Recommended |
| `project.urls` | Project URLs | Recommended |

## Building the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build source distribution and wheel
python -m build

# Or with uv
uv run python -m build
```

This creates files in `dist/`:
- `myjaconv-0.1.0.tar.gz` (source distribution)
- `myjaconv-0.1.0-py3-none-any.whl` (wheel)

## Publishing

### Option 1: Publish to TestPyPI (Recommended for first time)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your TestPyPI API token>
```

Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ myjaconv
```

### Option 2: Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your PyPI API token>
```

### Using .pypirc for Authentication

Create `~/.pypirc` for easier authentication:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxx
```

**Important**: Set file permissions to protect your tokens:
```bash
chmod 600 ~/.pypirc
```

## Version Management

### Semantic Versioning

Follow semantic versioning (SemVer): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Update Checklist

1. Update version in `pyproject.toml`
2. Update version in `myjaconv/__init__.py` (if defined there)
3. Update CHANGELOG (if exists)
4. Commit changes
5. Create git tag: `git tag v0.1.0`
6. Push tag: `git push origin v0.1.0`

## GitHub Actions (Optional)

Create `.github/workflows/publish.yml` for automated publishing:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Add `PYPI_API_TOKEN` to repository secrets:
1. Go to repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`, Value: your PyPI API token

## Pre-publish Checklist

- [ ] All tests pass: `uv run pytest`
- [ ] Code is formatted: `uv run ruff format .`
- [ ] No lint errors: `uv run ruff check .`
- [ ] README is up to date
- [ ] Version is updated in pyproject.toml
- [ ] Version is updated in __init__.py
- [ ] LICENSE file exists
- [ ] pyproject.toml has all required metadata

## Common Issues

### 1. Package name already taken

If `myjaconv` is taken on PyPI, consider alternative names:
- `myjaconv-phoneme`
- `jaconv-domino`
- `pydomino-jaconv`

### 2. Version already exists

You cannot overwrite an existing version. Increment the version number.

### 3. README not rendering

- Ensure README.md is valid Markdown
- Check with: `python -m readme_renderer README.md`

### 4. Missing files in distribution

Check `MANIFEST.in` or `tool.hatch.build` configuration.

## Quick Commands Summary

```bash
# Build
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ myjaconv

# Install from PyPI
pip install myjaconv
```

## References

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Hatch Documentation](https://hatch.pypa.io/)
- [Twine Documentation](https://twine.readthedocs.io/)
