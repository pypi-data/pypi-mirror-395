# Publishing to PyPI

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Create an API token at https://pypi.org/manage/account/token/
   - For production: Create a token with "Entire account" or project-specific scope
   - For TestPyPI: Create a token at https://test.pypi.org/manage/account/token/

## Publishing Steps

### 1. Build the package
```bash
uv build
```

This creates distribution files in the `dist/` directory.

### 2. Test on TestPyPI (recommended first)
```bash
# Set credentials (optional - uv will prompt if not set)
export UV_PUBLISH_USERNAME=__token__
export UV_PUBLISH_PASSWORD=your_testpypi_token_here

# Publish to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/
```

### 3. Test installation from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ hypertic
```

### 4. Publish to production PyPI
```bash
# Set credentials (optional - uv will prompt if not set)
export UV_PUBLISH_USERNAME=__token__
export UV_PUBLISH_PASSWORD=your_pypi_token_here

# Publish to production PyPI
uv publish
```

## Alternative: Using credentials file

You can also create a credentials file at `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your_pypi_token_here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your_testpypi_token_here
```

## Updating the package

1. Update the version in `pyproject.toml`
2. Build: `uv build`
3. Publish: `uv publish`

## Notes

- The package name `hypertic` must be unique on PyPI
- Once published, you cannot delete a package, only add new versions
- TestPyPI is a separate instance for testing - packages there don't affect production PyPI

