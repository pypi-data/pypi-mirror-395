# ORCA Transportation Model Orchestrator

The ORCA Orchestrator is a comprehensive Python tool for managing and executing the ORCA transportation model. It provides a unified interface for model initialization, execution, state management, and cloud synchronization.

## Overview

The orchestrator manages complex transportation modeling workflows by:
- Coordinating multiple sub-component models (ActivitySim, Quetzal, PopulationSim, etc.)
- Managing databank lifecycle (initialization, execution, archiving)
- Handling cloud synchronization with Azure Data Lake Storage (ADLS)
- Providing performance monitoring and error handling
- Maintaining execution state across iterations and steps

## Architecture

The orchestrator consists of several key components:

### Core Classes

1. **`OrcaOrchestrator`** - Main orchestrator class that manages model execution
2. **`OrcaLogger`** - Centralized logging with singleton behavior
3. **`OrcaState`** - State management for tracking iterations and steps
4. **`OrcaDatabank`** - Local file operations and databank management
5. **`OrcaFileSync`** - Cloud synchronization with Azure Data Lake Storage
6. **`OrcaPerformanceMonitor`** - Runtime and system resource monitoring

### Key Features

- **Multi-mode execution**: Local testing and cloud production modes
- **Iterative modeling**: Support for multiple model iterations with state persistence
- **Cloud integration**: Seamless synchronization with Azure Data Lake Storage
- **Error handling**: Comprehensive error dumps and recovery mechanisms
- **Performance monitoring**: Real-time tracking of system resources and execution time
- **Template management**: Automated copying and setup of model templates

## Usage

### Command Line Interface

The orchestrator provides an action-based command line interface:

```bash
python -m tlpytools.orca.cli [options]
```

The cli can also be access through the orca module, as it will be automatically redirected to cli:

```bash
python -m tlpytools.orca [options]
```

For information on how to use the cli commands, call for help:

```bash
python -m tlpytools.orca --help
```


### Actions

#### 1. Run Models (`run_models`)
Initialize and run the complete model workflow.

```bash
# Basic model run
python -m tlpytools.orca --action run_models --databank db_example

# Advanced options
python -m tlpytools.orca --action run_models \
    --databank db_example \
    --mode cloud_production \
    --iterations 3 \
    --steps activitysim quetzal \
    --project custom_project
```

#### 2. Initialize Databank (`initialize_databank`)
Create and set up a new databank without running models.

```bash
# Initialize new databank
python -m tlpytools.orca --action initialize_databank --databank db_example

# Overwrite existing databank
python -m tlpytools.orca --action initialize_databank --databank db_example --overwrite

# Dry run (show what would be done)
python -m tlpytools.orca --action initialize_databank --databank db_example --dry-run
```

#### 3. Cloud Synchronization (`adls_sync`)
Synchronize databank with Azure Data Lake Storage.

```bash
# Upload to cloud
python -m tlpytools.orca --action adls_sync --project my_project_folder --databank db_example --sync-action upload

# Download from cloud
python -m tlpytools.orca --action adls_sync --project my_project_folder --databank db_example --sync-action download

# List cloud contents
python -m tlpytools.orca --action adls_sync --project my_project_folder --databank db_example --sync-action list
```

#### 4. Unpack Land Use (`unpack_landuse`)
Extract land use files filtered by model year from zip archives.

```bash
python -m tlpytools.orca --action unpack_landuse \
    --model-year 2017 \
    --input landuse_data.zip \
    --output ./data
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--databank` | Name of the databank (scenario) | `db_test` |
| `--config` | Configuration file name | `orca_model_config.yaml` |
| `--state` | State file name | `orca_model_state.json` |
| `--mode` | Execution mode (`local_testing`, `cloud_production`) | `local_testing` |
| `--iterations` | Number of iterations to run | From config file |
| `--steps` | Specific model steps to run | From config file |
| `--overwrite` | Overwrite existing databank | `False` |
| `--dry-run` | Show what would be done without executing | `False` |
| `--project` | Override ADLS project folder path | From config file |
| `--verbose` | Enable verbose logging | `False` |

## Configuration

The orchestrator uses a YAML configuration file system with the following behavior:

### Configuration File Loading Hierarchy

1. **Primary Configuration**: The orchestrator always uses `orca_model_config.yaml` located in the databank directory for active operations.

2. **Initialization Configuration**: When creating a new databank, you can specify a custom configuration file via the `--config` CLI option or the `config_file` parameter in the constructor. This file is used only during initialization and is copied to become the primary configuration.

