# Release Checklist for sm-py-bc

## Pre-Release Preparation

- [x] ✅ Update `pyproject.toml` with PyPI metadata
- [x] ✅ Add LICENSE file (MIT)
- [x] ✅ Create MANIFEST.in for package files
- [x] ✅ Update README.md as main documentation
- [x] ✅ Create PUBLISHING.md guide
- [x] ✅ Build package successfully
- [x] ✅ Validate with `twine check`

## Before Publishing

- [ ] Run full test suite
  ```bash
  pytest tests/unit/
  ```

- [ ] Verify version number in `pyproject.toml`
  - Current: `0.1.0` (beta release)
  - Format: `MAJOR.MINOR.PATCH`

- [ ] Update README.md if needed
  - Installation instructions
  - Usage examples
  - API documentation links

- [ ] Check all URLs in pyproject.toml
  - Update GitHub username/organization
  - Verify repository exists and is public

## Publishing Steps

### 1. Test on Test PyPI (Optional but Recommended)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install and test
pip install --index-url https://test.pypi.org/simple/ sm-py-bc
python -c "from sm_bc.crypto.digests import SM3Digest; print('Import OK')"
```

### 2. Publish to PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# Verify installation
pip install sm-py-bc
python -c "from sm_bc.crypto.digests import SM3Digest; print('Package published!')"
```

### 3. Create Git Tag

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 4. Create GitHub Release

1. Go to: https://github.com/yourusername/sm-py-bc/releases/new
2. Select tag: `v0.1.0`
3. Release title: `v0.1.0 - Initial Beta Release`
4. Description:
   ```markdown
   ## 🎉 First Beta Release

   ### Features
   - Complete SM2/SM3/SM4 implementations
   - 183 passing unit tests
   - Zero external dependencies
   - Pure Python implementation

   ### Installation
   ```bash
   pip install sm-py-bc
   ```

   ### Quick Start
   See [README.md](README.md) for examples.
   ```
5. Attach files: `dist/sm_py_bc-0.1.0.tar.gz` and `dist/sm_py_bc-0.1.0-py3-none-any.whl`
6. Publish release

## Post-Release

- [ ] Announce on relevant channels
  - GitHub Discussions
  - Python cryptography communities
  - Chinese crypto forums

- [ ] Monitor PyPI downloads
  - https://pypi.org/project/sm-py-bc/

- [ ] Watch for issues
  - GitHub Issues
  - Installation problems
  - Bug reports

## Version Planning

### Next Releases

- **v0.2.0** - Performance improvements, additional features
- **v0.3.0** - GCM mode completion, key exchange finalization
- **v1.0.0** - Production stable release

### Version Bump Process

1. Edit `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Update CHANGELOG.md (create if needed)

3. Commit and tag:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.2.0"
   git tag v0.2.0
   git push origin main v0.2.0
   ```

4. Rebuild and republish:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   twine upload dist/*
   ```

## Troubleshooting

### Package name taken
- Try alternative: `sm-bc-py`, `pysm-bc`, `sm-crypto-py`
- Update in `pyproject.toml` → `name`

### Upload fails
- Check API token in `~/.pypirc`
- Verify account email is confirmed
- Try `--verbose` flag for details

### Import errors after install
- Check package structure in wheel:
  ```bash
  unzip -l dist/sm_py_bc-*.whl
  ```
- Verify `src/sm_bc/__init__.py` exists
- Test in clean virtualenv

## Resources

- **PyPI Project**: https://pypi.org/project/sm-py-bc/
- **Test PyPI**: https://test.pypi.org/project/sm-py-bc/
- **PyPI Help**: https://pypi.org/help/
- **Packaging Guide**: https://packaging.python.org/
