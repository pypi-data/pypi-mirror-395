"""
Azure Credential Manager

This module provides a centralized, reusable Azure credential manager for all
tlpytools modules that need to authenticate with Azure services (ADLS, Batch, etc.).

Key Features:
- Singleton pattern for credential reuse across modules
- Configurable DefaultAzureCredential with environment variable support
- Token caching with automatic refresh for Azure Batch API
- Support for multiple Azure service scopes
- Thread-safe credential and token management
"""

# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded, get_env_bool

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    def get_env_bool(key: str, default: bool = False, required: bool = False) -> bool:
        """Fallback function if env_config is not available"""
        import os

        value = os.environ.get(key)
        if value is None:
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default

        value_lower = value.lower().strip()
        if value_lower in ("true", "1", "yes", "on"):
            return True
        elif value_lower in ("false", "0", "no", "off"):
            return False
        else:
            return default


import logging
import threading
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AccessToken


class AzureCredentialManager:
    """
    Centralized Azure credential manager with singleton pattern.

    This class provides a thread-safe, singleton instance for managing Azure credentials
    across all tlpytools modules. It handles:
    - DefaultAzureCredential creation with configurable options
    - Token caching and automatic refresh for various Azure services
    - Support for multiple service scopes (Batch, Storage, etc.)

    Environment Variables:
        OPTION_EXCLUDE_MANAGED_IDENTITY_CREDENTIAL: Exclude managed identity auth (default: True)
        OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL: Exclude browser auth (default: False)
        OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL: Exclude shared token cache (default: False)
        OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL: Exclude VS Code auth (default: False)
        OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL: Exclude Azure CLI auth (default: False)
        OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL: Exclude PowerShell auth (default: False)

    Usage:
        # Get the credential manager instance
        credential_manager = AzureCredentialManager.get_instance()

        # Get the Azure credential for use with Azure SDK clients
        credential = credential_manager.get_credential()

        # Get an access token for a specific Azure service
        token = credential_manager.get_access_token("https://batch.core.windows.net/")

        # Use with Azure Storage clients
        file_system_client = FileSystemClient(
            account_url=account_url,
            file_system_name=container_name,
            credential=credential_manager.get_credential()
        )
    """

    _instance: Optional["AzureCredentialManager"] = None
    _lock = threading.Lock()

    def __new__(cls):
        """Implement singleton pattern with thread safety."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the credential manager (only runs once due to singleton)."""
        # Only initialize once
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._logger = logging.getLogger("AzureCredentialManager")
        self._credential: Optional[DefaultAzureCredential] = None
        self._token_cache: Dict[str, Dict[str, Any]] = {}
        self._token_cache_lock = threading.Lock()
        self._initialized = True

        self._logger.debug("AzureCredentialManager initialized")

    @classmethod
    def get_instance(cls) -> "AzureCredentialManager":
        """
        Get the singleton instance of AzureCredentialManager.

        Returns:
            AzureCredentialManager: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_credential(self, force_refresh: bool = False) -> DefaultAzureCredential:
        """
        Get the Azure credential, creating it if necessary.

        Args:
            force_refresh: Force creation of a new credential instance

        Returns:
            DefaultAzureCredential: The Azure credential instance
        """
        if self._credential is None or force_refresh:
            with self._lock:
                if self._credential is None or force_refresh:
                    if force_refresh and self._credential is not None:
                        self._logger.info(
                            "Forcing credential refresh due to authentication issues"
                        )
                        # Clear token cache when forcing refresh
                        self.clear_token_cache()
                    self._credential = self._create_credential()

        return self._credential

    def _create_credential(self) -> DefaultAzureCredential:
        """
        Create a new DefaultAzureCredential with configuration from environment variables.

        Returns:
            DefaultAzureCredential: Configured credential instance
        """
        self._logger.debug("Creating new DefaultAzureCredential...")

        # Get configuration from environment variables
        # Note: typo in original env var name preserved for backward compatibility
        exclude_managed_identity = get_env_bool(
            "OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL", default=False
        )
        exclude_interactive_browser = get_env_bool(
            "OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL", default=True
        )
        exclude_shared_token_cache = get_env_bool(
            "OPTION_EXCLUDE_SHARED_TOKEN_CACHE_CREDENTIAL", default=False
        )
        exclude_visual_studio_code = get_env_bool(
            "OPTION_EXCLUDE_VISUAL_STUDIO_CODE_CREDENTIAL", default=True
        )
        exclude_azure_cli = get_env_bool(
            "OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL", default=False
        )
        exclude_azure_powershell = get_env_bool(
            "OPTION_EXCLUDE_AZURE_POWERSHELL_CREDENTIAL", default=False
        )

        # Log the configuration
        self._logger.debug("Azure Credential Configuration:")
        self._logger.debug("  Exclude Managed Identity: %s", exclude_managed_identity)
        self._logger.debug(
            "  Exclude Interactive Browser: %s", exclude_interactive_browser
        )
        self._logger.debug(
            "  Exclude Shared Token Cache: %s", exclude_shared_token_cache
        )
        self._logger.debug(
            "  Exclude Visual Studio Code: %s", exclude_visual_studio_code
        )
        self._logger.debug("  Exclude Azure CLI: %s", exclude_azure_cli)
        self._logger.debug("  Exclude Azure PowerShell: %s", exclude_azure_powershell)

        credential = DefaultAzureCredential(
            exclude_managed_identity_credential=exclude_managed_identity,
            exclude_interactive_browser_credential=exclude_interactive_browser,
            exclude_shared_token_cache_credential=exclude_shared_token_cache,
            exclude_visual_studio_code_credential=exclude_visual_studio_code,
            exclude_cli_credential=exclude_azure_cli,
            exclude_powershell_credential=exclude_azure_powershell,
        )

        self._logger.info("DefaultAzureCredential created successfully")
        return credential

    def get_access_token(self, scope: str, force_refresh: bool = False) -> AccessToken:
        """
        Get an access token for a specific Azure service scope.

        This method implements token caching with automatic refresh. Tokens are
        cached per scope and automatically refreshed when they expire or are about
        to expire (5 minute buffer).

        Args:
            scope: The Azure service scope (e.g., "https://batch.core.windows.net/")
            force_refresh: Force retrieval of a new token even if cached token is valid

        Returns:
            AccessToken: The access token object containing the token string and expiry

        Common scopes:
            - Azure Batch: "https://batch.core.windows.net/"
            - Azure Storage: "https://storage.azure.com/"
            - Azure Resource Manager: "https://management.azure.com/"
        """
        current_time = datetime.now(timezone.utc)

        # Check if we have a cached token that's still valid
        with self._token_cache_lock:
            if scope in self._token_cache and not force_refresh:
                cached = self._token_cache[scope]
                token_expires_on = cached.get("expires_on", 0)

                # Refresh if token is expired or about to expire (5 minute buffer)
                if current_time.timestamp() < (token_expires_on - 300):
                    self._logger.debug("Using cached access token for scope: %s", scope)
                    return AccessToken(
                        token=cached["token"], expires_on=token_expires_on
                    )

        # Need to get a new token
        self._logger.debug("Retrieving new access token for scope: %s", scope)
        credential = self.get_credential()
        token = credential.get_token(scope)

        # Cache the token
        with self._token_cache_lock:
            self._token_cache[scope] = {
                "token": token.token,
                "expires_on": token.expires_on,
                "retrieved_at": current_time.timestamp(),
            }

        self._logger.debug(
            "Access token retrieved successfully for scope: %s (expires: %s)",
            scope,
            datetime.fromtimestamp(token.expires_on, tz=timezone.utc).isoformat(),
        )

        return token

    def get_batch_access_token(self, force_refresh: bool = False) -> str:
        """
        Get an access token for Azure Batch API.

        This is a convenience method for getting Batch API tokens.

        Args:
            force_refresh: Force retrieval of a new token

        Returns:
            str: The access token string
        """
        token = self.get_access_token("https://batch.core.windows.net/", force_refresh)
        return token.token

    def get_storage_access_token(self, force_refresh: bool = False) -> str:
        """
        Get an access token for Azure Storage.

        This is a convenience method for getting Storage API tokens.

        Args:
            force_refresh: Force retrieval of a new token

        Returns:
            str: The access token string
        """
        token = self.get_access_token("https://storage.azure.com/", force_refresh)
        return token.token

    def clear_token_cache(self, scope: Optional[str] = None) -> None:
        """
        Clear the token cache.

        Args:
            scope: If provided, clear only the token for this scope.
                   If None, clear all cached tokens.
        """
        with self._token_cache_lock:
            if scope is not None:
                if scope in self._token_cache:
                    del self._token_cache[scope]
                    self._logger.debug("Cleared token cache for scope: %s", scope)
            else:
                self._token_cache.clear()
                self._logger.debug("Cleared all token caches")

    def reset(self) -> None:
        """
        Reset the credential manager, clearing all cached credentials and tokens.

        This is useful for testing or when credential configuration changes.
        """
        with self._lock:
            self._credential = None
            self.clear_token_cache()
            self._logger.debug("AzureCredentialManager reset complete")


# Convenience functions for backward compatibility and ease of use
def get_azure_credential(force_refresh: bool = False) -> DefaultAzureCredential:
    """
    Get the Azure credential from the singleton credential manager.

    Args:
        force_refresh: Force creation of a new credential instance

    Returns:
        DefaultAzureCredential: The Azure credential instance
    """
    return AzureCredentialManager.get_instance().get_credential(force_refresh)


def get_batch_access_token(force_refresh: bool = False) -> str:
    """
    Get an access token for Azure Batch API.

    Args:
        force_refresh: Force retrieval of a new token

    Returns:
        str: The access token string
    """
    return AzureCredentialManager.get_instance().get_batch_access_token(force_refresh)


def get_storage_access_token(force_refresh: bool = False) -> str:
    """
    Get an access token for Azure Storage.

    Args:
        force_refresh: Force retrieval of a new token

    Returns:
        str: The access token string
    """
    return AzureCredentialManager.get_instance().get_storage_access_token(force_refresh)


__all__ = [
    "AzureCredentialManager",
    "get_azure_credential",
    "get_batch_access_token",
    "get_storage_access_token",
]
