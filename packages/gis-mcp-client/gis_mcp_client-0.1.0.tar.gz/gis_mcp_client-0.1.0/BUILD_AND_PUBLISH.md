# Building and Publishing to PyPI

This guide will walk you through building the `gis-mcp-client` package and publishing it to PyPI.

## Prerequisites

1. **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
2. **PyPI Account** - Create one at [pypi.org](https://pypi.org/account/register/)
3. **API Token** - Generate at [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)

## Step 1: Install Python (if not already installed)

### Windows:

1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```powershell
   python --version
   pip --version
   ```

## Step 2: Set Up Build Environment

### Create a virtual environment (recommended):

```powershell
# Navigate to project directory
cd D:\projects\gis-mcp-client

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
# venv\Scripts\activate.bat
```

### Install build tools:

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install build tools
pip install build twine
```

## Step 3: Update Version (if needed)

Before building, update the version in:

- `pyproject.toml` - Update the `version` field
- `src/gis_mcp_client/__init__.py` - Update `__version__`

For example, to release version 0.1.1:

- In `pyproject.toml`: `version = "0.1.1"`
- In `src/gis_mcp_client/__init__.py`: `__version__ = "0.1.1"`

## Step 4: Build the Package

### Clean previous builds (optional):

```powershell
# Remove old build artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
```

### Build the package:

```powershell
# Build source distribution and wheel
python -m build
```

This will create:

- `dist/gis-mcp-client-0.1.0.tar.gz` (source distribution)
- `dist/gis-mcp-client-0.1.0-py3-none-any.whl` (wheel)

### Verify the build:

```powershell
# Check the built files
ls dist
```

## Step 5: Test the Build Locally (Optional but Recommended)

### Install the package locally:

```powershell
# Install from the built wheel
pip install dist/gis_mcp_client-*.whl

# Or install in editable mode for development
pip install -e .
```

### Test import:

```powershell
python -c "from gis_mcp_client import GISMCPClient, RemoteStorage; print('Import successful!')"
```

## Step 6: Upload to TestPyPI (Recommended First Step)

TestPyPI is a testing version of PyPI. Always test here first!

### Upload to TestPyPI:

```powershell
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:

- **Username**: `__token__`
- **Password**: Your TestPyPI API token (starts with `pypi-`)

Get TestPyPI token at: [test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)

### Test installation from TestPyPI:

```powershell
# Create a new virtual environment for testing
python -m venv test-env
.\test-env\Scripts\Activate.ps1

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ gis-mcp-client
```

## Step 7: Upload to PyPI

Once you've verified the package works on TestPyPI:

### Upload to Production PyPI:

```powershell
# Upload to PyPI
python -m twine upload dist/*
```

You'll be prompted for:

- **Username**: `__token__`
- **Password**: Your PyPI API token (starts with `pypi-`)

**Important**: Once uploaded to PyPI, you cannot delete or modify a version. Only new versions can be uploaded.

## Step 8: Verify on PyPI

1. Visit: https://pypi.org/project/gis-mcp-client/
2. Verify the package details are correct
3. Test installation:
   ```powershell
   pip install gis-mcp-client
   ```

## Troubleshooting

### Common Issues:

1. **"python is not recognized"**

   - Python is not in PATH. Reinstall Python with "Add to PATH" checked.

2. **"ModuleNotFoundError: No module named 'build'"**

   - Install build tools: `pip install build twine`

3. **"HTTPError: 400 Bad Request"**

   - Version already exists on PyPI. Increment version number.

4. **"HTTPError: 401 Unauthorized"**

   - Invalid API token. Check token at pypi.org/manage/account/token/

5. **"File already exists"**
   - Version already published. Use a new version number.

### Build Errors:

- Ensure `pyproject.toml` is valid
- Check that all required files exist (README.md, LICENSE)
- Verify package structure matches `[tool.hatch.build.targets.wheel]` in pyproject.toml

## Quick Reference Commands

```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip build twine

# Build
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Clean build artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
```

## Next Steps After Publishing

1. **Tag the release in Git:**

   ```powershell
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Update version for next release** in both files

3. **Create a GitHub release** (if using GitHub)

## Security Notes

- **Never commit** your PyPI API tokens
- Use environment variables or token files for automation
- Keep your API tokens secure and rotate them regularly
