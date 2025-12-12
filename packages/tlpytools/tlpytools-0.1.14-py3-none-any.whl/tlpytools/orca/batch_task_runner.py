#!/usr/bin/env python3
"""
Azure Batch Task Runner - Python version of Synapse Pipeline PL_Batch_ORCA_Task

This script converts the Synapse pipeline functionality into a standalone Python program
that can submit and monitor Azure Batch tasks.
"""

# Load environment variables from .env file automatically
try:
    from ..env_config import ensure_env_loaded, get_env_var

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    def get_env_var(key: str, default: str = None, required: bool = False) -> str:
        """Fallback function if env_config is not available"""
        value = os.environ.get(key, default)
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value


import os
import sys
import time
import argparse
import logging
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any, Optional
from functools import wraps

import requests

try:
    from ..azure_credential import AzureCredentialManager
except ImportError:
    # Fallback if azure_credential is not available
    from azure.identity import DefaultAzureCredential

    class AzureCredentialManager:
        """Fallback credential manager if azure_credential module is not available"""

        @staticmethod
        def get_instance():
            return AzureCredentialManager()

        def get_credential(self):
            return DefaultAzureCredential()

        def get_batch_access_token(self, force_refresh=False):
            credential = self.get_credential()
            token = credential.get_token("https://batch.core.windows.net/")
            return token.token


try:
    from ..log import setup_logger
except ImportError:
    # Fallback if log module is not available
    def setup_logger(name, log_file=None, level=logging.INFO, console_output=True):
        logger = logging.getLogger(name)
        if not logger.handlers:
            if log_file:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(level)
        return logger


def is_authentication_error(status_code: int, response_text: str) -> bool:
    """Check if the response indicates an authentication/authorization error."""
    # Check for 401 Unauthorized or 403 Forbidden
    if status_code in [401, 403]:
        return True
    # Check for authentication-related error messages
    error_keywords = [
        "unauthorized",
        "authentication",
        "token expired",
        "invalid token",
    ]
    response_lower = response_text.lower()
    return any(keyword in response_lower for keyword in error_keywords)


