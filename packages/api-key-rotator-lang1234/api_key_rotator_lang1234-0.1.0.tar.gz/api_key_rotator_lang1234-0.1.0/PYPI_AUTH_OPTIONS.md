# PyPI Authentication Options

PyPI supports **two main authentication methods** for publishing packages. Here's when to use each:

## Option 1: API Tokens (Manual Publishing) ✅ Still Supported

**Best for**: Manual uploads from your local machine using `twine`

### How to Get API Tokens

1. **Create PyPI Account**: https://pypi.org/account/register/
2. **Go to Account Settings**: https://pypi.org/manage/account/
3. **Click "API tokens"** in the left sidebar
4. **Click "Add API token"**
5. **Fill in details**:
   - Token name: `api-key-rotator-upload`
   - Scope: "Entire account" (for first upload) or specific project (for updates)
6. **Copy the token** (starts with `pypi-AgE...`)

### Using API Tokens

**Create `.pypirc` file** at `C:\Users\Ly\.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC... (your actual token here)

[testpypi]
username = __token__
password = pypi-AgE... (your TestPyPI token here)
repository = https://test.pypi.org/legacy/
```

**Upload with twine**:
```powershell
python -m build
twine upload dist/*
```

⚠️ **Security**: Never commit `.pypirc` to version control!

---

## Option 2: Trusted Publishing (Automated via GitHub Actions) ⭐ Recommended

**Best for**: Automated publishing from GitHub releases (no tokens needed!)

**Benefits**:
✅ More secure (no long-lived tokens)  
✅ No secrets to manage  
✅ Automatic publishing on release  
✅ Recommended by PyPI  

### Setup Steps

#### 1. Create GitHub Repository

```powershell
cd E:\Repos\KeyRotatorPython
git init
git add .
git commit -m "Initial commit: API Key Rotator package"
gh repo create api-key-rotator --public --source=. --push
```

Or create manually at: https://github.com/new

#### 2. Configure Trusted Publisher on PyPI

1. **Go to PyPI**: https://pypi.org/manage/account/publishing/
2. **Click "Add a new pending publisher"**
3. **Fill in the form** (based on your screenshot):
   - **PyPI Project Name**: `api-key-rotator` (must match your package name)
   - **Owner**: Your GitHub username (e.g., `YourGitHubUsername`)
   - **Repository name**: `api-key-rotator` (your GitHub repo name)
   - **Workflow name**: `publish.yml` (the filename in .github/workflows/)
   - **Environment name**: `pypi` (optional, but recommended)
4. **Click "Add"**

#### 3. Create GitHub Actions Workflow

Create `.github/workflows/publish.yml` in your repository:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  pypi-publish:
    name: Upload release to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/api-key-rotator
    permissions:
      id-token: write  # IMPORTANT: this permission is mandatory for trusted publishing
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      
      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

#### 4. Create GitHub Environment (Optional but Recommended)

1. Go to your repo: **Settings** → **Environments**
2. Click **New environment**
3. Name: `pypi`
4. Add protection rules (optional):
   - Required reviewers
   - Wait timer
   - Deployment branches

#### 5. Create a Release to Publish

```powershell
# Tag your release
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Create release on GitHub (or use web interface)
gh release create v0.1.0 --title "v0.1.0" --notes "Initial release"
```

Or create manually at: `https://github.com/YourUsername/api-key-rotator/releases/new`

The workflow will automatically:
1. Build your package
2. Publish to PyPI using trusted publishing
3. No tokens needed!

---

## Comparison

| Feature | API Tokens | Trusted Publishing |
|---------|------------|-------------------|
| **Setup Complexity** | Easy | Moderate |
| **Use Case** | Manual uploads | Automated releases |
| **Security** | Good (rotate tokens) | Excellent (no secrets) |
| **Requires GitHub** | No | Yes |
| **Token Management** | Manual | None |
| **Revocation** | Manual | Automatic |
| **PyPI Recommendation** | ✅ Supported | ⭐ Recommended |

---

## Recommended Workflow

**For your first publication**:
1. Use **API Tokens** for initial testing on TestPyPI
2. Use **API Tokens** for first upload to PyPI (to create the project)
3. Set up **Trusted Publishing** for future updates

**Steps**:

```powershell
# 1. First upload with token (manual)
python -m build
twine upload dist/*  # Uses .pypirc

# 2. Set up GitHub repo
git init
git add .
git commit -m "Initial commit"
gh repo create api-key-rotator --public --source=. --push

# 3. Configure Trusted Publisher on PyPI
# (Follow steps in Option 2, section 2)

# 4. Create workflow file
# Create .github/workflows/publish.yml (see above)

# 5. Future releases are automatic
git tag v0.1.1 -m "Bug fix release"
git push origin v0.1.1
gh release create v0.1.1 --title "v0.1.1" --notes "Bug fixes"
# Package automatically publishes to PyPI!
```

---

## Quick Commands Reference

### Manual Publishing (API Token)
```powershell
python -m build
twine upload dist/*
```

### Automated Publishing (Trusted Publishing)
```powershell
git tag v0.1.1 -m "Release notes"
git push origin v0.1.1
gh release create v0.1.1 --title "v0.1.1" --notes "Release notes"
```

---

## FAQs

**Q: Do I need both methods?**  
A: No, choose one. API tokens for manual control, Trusted Publishing for automation.

**Q: Can I use Trusted Publishing without GitHub?**  
A: PyPI also supports GitLab, Google, and ActiveState (see tabs in your screenshot).

**Q: What if I don't want automation?**  
A: Use API tokens and upload manually with `twine`.

**Q: Is my current .pypirc file still valid?**  
A: Yes! API tokens still work perfectly for manual uploads.

**Q: Which should I use?**  
A: Start with API tokens for simplicity. Upgrade to Trusted Publishing once you have a GitHub repo and want automation.

---

## Your Screenshot Explained

The screen you shared is for setting up **Trusted Publishing** via **GitHub Actions**. This is:
- ✅ More secure than tokens (recommended by PyPI)
- ✅ Great for automated releases
- ⚠️ Requires a GitHub repository first
- ⚠️ Requires creating a GitHub Actions workflow

**You can still use API tokens** if you prefer manual uploads or don't want GitHub automation.
