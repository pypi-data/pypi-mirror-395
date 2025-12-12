# GitHub Actions Deployment Setup (Trusted Publishers)

This repository uses GitHub Actions with PyPI Trusted Publishers for secure, token-free deployment.

## Workflow

- **Develop Branch** → Publishes to [TestPyPI](https://test.pypi.org/)
- **Main Branch** → Publishes to [PyPI](https://pypi.org/)

## Setup Instructions

### 1. Configure Trusted Publisher on PyPI

**For Production PyPI:**
1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name:** `funsize-engineer`
   - **Owner:** `JessicaRudd`
   - **Repository name:** `funsize-engineer`
   - **Workflow name:** `publish.yml`
   - **Environment name:** (leave blank)
4. Click "Add"

**For TestPyPI:**
1. Go to https://test.pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in the same information as above
4. Click "Add"

### 2. Create Develop Branch

```bash
git checkout -b develop
git push -u origin develop
```

### 3. Deployment Process

**To deploy to TestPyPI:**
```bash
git checkout develop
# Make your changes
git add .
git commit -m "Your changes"
git push origin develop
```

**To deploy to Production PyPI:**
```bash
git checkout main
git merge develop
git push origin main
```

Or create a Pull Request from `develop` to `main` and merge it.

## How Trusted Publishers Work

- **No API tokens needed!** 🎉
- GitHub Actions authenticates using OpenID Connect (OIDC)
- More secure than static API tokens
- Automatically rotates credentials
- PyPI verifies the workflow is running from your authorized repository

## Testing the Package

**From TestPyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ funsize-engineer
```

**From PyPI:**
```bash
pip install funsize-engineer
```

## Notes

- The workflow automatically builds and uploads the package
- No secrets or tokens to manage in GitHub
- Each push to `develop` or `main` triggers a deployment

- The first deployment will create the project on PyPI/TestPyPI automatically
