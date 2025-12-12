# Azure Credential Manager

The Azure Credential Manager provides a centralized, thread-safe authentication system for all Azure services used by tlpytools. It implements a singleton pattern with automatic token caching and refresh for improved performance and consistency.

## Overview

The `AzureCredentialManager` class consolidates Azure authentication logic that was previously scattered across different modules (adls_server, batch_task_runner, etc.). This refactoring provides:

- **Centralized authentication**: Single source of truth for Azure credentials
- **Singleton pattern**: Credential instance is reused across all modules
- **Token caching**: Automatic caching and refresh of access tokens
- **Thread safety**: Safe for use in multi-threaded applications
- **Configurable**: Control authentication methods via environment variables
- **Consistent behavior**: Same authentication logic across all Azure services

## Architecture

### Before Refactoring

Previously, each module managed its own Azure credentials:

```python
# adls_server.py had its own credential management
class adls_util:
    AZ_CREDENTIAL = None
    
    @classmethod
    def get_azure_credential(cls):
        if cls.AZ_CREDENTIAL == None:
            cls.AZ_CREDENTIAL = DefaultAzureCredential(...)
        return cls.AZ_CREDENTIAL

# batch_task_runner.py had separate token management
class BatchTaskRunner:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self._access_token = None
        self._token_expires_on = None
```

This led to:
- Inconsistent authentication configuration
- Duplicated credential instances
- Separate token caching logic
- Difficulty in testing and debugging

### After Refactoring

Now all modules use the centralized `AzureCredentialManager`:

```python
from tlpytools.azure_credential import AzureCredentialManager

# All modules use the same credential instance
credential_manager = AzureCredentialManager.get_instance()
credential = credential_manager.get_credential()
```

## Usage

### Basic Usage

```python
from tlpytools.azure_credential import AzureCredentialManager

# Get the credential manager instance (singleton)
credential_manager = AzureCredentialManager.get_instance()

# Get the Azure credential for use with Azure SDK clients
credential = credential_manager.get_credential()

# Use with Azure Storage clients
from azure.storage.filedatalake import FileSystemClient

file_system_client = FileSystemClient(
    account_url="https://myaccount.dfs.core.windows.net",
    file_system_name="mycontainer",
    credential=credential
)
```

### Getting Access Tokens

For services that require access tokens (like Azure Batch API):

```python
# Get an access token for Azure Batch
token = credential_manager.get_batch_access_token()

# Or use the generic method with a specific scope
token = credential_manager.get_access_token("https://batch.core.windows.net/")

# Get an access token for Azure Storage
token = credential_manager.get_storage_access_token()
```

### Convenience Functions

For quick access without getting the manager instance:

```python
from tlpytools.azure_credential import (
    get_azure_credential,
    get_batch_access_token,
    get_storage_access_token
)

# Get credential directly
credential = get_azure_credential()

# Get tokens directly
batch_token = get_batch_access_token()
storage_token = get_storage_access_token()
```

### Integration with Existing Code

The refactored modules maintain backward compatibility:

```python
# adls_server.py - get_azure_credential() still works
from tlpytools.adls_server import adls_util

credential = adls_util.get_azure_credential()  # Now uses AzureCredentialManager

# batch_task_runner.py - automatically uses AzureCredentialManager
from tlpytools.orca.batch_task_runner import BatchTaskRunner

runner = BatchTaskRunner()  # Internally uses AzureCredentialManager
```

## Configuration

The credential manager uses environment variables to configure which authentication methods are enabled. This allows you to customize authentication behavior for different environments.

### Environment Variables

All authentication control variables accept boolean values: `true/false`, `1/0`, `yes/no`, `on/off` (case insensitive).

| Variable | Default | Description |
|----------|---------|-------------|
| `OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL` | `true` | Exclude managed identity authentication |
| `OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL` | `false` | Exclude interactive browser authentication |
| `OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL` | `false` | Exclude shared token cache authentication |
| `OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL` | `false` | Exclude VS Code authentication |
| `OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL` | `false` | Exclude Azure CLI authentication |
| `OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL` | `false` | Exclude Azure PowerShell authentication |

### Configuration Examples

**.env file for local development:**
```bash
# Enable interactive browser authentication for local development
OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL=false

# Disable managed identity (not available on local machine)
OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL=true

# Enable Azure CLI authentication (if you've run 'az login')
OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL=false
```

**.env file for Azure VM with managed identity:**
```bash
# Enable managed identity authentication
OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL=false

# Disable interactive browser (headless environment)
OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL=true

# Disable other methods to force managed identity
OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL=true
OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL=true
```

**.env file for CI/CD pipeline:**
```bash
# Use service principal (via environment variables)
# AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET

# Disable interactive methods
OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL=true
OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL=true
```

## Token Caching

The credential manager automatically caches access tokens to improve performance:

- Tokens are cached per scope (e.g., Batch API, Storage API)
- Automatic refresh when tokens expire (5-minute buffer before expiration)
- Thread-safe cache operations
- Reduces authentication overhead for repeated requests

### Token Cache Example

