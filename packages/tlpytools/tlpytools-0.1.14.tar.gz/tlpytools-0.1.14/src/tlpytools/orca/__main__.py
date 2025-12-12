"""
Entry point for running the ORCA orchestrator as a module.

This allows the module to be executed with:
    python -m tlpytools.orca

This command will execute the CLI interface with argument parsing.
"""

# Load environment variables before importing anything else
try:
    from ..env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

if __name__ == "__main__":
    from .cli import main

    main()
