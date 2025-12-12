"""
Simple tests to verify Azure Credential Manager refactoring
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone


def test_azure_credential_manager_import():
    """Test that AzureCredentialManager can be imported"""
    from tlpytools.azure_credential import AzureCredentialManager

    assert AzureCredentialManager is not None


def test_azure_credential_manager_singleton():
    """Test that AzureCredentialManager implements singleton pattern"""
    from tlpytools.azure_credential import AzureCredentialManager

    manager1 = AzureCredentialManager.get_instance()
    manager2 = AzureCredentialManager.get_instance()

    # Should be the same instance
    assert manager1 is manager2


def test_azure_credential_manager_convenience_functions():
    """Test convenience functions are available"""
    from tlpytools.azure_credential import (
        get_azure_credential,
        get_batch_access_token,
        get_storage_access_token,
    )

    assert callable(get_azure_credential)
    assert callable(get_batch_access_token)
    assert callable(get_storage_access_token)


def test_adls_server_uses_credential_manager():
    """Test that adls_server uses the credential manager"""
    from tlpytools.adls_server import adls_util
    from tlpytools.azure_credential import AzureCredentialManager

    with patch.object(AzureCredentialManager, "get_credential") as mock_get_credential:
        mock_credential = Mock()
        mock_get_credential.return_value = mock_credential

        credential = adls_util.get_azure_credential()

        # Should call the credential manager
        mock_get_credential.assert_called_once()


def test_batch_task_runner_uses_credential_manager():
    """Test that BatchTaskRunner uses the credential manager"""
    from tlpytools.orca.batch_task_runner import BatchTaskRunner
    from tlpytools.azure_credential import AzureCredentialManager

    # Mock environment variables
    env_vars = {
        "BATCH_ACCOUNT_ENDPOINT": "test.batch.azure.com",
        "IMAGE_REGISTRY_ENDPOINT": "test.azurecr.io",
        "AZURE_SUBSCRIPTION_ID": "test-subscription-id",
        "AZURE_RESOURCE_GROUP": "test-resource-group",
        "MANAGED_IDENTITY_NAME": "test-managed-identity",
    }

    with patch.dict(os.environ, env_vars):
        with patch.object(AzureCredentialManager, "get_instance") as mock_get_instance:
            mock_manager = Mock()
            mock_manager.get_batch_access_token.return_value = "test-token"
            mock_get_instance.return_value = mock_manager

            runner = BatchTaskRunner()

            # Should use the credential manager instance
            assert runner.credential_manager is mock_manager


def test_token_caching():
    """Test that token caching works correctly"""
    from tlpytools.azure_credential import AzureCredentialManager
    from azure.core.credentials import AccessToken

    manager = AzureCredentialManager.get_instance()

    # Mock the credential's get_token method
    mock_credential = Mock()
    future_time = datetime.now(timezone.utc).timestamp() + 3600  # 1 hour from now
    mock_token = AccessToken(token="test-token", expires_on=int(future_time))
    mock_credential.get_token.return_value = mock_token

    with patch.object(manager, "get_credential", return_value=mock_credential):
        # Clear cache first
        manager.clear_token_cache()

        # First call should retrieve token
        token1 = manager.get_access_token("https://batch.core.windows.net/")
        assert token1.token == "test-token"
        assert mock_credential.get_token.call_count == 1

        # Second call should use cached token
        token2 = manager.get_access_token("https://batch.core.windows.net/")
        assert token2.token == "test-token"
        assert mock_credential.get_token.call_count == 1  # Still 1, not 2

        # Force refresh should retrieve new token
        token3 = manager.get_access_token(
            "https://batch.core.windows.net/", force_refresh=True
        )
        assert token3.token == "test-token"
        assert mock_credential.get_token.call_count == 2  # Now 2


def test_credential_manager_reset():
    """Test that credential manager can be reset"""
    from tlpytools.azure_credential import AzureCredentialManager

    manager = AzureCredentialManager.get_instance()

    # Get a credential
    with patch("tlpytools.azure_credential.DefaultAzureCredential") as mock_cred_class:
        mock_cred = Mock()
        mock_cred_class.return_value = mock_cred

        credential1 = manager.get_credential()

        # Reset the manager
        manager.reset()

        # Get credential again - should create new one
        credential2 = manager.get_credential()

        # Should have called DefaultAzureCredential twice
        assert mock_cred_class.call_count == 2


def test_environment_variable_configuration():
    """Test that environment variables configure the credential correctly"""
    from tlpytools.azure_credential import AzureCredentialManager

    # Set up environment variables
    env_vars = {
        "OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL": "true",
        "OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL": "false",
        "OPTION_EXCLUDE_AZURE_CLI_CREDENTIAL": "true",
    }

    with patch.dict(os.environ, env_vars):
        manager = AzureCredentialManager.get_instance()
        manager.reset()  # Force recreation with new env vars

        with patch(
            "tlpytools.azure_credential.DefaultAzureCredential"
        ) as mock_cred_class:
            mock_cred = Mock()
            mock_cred_class.return_value = mock_cred

            credential = manager.get_credential()

            # Check that DefaultAzureCredential was called with correct parameters
            mock_cred_class.assert_called_once()
            call_kwargs = mock_cred_class.call_args[1]

            assert call_kwargs["exclude_managed_identity_credential"] is True
            assert call_kwargs["exclude_interactive_browser_credential"] is False
            assert call_kwargs["exclude_cli_credential"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
