"""
Unit tests for ORCA orchestrator components.

These tests use mock objects and test data to verify individual
components work correctly without requiring actual model execution.
"""

import unittest
import tempfile
import shutil
import os
import json
import yaml
from unittest.mock import Mock, patch, MagicMock
import logging
import sys
from pathlib import Path

# Import from the new namespace structure
from tlpytools.orca.orchestrator import (
    OrcaLogger,
    OrcaDatabank,
    OrcaState,
    OrcaOrchestrator,
    OrcaFileSync,
    check_databank_exists,
)


class TestOrcaLogger(unittest.TestCase):
    """Test the OrcaLogger class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test.log")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Note: OrcaLogger no longer uses singleton pattern, so no cleanup needed

    def test_logger_initialization(self):
        """Test logger can be initialized."""
        logger = OrcaLogger(self.log_file)
        self.assertIsNotNone(logger.logger)
        self.assertEqual(logger.log_file_path, self.log_file)
        self.assertTrue(os.path.exists(self.log_file))

    def test_logger_isolation(self):
        """Test logger instances are properly isolated."""
        log_file1 = os.path.join(self.test_dir, "test1.log")
        log_file2 = os.path.join(self.test_dir, "test2.log")

        logger1 = OrcaLogger(log_file1)
        logger2 = OrcaLogger(log_file2)

        # They should be different instances
        self.assertIsNot(logger1, logger2)

        # They should have different log file paths
        self.assertNotEqual(logger1.log_file_path, logger2.log_file_path)

    def test_child_logger(self):
        """Test child logger creation."""
        logger = OrcaLogger(self.log_file)
        child = logger.get_child_logger("test_child")
        self.assertIsNotNone(child)
        # Check that the child logger name ends with .test_child
        self.assertTrue(child.name.endswith(".test_child"))


class TestOrcaState(unittest.TestCase):
    """Test the OrcaState class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.test_dir, "state.json")
        self.logger = Mock()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_state_initialization_new(self):
        """Test state initialization with new file."""
        state = OrcaState(self.state_file, self.logger)
        self.assertEqual(state.get("status"), "not_started")
        self.assertEqual(state.get("current_iteration"), 1)
        self.assertTrue(os.path.exists(self.state_file))

    def test_state_initialization_existing(self):
        """Test state initialization with existing file."""
        # Create existing state file
        existing_state = {
            "status": "running",
            "current_iteration": 2,
            "steps": ["step1", "step2"],
            "completed_steps": ["step1"],
        }
        with open(self.state_file, "w") as f:
            json.dump(existing_state, f)

        state = OrcaState(self.state_file, self.logger)
        self.assertEqual(state.get("status"), "running")
        self.assertEqual(state.get("current_iteration"), 2)
        self.assertEqual(state.get("completed_steps"), ["step1"])

    def test_state_update_and_save(self):
        """Test updating and saving state."""
        state = OrcaState(self.state_file, self.logger)
        state.update(status="running", current_iteration=3)

        # Reload and verify
        state2 = OrcaState(self.state_file, self.logger)
        self.assertEqual(state2.get("status"), "running")
        self.assertEqual(state2.get("current_iteration"), 3)

    def test_mark_step_complete(self):
        """Test marking steps as complete."""
        state = OrcaState(self.state_file, self.logger)
        state.update(steps=["step1", "step2", "step3"])

        state.mark_step_complete("step1")
        self.assertIn("step1", state.get("completed_steps"))
        self.assertEqual(state.get("current_step_index"), 1)

    def test_get_next_step(self):
        """Test getting next step."""
        state = OrcaState(self.state_file, self.logger)
        state.update(steps=["step1", "step2", "step3"], current_step_index=0)

        next_step = state.get_next_step()
        self.assertEqual(next_step, "step1")

        state.mark_step_complete("step1")
        next_step = state.get_next_step()
        self.assertEqual(next_step, "step2")

    def test_iteration_completion(self):
        """Test iteration completion logic."""
        state = OrcaState(self.state_file, self.logger)
        state.update(steps=["step1", "step2"], total_iterations=2, current_iteration=1)

        # Complete first iteration
        state.mark_step_complete("step1")
        state.mark_step_complete("step2")

        # Should be able to increment iteration
        next_iter = state.increment_iteration()
        self.assertEqual(next_iter, 2)
        self.assertEqual(state.get("completed_steps"), [])
        self.assertEqual(state.get("current_step_index"), 0)

        # Complete second iteration
        state.mark_step_complete("step1")
        state.mark_step_complete("step2")

        # Should be all complete
        self.assertTrue(state.is_all_iterations_complete())


