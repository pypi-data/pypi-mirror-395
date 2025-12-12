#!/usr/bin/env python3
"""
Example usage of the Azure Batch Task Runner

This script demonstrates how to use the BatchTaskRunner class programmatically
instead of using the command-line interface.
"""

import os
from tlpytools.orca.batch_task_runner import BatchTaskRunner


def main():
    """Example of running a batch task programmatically"""

    # Set up environment variables (alternatively, you can use a .env file)
    # These should be set as actual environment variables in production
    os.environ["BATCH_ACCOUNT_ENDPOINT"] = os.getenv(
        "BATCH_ACCOUNT_ENDPOINT", "your-batch-account.batch.azure.com"
    )
    os.environ["IMAGE_REGISTRY_ENDPOINT"] = os.getenv(
        "IMAGE_REGISTRY_ENDPOINT", "your-registry.azurecr.io"
    )
    os.environ["AZURE_SUBSCRIPTION_ID"] = os.getenv(
        "AZURE_SUBSCRIPTION_ID", "your-subscription-id"
    )
    os.environ["AZURE_RESOURCE_GROUP"] = os.getenv(
        "AZURE_RESOURCE_GROUP", "your-resource-group"
    )
    os.environ["MANAGED_IDENTITY_NAME"] = os.getenv(
        "MANAGED_IDENTITY_NAME", "your-managed-identity"
    )

    # Create the batch runner
    runner = BatchTaskRunner()

    # Task configuration
    task_config = {
        "job_id": "job_medium",
        "project_name": "proj_unnamed",
        "databank_name": "db_demo_test",
        "docker_image": "orca/orca:develop",
        "max_retry_count": 0,
        "max_wall_clock_time": "PT1H",
        "poll_interval": 30,
        "timeout_minutes": 60,
    }

    try:
        print("Starting ORCA batch task...")

        # Option 1: Submit and wait for task to start
        success = runner.run_task(**task_config)

        if success:
            print("Task started successfully!")
        else:
            print("Task failed to start")

        # Option 2: Submit task only (without waiting)
        # task_id = runner.submit_task(
        #     job_id=task_config['job_id'],
        #     project_name=task_config['project_name'],
        #     databank_name=task_config['databank_name'],
        #     python_command=task_config['python_command'],
        #     python_env=task_config['python_env'],
        #     docker_image=task_config['docker_image'],
        #     max_retry_count=task_config['max_retry_count'],
        #     max_wall_clock_time=task_config['max_wall_clock_time']
        # )
        # print(f"Task {task_id} submitted. Check Azure Portal for progress.")

    except Exception as e:
        print(f"Error running batch task: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
