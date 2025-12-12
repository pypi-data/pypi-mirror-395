"""
TLPyTools - A set of tools for building models at the TransLink Forecasting Team
"""

__version__ = "0.1.14"

# Load environment variables from .env file automatically
from .env_config import load_env_file

# Load .env file on import
load_env_file()

# Core modules that should always be available (minimal dependencies)
from . import log
from .log import UnifiedLogger, setup_logger

# Import azure_credential module (requires azure-identity)
try:
    from . import azure_credential
    from .azure_credential import (
        AzureCredentialManager,
        get_azure_credential,
        get_batch_access_token,
        get_storage_access_token,
    )

    __all__ = [
        "log",
        "UnifiedLogger",
        "setup_logger",
        "azure_credential",
        "AzureCredentialManager",
        "get_azure_credential",
        "get_batch_access_token",
        "get_storage_access_token",
    ]
except ImportError:
    __all__ = ["log", "UnifiedLogger", "setup_logger"]

# Optional modules - try to import but continue if dependencies are missing
_optional_modules = {
    "config": "config module (requires yaml and other dependencies)",
    "adls_server": "adls_server module (requires azure dependencies)",
    "data": "data module (may require geopandas for spatial operations)",
    "data_store": "data_store module (may require geopandas for spatial operations)",
    "sql_server": "sql_server module (requires pyodbc and may require geopandas)",
}

for mod_name, mod_description in _optional_modules.items():
    try:
        module = __import__(f"{__name__}.{mod_name}", fromlist=[mod_name])
        globals()[mod_name] = module
        __all__.append(mod_name)
    except ImportError as e:
        # Create a placeholder that provides helpful error messages
        class MissingModulePlaceholder:
            def __init__(self, name, desc, import_error):
                self._module_name = name
                self._description = desc
                self._import_error = import_error

            def __getattr__(self, name):
                raise ImportError(
                    f"Module '{self._module_name}' is not available: {self._description}. "
                    f"Original error: {self._import_error}"
                )

        globals()[mod_name] = MissingModulePlaceholder(
            mod_name, mod_description, str(e)
        )
        # Still add to __all__ so users can see what's supposed to be available
        __all__.append(mod_name)

# Clean up temporary variables
del _optional_modules

# Optional namespaces that require additional dependencies
try:
    from . import orca

    __all__.append("orca")
except ImportError as e:
    # Create a placeholder for the orca namespace
    class MissingOrcaPlaceholder:
        def __getattr__(self, name):
            raise ImportError(
                "ORCA functionality requires additional dependencies. "
                "Install with: pip install tlpytools[orca]"
            )

    orca = MissingOrcaPlaceholder()
    __all__.append("orca")
