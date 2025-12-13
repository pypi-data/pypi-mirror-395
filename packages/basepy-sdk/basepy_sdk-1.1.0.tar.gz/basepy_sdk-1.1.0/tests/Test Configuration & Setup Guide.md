# Test Configuration & Setup Guide

## Overview

This guide explains how to set up and run the comprehensive test suite for BaseClient before deployment.

## Prerequisites

### Required Packages

```bash
pip install pytest pytest-cov pytest-benchmark pytest-mock
```

### Optional Packages

```bash
pip install pytest-xdist  # Parallel test execution
pip install pytest-timeout  # Test timeouts
pip install coverage[toml]  # Coverage configuration
```

## Test Structure

```
tests/
├── __init__.py
├── test_client.py           # Main test suite
├── test_wallet.py           # Wallet tests (if applicable)
├── conftest.py              # Shared fixtures
├── pytest.ini               # Pytest configuration
└── .coveragerc              # Coverage configuration
```

## Running Tests

### 1. Quick Smoke Tests (30 seconds)

Run basic sanity checks:

```bash
python -m pytest tests/test_client.py -v -m smoke
```

Or use the helper:

```bash
python tests/test_client.py --smoke
```

**Expected output:**
```
tests/test_client.py::TestSmoke::test_smoke_connection PASSED
tests/test_client.py::TestSmoke::test_smoke_get_block PASSED
tests/test_client.py::TestSmoke::test_smoke_get_balance PASSED
tests/test_client.py::TestSmoke::test_smoke_estimate_fee PASSED

==================== 4 passed in 2.45s ====================
```

### 2. Pre-Deployment Tests (2 minutes)

Critical tests that MUST pass before deployment:

```bash
python tests/test_client.py --deploy
```

**Expected output:**
```
============================================================
✅ ALL PRE-DEPLOYMENT TESTS PASSED
============================================================

You are clear to deploy!
```

### 3. Full Test Suite (5-10 minutes)

Run all tests with coverage:

```bash
python -m pytest tests/test_client.py -v --cov=basepy --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### 4. Specific Test Categories

Run tests by category:

```bash
# Network tests only
pytest tests/test_client.py -v -k "test_network"

# Account tests only
pytest tests/test_client.py -v -k "test_account"

# Performance tests only
pytest tests/test_client.py -v -k "test_performance"