class TestOrcaDatabank(unittest.TestCase):
    """Test the OrcaDatabank class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.logger = Mock()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_zip_directory(self):
        """Test directory zipping functionality."""
        databank = OrcaDatabank(self.test_dir, self.logger)

        # Create test files
        test_subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(test_subdir)
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("test content 1")
        with open(os.path.join(test_subdir, "file2.txt"), "w") as f:
            f.write("test content 2")

        zip_path = os.path.join(self.test_dir, "test.zip")
        success = databank.zip_directory(self.test_dir, zip_path)

        self.assertTrue(success)
        self.assertTrue(os.path.exists(zip_path))

    def test_copy_template_file(self):
        """Test template file copying."""
        databank = OrcaDatabank(self.test_dir, self.logger)

        # Create source file
        source_file = os.path.join(self.test_dir, "source.txt")
        with open(source_file, "w") as f:
            f.write("template content")

        # Copy to target
        target_file = os.path.join(self.test_dir, "target.txt")
        success = databank.copy_template_file(source_file, target_file)

        self.assertTrue(success)
        self.assertTrue(os.path.exists(target_file))

        with open(target_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "template content")

    def test_copy_input_data(self):
        """Test input data copying functionality."""
        # This would test the _copy_input_data method if it were public
        # For now, we test it indirectly through orchestrator initialization
        pass

    def test_cleanup_files_by_patterns(self):
        """Test file cleanup by patterns."""
        databank = OrcaDatabank(self.test_dir, self.logger)

        # Create test files
        files_to_create = ["keep.txt", "temp1.tmp", "temp2.tmp", "data.log"]

        for filename in files_to_create:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("test")

        # Clean up .tmp and .log files
        deleted = databank.cleanup_files_by_patterns(self.test_dir, ["*.tmp", "*.log"])

        self.assertEqual(len(deleted), 3)  # temp1.tmp, temp2.tmp, data.log
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "keep.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "temp1.tmp")))


class TestOrcaFileSync(unittest.TestCase):
    """Test the OrcaFileSync class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.file_sync = OrcaFileSync(self.logger)

    def test_get_adls_uri(self):
        """Test ADLS URI construction."""
        uri = self.file_sync.get_adls_uri(
            "test/file.txt", "container/folder", "https://storage.dfs.core.windows.net"
        )
        expected = "https://storage.dfs.core.windows.net/container/folder/test/file.txt"
        self.assertEqual(uri, expected)

    def test_get_adls_uri_with_leading_slash(self):
        """Test ADLS URI construction with leading slash."""
        uri = self.file_sync.get_adls_uri(
            "/test/file.txt", "container/folder", "https://storage.dfs.core.windows.net"
        )
        expected = "https://storage.dfs.core.windows.net/container/folder/test/file.txt"
        self.assertEqual(uri, expected)

    @patch("orchestrator.adls_tables.get_table_by_name")
    def test_download_from_adls_success(self, mock_get_table):
        """Test successful ADLS download."""
        # Mock the download response
        mock_get_table.return_value = b"test file content"

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.file_sync.download_from_adls(
                "test/file.txt", temp_dir, export_log=False
            )

            self.assertIsNotNone(result)
            self.assertTrue(os.path.exists(result))

            with open(result, "rb") as f:
                content = f.read()
            self.assertEqual(content, b"test file content")

    @patch("orchestrator.adls_tables.get_table_by_name")
    def test_download_from_adls_failure(self, mock_get_table):
        """Test failed ADLS download."""
        # Mock the download to return None (failure)
        mock_get_table.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.file_sync.download_from_adls(
                "test/file.txt", temp_dir, export_log=False
            )

            self.assertIsNone(result)


