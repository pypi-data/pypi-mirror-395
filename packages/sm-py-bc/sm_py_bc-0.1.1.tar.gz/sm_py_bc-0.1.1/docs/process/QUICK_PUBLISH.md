# Quick Publishing Guide

## One-Time Setup (5 minutes)

1. **Install tools**:
   ```bash
   pip install build twine
   ```

2. **Get PyPI token**:
   - Visit: https://pypi.org/manage/account/token/
   - Create new token (scope: entire account or this project)
   - Copy token (starts with `pypi-`)

3. **Configure credentials** (Windows):
   ```bash
   # Create file: %USERPROFILE%\.pypirc
   notepad %USERPROFILE%\.pypirc
   ```
   
   Paste this:
   ```ini
   [distutils]
   index-servers =
       pypi
   
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```

## Publish in 3 Commands

```bash
# 1. Build package
cd D:\code\sm-bc\sm-py-bc
python -m build

# 2. Check package
twine check dist/*

# 3. Upload to PyPI
twine upload dist/*
```

## Verify Installation

```bash
# Install from PyPI
pip install sm-py-bc

# Test import
python -c "from sm_bc.crypto.digests import SM3Digest; print('Success!')"
```

## Done! 🎉

Your package is now live at: **https://pypi.org/project/sm-py-bc/**

Anyone can install it with: `pip install sm-py-bc`

---

## Test First (Optional)

Upload to Test PyPI before production:

```bash
# Upload to test
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ sm-py-bc
```

## Next Steps

- Create Git tag: `git tag v0.1.0 && git push origin v0.1.0`
- Create GitHub release with dist files
- Share on social media / forums

## Troubleshooting

**"Package already exists"** → Edit version in `pyproject.toml`, rebuild
**"Authentication failed"** → Check `.pypirc` token, verify account email
**Import error** → Ensure `src/sm_bc/` structure is correct