def retry_with_token_refresh(max_retries: int = 2):
    """Decorator to retry Batch API calls with token refresh on authentication errors."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    # Check if this is an authentication error that we can retry
                    if hasattr(e, "args") and len(e.args) > 0:
                        error_msg = str(e)
                        # Look for status code in error message
                        if "Failed to" in error_msg and (
                            "401" in error_msg
                            or "403" in error_msg
                            or "unauthorized" in error_msg.lower()
                        ):
                            if attempt < max_retries - 1:
                                self.logger.warning(
                                    "Authentication error detected on attempt %d/%d: %s. Refreshing token and retrying...",
                                    attempt + 1,
                                    max_retries,
                                    error_msg,
                                )
                                # Force refresh the credential and token
                                self.credential_manager.get_credential(
                                    force_refresh=True
                                )
                                self.credential_manager.get_batch_access_token(
                                    force_refresh=True
                                )
                                time.sleep(1)  # Brief delay before retry
                                continue
                    raise
            raise last_exception

        return wrapper

    return decorator


class BatchTaskRunner:
    """Azure Batch Task Runner for ORCA tasks"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the Batch Task Runner with configuration from environment variables

        Args:
            logger: Optional logger instance. If not provided, a new logger will be created.
        """
        # Initialize logger
        if logger is not None:
            self.logger = logger
        else:
            # Create a default log file for batch task runner
            log_file = f"orca_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            self.logger = setup_logger(
                name="BatchTaskRunner",
                log_file=log_file,
                level=logging.INFO,
                console_output=True,
            )

        self.logger.info("Initializing BatchTaskRunner...")

        # Load required environment variables with validation
        self.api_version = get_env_var("BATCH_API_VERSION", "2024-07-01.20.0")
        self.batch_account_endpoint = get_env_var(
            "BATCH_ACCOUNT_ENDPOINT", required=True
        )
        self.image_registry_endpoint = get_env_var(
            "IMAGE_REGISTRY_ENDPOINT", required=True
        )
        self.subscription_id = get_env_var("AZURE_SUBSCRIPTION_ID", required=True)
        self.resource_group = get_env_var("AZURE_RESOURCE_GROUP", required=True)
        self.managed_identity_name = get_env_var("MANAGED_IDENTITY_NAME", required=True)

        # Log configuration
        self.logger.info("Batch API Version: %s", self.api_version)
        self.logger.info("Batch Account Endpoint: %s", self.batch_account_endpoint)
        self.logger.info("Image Registry Endpoint: %s", self.image_registry_endpoint)
        self.logger.info("Subscription ID: %s", self.subscription_id)
        self.logger.info("Resource Group: %s", self.resource_group)
        self.logger.info("Managed Identity Name: %s", self.managed_identity_name)

        # Initialize Azure credential manager
        self.credential_manager = AzureCredentialManager.get_instance()

        self.logger.info("BatchTaskRunner initialization completed")

    def _get_access_token(self) -> str:
        """Get Azure access token for Batch API using the credential manager"""
        self.logger.debug("Retrieving Azure access token for Batch API...")
        return self.credential_manager.get_batch_access_token()

    def _generate_task_id(self, project_name: str) -> str:
        """Generate a unique task ID similar to the Synapse pipeline"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        guid_prefix = str(uuid4())[:7]
        task_id = f"{timestamp}-{project_name}-{guid_prefix}"
        self.logger.debug("Generated task ID: %s", task_id)
        return task_id

    def _build_container_settings(
        self,
        docker_image: str,
        override_python_env: Optional[str] = None,
        override_python_command: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build container settings for the batch task"""
        self.logger.debug("Building container settings for image: %s", docker_image)

        managed_identity_resource_id = (
            f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/"
            f"providers/Microsoft.ManagedIdentity/userAssignedIdentities/{self.managed_identity_name}"
        )

        # Build base container run options
        container_run_options = (
            f"--workdir /home/ubuntu/orca --rm --volume /dev/shm:/dev/shm "
            f"--volume $AZ_BATCH_NODE_MOUNTS_DIR/datadisk:/home/ubuntu/orca"
        )

        # Add entrypoint only if both override_python_env and override_python_command are provided
        if override_python_env and override_python_command:
            # Add -m flag if override_python_command is not a script (doesn't end with .py)
            if override_python_command.endswith(".py"):
                entrypoint_cmd = f"{override_python_env} {override_python_command}"
            else:
                entrypoint_cmd = f"{override_python_env} -m {override_python_command}"
            container_run_options += f" --entrypoint {entrypoint_cmd}"
            self.logger.debug("Using custom entrypoint: %s", entrypoint_cmd)

        container_settings = {
            "imageName": f"{self.image_registry_endpoint}/{docker_image}",
            "registry": {
                "registryServer": self.image_registry_endpoint,
                "identityReference": {"resourceId": managed_identity_resource_id},
            },
            "workingDirectory": "containerImageDefault",
            "containerRunOptions": container_run_options,
        }

        self.logger.debug("Container settings built successfully")
        return container_settings

    def _build_constraints(
        self, max_retry_count: int, max_wall_clock_time: str
    ) -> Dict[str, Any]:
        """Build task constraints"""
        return {
            "maxTaskRetryCount": max_retry_count,
            "maxWallClockTime": max_wall_clock_time,
        }

    def _build_python_options(self, databank_name: str, project_name: str) -> str:
        """Build Python command line options default for orca command"""
        return f"--databank {databank_name} --project {project_name} --action run_models --mode cloud_production"

    def _build_task_payload(
        self,
        task_id: str,
        container_settings: Dict[str, Any],
        constraints: Dict[str, Any],
        python_options: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build the task payload for submission"""
        payload = {
            "id": task_id,
            "containerSettings": container_settings,
            "constraints": constraints,
            "environmentSettings": [],
            "userIdentity": {
                "autoUser": {"scope": "pool", "elevationLevel": "nonadmin"}
            },
        }

        # Only add commandLine if python_options is provided
        if python_options:
            payload["commandLine"] = python_options

        return payload

    @retry_with_token_refresh(max_retries=2)
    def submit_task(
        self,
        job_id: str,
        project_name: str,
        databank_name: str,
        override_python_env: Optional[str] = None,
        override_python_command: Optional[str] = None,
        override_python_options: Optional[str] = None,
        docker_image: str = "orca/orca:develop",
        max_retry_count: int = 0,
        max_wall_clock_time: str = "PT6H",
    ) -> str:
        """Submit a task to Azure Batch"""

        self.logger.info("Starting task submission for project: %s", project_name)
        self.logger.info("Job ID: %s", job_id)
        self.logger.info("Databank: %s", databank_name)
        self.logger.info("Docker image: %s", docker_image)

        # Generate task ID
        task_id = self._generate_task_id(project_name)

        # Build task components
        container_settings = self._build_container_settings(
            docker_image, override_python_env, override_python_command
        )
        constraints = self._build_constraints(max_retry_count, max_wall_clock_time)

        # Use override_python_options if provided, otherwise use default
        if override_python_options is not None:
            python_options = override_python_options
            self.logger.info("Using custom Python options: %s", python_options)
        else:
            python_options = self._build_python_options(databank_name, project_name)
            self.logger.info("Using default Python options: %s", python_options)

        # Build task payload
        task_payload = self._build_task_payload(
            task_id, container_settings, constraints, python_options
        )

        # Submit task
        url = f"https://{self.batch_account_endpoint}/jobs/{job_id}/tasks?api-version={self.api_version}"

        headers = {
            "Content-Type": "application/json; odata=minimalmetadata",
            "Authorization": f"Bearer {self._get_access_token()}",
        }

        self.logger.info("Submitting task %s to job %s...", task_id, job_id)
        response = requests.post(url, headers=headers, json=task_payload)

        if response.status_code not in [200, 201]:
            error_msg = (
                f"Failed to submit task: {response.status_code} - {response.text}"
            )
            self.logger.error(error_msg)
            raise Exception(error_msg)

        self.logger.info("Task %s submitted successfully!", task_id)
        return task_id

    @retry_with_token_refresh(max_retries=2)
    def check_task_status(self, job_id: str, task_id: str) -> Dict[str, Any]:
        """Check the status of a batch task"""
        self.logger.debug("Checking status for task %s in job %s", task_id, job_id)

        url = f"https://{self.batch_account_endpoint}/jobs/{job_id}/tasks/{task_id}?api-version={self.api_version}"

        headers = {
            "Content-Type": "application/json; odata=minimalmetadata",
            "Authorization": f"Bearer {self._get_access_token()}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            error_msg = (
                f"Failed to check task status: {response.status_code} - {response.text}"
            )
            self.logger.error(error_msg)
            raise Exception(error_msg)

        status_data = response.json()
        current_state = status_data.get("state", "unknown")
        self.logger.debug("Task %s current state: %s", task_id, current_state)

        return status_data

    def wait_for_task_completion(
        self,
        job_id: str,
        task_id: str,
        poll_interval: int = 30,
        timeout_minutes: int = 360,
        success_exit_states=None,
    ) -> bool:
        """Wait for task to reach success exit state, then continue"""

        if success_exit_states is None:
            success_exit_states = ["completed"]

        # Calculate max_polls based on timeout_minutes and poll_interval
        max_polls = max(1, (timeout_minutes * 60) // poll_interval)

        self.logger.info(
            "Waiting for task %s to start (polling every %d seconds, timeout: %d minutes, max polls: %d)...",
            task_id,
            poll_interval,
            timeout_minutes,
            max_polls,
        )

        for poll_count in range(1, max_polls + 1):
            try:
                # Wait before checking (except first iteration)
                if poll_count > 1:
                    time.sleep(poll_interval)

                # Check task status
                status = self.check_task_status(job_id, task_id)
                current_state = status.get("state", "unknown")

                self.logger.info(
                    "Poll %d/%d: Task state is '%s'",
                    poll_count,
                    max_polls,
                    current_state,
                )

                # Check if task has reached a running or completed state
                if current_state in success_exit_states:
                    self.logger.info(
                        "Task %s has reached '%s' state, success!",
                        task_id,
                        current_state,
                    )
                    return True

                # Check for failed states
                if current_state in ["failed"]:
                    self.logger.error("Task %s failed!", task_id)
                    if "executionInfo" in status:
                        exec_info = status["executionInfo"]
                        if "failureInfo" in exec_info:
                            self.logger.error(
                                "Failure reason: %s", exec_info["failureInfo"]
                            )
                    return False

            except Exception as e:
                self.logger.error(
                    "Error checking task status (poll %d): %s", poll_count, e
                )
                if poll_count == max_polls:
                    error_msg = (
                        f"Failed to check batch task status after {poll_count} attempts"
                    )
                    self.logger.error(error_msg)
                    raise Exception(error_msg)

        # Timeout reached
        timeout_msg = (
            f"Task did not reach a success state of {str(success_exit_states)} "
            f"within {timeout_minutes} minutes ({max_polls} polling attempts)"
        )
        self.logger.warning(timeout_msg)
        return False

    def run_task(
        self,
        job_id: str,
        project_name: str,
        databank_name: str,
        override_python_env: Optional[str] = None,
        override_python_command: Optional[str] = None,
        override_python_options: Optional[str] = None,
        docker_image: str = "orca/orca:develop",
        max_retry_count: int = 0,
        max_wall_clock_time: str = "PT6H",
        poll_interval: int = 30,
        timeout_minutes: int = 360,
    ) -> bool:
        """Submit a task and wait for it to start"""

        self.logger.info("Starting run_task for project: %s", project_name)

        # Submit the task
        task_id = self.submit_task(
            job_id=job_id,
            project_name=project_name,
            databank_name=databank_name,
            override_python_env=override_python_env,
            override_python_command=override_python_command,
            override_python_options=override_python_options,
            docker_image=docker_image,
            max_retry_count=max_retry_count,
            max_wall_clock_time=max_wall_clock_time,
        )

        # Wait for task to start
        success = self.wait_for_task_completion(
            job_id=job_id,
            task_id=task_id,
            poll_interval=poll_interval,
            timeout_minutes=timeout_minutes,
        )

        if not success:
            error_msg = f"Task {task_id} failed to start within the timeout period"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        self.logger.info("Task %s completed successfully!", task_id)
        return True


def main():
    """Main function to run the batch task"""
    parser = argparse.ArgumentParser(description="Azure Batch Task Runner for ORCA")

    # Required arguments
    parser.add_argument("--job-id", required=True, help="Batch job ID")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--databank", required=True, help="Databank name")

    # Optional arguments with defaults
    parser.add_argument(
        "--override-python-env",
        help="Python environment path (if not specified, uses docker image default)",
    )
    parser.add_argument(
        "--override-python-command",
        help="Python command to run (if not specified, uses docker image default)",
    )
    parser.add_argument(
        "--override-python-options",
        help="Python command line options (if not specified, uses default orca options)",
    )
    parser.add_argument(
        "--docker-image", default="orca/orca:develop", help="Docker image name"
    )
    parser.add_argument(
        "--max-retry-count", type=int, default=0, help="Maximum task retry count"
    )
    parser.add_argument(
        "--max-wall-clock-time",
        default="PT6H",
        help="Maximum wall clock time (ISO 8601 duration)",
    )
    parser.add_argument(
        "--poll-interval", type=int, default=30, help="Polling interval in seconds"
    )
    parser.add_argument(
        "--timeout-minutes", type=int, default=360, help="Timeout in minutes"
    )
    parser.add_argument(
        "--log-file",
        help="Log file path (optional, defaults to auto-generated filename)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    args = parser.parse_args()

    try:
        # Create logger if log file is specified
        logger = None
        if args.log_file:
            log_level = getattr(logging, args.log_level.upper())
            logger = setup_logger(
                name="BatchTaskRunner",
                log_file=args.log_file,
                level=log_level,
                console_output=True,
            )

        # Create batch runner
        runner = BatchTaskRunner(logger=logger)

        # Run the task
        success = runner.run_task(
            job_id=args.job_id,
            project_name=args.project,
            databank_name=args.databank,
            override_python_env=args.override_python_env,
            override_python_command=args.override_python_command,
            override_python_options=args.override_python_options,
            docker_image=args.docker_image,
            max_retry_count=args.max_retry_count,
            max_wall_clock_time=args.max_wall_clock_time,
            poll_interval=args.poll_interval,
            timeout_minutes=args.timeout_minutes,
        )

        if success:
            runner.logger.info("Task completed successfully!")
            sys.exit(0)
        else:
            runner.logger.error("Task failed!")
            sys.exit(1)

    except Exception as e:
        if "runner" in locals() and hasattr(runner, "logger"):
            runner.logger.error("Error: %s", e)
        else:
            # Fallback logging if runner doesn't exist
            logging.error("Error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
