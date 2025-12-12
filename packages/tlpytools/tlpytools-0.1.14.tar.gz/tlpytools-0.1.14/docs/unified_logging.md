# Unified Logging System in TLPyTools

## Overview

The TLPyTools library now features a unified logging system that provides consistent logging behavior across all classes and modules. This system allows for both unified logging (where multiple classes share the same log file) and separate logging (where each class has its own log file).

## Key Features

1. **Unified Logging**: Multiple classes can share the same logger instance and log to the same file
2. **Automatic Logger Creation**: If no logger is provided, classes automatically create their own logger
3. **Backwards Compatibility**: Existing code using the legacy `logger` class continues to work unchanged
4. **Consistent Formatting**: All loggers use the same format and include system information
5. **Easy Integration**: Simply inherit from `UnifiedLogger` or pass a logger instance to class constructors

## Main Classes and Functions

### `UnifiedLogger`
Base class that provides unified logging capabilities to any class that inherits from it.

### `setup_logger(name, log_file, level, console_output)`
Function to create a new logger instance with consistent formatting.

### `logger` (Legacy)
Backwards-compatible legacy logger class that now uses the unified system under the hood.

## Usage Patterns

### Pattern 1: Separate Loggers (Default Behavior)

Each class creates its own logger and log file:

```python
from tlpytools.data_store import DataStore
from tlpytools.log import UnifiedLogger

class MyClass(UnifiedLogger):
    def __init__(self):
        super().__init__()  # Creates MyClass.log
        
    def do_work(self):
        self.log.info("Doing some work")

# Each class gets its own log file
ds = DataStore(project_name="project1")  # Creates DataStore_project1.log
my_class = MyClass()  # Creates MyClass.log
```

### Pattern 2: Unified Logging (Shared Logger)

Multiple classes share the same logger and log file:

```python
from tlpytools.log import setup_logger
from tlpytools.data_store import DataStore

# Create a shared logger
shared_logger = setup_logger("MyProject", "my_project.log")

# All these classes will log to my_project.log
ds1 = DataStore(project_name="data1", logger=shared_logger)
ds2 = DataStore(project_name="data2", logger=shared_logger)

class MyClass(UnifiedLogger):
    def __init__(self, logger=None):
        super().__init__(logger=logger)
        
my_class = MyClass(logger=shared_logger)
```

### Pattern 3: Legacy Compatibility

Existing code continues to work unchanged:

```python
from tlpytools.log import logger

class MyLegacyClass(logger):
    def __init__(self):
        super().__init__()
        self.init_logger("my_legacy.log")
        
    def do_work(self):
        self.log.info("Legacy logging still works")
```

## Classes with Unified Logging Support

The following classes now support unified logging:

- `DataStore`: Data storage and management
- `ms_sql_tables`: SQL Server interactions  
- `adls_util`: Azure Data Lake Storage utilities
- `BatchTaskRunner`: Azure Batch task execution (already supported)
- Any class inheriting from `UnifiedLogger`

## Implementation Guidelines

### For New Classes

When creating new classes, inherit from `UnifiedLogger`:

```python
from tlpytools.log import UnifiedLogger
import logging

class MyNewClass(UnifiedLogger):
    def __init__(self, logger: logging.Logger = None, other_params=None):
        # Initialize logging first
        super().__init__(logger=logger, name="MyNewClass")
        
        # Your initialization code here
        self.log.info("MyNewClass initialized")
        
    def my_method(self):
        self.log.info("Executing my_method")
        try:
            # Your code here
            self.log.debug("Debug information")
        except Exception as e:
            self.log.error("Error in my_method: %s", str(e))
            raise
```

### For Existing Classes

Add unified logging support to existing classes:

```python
# Before
class ExistingClass:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

# After
from tlpytools.log import UnifiedLogger
import logging

class ExistingClass(UnifiedLogger):
    def __init__(self, param1, param2, logger: logging.Logger = None):
        # Add logger parameter and initialize logging
        super().__init__(logger=logger, name="ExistingClass")
        
        self.param1 = param1
        self.param2 = param2
        
        self.log.info("ExistingClass initialized with params: %s, %s", param1, param2)
```

## Logging Best Practices

1. **Use appropriate log levels**:
   - `DEBUG`: Detailed diagnostic information
   - `INFO`: General information about program execution
   - `WARNING`: Something unexpected happened but the program can continue
   - `ERROR`: A serious problem occurred

2. **Use lazy formatting**:
   ```python
   # Good
   self.log.info("Processing %d items", item_count)
   
   # Avoid
   self.log.info(f"Processing {item_count} items")
   ```

3. **Log exceptions properly**:
   ```python
   try:
       # risky operation
       pass
   except Exception as e:
       self.log.error("Operation failed: %s", str(e))
       # or for debugging, include traceback:
       self.log.exception("Operation failed")
   ```

4. **Log important state changes**:
   ```python
   self.log.info("Starting data processing")
   # ... processing code ...
   self.log.info("Data processing completed successfully")
   ```

## Migration Guide

### From Print Statements

Replace print statements with appropriate logging:

```python
# Before
print(f"Processing file: {filename}")
print(f"Warning: {warning_message}")

# After
self.log.info("Processing file: %s", filename)
self.log.warning("Warning: %s", warning_message)
```

### From Legacy logger Class

Existing code using the legacy `logger` class requires no changes and will continue to work. However, for new development, consider using `UnifiedLogger`:

```python
# Legacy (still works)
from tlpytools.log import logger

class MyClass(logger):
    def __init__(self):
        super().__init__()
        self.init_logger()

# Modern approach
from tlpytools.log import UnifiedLogger

class MyClass(UnifiedLogger):
    def __init__(self, logger=None):
        super().__init__(logger=logger)
```

## Configuration

### Environment Variables

The logging system respects environment variables for configuration:

- Log file paths can be configured through class parameters
- Log levels can be set when creating loggers
- System information is automatically logged on initialization

### Customization

You can customize logging behavior by:

1. **Setting log levels**:
   ```python
   import logging
   logger = setup_logger("MyLogger", "my.log", level=logging.DEBUG)
   ```

2. **Customizing log file locations**:
   ```python
   import os
   log_dir = os.path.join(os.getcwd(), "logs")
   os.makedirs(log_dir, exist_ok=True)
   log_file = os.path.join(log_dir, "my_app.log")
   logger = setup_logger("MyApp", log_file)
   ```

3. **Disabling console output**:
   ```python
   logger = setup_logger("MyLogger", "my.log", console_output=False)
   ```

## Examples

See `examples/unified_logging_example.py` for comprehensive examples demonstrating:
- Separate logging for each class
- Shared logging across multiple classes
- Integration with existing TLPyTools classes
- Best practices for logging in different scenarios

## Troubleshooting

### Common Issues

1. **Duplicate log messages**: This can happen if multiple handlers are added to the same logger. The unified system prevents this by clearing existing handlers.

2. **Log files not created**: Ensure the directory exists and you have write permissions.

3. **Import errors**: Make sure you're importing from the correct module:
   ```python
   from tlpytools.log import UnifiedLogger, setup_logger
   ```

### Getting Help

If you encounter issues with the unified logging system:

1. Check that you're using the latest version of TLPyTools
2. Verify your import statements
3. Check file permissions for log file locations
4. Review the examples in this documentation