3. **Template Configuration Fallback**: If no configuration exists, the orchestrator automatically creates one by searching for `orca_model_config_default.yaml` in the following order:
   - Current working directory: `./orca_model_config_default.yaml`
   - Orca subfolder of working directory: `./orca/orca_model_config_default.yaml`
   - Parent directory of databank: `../orca_model_config_default.yaml`
   - Package installation directory: `<package>/orca/orca_model_config_default.yaml`

### Configuration File Behavior

- **Custom Config During Initialization**: If you specify a custom config file (e.g., `my_custom_config.yaml`), the orchestrator searches for it in:
  - Absolute path (if provided)
  - Relative to current working directory
  - Relative to orchestrator script directory  
  - Relative to databank parent directory

- **Automatic Template Creation**: If neither a custom config nor default template is found, the orchestrator will raise a `FileNotFoundError` with details about the searched locations.

- **Example Configuration**: The package includes `orca_model_config_example.yaml` which demonstrates all available configuration options.

### Usage Examples

```bash
# Use default configuration (searches for orca_model_config_default.yaml)
python -m tlpytools.orca --action initialize_databank --databank db_example

# Use custom configuration file during initialization
python -m tlpytools.orca --action initialize_databank --databank db_example --config my_custom_config.yaml

# Existing databank always uses orca_model_config.yaml from databank directory
python -m tlpytools.orca --action run_models --databank db_example
```

The configuration file defines:

### Model Configuration Structure

```yaml
# Model execution settings
model_steps:
  - activitysim
  - quetzal
  - populationsim

iterations:
  total: 3
  start_at: 1

# Sub-component configurations
sub_components:
  activitysim:
    template_dir: "/path/to/activitysim/template"
    commands:
      - description: "Run ActivitySim"
        command: "python run_activitysim.py"
    output_archives:
      - pattern: "outputs/*.csv"
        archive_name: "activitysim_outputs"
    cleanup_patterns:
      - "*.tmp"
      - "temp_*"

# Input data sources
input_data:
  landuse:
    - source: "/shared/landuse/"
      target: "inputs/landuse/"
  networks:
    - source: "/shared/networks/"
      target: "inputs/networks/"

# Cloud operations
operational_mode:
  cloud:
    adls_url: "https://account.dfs.core.windows.net"
    adls_container: "raw"
    adls_folder: "orca_model_runs"

# Logging configuration
logging:
  level: INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Performance monitoring
performance_monitoring:
  enabled: true
  poll_interval: 1.0
  track_memory: true
  track_cpu: true
```

## Logging Configuration

The orchestrator supports configurable logging levels to control the verbosity of output:

### Logging Levels

Configure the logging level in your `orca_model_config.yaml`:

```yaml
logging:
  level: INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Available levels (from most to least verbose):
- **DEBUG**: Detailed information for diagnosing problems. Shows all internal operations, file operations, and step-by-step execution details.
- **INFO** (default, recommended): General informational messages about model progress. Shows one summary message per step/action.
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious errors

### Logging Behavior

- **INFO level** (default): Provides a clean, high-level view of model execution with approximately one log message per step or major action
- **DEBUG level**: Provides detailed diagnostic information useful for troubleshooting, including:
  - Detailed file operations
  - Environment setup information
  - Performance monitoring details
  - System information
  - Step-by-step execution details

### Example Usage

```bash
# Run with default INFO logging
python -m tlpytools.orca --action run_models --databank db_example

