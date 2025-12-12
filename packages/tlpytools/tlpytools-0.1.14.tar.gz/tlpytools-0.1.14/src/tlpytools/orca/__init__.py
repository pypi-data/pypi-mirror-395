"""
ORCA Model Orchestration Module

This module provides tools for orchestrating ORCA model runs, including
initialization, execution, and data synchronization.

This module is optional and requires additional dependencies.
Install with: pip install tlpytools[orca]
"""

# Load environment variables from .env file automatically
try:
    from ..env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

# Lazy imports to avoid importing orchestrator module when the package is imported
# This prevents the RuntimeWarning when using python -m tlpytools.orca
__all__ = ["OrcaOrchestrator"]


def __getattr__(name):
    """Implement lazy importing to avoid loading orchestrator on package import."""
    if name == "OrcaOrchestrator":
        try:
            from .orchestrator import OrcaOrchestrator

            return OrcaOrchestrator
        except ImportError:

            class _MissingOrcaPlaceholder:
                def __init__(self, *args, **kwargs):
                    raise ImportError(
                        "ORCA orchestrator functionality requires additional dependencies. "
                        "Install with: pip install tlpytools[orca]"
                    )

            return _MissingOrcaPlaceholder
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
