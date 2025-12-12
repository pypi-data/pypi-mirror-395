# Environment Variables Configuration

This document lists all environment variables used by tlpytools to avoid hardcoded secrets and sensitive information.

## Quick Start

1. Copy the example file: `cp .env.example .env` (or `copy .env.example .env` on Windows)
2. Edit `.env` with your actual Azure resource values
3. The package will automatically load your environment variables

## Automatic .env File Loading

**NEW**: TLPyTools now automatically loads environment variables from `.env` files when importing any tlpytools module or using the command line interface. The system uses an enhanced discovery logic with fallback support:

1. **Current working directory**: Checks for `.env` in the current directory
2. **Project root discovery**: Walks up parent directories until finding a `.git` folder (indicating project root)
3. **Fallback to tlpytools installation**: If no project `.env` files are found, automatically falls back to the `.env` file in the tlpytools installation directory
4. **Safe error handling**: Stops searching on permission errors or when reaching filesystem root

**No additional setup required** - TLPyTools will automatically discover and load project-specific `.env` files when available, or fall back to default configuration from the tlpytools installation directory!

### Example .env File
Copy `.env.example` to `.env` and customize the values:

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
notepad .env  # Windows
# or
nano .env     # Linux/macOS
```

### Environment Loading Features
- **Automatic discovery**: Searches current directory and parent directories
- **Intelligent fallback**: Falls back to tlpytools installation directory when no project `.env` files exist
- **Safe defaults**: Won't override existing environment variables
- **Cross-module support**: All tlpytools and orca modules load environment automatically
- **CLI integration**: Command-line tools automatically load .env files
- **Error handling**: Graceful fallback if python-dotenv is not installed
- **Project override**: Project-specific `.env` files take precedence over default configuration

## Required Environment Variables

**IMPORTANT**: The following environment variables are now **strictly enforced**. Applications will fail to start or initialize if these variables are not set or are empty.

### Azure Data Lake Storage (ADLS)
- `ORCA_ADLS_URL`: Azure Data Lake Storage endpoint URL (without https:// prefix)
  - Example: `yourstorageaccount.dfs.core.windows.net`
  - Used by: orchestrator.py, example files
  - **Strictly Required**: Application will fail with ValueError if not set
  - Note: The https:// prefix is automatically added by the application
  - **Breaking Change**: Previously used "yourstorageaccount.dfs.core.windows.net" as default

### Azure SQL Server
- `TLPT_AZURE_SQL_URI`: Azure SQL Server URI
  - Example: `yourserver.database.windows.net`
  - Used by: sql_server.py (azure_td_tables class)
  - **Strictly Required**: Class initialization will fail with ValueError if not set

### Azure Batch Service
All Azure Batch environment variables are now strictly enforced during BatchTaskRunner initialization:

- `BATCH_ACCOUNT_ENDPOINT`: Azure Batch account endpoint
  - Example: `yourbatch.canadacentral.batch.azure.com`
  - Used by: batch_task_runner.py
  - **Strictly Required**: BatchTaskRunner initialization will fail with ValueError if not set

- `IMAGE_REGISTRY_ENDPOINT`: Container registry endpoint
  - Example: `yourregistry.azurecr.io`
  - Used by: batch_task_runner.py
  - **Strictly Required**: BatchTaskRunner initialization will fail with ValueError if not set

- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID
  - Example: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
  - Used by: batch_task_runner.py
  - **Strictly Required**: BatchTaskRunner initialization will fail with ValueError if not set

- `AZURE_RESOURCE_GROUP`: Azure resource group name
  - Example: `your-resource-group`
  - Used by: batch_task_runner.py
  - **Strictly Required**: BatchTaskRunner initialization will fail with ValueError if not set

- `MANAGED_IDENTITY_NAME`: Managed identity name for authentication
  - Example: `your-managed-identity`
  - Used by: batch_task_runner.py
  - **Strictly Required**: BatchTaskRunner initialization will fail with ValueError if not set

### Error Behavior
When required environment variables are missing, you will see errors like:
```
ValueError: Required environment variable 'ORCA_ADLS_URL' is not set or is empty. 
Please set this variable in your .env file or system environment. 
See ENVIRONMENT_VARIABLES.md for details.
```

## Optional Environment Variables

### Azure Batch API
- `BATCH_API_VERSION`: Azure Batch API version
  - Default: `2024-07-01.20.0`
  - Used by: batch_task_runner.py

### Cache Configuration
- `TLPT_ADLS_CACHE_DIR`: Directory for ADLS cache files
  - Default: `C:/Temp/tlpytools/adls`
  - Used by: adls_server.py

### SQL Server Authentication
- `ms_sql_secret`: Encrypted password for SQL Server access
  - Used by: sql_server.py for encrypted offline mode
  - Optional: only needed for encrypted local data access

- `ms_sql_secret_salt`: Salt for encrypted password
  - Used by: sql_server.py for encrypted offline mode
  - Optional: only needed for encrypted local data access

- `ms_sql_salt`: Salt for data encryption
  - Used by: sql_server.py for encrypted offline mode
  - Optional: only needed for encrypted local data access

- `ms_sql_path`: Path to local SQL data
  - Used by: sql_server.py for encrypted offline mode
  - Optional: only needed for encrypted local data access

### Azure Authentication (for Service Principal)
- `AZURE_CLIENT_ID`: Azure service principal client ID
- `AZURE_TENANT_ID`: Azure tenant ID
- `AZURE_CLIENT_SECRET`: Azure service principal client secret

Note: These are only needed if using Service Principal authentication. The applications use DefaultAzureCredential which supports multiple authentication methods.

### Azure Credential Options

The Azure Credential Manager uses these environment variables to configure the DefaultAzureCredential authentication chain. These options control which authentication methods are attempted when connecting to Azure services.

- `OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL`: Control whether to exclude managed identity authentication
  - Default: `true` (excludes managed identity)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py, adls_server.py, batch_task_runner.py
  - Set to `false` when running on Azure VMs with managed identity

- `OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL`: Control whether to exclude interactive browser authentication
  - Default: `false` (allows interactive browser authentication)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py, adls_server.py, batch_task_runner.py
  - Set to `true` to disable browser-based authentication in headless environments

- `OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL`: Control whether to exclude shared token cache authentication
  - Default: `false` (allows shared token cache)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py
  - Set to `true` to disable shared token cache authentication

- `OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL`: Control whether to exclude VS Code authentication
  - Default: `false` (allows VS Code authentication)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py
  - Set to `true` to disable VS Code authentication

- `OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL`: Control whether to exclude Azure CLI authentication
  - Default: `false` (allows Azure CLI authentication)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py
  - Set to `true` to disable Azure CLI authentication

- `OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL`: Control whether to exclude Azure PowerShell authentication
  - Default: `false` (allows Azure PowerShell authentication)
  - Valid values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive)
  - Used by: azure_credential.py
  - Set to `true` to disable Azure PowerShell authentication

**Note**: The Azure Credential Manager provides a centralized authentication system for all Azure services used by tlpytools. It implements a singleton pattern with token caching for improved performance and consistency across modules.

## Setting Environment Variables

### Method 1: .env File (Recommended)
Create a `.env` file in your project directory. TLPyTools will automatically load it. If no project `.env` file exists, TLPyTools will fall back to the default configuration in the tlpytools installation directory.

```
ORCA_ADLS_URL=yourstorageaccount.dfs.core.windows.net
TLPT_AZURE_SQL_URI=yourserver.database.windows.net
BATCH_ACCOUNT_ENDPOINT=yourbatch.canadacentral.batch.azure.com
IMAGE_REGISTRY_ENDPOINT=yourregistry.azurecr.io
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_GROUP=your-resource-group
MANAGED_IDENTITY_NAME=your-managed-identity