# For detailed troubleshooting, set level to DEBUG in config file
# Then run the model
python -m tlpytools.orca --action run_models --databank db_example
```

Logs are written to `orca_YYYYMMDD_HHMMSS.log` in the databank directory.

## Execution Modes

### Local Testing Mode
- Executes models locally without cloud integration
- Suitable for development and testing
- All data remains on local filesystem

### Cloud Production Mode
- Integrates with Azure Data Lake Storage
- Automatic synchronization of databanks
- Suitable for production modeling workflows
- Supports distributed execution

## File Management

### Configuration File Management

The orchestrator implements a sophisticated configuration file management system:

#### File Naming Convention
- **Active Configuration**: Always named `orca_model_config.yaml` in the databank directory
- **Template Configuration**: Named `orca_model_config_default.yaml` for automatic template creation
- **Example Configuration**: `orca_model_config_example.yaml` provides documentation and examples

#### Configuration Resolution Process
1. **Databank Initialization**: 
   - If custom config specified via `--config`, search for it in multiple locations
   - If found, copy to databank as `orca_model_config.yaml`
   - If not found or not specified, search for `orca_model_config_default.yaml`
   - Copy template to databank as `orca_model_config.yaml`

2. **Existing Databank Operations**:
   - Always load `orca_model_config.yaml` from databank directory
   - If missing, attempt to recreate from template
   - Log configuration source for troubleshooting

#### Best Practices
- **Template Setup**: Place `orca_model_config_default.yaml` in your project root for consistent initialization
- **Custom Configurations**: Use descriptive names for project-specific configs (e.g., `production_config.yaml`)
- **Version Control**: Include template configurations in version control, exclude databank-specific configs
- **Documentation**: Use the example config as a reference for all available options

### Databank Structure
```
databank_name/
├── orca_model_config.yaml       # Configuration file
├── orca_model_state.json        # Execution state
├── orca_20251030_172324.log      # Orchestrator logs
├── inputs/                      # Shared input data
├── outputs/                     # Model outputs
├── activitysim/                 # Sub-component folder
├── quetzal/                     # Sub-component folder
└── .cloud_sync_conflict/        # Conflict resolution
```

### Cloud Synchronization Behavior

#### Upload Logic:
- Sub-component folders are zipped before upload
- Config files are uploaded individually with conflict handling
- Output files are uploaded individually (never overwritten)
- Error dumps are uploaded to special error_dumps/ folder

#### Download Logic:
- Empty local databank: Downloads everything
- Existing local databank: Downloads only new output files
- Conflict files are moved to `.cloud_sync_conflict/` folder

## State Management

The orchestrator maintains execution state in `orca_model_state.json`:

```json
{
  "start_at": 1,
  "total_iterations": 3,
  "current_iteration": 1,
  "steps": ["activitysim", "quetzal"],
  "completed_steps": ["activitysim"],
  "current_step_index": 1,
  "status": "running",
  "start_time": "2025-01-15 10:30:00",
  "last_updated": "2025-01-15 11:45:00"
}
```

## Performance Monitoring

When enabled, the orchestrator tracks:
- Runtime duration for each step
- System memory usage (GB)
- CPU utilization (%)
- Process-specific metrics

Monitoring data is exported to CSV files for analysis.

## Error Handling

### Error Dumps
When a model execution fails, the orchestrator creates comprehensive error dumps containing:
- All data from the failed step directory
- Configuration files
- Log files
- System state information
- Optionally, entire databank content

### Recovery
The state file enables resuming execution from the last successful step.

## Dependencies

### Required:
- Python 3.7+
- PyYAML
- Standard library modules (json, logging, argparse, etc.)

### Optional:
- `psutil` - For system monitoring
- `tlpytools.adls_server` - For Azure Data Lake Storage integration
- `tlpytools.azure_credential` - For centralized Azure authentication (recommended)

### Azure-related:
- `azure-identity` - Required for Azure authentication
- `azure-storage-filedatalake` - Required for ADLS operations
- `requests` - Required for Azure Batch API calls

## Environment Variables

### ORCA-specific Variables
- `UPLOAD_OUTPUTS_ONLY` - If set to True, only uploads outputs and config files to cloud
- Performance monitoring can be controlled via config file

### Azure Authentication Variables
The orchestrator and batch task runner use centralized Azure authentication via `AzureCredentialManager`. 
Configure authentication behavior with these environment variables:

- `OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL` (default: `true`)
- `OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL` (default: `false`)
- `OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL` (default: `false`)
- `OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL` (default: `false`)
- `OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL` (default: `false`)
- `OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL` (default: `false`)

### Required Azure Service Variables
See [ENVIRONMENT_VARIABLES.md](../../../ENVIRONMENT_VARIABLES.md) for complete list of required and optional environment variables, including:

- `ORCA_ADLS_URL` - Azure Data Lake Storage endpoint
- `BATCH_ACCOUNT_ENDPOINT` - Azure Batch account endpoint
- `IMAGE_REGISTRY_ENDPOINT` - Container registry endpoint
- `AZURE_SUBSCRIPTION_ID` - Azure subscription ID
- `AZURE_RESOURCE_GROUP` - Azure resource group name
- `MANAGED_IDENTITY_NAME` - Managed identity name

For detailed authentication configuration, see [docs/azure_credential_manager.md](../../../docs/azure_credential_manager.md).

## Logging

The orchestrator provides comprehensive logging with:
- Singleton logger pattern for consistency
- File and console output
- Configurable log levels
- System information capture
- Azure SDK logging suppression

Log files are created in the databank directory as `orca_YYYYMMDD_HHMMSS.log`.

## Examples

### Complete Workflow Example
```bash
# 1. Initialize a new databank
python -m tlpytools.orca --action initialize_databank --databank scenario_2030

