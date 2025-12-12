"""
Test configuration file for pytest.

This file configures pytest settings for the ORCA orchestrator test suite.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the orca directory to Python path for imports
current_dir = Path(__file__).parent
orca_dir = current_dir.parent
sys.path.insert(0, str(orca_dir))


def pytest_configure(config):
    """Configure pytest."""
    # Add custom markers
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Mark unit tests
        if "test_unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)

        # Mark integration tests
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture to provide test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_workspace(tmp_path):
    """Fixture to provide a temporary workspace for tests."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace
