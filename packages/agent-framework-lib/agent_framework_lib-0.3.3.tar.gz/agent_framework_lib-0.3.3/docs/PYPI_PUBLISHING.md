# PyPI Publishing Guide for Agent Framework

This guide provides step-by-step instructions for publishing the Agent Framework to PyPI.

## Prerequisites

### 1. Install Required Tools

```bash
# Install build tools
pip install build twine

# Or using uv (recommended)
uv add --dev build twine
```

### 2. PyPI Account Setup

1. Create accounts on:

   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)
2. Set up API tokens:

   - Go to Account Settings → API tokens
   - Create a token with "Entire account" scope
   - Save the token securely

### 3. Configure Authentication

Create or update `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
```

## Pre-Publishing Checklist

### 1. Version Management

Update version in `pyproject.toml`:

```toml
[project]
version = "0.1.0"  # Update this before each release
```

### 2. Update Documentation

- [ ] Update `CHANGELOG.md` with new changes
- [ ] Ensure `README.md` is up to date
- [ ] Verify all documentation links work
- [ ] Update version references if needed

### 3. Code Quality

```bash
# Run tests
uv run pytest

# Check code formatting
uv run black --check agent_framework/

# Run type checking (optional)
uv run mypy agent_framework/

# Check for security issues (optional)
pip install safety
safety check
```

### 4. Dependency Verification

```bash
# Check dependencies
pip-audit  # Install with: uv add pip-audit

# Verify package builds correctly
uv run python -m build --check
```

## Building the Package

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 2. Build the Package

```bash
# Build source distribution and wheel
uv run python -m build

# This creates:
# - dist/agent-framework-lib-X.X.X.tar.gz (source distribution)
# - dist/agent_framework_lib-X.X.X-py3-none-any.whl (wheel)
```

### 3. Verify Build Contents

```bash
# Check what's included in the package
tar -tzf dist/agent-framework-lib-*.tar.gz

# Or for wheel
unzip -l dist/agent_framework_lib-*.whl
```

## Testing the Package

### 1. Test on TestPyPI

```bash
# Upload to TestPyPI first
uv run twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ agent-framework-lib
```

### 2. Test Local Installation

```bash
# Install from local build
uv add dist/agent_framework_lib-*.whl

# Test basic functionality
python -c "from agent_framework import AgentInterface, create_basic_agent_server; print('Import successful')"
```

### 3. Test in Clean Environment

```bash
# Create clean virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install and test
uv add agent-framework-lib
python -c "
from agent_framework import AgentInterface, StructuredAgentInput, StructuredAgentOutput

class TestAgent(AgentInterface):
    async def get_metadata(self):
        return {'name': 'Test Agent'}
  
    async def handle_message(self, session_id, agent_input):
        return StructuredAgentOutput(response_text='Hello World')
  
    async def get_state(self):
        return {}
  
    async def load_state(self, state):
        pass

print('Basic functionality test passed')
"

# Clean up
deactivate
rm -rf test_env
```

## Publishing to PyPI

### 1. Final Checks

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version number is correct
- [ ] CHANGELOG.md is updated
- [ ] No sensitive information in code

### 2. Upload to PyPI

```bash
# Upload to production PyPI
uv run twine upload dist/*

# Or upload specific files
uv run twine upload dist/agent-framework-lib-0.1.0.tar.gz dist/agent_framework_lib-0.1.0-py3-none-any.whl
```

### 3. Verify Upload

- Check the package page: https://pypi.org/project/agent-framework-lib/
- Test installation: `uv add agent-framework-lib`
- Verify metadata and description display correctly

## Post-Publishing

### 1. Tag the Release

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 2. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v0.1.0`
4. Title: `Agent Framework v0.1.0`
5. Copy relevant section from CHANGELOG.md
6. Attach build artifacts (optional)

### 3. Update Documentation

- Update installation instructions
- Add release announcement
- Update example code if needed

## Version Management Strategy

### Semantic Versioning

- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Workflow

1. **Development**: Work on `main` branch
2. **Pre-release**: Create release branch `release/v0.1.0`
3. **Testing**: Test thoroughly on TestPyPI
4. **Release**: Merge to `main`, tag, and publish
5. **Post-release**: Update version for next development cycle

## Troubleshooting

### Common Issues

1. **Import Errors**: Check `__init__.py` files and package structure
2. **Missing Files**: Verify MANIFEST.in includes all necessary files
3. **Dependency Conflicts**: Use `--force-reinstall` during testing
4. **Upload Errors**: Check API token and network connectivity

### Debug Commands

```bash
# Check package metadata
uv run python setup.py check --metadata

# Validate package structure
twine check dist/*

# Test import without installation
PYTHONPATH=. python -c "import agent_framework; print('OK')"
```

### Rolling Back

```bash
# Delete a release (use with caution)
# Note: PyPI doesn't allow re-uploading the same version
uv add pkginfo
python -c "
import pkginfo
info = pkginfo.get_metadata('dist/agent-framework-lib-0.1.0.tar.gz')
print(f'Would publish: {info.name} {info.version}')
"
```

## Security Considerations

- Never commit API tokens to version control
- Use environment variables for sensitive data
- Regularly rotate PyPI tokens
- Enable 2FA on PyPI accounts
- Review dependencies for security vulnerabilities

## Automation (Future)

Consider setting up GitHub Actions for automated publishing:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: uv add build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

---

For questions or issues with publishing, refer to:

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Setuptools Documentation](https://setuptools.readthedocs.io/)
