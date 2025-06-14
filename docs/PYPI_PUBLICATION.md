# PyPI Publication Guide for Yendoria

## 📦 Publishing to Python Package Index

### Prerequisites
1. Create PyPI account at https://pypi.org
2. Create TestPyPI account at https://test.pypi.org
3. Install twine: `pip install twine`

### Setup PyPI Token
```bash
# Create API token on PyPI
# Add to GitHub Secrets as PYPI_API_TOKEN
```

### Test Publication (TestPyPI)
```bash
# Upload to test repository
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-test-token-here
poetry publish --repository testpypi

# Test installation
pip install --index-url https://test.pypi.org/simple/ yendoria
```

### Production Publication
```bash
# Upload to production PyPI
poetry config pypi-token.pypi your-token-here
poetry publish

# Users can then install with:
pip install yendoria
```

### Automated PyPI Release
Update `.github/workflows/release.yml`:

```yaml
- name: Publish to PyPI
  if: steps.release.conclusion == 'success'
  env:
    POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    poetry publish
```

### Benefits of PyPI
- **Easy Installation**: `pip install yendoria`
- **Dependency Management**: Automatic dependency resolution
- **Version Management**: Users can specify versions
- **Global Availability**: Accessible worldwide
- **Package Discovery**: Listed in PyPI search

### Considerations
- **Name Availability**: Check if 'yendoria' is available
- **Licensing**: Ensure proper license specification
- **Documentation**: Include proper README for PyPI page
- **Security**: Use API tokens, not passwords