# 2. Run the complete model workflow
python -m tlpytools.orca --action run_models --databank scenario_2030 --iterations 5

# 3. Upload results to cloud
python -m tlpytools.orca --action adls_sync --project my_project_folder --databank scenario_2030 --sync-action upload
```

### Cloud Production Example
```bash
# Initialize and run in cloud production mode
python -m tlpytools.orca --action run_models \
    --databank production_scenario \
    --mode cloud_production \
    --iterations 10 \
    --project production_runs
```

### Debugging Example
```bash
# Run with verbose logging and dry-run
python -m tlpytools.orca --action initialize_databank \
    --databank debug_scenario \
    --verbose \
    --dry-run
```

## Troubleshooting

### Common Issues

1. **Configuration not found**: 
   - **Error**: `FileNotFoundError: Default configuration template not found`
   - **Solution**: Ensure `orca_model_config_default.yaml` exists in one of the searched locations, or specify a custom config with `--config`
   - **Debug**: Check log messages for exact search paths

2. **Custom config not found during initialization**:
   - **Error**: Warning message about falling back to default
   - **Solution**: Verify the custom config file path and ensure it exists in one of the searched locations
   - **Debug**: Use absolute paths for custom config files to avoid path resolution issues

3. **Invalid YAML syntax**:
   - **Error**: `yaml.YAMLError` during configuration loading
   - **Solution**: Validate YAML syntax using online validators or `python -c "import yaml; yaml.safe_load(open('config.yaml'))"`
   - **Debug**: Check line numbers in error messages for specific syntax issues

4. **Configuration search path issues**:
   - **Problem**: Template not found despite existing
   - **Solution**: Ensure file is in one of these locations:
     - Current working directory: `./orca_model_config_default.yaml`
     - Orca subfolder: `./orca/orca_model_config_default.yaml`  
     - Databank parent: `../orca_model_config_default.yaml`
     - Package directory: `<package>/orca/orca_model_config_default.yaml`

2. **Cloud authentication**: 
   - Verify Azure credentials are configured correctly
   - Check that required environment variables are set (see [ENVIRONMENT_VARIABLES.md](../../../ENVIRONMENT_VARIABLES.md))
   - Test authentication with: `az login` (for Azure CLI method)
   - Review authentication configuration in [docs/azure_credential_manager.md](../../../docs/azure_credential_manager.md)
   - Check credential manager logs for authentication method being used
   - Try different authentication methods by adjusting `OPTION_EXCLUDE_*` environment variables
3. **Permission errors**: Check file system permissions for databank directory
4. **Memory issues**: Monitor system resources during large model runs

### Debug Tips

1. **Configuration Issues**:
   - Use `--verbose` flag to see detailed configuration loading messages
   - Check `orca_*.log` for configuration file search paths and resolution
   - Verify YAML syntax with: `python -c "import yaml; print(yaml.safe_load(open('your_config.yaml')))"`
   - List search locations for default config in log messages

2. **General Debugging**:
   - Use `--verbose` flag for detailed logging
   - Check `orca_*.log` for detailed execution information
   - Use `--dry-run` to validate configuration without execution
   - Monitor state file for execution progress

## Integration

The orchestrator is designed to integrate with:
- ActivitySim transportation modeling framework
- Quetzal strategic modeling platform
- PopulationSim population synthesis tool
- Azure Data Lake Storage for cloud workflows
- Azure Batch for distributed cloud computing
- Various transportation modeling tools and utilities

### Azure Services Integration

The orchestrator uses the centralized `AzureCredentialManager` for all Azure service authentication:

- **Azure Data Lake Storage (ADLS)**: File storage and databank synchronization
- **Azure Batch**: Distributed task execution and job management
- **Azure Identity**: Centralized authentication with token caching

This integration provides:
- Consistent authentication across all Azure services
- Automatic token refresh and caching for better performance
- Thread-safe credential management
- Configurable authentication methods

For specific integration details, refer to:
- Sub-component documentation and configuration examples
- [docs/azure_credential_manager.md](../../../docs/azure_credential_manager.md) for Azure authentication
- [ENVIRONMENT_VARIABLES.md](../../../ENVIRONMENT_VARIABLES.md) for environment configuration


## Azure Batch Task Runner

The `batch_task_runner.py` script provides basic task add functionality for Modelers to interact with a Azure Batch Account REST API to send new tasks to perform computing tasks on Azure Cloud.

### Features

- Submits tasks to Azure Batch using the REST API
- Monitors task status with configurable polling
- Uses Azure managed identity for authentication
- Configurable through command-line arguments and environment variables
- Mirrors the functionality of the original Synapse pipeline

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (see `.env.example` for reference):
```bash
# Copy and modify the example file
cp .env.example .env
# Edit .env with your specific values
```

### Environment Variables

The following environment variables are used by the script:

#### Required
- `BATCH_ACCOUNT_ENDPOINT`: Azure Batch account endpoint
- `IMAGE_REGISTRY_ENDPOINT`: Container registry endpoint
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID
- `AZURE_RESOURCE_GROUP`: Azure resource group name
- `MANAGED_IDENTITY_NAME`: Managed identity name for authentication

#### Optional (with defaults)
- `BATCH_API_VERSION`: Batch API version (default: 2024-07-01.20.0)

### Authentication

The script uses the centralized `AzureCredentialManager` from `tlpytools.azure_credential`, which provides consistent authentication across all tlpytools Azure services. The credential manager uses Azure's `DefaultAzureCredential` which supports multiple authentication methods:

1. **Environment Variables**: Service Principal credentials (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
2. **Managed Identity**: When running on Azure resources
3. **Azure CLI**: `az login` 
4. **Azure PowerShell**: PowerShell Azure authentication
5. **Visual Studio Code**: VS Code Azure extension
6. **Interactive Browser**: For development

#### Authentication Configuration

Control which authentication methods are enabled via environment variables:

- `OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL` (default: `true`) - Exclude managed identity
- `OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL` (default: `false`) - Exclude interactive browser
- `OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL` (default: `false`) - Exclude Azure CLI
- `OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL` (default: `false`) - Exclude Azure PowerShell
- `OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL` (default: `false`) - Exclude shared token cache
- `OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL` (default: `false`) - Exclude VS Code

See [ENVIRONMENT_VARIABLES.md](../../../ENVIRONMENT_VARIABLES.md) for complete configuration details.

#### Benefits of Centralized Authentication

- **Token Caching**: Automatic caching and refresh of access tokens for better performance
- **Consistency**: Same authentication behavior across ADLS and Batch operations
- **Thread Safety**: Safe for use in multi-threaded applications
- **Easy Configuration**: Single set of environment variables controls all authentication

For more details about the Azure credential manager, see [docs/azure_credential_manager.md](../../../docs/azure_credential_manager.md).

### Usage

#### Basic Usage
```bash
python batch_task_runner.py --job-id job_large --project my_project --databank my_databank
```

#### Full Example with All Options
```bash
python batch_task_runner.py \
    --job-id job_large \
    --project orca_optimization \
    --databank db_test \
    --python-command orca/orchestrator.py \
    --python-env orca \
    --docker-image orca/orca:develop \
    --max-retry-count 2 \
    --max-wall-clock-time PT8H \
    --poll-interval 45 \
    --max-polls 15
```

### Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--job-id` | Yes | - | Batch job ID where the task will be submitted |
| `--project` | Yes | - | Project name (used in task ID generation) |
| `--databank` | Yes | - | Databank name for the ORCA task |
| `--python-command` | No | `orca/orchestrator.py` | Python script to execute |
| `--python-env` | No | `orca` | Conda environment name |
| `--docker-image` | No | `orca/orca:develop` | Docker image to use |
| `--max-retry-count` | No | `0` | Maximum number of task retries |
| `--max-wall-clock-time` | No | `PT6H` | Maximum wall clock time (ISO 8601) |
| `--poll-interval` | No | `30` | Polling interval in seconds |
| `--max-polls` | No | `10` | Maximum number of polling attempts |

### How It Works

1. **Task Submission**: Creates a unique task ID and submits it to the specified Azure Batch job
2. **Status Monitoring**: Polls the task status at regular intervals
3. **Early Exit**: Stops polling when the task reaches 'running' or 'completed' state
4. **Timeout Handling**: Fails if the task doesn't start within the specified timeout

### Task ID Format

Task IDs are generated using the format: `YYYYMMDD-HHMMSS-{project}-{7-char-guid}`

Example: `20250904-143022-orca_optimization-a1b2c3d`

