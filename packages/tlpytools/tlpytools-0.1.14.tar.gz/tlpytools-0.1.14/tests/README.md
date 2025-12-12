# ORCA Orchestrator Tests

This directory contains comprehensive tests for the ORCA orchestrator.

## Test Structure

- `test_orca_unit.py` - Unit tests with mocks and fake data
- `test_orca_integration.py` - Integration tests with live execution
- `run_tests.py` - Test runner script
- `conftest.py` - Test configuration (for pytest if available)

## Test Categories

### Unit Tests
- Test individual components in isolation
- Use mocks and fake data
- Fast execution
- No external dependencies

### Integration Tests
- Test complete workflows end-to-end
- Use real configurations and live execution
- Test three main scenarios:
  1. Local testing mode (full run)
  2. Cloud production initialization
  3. Cloud production download and run

## Running Tests

### Using the Test Runner (Recommended)
```bash
# Run all tests
python orca/tests/run_tests.py

# Run only unit tests
python orca/tests/run_tests.py --type unit

# Run only integration tests
python orca/tests/run_tests.py --type integration
```

### Using unittest directly
```bash
# Run all tests
python -m unittest discover orca/tests

# Run specific test file
python -m unittest orca.tests.test_unit
python -m unittest orca.tests.test_integration
```

### Using pytest (if installed)
```bash
# Run all tests
pytest orca/tests/

# Run only unit tests
pytest orca/tests/test_orca_unit.py

# Run only integration tests
pytest orca/tests/test_orca_integration.py

# Run with markers
pytest -m unit
pytest -m integration
```

## Test Requirements

### Unit Tests
- No external dependencies
- Python standard library only

### Integration Tests
- Requires write access to temporary directories
- May require network access for cloud operations (but handles failures gracefully)
- Uses real ORCA configuration files

## Expected Test Duration

- Unit tests: < 30 seconds
- Integration tests: 2-5 minutes (depends on system performance)

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're running tests from the correct directory
2. **Permission errors**: Ensure write access to temporary directories
3. **Network errors**: Cloud operations may fail in test environment (this is expected)

### Test Data

Integration tests create temporary directories and clean up automatically.
To preserve test data for inspection, comment out the `shutil.rmtree()` calls
in the test teardown methods.

## Test Coverage

The tests cover:
- Logger initialization and singleton behavior
- State management and persistence
- Databank operations (zipping, copying, cleanup)
- File synchronization (with mocked cloud operations)
- Complete orchestrator workflows
- Error handling and recovery
- Configuration loading and validation