# Error handling tests
pytest tests/test_client.py -v -k "test_error"
```

### 5. Parallel Execution

Speed up tests with parallel execution:

```bash
pytest tests/test_client.py -n auto
```

## Test Configuration Files

### pytest.ini

Create `pytest.ini` in project root:

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Markers
markers =
    smoke: Quick smoke tests
    integration: Integration tests with real RPC
    unit: Unit tests with mocks
    slow: Slow-running tests
    benchmark: Performance benchmarks

# Timeout
timeout = 300

# Coverage
[coverage:run]
source = basepy
omit = 
    */tests/*
    */examples/*
    */setup.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### .coveragerc

Create `.coveragerc` for coverage configuration:

```ini
[run]
source = basepy
omit =
    */tests/*
    */examples/*
    */setup.py
    */__pycache__/*

[report]
precision = 2
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### conftest.py

Create `tests/conftest.py` for shared fixtures:

```python
"""
Shared test fixtures and configuration
"""

import pytest
from basepy import BaseClient, Config
from basepy.utils import BASE_MAINNET_CHAIN_ID, BASE_SEPOLIA_CHAIN_ID


@pytest.fixture(scope="session")
def mainnet_client():
    """Shared mainnet client for all tests"""
    return BaseClient(chain_id=BASE_MAINNET_CHAIN_ID)


@pytest.fixture(scope="session")
def testnet_client():
    """Shared testnet client for all tests"""
    return BaseClient(chain_id=BASE_SEPOLIA_CHAIN_ID)


@pytest.fixture
def test_config():
    """Test configuration with reduced limits"""
    config = Config()
    config.MAX_RETRIES = 2
    config.CACHE_TTL = 1
    config.RATE_LIMIT_REQUESTS = 10
    return config


@pytest.fixture(autouse=True)
def reset_client_state(mainnet_client):
    """Reset client state before each test"""
    mainnet_client.clear_cache()
    mainnet_client.reset_metrics()
    yield
    # Cleanup after test
    mainnet_client.clear_cache()


@pytest.fixture
def test_addresses():
    """Common test addresses"""
    return {
        'usdc': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        'dai': '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb',
        'whale': '0x20FE51A9229EEf2cF8Ad9E89d91CAb9312cF3b7A',
        'zero': '0x0000000000000000000000000000000000000000',
    }


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for basic functionality"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests with real RPC calls"
    )
    config.addinivalue_line(
        "markers", "unit: Unit tests with mocked dependencies"
    )
```

## Test Coverage Goals

### Minimum Acceptable Coverage

- **Overall:** 80%+
- **client.py:** 90%+
- **Critical paths:** 100%

### Check Coverage

```bash
# Generate coverage report
pytest --cov=basepy --cov-report=term-missing

# View detailed HTML report
pytest --cov=basepy --cov-report=html
open htmlcov/index.html
```

## Continuous Integration (CI/CD)

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-benchmark
    
    - name: Run smoke tests
      run: |
        pytest tests/test_client.py -v -m smoke
    
    - name: Run full test suite
      run: |
        pytest tests/test_client.py -v --cov=basepy --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  pre-deploy:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run pre-deployment tests
      run: |
        python tests/test_client.py --deploy
```

## Pre-Deployment Checklist

Before deploying to production, ensure:

### 1. All Tests Pass

```bash
# Run pre-deployment tests
python tests/test_client.py --deploy
```

**Must see:**
```
✅ ALL PRE-DEPLOYMENT TESTS PASSED
```

### 2. Coverage Meets Threshold

```bash
pytest --cov=basepy --cov-report=term --cov-fail-under=80
```

**Must see:**
```
Required test coverage of 80% reached.
```

### 3. No Critical Issues

```bash
# Check for critical test failures
pytest tests/test_client.py -v -x
```

**Must complete without failures.**

### 4. Performance Benchmarks

```bash
pytest tests/test_client.py -v -k benchmark
```

**Verify benchmarks are within acceptable ranges.**

### 5. Manual Verification

Test key features manually:

```python
from basepy import BaseClient

client = BaseClient()

# 1. Connection
assert client.is_connected()

# 2. Basic operations
assert client.get_block_number() > 0

# 3. Base L2 features
tx = {
    'to': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    'from': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    'value': 0,
    'data': '0x'
}
cost = client.estimate_total_fee(tx)
assert 'total_fee' in cost

# 4. Health check
health = client.health_check()
assert health['status'] == 'healthy'

print("✅ Manual verification passed!")
```

## Troubleshooting Tests

### Problem: Tests fail with "Connection refused"

**Solution:**
- Check internet connectivity
- Verify RPC endpoints are accessible
- Try different RPC provider

```python
# Test RPC connectivity
import requests
response = requests.get('https://mainnet.base.org')
print(response.status_code)  # Should be 200
```

### Problem: Tests are too slow

**Solutions:**

1. Run smoke tests only:
```bash
pytest -m smoke
```

2. Use parallel execution:
```bash
pytest -n auto
```

3. Skip integration tests:
```bash
pytest -m "not integration"
```

### Problem: Random test failures

**Possible causes:**
- Network instability
- RPC rate limiting
- Race conditions

**Solutions:**

1. Increase timeouts in pytest.ini:
```ini
[pytest]
timeout = 600
```

2. Add retry decorator to flaky tests:
```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_flaky_operation():
    # Test code
    pass
```

3. Mock external dependencies:
```python
@patch('basepy.client.Web3')
def test_with_mock(mock_w3):
    # Test with mocked Web3
    pass
```

### Problem: Coverage too low

**Solutions:**

1. Identify uncovered code:
```bash
pytest --cov=basepy --cov-report=term-missing
```

2. Add tests for uncovered lines

3. Check if uncovered code is testable:
   - Error handlers
   - Edge cases
   - Utility functions

## Test Maintenance

### Weekly Tasks

- [ ] Run full test suite
- [ ] Review and update test data (addresses, contracts)
- [ ] Check for deprecated RPC endpoints

### Before Each Release

- [ ] Run pre-deployment tests
- [ ] Verify coverage ≥ 80%
- [ ] Update test fixtures if needed
- [ ] Review and update benchmarks

### Monthly Tasks

- [ ] Review test performance
- [ ] Update test dependencies
- [ ] Cleanup obsolete tests
- [ ] Add tests for new features

## Best Practices

### 1. Test Naming

```python
# ✅ Good - clear what is tested
def test_get_balance_returns_integer():
    pass

def test_get_balance_raises_error_for_invalid_address():
    pass

# ❌ Bad - unclear
def test_balance():
    pass
```

### 2. Test Independence

```python
# ✅ Good - each test is independent
def test_feature_a():
    client = BaseClient()
    result = client.method_a()
    assert result == expected

def test_feature_b():
    client = BaseClient()
    result = client.method_b()
    assert result == expected

# ❌ Bad - tests depend on each other
def test_setup():
    global client
    client = BaseClient()

def test_feature():
    # Depends on test_setup
    result = client.method()
```

### 3. Use Fixtures

```python
# ✅ Good - use fixtures
@pytest.fixture
def client():
    return BaseClient()

def test_with_fixture(client):
    result = client.get_block_number()
    assert isinstance(result, int)
```

### 4. Clear Assertions

```python
# ✅ Good - clear assertion message
assert balance > 0, f"Expected positive balance, got {balance}"

# ❌ Bad - no context on failure
assert balance > 0
```

## Resources

- **Pytest Documentation:** https://docs.pytest.org/
- **Coverage.py:** https://coverage.readthedocs.io/
- **Base Documentation:** https://docs.base.org/
- **Web3.py Testing:** https://web3py.readthedocs.io/en/stable/testing.html

## Summary

### Quick Commands

```bash
# Development workflow
pytest -m smoke              # Quick check
pytest -v                    # Full tests
pytest --cov                 # With coverage

# Before deployment
python tests/test_client.py --deploy

# CI/CD
pytest --cov --cov-report=xml  # For coverage upload
```

### Success Criteria

✅ All smoke tests pass  
✅ All pre-deployment tests pass  
✅ Coverage ≥ 80%  
✅ No critical test failures  
✅ Benchmarks within acceptable ranges  

**When all criteria are met → Deploy with confidence! 🚀**