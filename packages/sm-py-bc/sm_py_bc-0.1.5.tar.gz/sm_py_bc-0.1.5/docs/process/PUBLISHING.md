# Publishing sm-py-bc to PyPI

## Prerequisites

1. **Install build tools**:
   ```bash
   pip install build twine
   ```

2. **Create PyPI account**:
   - Main PyPI: https://pypi.org/account/register/
   - Test PyPI (optional): https://test.pypi.org/account/register/

3. **Generate API Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Save it securely (you won't see it again)

4. **Configure credentials**:
   ```bash
   # Create .pypirc in your home directory
   # Windows: %USERPROFILE%\.pypirc
   # Linux/Mac: ~/.pypirc
   
   # Use .pypirc.example as template
   ```

## Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:
- `dist/sm-py-bc-0.1.0.tar.gz` (source distribution)
- `dist/sm_py_bc-0.1.0-py3-none-any.whl` (wheel)

## Validate Package

```bash
# Check package metadata
twine check dist/*

# Optionally test installation locally
pip install dist/sm-py-bc-0.1.0.tar.gz
```

## Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ sm-py-bc
```

## Publish to PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# Verify it's available
pip install sm-py-bc
```

## Post-Publication

1. **Create Git tag**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create GitHub release**:
   - Go to GitHub repository
   - Create release from tag
   - Attach distribution files

3. **Update version**:
   - Edit `pyproject.toml`
   - Increment version number
   - Commit changes

## Troubleshooting

### Package name already exists
If `sm-py-bc` is taken:
1. Edit `pyproject.toml` → `name = "sm-py-bc-alt"`
2. Rebuild and retry

### Authentication failed
- Check `.pypirc` format
- Verify API token is correct
- Use `--verbose` flag: `twine upload --verbose dist/*`

### Import issues after install
- Ensure `src/sm_bc` structure is correct
- Check `__init__.py` files exist
- Verify `pyproject.toml` package discovery

## Version Management

Following semantic versioning:
- `0.1.0` - Initial beta release
- `0.2.0` - Minor features/improvements
- `1.0.0` - Stable production release
- `1.0.1` - Bug fixes

Update in `pyproject.toml`:
```toml
version = "0.2.0"
```

## CI/CD Automation (Future)

Consider automating with GitHub Actions:
```yaml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```
