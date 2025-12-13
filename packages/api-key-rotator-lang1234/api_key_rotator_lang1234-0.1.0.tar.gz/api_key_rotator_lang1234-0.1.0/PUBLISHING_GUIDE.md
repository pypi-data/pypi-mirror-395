# PyPI Publishing Guide for api-key-rotator

Complete step-by-step guide to publish your package to PyPI.

## Prerequisites

Before publishing, ensure you have:
- [x] Completed package code and documentation
- [ ] A PyPI account (https://pypi.org/account/register/)
- [ ] A TestPyPI account (https://test.pypi.org/account/register/)
- [ ] Python 3.7+ installed
- [ ] Git repository (optional but recommended)

## Step 1: Set Up PyPI Accounts

### 1.1 Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Fill in your details and verify your email
3. Enable two-factor authentication (recommended)

### 1.2 Create TestPyPI Account
1. Go to https://test.pypi.org/account/register/
2. This is a separate account from PyPI (for testing)
3. Verify your email

## Step 2: Generate API Tokens

### 2.1 PyPI Token
1. Log in to https://pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name: `api-key-rotator-upload`
5. Scope: "Entire account" (for first upload) or "Project: api-key-rotator" (for updates)
6. **IMPORTANT**: Copy the token immediately - you won't see it again!
7. Token format: `pypi-AgE...`

### 2.2 TestPyPI Token
1. Log in to https://test.pypi.org
2. Repeat the same process as above
3. Name: `api-key-rotator-test-upload`

## Step 3: Install Build Tools

Open your terminal and run:

```powershell
# Install build tools
pip install --upgrade pip
pip install --upgrade build twine
```

**What these do:**
- `build`: Creates distribution packages (wheel and source)
- `twine`: Uploads packages to PyPI securely

## Step 4: Configure PyPI Credentials

Create a `.pypirc` file in your home directory:

**Windows Location:** `C:\Users\YourUsername\.pypirc`

```powershell
# Create the .pypirc file
New-Item -Path "$env:USERPROFILE\.pypirc" -ItemType File -Force
notepad "$env:USERPROFILE\.pypirc"
```

**Content of `.pypirc`:**
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgE... (your actual PyPI token)

[testpypi]
username = __token__
password = pypi-AgE... (your actual TestPyPI token)
repository = https://test.pypi.org/legacy/
```

**⚠️ IMPORTANT**: Never commit `.pypirc` to version control! It contains sensitive credentials.

## Step 5: Prepare Your Package

### 5.1 Update Package Information

Before publishing, update these files:

**`setup.py` and `pyproject.toml`:**
- Change `author` from "Your Name" to your actual name
- Change `author_email` to your email
- Update `url` with your GitHub repository URL
- Verify the version number (0.1.0 for first release)

**`api_key_rotator/__init__.py`:**
- Update `__author__` with your name

### 5.2 Verify Package Structure

Your directory should look like this:
```
api-key-rotator/
├── api_key_rotator/
│   ├── __init__.py
│   └── rotator.py
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Step 6: Build the Package

Navigate to your project directory and build:

```powershell
# Navigate to project directory
cd E:\Repos\KeyRotatorPython

# Clean previous builds (if any)
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build the package
python -m build
```

**Expected output:**
```
Successfully built api-key-rotator-0.1.0.tar.gz and api_key_rotator-0.1.0-py3-none-any.whl
```

This creates two files in the `dist/` directory:
- `.tar.gz` - Source distribution
- `.whl` - Wheel distribution (recommended format)

## Step 7: Test on TestPyPI First

**IMPORTANT**: Always test on TestPyPI before uploading to real PyPI!

```powershell
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

**Verify on TestPyPI:**
1. Go to https://test.pypi.org/project/api-key-rotator/
2. Check that your package appears correctly
3. Verify the README renders properly
4. Check all metadata

**Test Installation from TestPyPI:**
```powershell
# Create a test virtual environment
python -m venv test_env
.\test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ api-key-rotator

# Test the package
python -c "from api_key_rotator import KeyRotator; print('Success!')"

# Deactivate and clean up
deactivate
Remove-Item -Recurse -Force test_env
```

## Step 8: Upload to Real PyPI

Once you've verified everything works on TestPyPI:

```powershell
# Upload to PyPI
twine upload dist/*
```

**You'll see:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading api_key_rotator-0.1.0-py3-none-any.whl
Uploading api-key-rotator-0.1.0.tar.gz
```

## Step 9: Verify Publication

1. Visit: https://pypi.org/project/api-key-rotator/
2. Your package should be live!
3. Test installation:

```powershell
pip install api-key-rotator
```

## Step 10: Post-Publication

### 10.1 Tag the Release in Git (if using Git)
```powershell
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 10.2 Create GitHub Release (if using GitHub)
1. Go to your repository
2. Click "Releases" → "Create a new release"
3. Choose tag v0.1.0
4. Title: "Version 0.1.0"
5. Add release notes from your changelog

## Updating the Package (Future Versions)

When you need to release a new version:

### 1. Update Version Number
Update in ALL these files:
- `setup.py` - `version="0.1.1"`
- `pyproject.toml` - `version = "0.1.1"`
- `api_key_rotator/__init__.py` - `__version__ = "0.1.1"`
- `README.md` - Add to changelog

### 2. Build and Upload
```powershell
# Clean old builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build new version
python -m build

# Upload to PyPI (skip TestPyPI for minor updates if you want)
twine upload dist/*
```

**Note**: You can only upload each version once. If you make a mistake, you must increment the version number.

## Versioning Best Practices

Follow Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`

- **MAJOR** (1.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.1.0): New features, backwards-compatible
- **PATCH** (0.0.1): Bug fixes, backwards-compatible

Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.1` → `0.2.0`: New feature added
- `0.9.0` → `1.0.0`: First stable release
- `1.5.0` → `2.0.0`: Breaking API change

## Common Issues and Troubleshooting

### Issue: "HTTPError: 403 Forbidden"
**Solution**: Your API token is invalid or expired. Generate a new one.

### Issue: "File already exists"
**Solution**: You're trying to upload a version that already exists. Increment your version number.

### Issue: "Invalid distribution filename"
**Solution**: Ensure your package name in `setup.py` matches the expected format (lowercase, hyphens).

### Issue: README not rendering on PyPI
**Solution**: Ensure `long_description_content_type="text/markdown"` is set in `setup.py`.

### Issue: "Package name too similar to existing package"
**Solution**: Choose a more unique package name.

### Issue: Import errors after installation
**Solution**: Ensure your `__init__.py` properly exports the classes/functions.

## Security Best Practices

1. **Never commit credentials**: Add `.pypirc` to `.gitignore`
2. **Use API tokens**: Never use username/password
3. **Scope tokens appropriately**: Use project-scoped tokens when possible
4. **Rotate tokens regularly**: Generate new tokens periodically
5. **Enable 2FA**: On your PyPI account
6. **Review before publishing**: Always test on TestPyPI first

## Optional: Automate with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
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

**Setup:**
1. Go to your GitHub repository settings
2. Secrets and variables → Actions → New repository secret
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI API token
5. When you create a GitHub release, it will automatically publish to PyPI

## Quick Reference Commands

```powershell
# Install tools
pip install --upgrade build twine

# Build package
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ api-key-rotator

# Install from PyPI
pip install api-key-rotator

# Clean build artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info
```

## Useful Links

- PyPI: https://pypi.org
- TestPyPI: https://test.pypi.org
- Python Packaging Guide: https://packaging.python.org
- Twine Documentation: https://twine.readthedocs.io
- Semantic Versioning: https://semver.org

---

**Congratulations!** 🎉 Your package is now published and available for anyone to install with `pip install api-key-rotator`.