```python
credential_manager = AzureCredentialManager.get_instance()

# First call - retrieves new token
token1 = credential_manager.get_batch_access_token()

# Subsequent calls - uses cached token (no API call)
token2 = credential_manager.get_batch_access_token()

# Force refresh if needed
token3 = credential_manager.get_batch_access_token(force_refresh=True)

# Clear cache for specific scope
credential_manager.clear_token_cache("https://batch.core.windows.net/")

# Clear all cached tokens
credential_manager.clear_token_cache()
```

## Thread Safety

The credential manager is designed to be thread-safe:

- Singleton instance creation uses double-checked locking
- Token cache operations are protected by locks
- Safe for use in multi-threaded applications

```python
import concurrent.futures

credential_manager = AzureCredentialManager.get_instance()

# Safe to use in multiple threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(credential_manager.get_batch_access_token)
        for _ in range(100)
    ]
    tokens = [f.result() for f in futures]
```

## Advanced Usage

### Custom Credential Creation

```python
# Get the credential with specific configuration
credential = credential_manager.get_credential()

# Force creation of a new credential (e.g., after config change)
credential = credential_manager.get_credential(force_refresh=True)
```

### Reset Credential Manager

Useful for testing or when authentication configuration changes:

```python
# Reset all credentials and tokens
credential_manager.reset()

# Next call will create new credential with current configuration
credential = credential_manager.get_credential()
```

### Working with Multiple Scopes

```python
from azure.core.credentials import AccessToken

# Get tokens for different Azure services
batch_token = credential_manager.get_access_token("https://batch.core.windows.net/")
storage_token = credential_manager.get_access_token("https://storage.azure.com/")
arm_token = credential_manager.get_access_token("https://management.azure.com/")

# Each scope has its own cached token with independent expiration
```

## Migration Guide

If you're updating existing code to use the new Azure Credential Manager:

### For Module Developers

**Before:**
```python
from azure.identity import DefaultAzureCredential

class MyClass:
    def __init__(self):
        self.credential = DefaultAzureCredential(
            exclude_managed_identity_credential=True,
            exclude_interactive_browser_credential=False,
        )
```

**After:**
```python
from tlpytools.azure_credential import AzureCredentialManager

class MyClass:
    def __init__(self):
        self.credential_manager = AzureCredentialManager.get_instance()
        self.credential = self.credential_manager.get_credential()
```

### For Token Management

**Before:**
```python
class MyClass:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self._access_token = None
        self._token_expires_on = None
    
    def _get_access_token(self):
        current_time = datetime.now(timezone.utc)
        if (self._access_token is None or 
            current_time.timestamp() >= (self._token_expires_on - 300)):
            token = self.credential.get_token("https://batch.core.windows.net/")
            self._access_token = token.token
            self._token_expires_on = token.expires_on
        return self._access_token
```

**After:**
```python
class MyClass:
    def __init__(self):
        self.credential_manager = AzureCredentialManager.get_instance()
    
    def _get_access_token(self):
        # Token caching handled automatically
        return self.credential_manager.get_batch_access_token()
```

## Troubleshooting

### Authentication Failures

If you encounter authentication errors:

1. **Check environment variables**: Ensure credential options are set correctly
2. **Verify Azure login**: Run `az login` to verify Azure CLI authentication
3. **Check logs**: Enable debug logging to see which authentication methods are attempted
4. **Test credential creation**: Try creating credential manually to identify the issue

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Try to get credential
from tlpytools.azure_credential import get_azure_credential
credential = get_azure_credential()
```

### Token Expiration Issues

If you're getting token expiration errors:

```python
# Force refresh of token
credential_manager = AzureCredentialManager.get_instance()
token = credential_manager.get_batch_access_token(force_refresh=True)

# Or clear the cache and get a new token
credential_manager.clear_token_cache()
token = credential_manager.get_batch_access_token()
```

### Credential Configuration Changes

If you change authentication configuration:

```python
# Reset the credential manager to pick up new configuration
credential_manager = AzureCredentialManager.get_instance()
credential_manager.reset()

# Next call will use new configuration
credential = credential_manager.get_credential()
```

## Best Practices

1. **Use the singleton**: Always get the instance with `get_instance()` rather than creating new instances
2. **Configure via environment**: Use environment variables to configure authentication methods
3. **Trust the cache**: Don't manually manage token expiration; let the manager handle it
4. **Use convenience functions**: For simple use cases, use the module-level functions
5. **Check logs**: Enable logging to understand which authentication method is being used
6. **Test thoroughly**: Test authentication in all deployment environments

## Benefits

The centralized Azure Credential Manager provides:

- **Simplified code**: Less boilerplate for credential management
- **Better performance**: Token caching reduces authentication overhead
- **Consistency**: Same authentication behavior across all modules
- **Easier testing**: Single point to mock authentication
- **Better debugging**: Centralized logging of authentication attempts
- **Flexibility**: Easy to configure authentication methods via environment variables
- **Thread safety**: Safe for use in multi-threaded applications
- **Maintainability**: Changes to authentication logic only need to be made in one place

## See Also

- [ENVIRONMENT_VARIABLES.md](../ENVIRONMENT_VARIABLES.md) - Full list of environment variables
- [AZURE_AUTHENTICATION_REFACTOR.md](../AZURE_AUTHENTICATION_REFACTOR.md) - Details about the authentication refactoring
- [Azure Identity Documentation](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme) - Official Azure Identity library documentation
