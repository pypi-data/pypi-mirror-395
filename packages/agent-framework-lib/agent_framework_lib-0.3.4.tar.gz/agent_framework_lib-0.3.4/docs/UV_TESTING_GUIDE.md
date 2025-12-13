# UV-Based Testing Guide for Agent Framework

This guide explains how to use UV for testing the Agent Framework, providing fast, reliable, and consistent test execution across different environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Test Types](#test-types)
- [Running Tests](#running-tests)
- [Development Workflow](#development-workflow)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Installing UV

UV is a fast Python package installer and resolver. Install it using one of these methods:

**Unix/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip:**
```bash
uv add uv
```

**Using Homebrew (macOS):**
```bash
brew install uv
```

### Verify Installation

```bash
uv --version
```

## Quick Start

1. **Install test dependencies:**
   ```bash
   uv sync --group test
   ```

2. **Run all tests:**
   ```bash
   uv run pytest
   ```

3. **Run tests with coverage:**
   ```bash
   uv run pytest --cov=agent_framework --cov-report=html
   ```

## Test Types

The Agent Framework uses pytest markers to categorize tests:

### Available Test Markers

- `unit` - Fast, isolated unit tests
- `integration` - Tests that involve multiple components
- `performance` - Benchmark and performance tests
- `multimodal` - Tests requiring multimodal AI capabilities
- `storage` - Tests involving file storage backends
- `slow` - Tests that take longer to execute

### Test Categories

| Category | Description | Typical Runtime |
|----------|-------------|-----------------|
| Unit | Individual component tests | < 1 second each |
| Integration | Multi-component workflows | 1-5 seconds each |
| Performance | Benchmarks and load tests | 5-30 seconds each |
| Multimodal | AI vision/audio processing | 10-60 seconds each |
| Storage | File system operations | 1-10 seconds each |

## Running Tests

### Using UV Commands

#### Basic Test Execution
```bash
# Run all tests
uv run pytest

# Run specific test types
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m "not slow"

# Run tests with coverage
uv run pytest --cov=agent_framework --cov-report=html --cov-report=term

# Run tests in parallel
uv run pytest -n auto

# Run specific test file
uv run pytest tests/test_file_storage.py

# Run specific test function
uv run pytest tests/test_file_storage.py::test_store_file
```

#### Advanced Options
```bash
# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x

# Show local variables in tracebacks
uv run pytest -l

# Run only failed tests from last run
uv run pytest --lf

# Run tests matching pattern
uv run pytest -k "test_storage"
```

### Using Test Scripts

#### Shell Script (Unix/macOS)
```bash
# Make executable (first time only)
chmod +x scripts/test.sh

# Run different test types
./scripts/test.sh unit
./scripts/test.sh integration
./scripts/test.sh coverage
./scripts/test.sh fast
./scripts/test.sh all
```

#### Batch Script (Windows)
```cmd
scripts\test.bat unit
scripts\test.bat integration
scripts\test.bat coverage
scripts\test.bat all
```

#### Python Test Runner
```bash
# Basic usage
python scripts/test_runner.py unit
python scripts/test_runner.py coverage

# With additional options
python scripts/test_runner.py all --verbose --fail-fast

# Install dependencies and run tests
python scripts/test_runner.py --install-deps unit

# Run linting and tests
python scripts/test_runner.py --lint unit
```

### Using Makefile

```bash
# Install dependencies
make install

# Run different test types
make test
make test-unit
make test-integration
make test-coverage
make test-fast
make test-parallel

# Code quality
make lint
make format
make type-check

# Full CI pipeline
make test-ci

# Quick development check
make test-quick
```

## Development Workflow

### Recommended Development Cycle

1. **Setup (once per project):**
   ```bash
   make dev-setup
   # or
   uv sync --group test
   ```

2. **Before coding:**
   ```bash
   make test-fast
   # or
   uv run pytest -m "not slow"
   ```

3. **During development:**
   ```bash
   # Run tests for specific module
   uv run pytest tests/test_your_module.py -v
   
   # Run tests with file watching (if using pytest-watch)
   uv run ptw tests/test_your_module.py
   ```

4. **Before committing:**
   ```bash
   make lint test-coverage
   # or
   python scripts/test_runner.py --lint coverage
   ```

5. **Full validation:**
   ```bash
   make test-ci
   ```

### Test-Driven Development (TDD)

1. **Write failing test:**
   ```bash
   uv run pytest tests/test_new_feature.py::test_new_function -v
   ```

2. **Implement feature:**
   ```python
   # Write minimal code to pass test
   ```

3. **Run test again:**
   ```bash
   uv run pytest tests/test_new_feature.py::test_new_function -v
   ```

4. **Refactor and repeat**

### Performance Testing

```bash
# Run performance tests with benchmarks
uv run pytest -m performance --benchmark-only

# Compare performance over time
uv run pytest -m performance --benchmark-compare

# Save benchmark results
uv run pytest -m performance --benchmark-save=baseline
```

## Continuous Integration

### GitHub Actions

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/uv-tests.yml`) that:

- Tests across multiple Python versions (3.10-3.13)
- Tests on multiple operating systems (Ubuntu, Windows, macOS)
- Runs different test categories in parallel
- Generates coverage reports
- Runs performance benchmarks
- Tests multimodal capabilities

### Local CI Simulation

```bash
# Run the same checks as CI
make test-ci

# Or step by step
make clean
make install
make lint
make test-coverage
```

## Configuration

### pyproject.toml

The project's `pyproject.toml` includes comprehensive test configuration:

```toml
[tool.pytest.ini_options]
# Test discovery and execution
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Coverage settings
addopts = [
    "--cov=agent_framework",
    "--cov-report=html:htmlcov",
    "--cov-report=term-missing",
    "--cov-report=xml",
]

# Test markers
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "performance: marks tests as performance tests",
    "multimodal: marks tests that require multimodal capabilities",
    "storage: marks tests that require storage backends",
]
```

### UV Dependencies

Test dependencies are managed in dependency groups:

```toml
[dependency-groups]
test = [
    "pytest>=8.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.10.0",
    "pytest-cov>=6.2.1",
    "pytest-benchmark>=4.0.0",
    "pytest-xdist>=3.3.0",
    "coverage>=7.0.0",
]
```

## Environment Variables

### Test Configuration

```bash
# MongoDB for storage tests
export MONGODB_URL="mongodb://localhost:27017/test_db"

# OpenAI for multimodal tests
export OPENAI_API_KEY="your-api-key"

# Storage backend configuration
export DEFAULT_STORAGE_BACKEND="local"
export S3_BUCKET_NAME="test-bucket"
```

### Coverage Settings

```bash
# Coverage configuration
export COVERAGE_CORE="sysmon"  # For better performance
```

## Troubleshooting

### Common Issues

#### UV Not Found
```bash
# Error: command not found: uv
# Solution: Install UV or add to PATH
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal
```

#### Dependencies Not Installing
```bash
# Error: Failed to resolve dependencies
# Solution: Clear cache and reinstall
uv cache clean
uv sync --group test
```

#### Tests Failing Due to Missing Dependencies
```bash
# Error: ModuleNotFoundError
# Solution: Install all dependency groups
uv sync --all-groups
```

#### Permission Errors (Windows)
```cmd
# Error: Permission denied
# Solution: Run as administrator or use PowerShell
powershell -Command "& {scripts\test.bat unit}"
```

### Performance Issues

#### Slow Test Execution
```bash
# Use parallel execution
uv run pytest -n auto

# Skip slow tests during development
uv run pytest -m "not slow"

# Run only fast unit tests
uv run pytest -m unit
```

#### Memory Issues
```bash
# Limit parallel workers
uv run pytest -n 2

# Run tests sequentially
uv run pytest -n 0
```

### Debugging Tests

#### Verbose Output
```bash
uv run pytest -v -s tests/test_specific.py
```

#### Debug Mode
```bash
uv run pytest --pdb tests/test_specific.py
```

#### Logging
```bash
uv run pytest --log-cli-level=DEBUG tests/test_specific.py
```

## Best Practices

### Writing Tests

1. **Use descriptive test names:**
   ```python
   def test_file_storage_stores_file_with_correct_metadata():
       pass
   ```

2. **Use appropriate markers:**
   ```python
   @pytest.mark.unit
   def test_fast_unit_test():
       pass
   
   @pytest.mark.integration
   @pytest.mark.slow
   def test_complex_workflow():
       pass
   ```

3. **Use fixtures for setup:**
   ```python
   @pytest.fixture
   async def file_storage():
       storage = LocalFileStorage()
       yield storage
       await storage.cleanup()
   ```

### Running Tests Efficiently

1. **During development:**
   ```bash
   # Fast feedback loop
   uv run pytest -m unit -x
   ```

2. **Before commits:**
   ```bash
   # Comprehensive check
   make test-coverage
   ```

3. **For CI/CD:**
   ```bash
   # Full validation
   make test-ci
   ```

### Test Organization

- Keep unit tests fast (< 1 second each)
- Mark slow tests appropriately
- Use integration tests for workflows
- Separate performance tests
- Mock external dependencies in unit tests

## Examples

### Running Specific Test Scenarios

```bash
# Test file storage functionality
uv run pytest -m storage -v

# Test multimodal features (requires API keys)
uv run pytest -m multimodal -v

# Test performance with benchmarks
uv run pytest -m performance --benchmark-only

# Test everything except slow tests
uv run pytest -m "not slow" --cov=agent_framework

# Test with specific Python version
uv run --python 3.11 pytest

# Test with environment variables
MONGODB_URL=mongodb://localhost:27017/test uv run pytest -m storage
```

### Development Workflow Example

```bash
# 1. Start development session
make dev-setup

# 2. Run quick tests to ensure baseline
make test-fast

# 3. Develop feature with TDD
uv run pytest tests/test_new_feature.py::test_specific_function -v

# 4. Run related tests
uv run pytest tests/test_new_feature.py -v

# 5. Run full test suite before commit
make test-coverage

# 6. Check code quality
make lint

# 7. Final validation
make test-ci
```

This guide provides comprehensive coverage of UV-based testing for the Agent Framework. For additional help, refer to the [pytest documentation](https://docs.pytest.org/) and [UV documentation](https://docs.astral.sh/uv/).