class TestOrcaOrchestrator(unittest.TestCase):
    """Test the OrcaOrchestrator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.databank_name = "test_databank"
        self.databank_path = os.path.join(self.test_dir, self.databank_name)

        # Create a simple test config
        self.test_config = {
            "model_steps": ["step1", "step2"],
            "iterations": {"total": 2, "start_at": 1},
            "input_data": {
                "landuse": [
                    {"source": "ABM/BaseNetworks/Inputs/landuse_synpop_2017.zip"},
                    {"source": "ABM/BaseNetworks/Inputs/landuse_synpop_2023.zip"},
                ],
                "networks": [
                    {"source": "ABM/BaseNetworks/base_network_*.txt"},
                    {"source": "ABM/BaseNetworks/bridge_crossing_gy.csv"},
                ],
            },
            "sub_components": {
                "step1": {
                    "environment": {"default": "python"},
                    "commands": [
                        {"command": "echo 'step1'", "description": "Test step 1"}
                    ],
                    "source_template": [],
                    "cleanup_patterns": ["*.tmp"],
                    "output_archives": [
                        {"archive_name": "results", "patterns": ["outputs/**"]}
                    ],
                },
                "step2": {
                    "environment": {"default": "python"},
                    "commands": [
                        {"command": "echo 'step2'", "description": "Test step 2"}
                    ],
                    "source_template": [],
                    "cleanup_patterns": ["*.tmp"],
                    "output_archives": [
                        {"archive_name": "main", "patterns": ["outputs/**"]},
                        {"archive_name": "logs", "patterns": ["*.log", "*.txt"]},
                    ],
                },
            },
            "operational_mode": {
                "type": "local_testing",
                "cloud": {
                    "adls_url": "https://test.dfs.core.windows.net",
                    "adls_container": "test",
                    "adls_folder": "test_folder",
                },
            },
        }

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Note: OrcaLogger no longer uses singleton pattern, so no cleanup needed

    def _create_test_orchestrator(self, mode="local_testing"):
        """Helper to create test orchestrator with config."""
        os.makedirs(self.databank_path, exist_ok=True)

        # Write test config file
        config_file = os.path.join(self.databank_path, "orca_model_config.yaml")
        with open(config_file, "w") as f:
            yaml.dump(self.test_config, f)

        # Change to the test directory for orchestrator initialization
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        try:
            orchestrator = OrcaOrchestrator(databank_name=self.databank_name, mode=mode)
            return orchestrator
        finally:
            os.chdir(original_cwd)

    def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = self._create_test_orchestrator()

        self.assertEqual(orchestrator.databank_name, self.databank_name)
        self.assertEqual(orchestrator.mode, "local_testing")
        self.assertTrue(os.path.exists(orchestrator.databank_path))
        self.assertTrue(os.path.exists(orchestrator.config_file))

    def test_load_configuration(self):
        """Test configuration loading."""
        orchestrator = self._create_test_orchestrator()
        config = orchestrator._load_configuration()

        self.assertEqual(config["model_steps"], ["step1", "step2"])
        self.assertEqual(config["iterations"]["total"], 2)

    def test_state_initialization_from_config(self):
        """Test state initialization from config."""
        orchestrator = self._create_test_orchestrator()

        # State should be initialized from config
        self.assertEqual(orchestrator.state.get("steps"), ["step1", "step2"])
        self.assertEqual(orchestrator.state.get("total_iterations"), 2)
        self.assertEqual(orchestrator.state.get("status"), "initialized")

    @patch("subprocess.run")
    def test_execute_step(self, mock_subprocess):
        """Test step execution."""
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "success"
        mock_subprocess.return_value.stderr = ""

        orchestrator = self._create_test_orchestrator()

        # Create step directory
        step_dir = os.path.join(orchestrator.databank_path, "step1")
        os.makedirs(step_dir, exist_ok=True)

        success = orchestrator._execute_step("step1")
        self.assertTrue(success)

    def test_archive_outputs_new_format(self):
        """Test output archiving with new output_archives format."""
        orchestrator = self._create_test_orchestrator()

        # Create step directory with test files
        step_dir = os.path.join(orchestrator.databank_path, "step2")
        os.makedirs(step_dir, exist_ok=True)

        # Create outputs subdirectory with test files
        outputs_dir = os.path.join(step_dir, "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        with open(os.path.join(outputs_dir, "result.txt"), "w") as f:
            f.write("test result")

        # Create log files
        with open(os.path.join(step_dir, "test.log"), "w") as f:
            f.write("test log")
        with open(os.path.join(step_dir, "info.txt"), "w") as f:
            f.write("test info")

        # Create outputs directory in databank
        databank_outputs = os.path.join(orchestrator.databank_path, "outputs")
        os.makedirs(databank_outputs, exist_ok=True)

        # Test archiving
        orchestrator._archive_outputs("step2")

        # Check that multiple archives were created
        archive_files = [f for f in os.listdir(databank_outputs) if f.endswith(".zip")]

        # Should have 2 archives: step2_main_iter1.zip and step2_logs_iter1.zip
        expected_archives = ["step2_main_iter1.zip", "step2_logs_iter1.zip"]

        for expected in expected_archives:
            self.assertIn(
                expected, archive_files, f"Expected archive {expected} not found"
            )

    def test_archive_outputs_no_config(self):
        """Test output archiving when no output_archives config exists."""
        orchestrator = self._create_test_orchestrator()

        # Create a step config without output_archives
        orchestrator.config["sub_components"]["step3"] = {
            "environment": {"default": "python"},
            "commands": [{"command": "echo 'step3'", "description": "Test step 3"}],
        }

        # Create step directory
        step_dir = os.path.join(orchestrator.databank_path, "step3")
        os.makedirs(step_dir, exist_ok=True)

        # Should not create any archives
        orchestrator._archive_outputs("step3")

        # Check that no archives were created for this step
        databank_outputs = os.path.join(orchestrator.databank_path, "outputs")
        if os.path.exists(databank_outputs):
            archive_files = [
                f for f in os.listdir(databank_outputs) if f.startswith("step3_")
            ]
            self.assertEqual(len(archive_files), 0)

    def test_get_adls_config(self):
        """Test ADLS config retrieval."""
        orchestrator = self._create_test_orchestrator()

        adls_url, adls_container, adls_folder = orchestrator.get_adls_config()

        self.assertEqual(adls_url, "https://test.dfs.core.windows.net")
        self.assertEqual(adls_container, "test")
        self.assertEqual(adls_folder, "test_folder")

    def test_input_data_initialization(self):
        """Test that input_data configuration is properly loaded."""
        orchestrator = self._create_test_orchestrator()

        # Check that input_data section exists in config
        self.assertIn("input_data", orchestrator.config)

        input_data = orchestrator.config["input_data"]
        self.assertIn("landuse", input_data)
        self.assertIn("networks", input_data)

        # Check structure
        self.assertEqual(len(input_data["landuse"]), 2)
        self.assertEqual(len(input_data["networks"]), 2)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_check_databank_exists_empty(self):
        """Test checking non-existent databank."""
        result = check_databank_exists(os.path.join(self.test_dir, "nonexistent"))
        self.assertFalse(result["exists"])

    def test_check_databank_exists_with_state(self):
        """Test checking existing databank with state file."""
        databank_path = os.path.join(self.test_dir, "test_databank")
        os.makedirs(databank_path)

        # Create state file
        state_file = os.path.join(databank_path, "orca_model_state.json")
        with open(state_file, "w") as f:
            json.dump({"status": "initialized"}, f)

        result = check_databank_exists(databank_path)
        self.assertTrue(result["exists"])
        self.assertIn("orca_model_state.json", result["files"])

    def test_check_databank_exists_without_state(self):
        """Test checking directory without state file."""
        databank_path = os.path.join(self.test_dir, "test_databank")
        os.makedirs(databank_path)

        # Create some other files but no state file
        with open(os.path.join(databank_path, "other.txt"), "w") as f:
            f.write("test")

        result = check_databank_exists(databank_path)
        self.assertFalse(result["exists"])


if __name__ == "__main__":
    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)

    unittest.main()
