# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

import os
import logging
import platform
import datetime
import time
import contextlib
import numpy as np
import pandas as pd


def setup_logger(name, log_file=None, level=logging.INFO, console_output=True):
    """
    Set up a logger with file and optionally console output.

    Args:
        name (str): Logger name
        log_file (str, optional): Path to log file
        level (int): Logging level (default: INFO)
        console_output (bool): Whether to output to console

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Log initial information
    logger.info("=== Logging initialized ===")
    logger.info(f"Time: {datetime.datetime.now()}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Platform: {platform.platform()}")

    # Log version information
    try:
        logger.info(f"numpy: {np.__version__}")
        logger.info(f"pandas: {pd.__version__}")
    except Exception as e:
        logger.warning(f"Could not log version information: {e}")

    return logger


def log_with_context(logger, level, message, extra_data=None):
    """
    Log a message with additional context data.

    Args:
        logger (logging.Logger): Logger instance
        level (int): Logging level
        message (str): Log message
        extra_data (dict, optional): Additional context data
    """
    if extra_data:
        context_str = " | ".join([f"{k}={v}" for k, v in extra_data.items()])
        full_message = f"{message} | {context_str}"
    else:
        full_message = message

    logger.log(level, full_message)


@contextlib.contextmanager
def performance_timer(logger, operation_name):
    """
    Context manager for timing operations and logging performance.

    Args:
        logger (logging.Logger): Logger instance
        operation_name (str): Name of the operation being timed

    Usage:
        with performance_timer(logger, 'data_processing'):
            # ... your code here
    """
    start_time = time.time()
    logger.info(f"Starting {operation_name}")

    try:
        yield
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Completed {operation_name} in {duration:.2f} seconds")
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"Failed {operation_name} after {duration:.2f} seconds: {e}")
        raise


def configure_pandas_logging():
    """
    Configure pandas to reduce noisy logging.
    """
    # Suppress pandas PerformanceWarning
    import warnings

    warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

    # Set pandas options for better logging
    pd.set_option("mode.chained_assignment", None)


class UnifiedLogger:
    """Unified logger class that provides consistent logging across tlpytools."""

    _initialized_loggers = set()  # Track which loggers have been initialized

    def __init__(
        self,
        logger: logging.Logger = None,
        name: str = None,
        log_file: str = None,
        level: int = logging.INFO,
    ):
        """
        Initialize unified logger.

        Args:
            logger: Optional existing logger instance. If provided, uses this logger.
            name: Logger name. If not provided and logger is None, uses the class name.
            log_file: Log file path. If not provided, creates one based on the class name.
            level: Logging level (default: INFO).
        """
        if logger is not None:
            # Use provided logger
            self.log = logger
        else:
            # Create new logger
            if name is None:
                name = type(self).__name__

            if log_file is None:
                log_file = f"{name}.log"

            self.log = setup_logger(name, log_file, level)

        # Log initialization info only once per logger
        logger_id = self.log.name if hasattr(self.log, "name") else str(id(self.log))
        if logger_id not in self._initialized_loggers:
            self._log_initialization_info()
            self._initialized_loggers.add(logger_id)

    def _log_initialization_info(self):
        """Log standard initialization information."""
        self.log.info("=== Logging initialized ===")
        self.log.info("Time: %s", datetime.datetime.now())
        self.log.info("Working directory: %s", os.getcwd())
        self.log.info("Platform: %s", platform.platform())

        # Log version information
        try:
            self.log.info("numpy: %s", np.__version__)
            self.log.info("pandas: %s", pd.__version__)
        except Exception as e:
            self.log.warning("Could not log version information: %s", str(e))


class logger(UnifiedLogger):
    """Legacy logger class for backwards compatibility."""

    def __init__(self) -> None:
        # Initialize with None logger so UnifiedLogger creates a new one
        super().__init__(logger=None)

    def init_logger(self, logFile=None, computer="run"):
        """Legacy method for backwards compatibility."""
        # if log file name is None, use source class name
        if logFile == None:
            filename = "{}.log".format(type(self).__name__)
            logFile = filename

        # get computer name
        name = "{}_{}".format(computer, platform.node())

        # Create new logger using the modern setup_logger function
        self.log = setup_logger(name, logFile, logging.DEBUG)

        # Note: Don't call _log_initialization_info() again since setup_logger already logs initialization


class analyzer:
    """not implemented: analyze performance of log by analyzing time points"""

    def __init__(self) -> None:
        self.log = None