# Azure Authentication Control
OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL=true
OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL=false
```

### Method 2: System Environment Variables

### Windows (Command Prompt)
```cmd
set ORCA_ADLS_URL=yourstorageaccount.dfs.core.windows.net
set TLPT_AZURE_SQL_URI=yourserver.database.windows.net
```

### Windows (PowerShell)
```powershell
$env:ORCA_ADLS_URL="yourstorageaccount.dfs.core.windows.net"
$env:TLPT_AZURE_SQL_URI="yourserver.database.windows.net"
```

### Linux/macOS
```bash
export ORCA_ADLS_URL="yourstorageaccount.dfs.core.windows.net"
export TLPT_AZURE_SQL_URI="yourserver.database.windows.net"
```

### Using .env file
Create a `.env` file in your project root (this is the same as Method 1 above):
```
ORCA_ADLS_URL=yourstorageaccount.dfs.core.windows.net
TLPT_AZURE_SQL_URI=yourserver.database.windows.net
BATCH_ACCOUNT_ENDPOINT=yourbatch.canadacentral.batch.azure.com
IMAGE_REGISTRY_ENDPOINT=yourregistry.azurecr.io
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_GROUP=your-resource-group
MANAGED_IDENTITY_NAME=your-managed-identity
```

## .env File Discovery and Fallback Behavior

TLPyTools uses an intelligent discovery system to locate and load environment variables:

### Discovery Order
1. **Project-specific .env files**: Searches current working directory and parent directories up to the project root (indicated by a `.git` folder)
2. **Fallback to installation directory**: If no project `.env` files are found, automatically uses the `.env` file from the tlpytools installation directory

### Benefits of Fallback System
- **Default configuration**: Provides working default values for Azure resources without requiring project setup
- **Project override capability**: Project-specific `.env` files take precedence over defaults when present
- **Seamless development**: New projects work immediately with default configuration, existing projects maintain their custom settings
- **No configuration required**: Works out-of-the-box for standard Azure environments

### Example Scenarios

**Scenario 1: New Project (No .env file)**
```
Project Directory: /path/to/new/project
├── main.py
└── (no .env file)

