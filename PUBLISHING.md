# Publishing to PyPI

This guide explains how to publish `llm-guardrails` to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org)
2. **API Token**: Generate an API token in your PyPI account settings
3. **Build Tools**: Install build and twine
   ```bash
   pip install build twine
   ```

## Publishing Steps

### 1. Prepare Your Environment

Create a `.pypirc` file in your home directory (`~/.pypirc`) for authentication:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
```

Or use environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
```

### 2. Build the Package

```bash
python -m build
```

This creates:
- `dist/llm-guardrails-0.3.17.tar.gz` (source distribution)
- `dist/llm_guardrails-0.3.17-py3-none-any.whl` (wheel)

### 3. Verify the Build (Optional)

```bash
twine check dist/*
```

### 4. Upload to PyPI

**Test PyPI (Recommended First):**
```bash
twine upload --repository testpypi dist/*
```

**Production PyPI:**
```bash
twine upload dist/*
```

### 5. Verify Upload

```bash
pip install llm-guardrails
```

Check the package on PyPI: https://pypi.org/project/llm-guardrails/

## Troubleshooting

### Invalid Distribution Error
- Ensure all filenames are valid
- Run `twine check dist/*` before uploading

### Authentication Failed
- Verify your API token is correct
- Check `.pypirc` formatting
- Try using environment variables instead

### Version Already Exists
- PyPI doesn't allow re-uploading the same version
- Update version in `pyproject.toml` and rebuild

## Automating with GitHub Actions

To automate publishing on git tags, create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

Then add your PyPI API token as a GitHub secret: `PYPI_API_TOKEN`

## After Publishing

1. Verify on PyPI: https://pypi.org/project/llm-guardrails/
2. Create a GitHub Release with release notes
3. Update documentation if needed
4. Announce on social media/forums

## Package Information

- **Package Name**: `llm-guardrails`
- **Repository**: https://github.com/Nikhilsinghbora/llm-guardrails
- **Author**: Nikhil Singh Bora (nikhilsinghbora17@gmail.com)
- **Original Project**: https://github.com/protectai/llm-guard
