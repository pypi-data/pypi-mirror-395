#!/usr/bin/env python3
"""
Example demonstrating unified logging across tlpytools.

This example shows how the unified logging system works:
1. Classes can accept an optional logger instance
2. If no logger is provided, each class creates its own
3. If a logger is provided, all classes share the same log file
"""

from tlpytools.log import UnifiedLogger, setup_logger
from tlpytools.data_store import DataStore


class ExampleClass1(UnifiedLogger):
    """Example class that uses unified logging."""

    def __init__(self, logger=None):
        super().__init__(logger=logger, name="ExampleClass1")

    def do_work(self):
        """Example method that logs its activities."""
        self.log.info("ExampleClass1 is starting work")
        self.log.debug("Processing data...")
        self.log.info("ExampleClass1 work completed")


class ExampleClass2(UnifiedLogger):
    """Another example class that uses unified logging."""

    def __init__(self, logger=None):
        super().__init__(logger=logger, name="ExampleClass2")

    def do_work(self):
        """Example method that logs its activities."""
        self.log.info("ExampleClass2 is starting work")
        self.log.warning("This is a warning message")
        self.log.info("ExampleClass2 work completed")


def demo_separate_loggers():
    """Demonstrate each class creating its own logger."""
    print("\n=== Demo 1: Separate loggers ===")

    # Each class will create its own logger and log file
    class1 = ExampleClass1()  # Creates ExampleClass1.log
    class2 = ExampleClass2()  # Creates ExampleClass2.log

    class1.do_work()
    class2.do_work()

    print("Check ExampleClass1.log and ExampleClass2.log files")


def demo_shared_logger():
    """Demonstrate sharing a logger across multiple classes."""
    print("\n=== Demo 2: Shared logger ===")

    # Create a main logger that will be shared
    main_logger = setup_logger("SharedExample", "shared_example.log")

    # Both classes will use the same logger
    class1 = ExampleClass1(logger=main_logger)
    class2 = ExampleClass2(logger=main_logger)

    # Also create a DataStore with the shared logger
    data_store = DataStore(project_name="demo", logger=main_logger)

    class1.do_work()
    class2.do_work()

    # DataStore operations will also go to the same log
    data_store.log.info("DataStore operations logged to shared file")

    print("Check shared_example.log file - all output should be there")


def demo_datastore_integration():
    """Demonstrate DataStore with unified logging."""
    print("\n=== Demo 3: DataStore with unified logging ===")

    # Create DataStore without logger (creates its own)
    ds1 = DataStore(project_name="project1")
    ds1.log.info("DataStore project1 with its own logger")

    # Create DataStore with shared logger
    shared_logger = setup_logger("DataStoreDemo", "datastore_demo.log")
    ds2 = DataStore(project_name="project2", logger=shared_logger)
    ds2.log.info("DataStore project2 with shared logger")

    print("Check DataStore_project1.log and datastore_demo.log files")


if __name__ == "__main__":
    print("Unified Logging Example")
    print("=" * 50)

    demo_separate_loggers()
    demo_shared_logger()
    demo_datastore_integration()

    print("\n=== Summary ===")
    print("This example demonstrates:")
    print("1. Classes can create their own loggers if none provided")
    print("2. Classes can share a logger for unified logging")
    print("3. The UnifiedLogger class makes it easy to add logging to any class")
    print("4. Backwards compatibility is maintained with the legacy logger class")
