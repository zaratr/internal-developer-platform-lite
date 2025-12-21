# Testing Strategy

## Overview
IDP-Lite employs a multi-layered testing strategy to ensure platform reliability and service quality.

## Test Layers

### 1. Unit Tests
**Location**: `tests/test_*.py`

**Coverage**:
- Template generation logic
- Configuration providers
- CLI argument parsing

**Run**: `pytest tests/test_template_generation.py tests/test_config_provider.py`

### 2. Integration Tests
**Location**: `tests/test_api_integration.py`, `tests/test_generated_services.py`

**Coverage**:
- Control Plane API endpoints
- Service creation via API
- Generated service structure validation
- Prometheus metrics presence

**Run**: `pytest tests/test_api_integration.py tests/test_generated_services.py`

### 3. End-to-End Tests
**Location**: `tests/test_e2e_workflow.py`

**Coverage**:
- Complete service creation workflow (CLI → Files)
- FastAPI service generation and validation
- Spring Boot service generation and validation
- AI enhancement feature
- Template placeholder replacement

**Run**: `pytest tests/test_e2e_workflow.py -v`

## Running All Tests
```bash
# Install test dependencies
pip install pytest httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=platform --cov-report=html

# Run specific test file
pytest tests/test_e2e_workflow.py -v
```

## CI/CD Integration
Tests run automatically in GitHub Actions on every push:
- Linting (ruff)
- Unit tests
- Integration tests
- E2E tests (in isolated temp directories)

## Test Philosophy
1. **Fast Feedback**: Unit tests run in milliseconds
2. **Realistic**: Integration tests use actual API client
3. **Isolated**: E2E tests use temporary directories
4. **Comprehensive**: Cover happy paths and error cases

## Future Enhancements
- Add contract tests for API versioning
- Add performance benchmarks for service generation
- Add browser tests for React Dashboard (Playwright)
- Add mutation testing for critical paths
