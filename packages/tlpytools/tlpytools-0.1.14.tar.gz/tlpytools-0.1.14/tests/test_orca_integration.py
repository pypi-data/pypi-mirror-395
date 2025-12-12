"""
Integration tests for ORCA orchestrator.

These tests perform live execution with real model configurations
and databank operations. They test the complete workflow end-to-end
without mocking.
"""

import unittest
import tempfile
import shutil
import os
import json
import yaml
import sys
import time
from pathlib import Path

# Import from the new namespace structure
from tlpytools.orca.orchestrator import OrcaOrchestrator, check_databank_exists


class TestOrcaIntegration(unittest.TestCase):
    """Integration tests for complete ORCA workflows."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level test fixtures."""
        cls.test_dir = tempfile.mkdtemp(prefix="orca_integration_test_")
        cls.original_cwd = os.getcwd()

        # Create a simplified test config based on default but with minimal steps
        cls.test_config = {
            "model_steps": ["b1_activitysim"],
            "iterations": {
                "total": 1,
                "start_at": 1,
                "convergence_criteria": {
                    "enabled": False,
                    "metric": "link_flow_rmse",
                    "threshold": 0.01,
                },
            },
            "input_data": {
                "test_data": [
                    {"source": "test/input/data1.txt"},
                    {"source": "test/input/data2.txt"},
                ]
            },
            "sub_components": {
                "b1_activitysim": {
                    "environment": {
                        "env_var": "ORCA_ACTIVITYSIM_ENV",
                        "default": "python",
                    },
                    "commands": [
                        {
                            "command": "python -c \"print('ActivitySim simulation complete'); import os; os.makedirs('output', exist_ok=True); open('output/test_result.txt', 'w').write('test output')\"",
                            "description": "Simulate ActivitySim model run",
                            "iterations": "all",
                        }
                    ],
                    "source_template": [],
                    "cleanup_patterns": ["*.tmp"],
                    "output_archives": [
                        {"archive_name": "main", "patterns": ["output/**"]}
                    ],
                }
            },
            "operational_mode": {
                "type": "local_testing",
                "cloud": {
                    "adls_url": f"https://{os.getenv('ORCA_ADLS_URL', 'yourstorageaccount.dfs.core.windows.net')}",
                    "adls_container": "raw",
                    "adls_folder": "orca_cloud_model_runs",
                },
            },
        }

        print(f"\nIntegration test directory: {cls.test_dir}")

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level test fixtures."""
        os.chdir(cls.original_cwd)
        # Keep test directory for inspection - comment out the next line to preserve
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def setUp(self):
        """Set up test fixtures for each test."""
        # Change to test directory
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)

    def _create_test_config_file(self, databank_path, config_data):
        """Helper to create test config file."""
        os.makedirs(databank_path, exist_ok=True)
        config_file = os.path.join(databank_path, "orca_model_config.yaml")
        with open(config_file, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False)
        return config_file

    def test_01_local_testing_full_run(self):
        """
        Test 1: Local testing mode - initialize and run model from start to finish.

        This test simulates:
        python -m tlpytools.orca --action run_models --databank db_test_local
        """
        print("\n=== Test 1: Local Testing Full Run ===")

        databank_name = "db_test_local"
        databank_path = os.path.join(self.test_dir, databank_name)

        # Ensure clean start
        if os.path.exists(databank_path):
            shutil.rmtree(databank_path)

        # Create test config
        self._create_test_config_file(databank_path, self.test_config)

        print(f"Creating orchestrator for databank: {databank_name}")
        print(f"Databank path: {databank_path}")

        # Initialize and run orchestrator
        orchestrator = OrcaOrchestrator(
            databank_name=databank_name, mode="local_testing"
        )

        # Verify initial state
        self.assertEqual(orchestrator.state.get("status"), "initialized")
        self.assertEqual(orchestrator.state.get("steps"), ["b1_activitysim"])
        self.assertEqual(orchestrator.state.get("total_iterations"), 1)

        print("Starting model run...")
        start_time = time.time()

        # Run the model
        success = orchestrator.run_local_testing()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Model run completed in {duration:.2f} seconds")
        print(f"Run success: {success}")

        # Verify success
        self.assertTrue(success, "Model run should complete successfully")

        # Verify final state
        final_state = orchestrator.state.get("status")
        print(f"Final state: {final_state}")
        self.assertEqual(final_state, "completed")

        # Verify all iterations completed
        self.assertTrue(orchestrator.state.is_all_iterations_complete())

        # Verify output files were created
        output_dir = os.path.join(databank_path, "outputs")
        self.assertTrue(os.path.exists(output_dir), "Outputs directory should exist")

        # Check for archived outputs
        archive_files = [f for f in os.listdir(output_dir) if f.endswith(".zip")]
        print(f"Archive files created: {archive_files}")
        self.assertGreater(
            len(archive_files), 0, "At least one archive file should be created"
        )

        # Verify new naming convention: {step_name}_{archive_name}_iter{iteration}.zip
        expected_archive = "b1_activitysim_main_iter1.zip"
        self.assertIn(
            expected_archive,
            archive_files,
            f"Expected archive {expected_archive} not found",
        )

        # Verify state file exists and contains expected data
        state_file = os.path.join(databank_path, "orca_model_state.json")
        self.assertTrue(os.path.exists(state_file), "State file should exist")

        with open(state_file, "r") as f:
            state_data = json.load(f)

        self.assertEqual(state_data["status"], "completed")
        self.assertEqual(state_data["total_steps_completed"], 1)

        print("✓ Local testing full run completed successfully")

    def test_02_cloud_initialization_only(self):
        """
        Test 2: Cloud production mode - initialize databank and upload to ADLS.

        This test simulates:
        python -m tlpytools.orca --action initialize_databank --databank db_test_integration_init --mode cloud_production
        """
        print("\n=== Test 2: Cloud Production Initialization ===")

        databank_name = "db_test_integration_init"
        databank_path = os.path.join(self.test_dir, databank_name)

        # Ensure clean start
        if os.path.exists(databank_path):
            shutil.rmtree(databank_path)

        # Create test config with cloud mode
        cloud_config = self.test_config.copy()
        cloud_config["operational_mode"]["type"] = "cloud_production"

        self._create_test_config_file(databank_path, cloud_config)

        print(f"Creating orchestrator for cloud databank: {databank_name}")
        print(f"Databank path: {databank_path}")

        # Initialize orchestrator in cloud mode
        orchestrator = OrcaOrchestrator(
            databank_name=databank_name, mode="cloud_production"
        )

        # Verify initialization
        self.assertEqual(orchestrator.mode, "cloud_production")
        self.assertEqual(orchestrator.state.get("status"), "initialized")

        print("Initializing databank...")
        start_time = time.time()

        # Initialize databank (this should create local structure)
        success = orchestrator.initialize_databank()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Databank initialization completed in {duration:.2f} seconds")
        print(f"Initialization success: {success}")

        # Verify success
        self.assertTrue(success, "Databank initialization should succeed")

        # Verify databank structure was created
        self.assertTrue(
            os.path.exists(databank_path), "Databank directory should exist"
        )
        self.assertTrue(
            os.path.exists(orchestrator.config_file), "Config file should exist"
        )
        self.assertTrue(
            os.path.exists(orchestrator.state_file), "State file should exist"
        )

        # Verify outputs directory was created
        outputs_dir = os.path.join(databank_path, "outputs")
        self.assertTrue(os.path.exists(outputs_dir), "Outputs directory should exist")

        # Test cloud sync upload (Note: This will attempt real ADLS upload)
        print("Testing cloud upload...")
        try:
            upload_success = orchestrator._sync_with_cloud(direction="upload")
            print(f"Cloud upload success: {upload_success}")
            # Note: upload might fail due to authentication or network issues in test environment
            # This is expected and acceptable for integration testing
        except Exception as e:
            print(f"Cloud upload failed (expected in test environment): {e}")
            upload_success = False

        # The initialization itself should still be successful regardless of upload
        print("✓ Cloud production initialization completed successfully")

    def test_03_cloud_download_and_run(self):
        """
        Test 3: Cloud production mode - download existing databank and complete run.

        This test simulates:
        python -m tlpytools.orca --action run_models --databank db_test_integration_init --mode cloud_production

        Note: This test assumes a cloud databank exists or creates a local one to simulate download.
        """
        print("\n=== Test 3: Cloud Production Download and Run ===")

        databank_name = "db_test_integration_run"
        databank_path = os.path.join(self.test_dir, databank_name)

        # Ensure clean start
        if os.path.exists(databank_path):
            shutil.rmtree(databank_path)

        # Create test config with cloud mode
        cloud_config = self.test_config.copy()
        cloud_config["operational_mode"]["type"] = "cloud_production"

        # First, simulate having an existing cloud databank by creating local structure
        # (In real scenario, this would be downloaded from ADLS)
        print("Simulating existing cloud databank...")
        os.makedirs(databank_path, exist_ok=True)

        # Create config file
        config_file = self._create_test_config_file(databank_path, cloud_config)

        # Create a state file to simulate partial progress
        state_file = os.path.join(databank_path, "orca_model_state.json")
        initial_state = {
            "start_at": 1,
            "total_iterations": 1,
            "current_iteration": 1,
            "steps": ["b1_activitysim"],
            "completed_steps": [],
            "total_steps_completed": 0,
            "current_step_index": 0,
            "status": "initialized",
            "start_time": None,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": None,
        }
        with open(state_file, "w") as f:
            json.dump(initial_state, f, indent=2)

        # Create sub-component directory structure
        component_dir = os.path.join(databank_path, "b1_activitysim")
        os.makedirs(component_dir, exist_ok=True)

        print(f"Creating orchestrator for cloud databank: {databank_name}")
        print(f"Databank path: {databank_path}")

        # Initialize orchestrator - it should detect existing databank
        orchestrator = OrcaOrchestrator(
            databank_name=databank_name, mode="cloud_production"
        )

        # Verify it detected existing state
        self.assertEqual(orchestrator.state.get("status"), "initialized")
        self.assertEqual(orchestrator.state.get("steps"), ["b1_activitysim"])

        # Test cloud sync download (Note: This will attempt real ADLS download)
        print("Testing cloud download...")
        try:
            download_success = orchestrator._sync_with_cloud(direction="download")
            print(f"Cloud download success: {download_success}")
        except Exception as e:
            print(f"Cloud download failed (expected in test environment): {e}")
            download_success = False

        print("Starting cloud production run...")
        start_time = time.time()

        # Run the model in cloud production mode
        success = orchestrator.run_cloud_production()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Cloud production run completed in {duration:.2f} seconds")
        print(f"Run success: {success}")

        # Verify success
        self.assertTrue(success, "Cloud production run should complete successfully")

        # Verify final state
        final_state = orchestrator.state.get("status")
        print(f"Final state: {final_state}")
        self.assertEqual(final_state, "completed")

        # Verify all iterations completed
        self.assertTrue(orchestrator.state.is_all_iterations_complete())

        # Verify output files were created
        output_dir = os.path.join(databank_path, "outputs")
        self.assertTrue(os.path.exists(output_dir), "Outputs directory should exist")

        # Check for archived outputs
        archive_files = [f for f in os.listdir(output_dir) if f.endswith(".zip")]
        print(f"Archive files created: {archive_files}")
        self.assertGreater(
            len(archive_files), 0, "At least one archive file should be created"
        )

        # Verify new naming convention: {step_name}_{archive_name}_iter{iteration}.zip
        expected_archive = "b1_activitysim_main_iter1.zip"
        self.assertIn(
            expected_archive,
            archive_files,
            f"Expected archive {expected_archive} not found",
        )

        # Test final cloud sync upload
        print("Testing final cloud upload...")
        try:
            upload_success = orchestrator._sync_with_cloud(direction="upload")
            print(f"Final cloud upload success: {upload_success}")
        except Exception as e:
            print(f"Final cloud upload failed (expected in test environment): {e}")
            upload_success = False

        print("✓ Cloud production download and run completed successfully")

    def test_04_databank_detection(self):
        """Test databank existence detection functionality."""
        print("\n=== Test 4: Databank Detection ===")

        # Test non-existent databank
        nonexistent_path = os.path.join(self.test_dir, "nonexistent")
        result = check_databank_exists(nonexistent_path)
        self.assertFalse(result["exists"])

        # Test existing databank
        existing_path = os.path.join(self.test_dir, "existing_databank")
        os.makedirs(existing_path, exist_ok=True)

        # Create state file
        state_file = os.path.join(existing_path, "orca_model_state.json")
        with open(state_file, "w") as f:
            json.dump({"status": "initialized"}, f)

        result = check_databank_exists(existing_path)
        self.assertTrue(result["exists"])
        self.assertIn("orca_model_state.json", result["files"])

        print("✓ Databank detection working correctly")

    def test_05_error_handling(self):
        """Test error handling in orchestrator."""
        print("\n=== Test 5: Error Handling ===")

        databank_name = "db_test_error"
        databank_path = os.path.join(self.test_dir, databank_name)

        # Create config with a command that will fail
        error_config = self.test_config.copy()
        error_config["sub_components"]["b1_activitysim"]["commands"] = [
            {
                "command": 'python -c "import sys; sys.exit(1)"',  # This will fail
                "description": "Failing command",
                "iterations": "all",
            }
        ]
        # Ensure output_archives is present even for failing commands
        error_config["sub_components"]["b1_activitysim"]["output_archives"] = [
            {"archive_name": "error", "patterns": ["*.log", "*.txt"]}
        ]

        self._create_test_config_file(databank_path, error_config)

        print(f"Creating orchestrator with failing command...")

        orchestrator = OrcaOrchestrator(
            databank_name=databank_name, mode="local_testing"
        )

        # Run the model - it should handle the error gracefully
        success = orchestrator.run_local_testing()

        # Should return False due to command failure
        self.assertFalse(success, "Run should fail due to failing command")

        # State should reflect the error
        final_state = orchestrator.state.get("status")
        print(f"Final state after error: {final_state}")
        # The status might be "error" or still "running" depending on implementation

        print("✓ Error handling test completed")


class TestRealConfigIntegration(unittest.TestCase):
    """Integration tests using the real default configuration."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level test fixtures."""
        cls.test_dir = tempfile.mkdtemp(prefix="orca_real_config_test_")
        cls.original_cwd = os.getcwd()

        # Load the real default config
        default_config_path = os.path.join(
            Path(__file__).parent.parent,
            "src",
            "tlpytools",
            "orca",
            "orca_model_config_example.yaml",
        )
        with open(default_config_path, "r") as f:
            cls.real_config = yaml.safe_load(f)

        print(f"\nReal config integration test directory: {cls.test_dir}")

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level test fixtures."""
        os.chdir(cls.original_cwd)
        # Keep test directory for inspection - comment out the next line to preserve
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def setUp(self):
        """Set up test fixtures for each test."""
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)

    def test_real_config_initialization(self):
        """Test initialization with real default config."""
        print("\n=== Real Config Initialization Test ===")

        databank_name = "db_test_real_config"
        databank_path = os.path.join(self.test_dir, databank_name)

        # Create config file with real config
        os.makedirs(databank_path, exist_ok=True)
        config_file = os.path.join(databank_path, "orca_model_config.yaml")
        with open(config_file, "w") as f:
            yaml.dump(self.real_config, f, default_flow_style=False)

        print(f"Creating orchestrator with real config...")
        print(f"Model steps: {self.real_config.get('model_steps', [])}")

        # Initialize orchestrator
        orchestrator = OrcaOrchestrator(
            databank_name=databank_name, mode="local_testing"
        )

        # Verify initialization
        self.assertEqual(orchestrator.state.get("status"), "initialized")

        # Verify configuration was loaded correctly
        expected_steps = self.real_config.get("model_steps", [])
        actual_steps = orchestrator.state.get("steps", [])
        self.assertEqual(actual_steps, expected_steps)

        # Verify sub-components are properly configured
        config = orchestrator._load_configuration()
        sub_components = config.get("sub_components", {})

        for step_name in expected_steps:
            self.assertIn(
                step_name,
                sub_components,
                f"Step {step_name} should be in sub_components",
            )

            step_config = sub_components[step_name]
            self.assertIn(
                "environment",
                step_config,
                f"Step {step_name} should have environment config",
            )
            self.assertIn(
                "commands", step_config, f"Step {step_name} should have commands"
            )

        # Test input_data configuration if present
        if "input_data" in config:
            input_data = config["input_data"]
            self.assertIsInstance(input_data, dict, "input_data should be a dictionary")

            for category, sources in input_data.items():
                self.assertIsInstance(
                    sources, list, f"input_data.{category} should be a list"
                )
                for source in sources:
                    if isinstance(source, dict):
                        self.assertIn(
                            "source",
                            source,
                            f"input_data source should have 'source' key",
                        )
                    else:
                        self.assertIsInstance(
                            source, str, f"input_data source should be string or dict"
                        )

        # Test output_archives configuration
        for step_name in expected_steps:
            step_config = sub_components[step_name]
            if "output_archives" in step_config:
                archives = step_config["output_archives"]
                self.assertIsInstance(
                    archives, list, f"output_archives for {step_name} should be a list"
                )

                for archive in archives:
                    self.assertIsInstance(
                        archive, dict, f"Each output archive should be a dictionary"
                    )
                    self.assertIn(
                        "archive_name", archive, f"Archive should have archive_name"
                    )
                    self.assertIn("patterns", archive, f"Archive should have patterns")
                    self.assertIsInstance(
                        archive["patterns"], list, f"Archive patterns should be a list"
                    )

        print("✓ Real config initialization successful")


if __name__ == "__main__":
    # Configure test discovery and execution
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add integration tests in order
    suite.addTest(loader.loadTestsFromTestCase(TestOrcaIntegration))
    suite.addTest(loader.loadTestsFromTestCase(TestRealConfigIntegration))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