Result: Uses fallback configuration from tlpytools installation
Environment: Default Azure resources from tlpytools/.env
```

**Scenario 2: Existing Project (With .env file)**
```
Project Directory: /path/to/existing/project
├── .env (PROJECT_VAR=custom_value, ORCA_ADLS_URL=project.storage.net)
├── main.py
└── .git/

Result: Uses project-specific configuration
Environment: Custom values from project .env file override defaults
```

## Verification

To verify that your environment variables are loaded correctly:

```python
import tlpytools
import os

print("ORCA_ADLS_URL:", os.getenv("ORCA_ADLS_URL"))
print("TLPT_AZURE_SQL_URI:", os.getenv("TLPT_AZURE_SQL_URI"))
```

Or use the CLI:
```bash
python -c "import tlpytools; import os; print('ORCA_ADLS_URL:', os.getenv('ORCA_ADLS_URL'))"
```

## GitHub CI/CD Integration

**IMPORTANT**: The GitHub workflows have been updated to handle required environment variables during testing:

- **test.yml**: Automatically copies `.env.example` to `.env` before running tests
- **deploy.yml**: Automatically copies `.env.example` to `.env` before running tests
- **No secrets required**: Tests use example values from `.env.example`
- **No .env files committed**: The `.env` file is never committed to version control

This ensures that:
1. CI/CD pipelines don't fail due to missing required environment variables
2. Tests can run with example values without requiring real Azure credentials
3. Security is maintained by not committing real credentials

### For Local Development
To set up your environment variables for local development:

**Step 1: Copy and edit the example file from tlpytools package directory**
```bash
# Copy the example file from tlpytools installation
cp /path/to/tlpytools/.env.example .env

# On Windows
copy "C:\ProgramData\tlpytools\.env.example" .env
```

```bash
# Edit with your values
notepad .env  # Windows
# or
nano .env     # Linux/macOS
```

Alternatively, you may copy a production-ready .env file already prepared. TransLink staff with approcipate access can find the file in Teams SharePoint under this path - `Team - R&A Forecasting\ABM Development\_abm_input_data\orca_env\.env`.

**Step 2: Choose where to save your production-ready .env file**

You have two options for where to place your configured `.env` file:

**Option A: Project Directory (Recommended for project-specific settings)**
- Save the `.env` file in your project root directory
- Benefits:
  - Project-specific configuration
  - Can be different for each project
  - Takes precedence over package defaults
  - Keeps sensitive credentials isolated per project
- Location: `your-project/.env`
- **Important**: Never commit this file to version control

**Option B: Package Directory (Recommended for shared default settings)**
- Save the `.env` file in the tlpytools installation directory
- Benefits:
  - Shared default configuration across all projects
  - No need to set up environment for new projects
  - Centralized credential management
- Location: `/path/to/tlpytools/.env` (or `C:\ProgramData\tlpytools\.env` on Windows)
- Use case: When you want the same Azure resources for all tlpytools projects

**Recommendation**: Use Option A (project directory) for production work with different environments, and Option B (package directory) for development with consistent Azure resources. Option A will have precedence over Option B if both approaches are used.

## Security Notes

1. **Never commit environment files with real values to version control**
2. **Use Azure Key Vault for production secrets management**
3. **Ensure proper access controls are in place for all Azure resources**
4. **Regularly rotate credentials and access keys**
5. **Use Managed Identity when running on Azure resources for enhanced security**


## Troubleshooting

### Environment Variable Errors
If you encounter errors like "Required environment variable 'XXX' is not set or is empty":

1. **Check if .env file exists**: Look for `.env` file in your project root or current directory
2. **Create .env file**: Copy from example: `cp .env.example .env`
3. **Verify .env content**: Open `.env` and ensure required variables are set with actual values
4. **Check for empty values**: Ensure variables aren't just empty strings
5. **Verify file location**: Place `.env` in project root (where `.git` folder exists) or current working directory
6. **Check fallback configuration**: If no project `.env` exists, verify the tlpytools installation directory contains a valid `.env` file with required variables

### Authentication Errors
If you encounter Azure authentication errors after setting environment variables:

1. **Verify all required environment variables are set correctly**
2. **Check that your Azure credentials are valid**
3. **Ensure your Azure resources exist and are accessible**
4. **Verify network connectivity to Azure services**
5. **Check Azure resource permissions and access policies**
6. **Test with Azure CLI**: Run `az login` to verify your Azure authentication

### Import Failures
If package imports fail completely:
1. Check if you're trying to import classes that require environment variables (like `azure_td_tables`)
2. Set up your `.env` file before importing these classes
3. Consider importing only the modules you need to avoid unnecessary dependency loading
