"""
Test runner script for TLPyTools test suite.

This script provides a simple way to run tests without requiring pytest.
Runs all tests in the tests directory by default.
"""

import unittest
import sys
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))


def run_unit_tests():
    """Run only ORCA unit tests."""
    print("Running ORCA unit tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(current_dir), pattern="test_orca_unit.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_integration_tests():
    """Run only ORCA integration tests."""
    print("Running ORCA integration tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(current_dir), pattern="test_orca_integration.py"
    )
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_core_tests():
    """Run core functionality tests."""
    print("Running core functionality tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(current_dir), pattern="test_basic.py")
    suite.addTests(loader.discover(start_dir=str(current_dir), pattern="test_core.py"))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_orca_tests():
    """Run all ORCA tests (unit + integration)."""
    print("Running all ORCA tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(current_dir), pattern="test_orca_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_all_tests():
    """Run all tests in the tests directory."""
    print("Running all tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(current_dir), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    """Main test runner function."""
    import argparse

    parser = argparse.ArgumentParser(description="TLPyTools test runner")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "core", "orca", "all"],
        default="all",
        help="Type of tests to run (default: all)",
    )

    args = parser.parse_args()

    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    elif args.type == "core":
        success = run_core_tests()
    elif args.type == "orca":
        success = run_orca_tests()
    else:
        success = run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
