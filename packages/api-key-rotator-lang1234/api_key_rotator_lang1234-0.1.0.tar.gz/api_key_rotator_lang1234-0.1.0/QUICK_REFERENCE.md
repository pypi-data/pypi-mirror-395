# Quick Reference - PyPI Publishing Commands

## Authentication Options

**Two ways to publish**:
1. **API Tokens** (manual uploads) - See steps below
2. **Trusted Publishing** (automated via GitHub) - See `PYPI_AUTH_OPTIONS.md`

PyPI **DOES support API tokens** - they're still the standard for manual uploads!

---

## One-Time Setup (API Token Method)

### 1. Install Tools
```powershell
pip install --upgrade pip build twine
```

### 2. Update Package Info
Edit these files and replace placeholder information:
- `setup.py` - lines 11-13 (author, email, url)
- `pyproject.toml` - lines 12-16 (author, email)
- `api_key_rotator/__init__.py` - line 9 (author)

### 3. Create PyPI Accounts
- PyPI: https://pypi.org/account/register/
- TestPyPI: https://test.pypi.org/account/register/
- Enable 2FA on both

### 4. Generate API Tokens ✅ This Still Works!
- PyPI: **Account Settings** → **API tokens** → **"Add API token"**
- TestPyPI: Same process on test.pypi.org
- Token format: `pypi-AgEIcHlwaS5vcmcC...`
- Save tokens securely!

### 5. Configure Credentials
Create `C:\Users\Ly\.pypirc`:
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

---

## Publishing Workflow

### Build the Package
```powershell
cd E:\Repos\KeyRotatorPython
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
python -m build
```

### Test on TestPyPI (Recommended)
```powershell
# Upload
twine upload --repository testpypi dist/*

# Verify at: https://test.pypi.org/project/api-key-rotator/

# Test install
pip install --index-url https://test.pypi.org/simple/ api-key-rotator
```

### Publish to PyPI
```powershell
twine upload dist/*
```

### Verify Publication
- Visit: https://pypi.org/project/api-key-rotator/
- Test install: `pip install api-key-rotator`

---

## Updating to New Version

### 1. Update Version Numbers
Edit ALL three files:
- `setup.py` → `version="0.1.1"`
- `pyproject.toml` → `version = "0.1.1"`
- `api_key_rotator/__init__.py` → `__version__ = "0.1.1"`

### 2. Update Changelog
Add to `README.md`:
```markdown
### 0.1.1 (YYYY-MM-DD)
- Bug fix: Description of fix
- New feature: Description
```

### 3. Rebuild and Republish
```powershell
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
python -m build
twine upload dist/*
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `403 Forbidden` | Regenerate API token, update `.pypirc` |
| `File already exists` | Increment version number (can't reuse versions) |
| Import errors | Check `__init__.py` exports |
| README not rendering | Verify `long_description_content_type="text/markdown"` |

---

## Quick Test Locally
```powershell
# Run examples
python examples.py

# Interactive test
python
>>> from api_key_rotator import KeyRotator
>>> rotator = KeyRotator(['key1', 'key2'])
>>> rotator.get_key()
```

---

## Helpful Links
- **PyPI Package**: https://pypi.org/project/api-key-rotator/ (after publishing)
- **TestPyPI**: https://test.pypi.org/project/api-key-rotator/
- **Full Guide**: See `PUBLISHING_GUIDE.md` for detailed instructions

---

**Note**: You can only upload each version once. If you make a mistake, increment the version and republish.
