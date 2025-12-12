"""
Simplified tests for core TLPyTools functionality.
Tests only basic functionality without heavy dependencies.
"""

import unittest
import tempfile
import shutil
import os
import json
import yaml
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch

# Import core modules
from tlpytools import data, config, log
from tlpytools.data_store import DataStore


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of core modules."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

        # Create test dataframes
        self.test_df = pd.DataFrame(
            {
                "zone_id": [1, 2, 3, 4, 5],
                "households": [100, 200, 150, 300, 75],
                "population": [250, 500, 375, 750, 187],
                "area_type": ["urban", "suburban", "urban", "rural", "suburban"],
            }
        )

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_data_validation(self):
        """Test dataframe validation."""
        # Valid case
        result = data.validate_dataframe(self.test_df, ["zone_id", "households"])
        self.assertTrue(result)

        # Missing columns
        result = data.validate_dataframe(self.test_df, ["zone_id", "missing_col"])
        self.assertFalse(result)

        # Empty dataframe
        empty_df = pd.DataFrame()
        result = data.validate_dataframe(empty_df, ["zone_id"])
        self.assertFalse(result)

    def test_config_loading(self):
        """Test configuration loading."""
        # Create test config
        test_config = {
            "database": {"host": "localhost", "port": 5432},
            "model": {"iterations": 10},
        }

        config_file = os.path.join(self.test_dir, "test_config.yaml")
        with open(config_file, "w") as f:
            yaml.dump(test_config, f)

        # Load config
        loaded_config = config.load_config(config_file)
        self.assertEqual(loaded_config["database"]["host"], "localhost")
        self.assertEqual(loaded_config["model"]["iterations"], 10)

    def test_config_get_value(self):
        """Test getting config values with dot notation."""
        test_config = {
            "database": {"host": "localhost", "port": 5432},
            "model": {"iterations": 10},
        }

        # Existing value
        host = config.get_config_value(test_config, "database.host")
        self.assertEqual(host, "localhost")

        # Non-existing value with default
        timeout = config.get_config_value(test_config, "database.timeout", 30)
        self.assertEqual(timeout, 30)

    def test_logger_setup(self):
        """Test logger setup."""
        log_file = os.path.join(self.test_dir, "test.log")
        logger = log.setup_logger("test_logger", log_file)

        self.assertIsNotNone(logger)
        logger.info("Test message")

        # Verify log file exists and contains message
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r") as f:
            log_content = f.read()
        self.assertIn("Test message", log_content)

    def test_datastore_basic(self):
        """Test basic DataStore functionality."""
        store = DataStore(base_path=self.test_dir, project_name="test_project")

        # Save data
        result = store.save_data(self.test_df, "test_data")
        self.assertTrue(result)

        # Check existence
        self.assertTrue(store.dataset_exists("test_data"))

        # Load data
        loaded_df = store.load_data("test_data")
        self.assertIsNotNone(loaded_df)
        pd.testing.assert_frame_equal(self.test_df, loaded_df)

        # List datasets
        datasets = store.list_datasets()
        self.assertIn("test_data", datasets)

    def test_data_standardization(self):
        """Test data standardization functions."""
        standardized = data.standardize_zone_data(self.test_df)
        self.assertEqual(len(standardized), len(self.test_df))

        # Test aggregation
        district_mapping = {1: "A", 2: "A", 3: "B", 4: "B", 5: "C"}
        result = data.aggregate_to_districts(
            self.test_df,
            district_mapping,
            zone_col="zone_id",
            sum_cols=["households", "population"],
        )

        self.assertEqual(len(result), 3)  # 3 districts

        # Check aggregation worked
        district_a = result[result["district"] == "A"]
        self.assertEqual(district_a["households"].iloc[0], 300)  # 100 + 200

    def test_density_calculation(self):
        """Test density calculation."""
        area_data = pd.DataFrame({"zone_id": [1, 2, 3], "area_km2": [10.0, 5.0, 20.0]})

        result = data.calculate_density(
            self.test_df.head(3),
            area_data,
            pop_col="population",
            area_col="area_km2",
            join_col="zone_id",
        )

        self.assertIn("population_density", result.columns)
        # Check calculation (250 / 10.0 = 25.0)
        self.assertAlmostEqual(result.iloc[0]["population_density"], 25.0)


class TestOrcaIntegration(unittest.TestCase):
    """Test ORCA integration with updated namespace."""

    def test_orca_import(self):
        """Test that ORCA can be imported from new namespace."""
        try:
            from tlpytools.orca.orchestrator import OrcaOrchestrator

            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"ORCA import failed: {e}")

    def test_orca_functions_exist(self):
        """Test that key ORCA functions exist."""
        from tlpytools.orca.orchestrator import OrcaOrchestrator, check_databank_exists

        # These should be callable
        self.assertTrue(callable(OrcaOrchestrator))
        self.assertTrue(callable(check_databank_exists))


if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTest(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTest(loader.loadTestsFromTestCase(TestOrcaIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(
            f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)"
        )

    # Exit with error code if tests failed
    exit(0 if result.wasSuccessful() else 1)
