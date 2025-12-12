"""
Command Line Interface for ORCA Orchestrator

This module provides the command-line interface for the ORCA orchestrator,
separating argument parsing and CLI handling from the core orchestrator logic.
"""

import os
import sys
import argparse
import logging
import shutil
from pathlib import Path

# Load environment variables before importing anything else
try:
    from ..env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

from .orchestrator import (
    OrcaOrchestrator,
    get_orca_logger,
    check_databank_exists,
    unpack_landuse_action,
    ORCA_DIR,
)


def main():
    """Main entry point for the ORCA orchestrator with action-based interface."""
    parser = argparse.ArgumentParser(
        description="ORCA Transportation Model Orchestrator - Unified interface for all ORCA operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Actions:
  run_models            Initialize and run complete model workflow
  initialize_databank   Initialize databank without running models  
  adls_sync            Synchronize databank with Azure Data Lake Storage
  unpack_landuse       Extract landuse files filtered by model year from zip archives

Examples:
  # Run complete model workflow (most common use case)
  python -m tlpytools.orca.cli --action run_models --databank db_test

  # Initialize databank only
  python -m tlpytools.orca.cli --action initialize_databank --databank db_test --overwrite

  # Cloud synchronization
  python -m tlpytools.orca.cli --action adls_sync --databank db_test --sync-action upload
  python -m tlpytools.orca.cli --action adls_sync --databank db_test --sync-action download --overwrite
  python -m tlpytools.orca.cli --action adls_sync --databank db_test --sync-action list

  # Cloud synchronization with custom project folder
  python -m tlpytools.orca.cli --action adls_sync --databank db_test --sync-action upload --project my_custom_project

  # Utility functions
  python -m tlpytools.orca.cli --action unpack_landuse --model-year 2017 --input landuse.zip --output data

  # Advanced model running with options
  python -m tlpytools.orca.cli --action run_models --databank db_test --mode cloud_production --iterations 3 --resume --project my_custom_project
        """,
    )

    parser.add_argument(
        "--action",
        choices=["run_models", "initialize_databank", "adls_sync", "unpack_landuse"],
        default="run_models",
        help="Action to perform",
    )

    parser.add_argument(
        "--databank", default="db_test", help="Name of the databank (scenario)"
    )

    parser.add_argument(
        "--config",
        default="orca_model_config.yaml",
        help="Configuration file name (default: orca_model_config.yaml)",
    )

    parser.add_argument(
        "--state",
        default="orca_model_state.json",
        help="State file name (default: orca_model_state.json)",
    )

    parser.add_argument(
        "--mode",
        choices=["local_testing", "cloud_production"],
        default="local_testing",
        help="Execution mode (default: local_testing)",
    )

    # Arguments for run_models action
    parser.add_argument(
        "--iterations",
        type=int,
        help="Number of iterations to run (overrides config file setting)",
    )

    parser.add_argument(
        "--steps",
        nargs="+",
        help="Specific model steps to run (e.g., --steps activitysim quetzal). If not specified, uses config file setting",
    )

    # Arguments for initialize_databank action
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing databank if it exists",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually creating files",
    )

    # Arguments for adls_sync action
    parser.add_argument(
        "--sync-action",
        choices=["upload", "download", "list"],
        help="ADLS synchronization action: upload to ADLS, download from ADLS, or list ADLS contents",
    )

    # Arguments for unpack_landuse action
    parser.add_argument(
        "--model-year",
        help="Model year to filter files by (required for unpack_landuse)",
    )

    parser.add_argument("--input", help="Input file path (required for unpack_landuse)")

    parser.add_argument(
        "--output", help="Output directory path (required for unpack_landuse)"
    )

    parser.add_argument(
        "--project",
        help="Override the ADLS project folder path (adls_folder) from config file",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Action-specific validation and execution
    if args.action == "run_models":
        # Validate required arguments for run_models
        if not args.databank:
            parser.error("--databank is required for run_models action")

        # Set up logging
        action_logger = get_orca_logger("run_models", log_file_path="run_models.log")

        action_logger.info("=" * 60)
        action_logger.info("ORCA Model Runner Starting")
        action_logger.info("=" * 60)
        action_logger.info("Databank: %s", args.databank)
        action_logger.info("Mode: %s", args.mode)
        action_logger.info("Config: %s", args.config)

        if args.iterations:
            action_logger.info("Iterations (override): %d", args.iterations)
        if args.steps:
            action_logger.info("Steps (override): %s", args.steps)
        if args.project:
            action_logger.info("Project (override): %s", args.project)

        try:
            # Create the orchestrator instance
            orchestrator = OrcaOrchestrator(
                databank_name=args.databank,
                config_file=args.config,
                state_file=args.state,
                mode=args.mode,
                project_folder=args.project,
            )

            # Apply command-line overrides to configuration
            if args.iterations:
                action_logger.info(
                    "Overriding iterations in config: %d", args.iterations
                )
                orchestrator.config["iterations"]["total"] = args.iterations
                # Update state with new iteration count
                orchestrator.state.update(total_iterations=args.iterations)

            if args.steps:
                action_logger.info("Overriding model steps in config: %s", args.steps)
                orchestrator.config["model_steps"] = args.steps
                # Update state with new steps
                orchestrator.state.update(steps=args.steps)

            # Run the model
            action_logger.info("Starting model execution...")
            success = orchestrator.run()

            # Report results
            action_logger.info("=" * 60)
            if success:
                action_logger.info("[SUCCESS] Model execution completed successfully!")

                # Print summary information
                total_iterations = orchestrator.state.get("total_iterations", 0)
                total_steps_completed = orchestrator.state.get(
                    "total_steps_completed", 0
                )

                action_logger.info("Summary:")
                action_logger.info("  - Total iterations: %d", total_iterations)
                action_logger.info(
                    "  - Total steps completed: %d", total_steps_completed
                )
                action_logger.info(
                    "  - Databank location: %s", orchestrator.databank_path
                )

                if args.mode == "cloud_production":
                    action_logger.info("  - Cloud sync: enabled")
                    action_logger.info("  - Model outputs backed up to ADLS")

                # Check for outputs directory
                outputs_dir = os.path.join(orchestrator.databank_path, "outputs")
                if os.path.exists(outputs_dir):
                    output_files = []
                    for _, _, files in os.walk(outputs_dir):
                        output_files.extend(files)
                    action_logger.info(
                        "  - Output files generated: %d", len(output_files)
                    )

                action_logger.info("=" * 60)
                action_logger.info(
                    "Model run completed. Check the databank directory for results:"
                )
                action_logger.info("  %s", orchestrator.databank_path)

            else:
                action_logger.error("[FAILED] Model execution failed!")

                # Print error information if available
                error_msg = orchestrator.state.get("error")
                if error_msg:
                    action_logger.error("Error details: %s", error_msg)

                # Print current state for debugging
                current_step = orchestrator.state.get_next_step()
                current_iteration = orchestrator.state.get_display_iteration()
                action_logger.error(
                    "Failed at iteration %d, step: %s", current_iteration, current_step
                )

                action_logger.info("=" * 60)
                action_logger.info("Check the logs for detailed error information.")
                action_logger.info(
                    "Model state saved to: %s", orchestrator.state.state_file_path
                )

            sys.exit(0 if success else 1)

        except KeyboardInterrupt:
            action_logger.warning("Model execution interrupted by user")
            action_logger.info(
                "Model state has been saved and can resume from last successfully completed step."
            )
            sys.exit(1)

        except (OSError, IOError, RuntimeError) as e:
            action_logger.error("Unexpected error during model execution: %s", str(e))
            action_logger.error("Check the logs for detailed error information")
            sys.exit(1)

    elif args.action == "initialize_databank":
        # Validate required arguments for initialize_databank
        if not args.databank:
            parser.error("--databank is required for initialize_databank action")

        # Set up logging
        action_logger = get_orca_logger(
            "initialize_databank", log_file_path="initialize_databank.log"
        )

        action_logger.info("=" * 60)
        action_logger.info("ORCA Databank Initializer")
        action_logger.info("=" * 60)
        action_logger.info("Databank: %s", args.databank)
        action_logger.info("Config: %s", args.config)
        if args.project:
            action_logger.info("Project (override): %s", args.project)

        if args.dry_run:
            action_logger.info("Mode: DRY RUN (no files will be created)")
        if args.overwrite:
            action_logger.info("Overwrite: enabled")

        try:
            # Check if databank already exists
            databank_path = os.path.abspath(args.databank)
            existing_info = check_databank_exists(databank_path)

            if existing_info["exists"]:
                action_logger.warning("Databank already exists at: %s", databank_path)

                # Show what's in the existing databank
                if existing_info.get("error"):
                    action_logger.error(
                        "Error checking databank: %s", existing_info["error"]
                    )
                    sys.exit(1)

                if existing_info["directories"]:
                    action_logger.info(
                        "Existing directories: %s",
                        ", ".join(existing_info["directories"]),
                    )
                if existing_info["files"]:
                    action_logger.info(
                        "Existing files: %s", ", ".join(existing_info["files"])
                    )

                if not args.overwrite:
                    action_logger.error("Use --overwrite to replace existing databank")
                    sys.exit(1)
                else:
                    action_logger.warning("Will overwrite existing databank")
                    if not args.dry_run:
                        # Remove existing databank
                        action_logger.info("Removing existing databank...")
                        shutil.rmtree(databank_path)

            if args.dry_run:
                action_logger.info(
                    "DRY RUN: Would create databank at: %s", databank_path
                )
                action_logger.info(
                    "DRY RUN: Would copy template files from sub-components"
                )
                action_logger.info(
                    "DRY RUN: Would create configuration file: %s", args.config
                )
                action_logger.info("DRY RUN: Would initialize model state file")
                action_logger.info("DRY RUN: Would create outputs directory structure")

                # Show what templates would be copied
                try:
                    # Find default config using the same logic as _create_template_config
                    default_config_locations = [
                        os.path.join(os.getcwd(), "orca_model_config_default.yaml"),
                        os.path.join(
                            os.getcwd(), "orca", "orca_model_config_default.yaml"
                        ),
                        os.path.join(ORCA_DIR, "orca_model_config_default.yaml"),
                    ]

                    default_config_path = None
                    for path in default_config_locations:
                        if os.path.exists(path):
                            default_config_path = path
                            break

                    if default_config_path:
                        import yaml

                        with open(default_config_path, "r", encoding="utf-8") as f:
                            config = yaml.safe_load(f)

                        if "sub_components" in config:
                            action_logger.info(
                                "DRY RUN: Templates that would be copied:"
                            )
                            for step_name in config["sub_components"]:
                                action_logger.info("  - %s", step_name)
                except (FileNotFoundError, yaml.YAMLError, KeyError) as e:
                    action_logger.warning("Could not preview templates: %s", str(e))

                action_logger.info("DRY RUN: Initialization preview completed")
                sys.exit(0)

            # Create the orchestrator instance (this will initialize the databank)
            action_logger.info("Creating databank structure...")
            orchestrator = OrcaOrchestrator(
                databank_name=args.databank,
                config_file=args.config,
                state_file=args.state,
                mode=args.mode,
                project_folder=args.project,
            )

            # Use the new initialize_databank method
            success = orchestrator.initialize_databank()

            if success:
                action_logger.info("[SUCCESS] Databank initialization completed!")
                action_logger.info("=" * 60)
                action_logger.info("Databank is ready for model execution!")
                action_logger.info("To run the model, use:")
                action_logger.info(
                    "  python -m tlpytools.orca.cli --action run_models --databank %s",
                    args.databank,
                )
            else:
                action_logger.error("[FAILED] Databank initialization failed!")
                sys.exit(1)

        except KeyboardInterrupt:
            action_logger.warning("Initialization interrupted by user")
            sys.exit(1)

        except (OSError, IOError) as e:
            action_logger.error("File system error during initialization: %s", str(e))
            sys.exit(1)

        except ImportError as e:
            action_logger.error("Required module not found: %s", str(e))
            action_logger.error("Make sure all dependencies are installed")
            sys.exit(1)

    elif args.action == "adls_sync":
        # Validate required arguments for adls_sync
        if not args.databank:
            parser.error("--databank is required for adls_sync action")
        if not args.sync_action:
            parser.error("--sync-action is required for adls_sync action")

        # Set up logging
        action_logger = get_orca_logger(
            "adls_data_sync", log_file_path="adls_data_sync.log"
        )

        action_logger.info("=" * 60)
        action_logger.info("ORCA ADLS Data Synchronization")
        action_logger.info("=" * 60)
        action_logger.info("Databank: %s", args.databank)
        action_logger.info("Action: %s", args.sync_action)

        if args.config:
            action_logger.info("Config file: %s", args.config)
        if args.overwrite:
            action_logger.info("Overwrite: enabled")
        if args.project:
            action_logger.info("Project (override): %s", args.project)

        try:
            # For download operations, we may need to create the orchestrator even if databank doesn't exist locally
            if args.sync_action == "download" and not os.path.exists(args.databank):
                # Create minimal structure for download
                os.makedirs(args.databank, exist_ok=True)

            orchestrator = OrcaOrchestrator(
                databank_name=args.databank,
                config_file=args.config,
                state_file=args.state,
                mode="local_testing",  # Assume local testing when triggering sync action manually to avoid triggering additional sync commands
                project_folder=args.project,
            )

            # Log ADLS settings
            adls_url, adls_container, adls_folder = orchestrator.get_adls_config()
            action_logger.info("ADLS Account URL: %s", adls_url)
            action_logger.info("ADLS Container: %s", adls_container)
            action_logger.info("ADLS Folder: %s", adls_folder)

            # Perform synchronization
            success = orchestrator.sync_with_adls(
                direction=args.sync_action,
            )

            # Report results
            action_logger.info("=" * 60)
            if success:
                action_logger.info("[SUCCESS] Synchronization completed successfully!")

                if args.sync_action == "upload":
                    action_logger.info(
                        "Databank '%s' has been uploaded to ADLS", args.databank
                    )
                    action_logger.info(
                        "Cloud location: %s/%s/%s/%s",
                        adls_url,
                        adls_container,
                        adls_folder,
                        args.databank,
                    )

                elif args.sync_action == "download":
                    action_logger.info(
                        "Databank '%s' has been downloaded from ADLS", args.databank
                    )
                    action_logger.info(
                        "Local location: %s", os.path.abspath(args.databank)
                    )

                elif args.sync_action == "list":
                    action_logger.info(
                        "ADLS contents listed for databank '%s'", args.databank
                    )

            else:
                action_logger.error("[FAILED] Synchronization failed!")
                action_logger.error("Check the logs for detailed error information")

            # Exit with appropriate code
            sys.exit(0 if success else 1)

        except KeyboardInterrupt:
            action_logger.warning("Synchronization interrupted by user")
            sys.exit(1)

        except (OSError, IOError) as e:
            action_logger.error("File system error during synchronization: %s", str(e))
            sys.exit(1)

        except ImportError as e:
            action_logger.error("Required module not found: %s", str(e))
            action_logger.error(
                "Make sure tlpytools and other dependencies are installed"
            )
            sys.exit(1)

    elif args.action == "unpack_landuse":
        # Validate required arguments for unpack_landuse
        if not args.model_year:
            parser.error("--model-year is required for unpack_landuse action")
        if not args.input:
            parser.error("--input is required for unpack_landuse action")
        if not args.output:
            parser.error("--output is required for unpack_landuse action")

        success = unpack_landuse_action(args)
        sys.exit(0 if success else 1)

    else:
        parser.error(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()
