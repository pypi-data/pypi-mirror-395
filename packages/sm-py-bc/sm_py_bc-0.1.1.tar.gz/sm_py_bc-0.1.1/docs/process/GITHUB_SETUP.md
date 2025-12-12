# GitHub Setup Guide

## 📋 Prerequisites

1. **Install GitHub CLI**:
   ```bash
   # Windows (using winget)
   winget install GitHub.cli
   
   # Or download from: https://cli.github.com/
   ```

2. **Login to GitHub**:
   ```bash
   gh auth login
   ```
   Follow the prompts to authenticate.

## 🚀 Quick Setup (Using gh CLI)

### Option 1: Create New Repository

```bash
cd D:\code\sm-bc\sm-py-bc

# Initialize git if not already done
git init

# Create repository on GitHub
gh repo create sm-py-bc --public --source=. --description "SM2/SM3/SM4 implementation in Python based on Bouncy Castle"

# Add all files
git add .

# Commit
git commit -m "Initial commit: SM2/SM3/SM4 Python implementation"

# Push to GitHub
git push -u origin main
```

### Option 2: Push to Existing Repository

```bash
cd D:\code\sm-bc\sm-py-bc

# Initialize git
git init

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/sm-py-bc.git

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Push
git branch -M main
git push -u origin main
```

## 📝 Step-by-Step Manual Setup

### 1. Initialize Git Repository

```bash
cd D:\code\sm-bc\sm-py-bc
git init
```

### 2. Create Repository on GitHub

```bash
gh repo create sm-py-bc \
  --public \
  --description "SM2/SM3/SM4 cryptography library in pure Python" \
  --homepage "https://github.com/YOUR_USERNAME/sm-py-bc"
```

Or create manually:
1. Go to https://github.com/new
2. Name: `sm-py-bc`
3. Description: `SM2/SM3/SM4 implementation in Python based on Bouncy Castle`
4. Public
5. Don't initialize with README (we have one)
6. Create repository

### 3. Add Files and Commit

```bash
# Add all files
git add .

# Check status
git status

# Commit
git commit -m "Initial commit: Complete SM2/SM3/SM4 implementation

- SM2: Digital signatures, encryption/decryption, key exchange
- SM3: Cryptographic hash function
- SM4: Block cipher with CBC, CTR, OFB, CFB, GCM modes
- Pure Python implementation, zero dependencies
- 183+ unit tests
- PyPI ready with complete packaging"
```

### 4. Push to GitHub

```bash
# Add remote (if not done by gh repo create)
git remote add origin https://github.com/YOUR_USERNAME/sm-py-bc.git

# Push
git branch -M main
git push -u origin main
```

## ⚙️ Configure GitHub Actions

The workflows are already created in `.github/workflows/`:
- `ci.yml` - Run tests on every push
- `daily-full-test.yml` - Comprehensive daily tests
- `publish.yml` - Publish to PyPI

### Set Up Secrets

For publishing to PyPI, add secrets:

```bash
# Add PyPI API token
gh secret set PYPI_API_TOKEN

# Add Test PyPI token (optional)
gh secret set TEST_PYPI_API_TOKEN

# Add Codecov token (optional)
gh secret set CODECOV_TOKEN
```

Or manually:
1. Go to: https://github.com/YOUR_USERNAME/sm-py-bc/settings/secrets/actions
2. Click "New repository secret"
3. Add:
   - `PYPI_API_TOKEN`: Your PyPI token
   - `TEST_PYPI_API_TOKEN`: Your Test PyPI token

## 📦 Update PyPI URLs in pyproject.toml

Before publishing, update the URLs:

```bash
# Edit pyproject.toml
# Replace "yourusername" with your GitHub username
```

Or use sed:
```bash
sed -i 's/yourusername/YOUR_GITHUB_USERNAME/g' pyproject.toml
```

## ✅ Verify Setup

```bash
# Check remote
git remote -v

# Check GitHub repo
gh repo view

# Check Actions status
gh run list

# View repository in browser
gh repo view --web
```

## 🎯 Post-Setup Tasks

### 1. Configure Repository Settings

```bash
# Enable issues
gh repo edit --enable-issues

# Enable wiki
gh repo edit --enable-wiki

# Add topics
gh repo edit --add-topic python --add-topic cryptography \
  --add-topic sm2 --add-topic sm3 --add-topic sm4 \
  --add-topic chinese-crypto --add-topic gm-crypto
```

### 2. Create First Release

```bash
# Create and push tag
git tag -a v0.1.0 -m "Release v0.1.0 - Initial beta release"
git push origin v0.1.0

# Create GitHub release
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Beta Release" \
  --notes "First beta release with complete SM2/SM3/SM4 implementation" \
  dist/sm_py_bc-0.1.0.tar.gz \
  dist/sm_py_bc-0.1.0-py3-none-any.whl
```

### 3. Add Branch Protection (Optional)

```bash
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=build-and-test
```

## 🔄 Workflow Usage

### Trigger Manual Test

```bash
gh workflow run daily-full-test.yml
```

### Publish to Test PyPI

```bash
gh workflow run publish.yml -f repository=testpypi
```

### View Workflow Runs

```bash
gh run list
gh run view <run-id>
gh run watch
```

## 📊 Monitor CI Status

```bash
# Watch latest run
gh run watch

# View logs
gh run view --log

# Re-run failed jobs
gh run rerun <run-id>
```

## 🎨 Add Badges to README

Add these to the top of README.md:

```markdown
[![CI](https://github.com/YOUR_USERNAME/sm-py-bc/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/sm-py-bc/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/sm-py-bc.svg)](https://pypi.org/project/sm-py-bc/)
[![Python](https://img.shields.io/pypi/pyversions/sm-py-bc.svg)](https://pypi.org/project/sm-py-bc/)
[![License](https://img.shields.io/github/license/YOUR_USERNAME/sm-py-bc.svg)](LICENSE)
```

## 🐛 Troubleshooting

### gh command not found
```bash
# Verify installation
gh --version

# Re-login
gh auth logout
gh auth login
```

### Permission denied
```bash
# Check authentication
gh auth status

# Refresh token
gh auth refresh
```

### Push rejected
```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

## 📚 Resources

- **GitHub CLI Docs**: https://cli.github.com/manual/
- **GitHub Actions**: https://docs.github.com/en/actions
- **PyPI Publishing**: https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

## 🎉 Quick Command Reference

```bash
# Create repo and push
gh repo create sm-py-bc --public --source=. && git push -u origin main

# Add secrets
gh secret set PYPI_API_TOKEN

# Create release
gh release create v0.1.0 dist/*

# View repo
gh repo view --web

# Check CI status
gh run list --limit 5
```

---

**Ready to publish!** 🚀
