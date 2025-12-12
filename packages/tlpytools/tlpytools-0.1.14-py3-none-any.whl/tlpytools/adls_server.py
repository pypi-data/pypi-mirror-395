# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

# import pyspark
# from delta.tables import *
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
from azure.storage.filedatalake import (
    # DataLakeServiceClient,
    DataLakeFileClient,
    DataLakeDirectoryClient,
    FileSystemClient,
)
from io import BytesIO
import os
import time
import logging
from functools import wraps

# Import the unified logger
from .log import UnifiedLogger, setup_logger

# Import the centralized Azure credential manager
from .azure_credential import AzureCredentialManager


def is_authorization_error(exception: Exception) -> bool:
    """Check if the exception is an Azure authorization/permission error."""
    if isinstance(exception, HttpResponseError):
        error_code = getattr(exception, "error_code", "")
        error_message = str(exception).lower()
        # Check for common authorization error patterns
        return (
            error_code
            in [
                "AuthorizationPermissionMismatch",
                "AuthorizationFailed",
                "AuthenticationFailed",
            ]
            or "authorizationpermissionmismatch" in error_message
            or "not authorized" in error_message
            or "authentication failed" in error_message
        )
    return False


def retry_with_credential_refresh(max_retries: int = 2):
    """Decorator to retry ADLS operations with credential refresh on authorization errors."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if is_authorization_error(e) and attempt < max_retries - 1:
                        # Log the retry attempt
                        logger = logging.getLogger("adls_util")
                        logger.warning(
                            "Authorization error detected on attempt %d/%d: %s. Refreshing credentials and retrying...",
                            attempt + 1,
                            max_retries,
                            str(e),
                        )
                        # Force refresh the credential
                        AzureCredentialManager.get_instance().get_credential(
                            force_refresh=True
                        )
                        time.sleep(60)  # Brief delay before retry
                    else:
                        raise
            raise last_exception

        return wrapper

    return decorator


class adls_util(UnifiedLogger):

    # global variables
    UPLOAD_TIMEOUT_SECS = 5 * 3600
    UPLOAD_CHUNK_SIZE = 10 * 1024 * 1024

    def __init__(self, logger: logging.Logger = None):
        """
        Initialize adls_util with unified logging.

        Args:
            logger (logging.Logger, optional): Logger instance. If not provided, creates new logger.
        """
        super().__init__(logger=logger, name="adls_util")

    @classmethod
    def create_directory(
        cls,
        file_system_client: FileSystemClient,
        directory_name: str,
    ) -> DataLakeDirectoryClient:
        directory_client = file_system_client.create_directory(directory_name)

        return directory_client

    @classmethod
    def list_directory_contents(
        cls,
        file_system_client: FileSystemClient,
        directory_name: str,
    ):
        paths = file_system_client.get_paths(path=directory_name)

        # Note: Using classmethod, so create temp logger for this operation
        import logging

        logger = logging.getLogger("adls_util")
        for path in paths:
            logger.info("Directory listing: %s", path.name)

    @classmethod
    def file_exists(cls, file_client: DataLakeFileClient):
        try:
            file_client.get_file_properties()
            return True
        except ResourceNotFoundError:
            return False

    @classmethod
    def upload_file_to_directory(
        cls,
        directory_client: DataLakeDirectoryClient,
        upload_file_name: str,
        local_file_name: str,
        local_path: str,  # directory path
    ):
        file_client = directory_client.get_file_client(upload_file_name)

        # Note: Using classmethod, so create temp logger for this operation
        import logging

        logger = logging.getLogger("adls_util")

        # handle existing file conflict
        if cls.file_exists(file_client):
            file_timestamp = time.strftime("%Y%m%d%H%M", time.localtime())
            split_file_name = upload_file_name.split(".")
            old_renamed_file_name = f"{'.'.join(split_file_name[:-1])}_{file_timestamp}_bak.{split_file_name[-1]}"
            cls.rename_file(
                directory_client=directory_client,
                old_file_name=upload_file_name,
                new_file_name=old_renamed_file_name,
            )
            logger.warning(
                "File %s already exist in azure directory, and it has been renamed with a timestamp.",
                upload_file_name,
            )
        # upload file
        with open(file=os.path.join(local_path, local_file_name), mode="rb") as data:
            # to adjust additional options, see: https://learn.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake.datalakefileclient?view=azure-python#azure-storage-filedatalake-datalakefileclient-upload-data
            file_client.upload_data(
                data,
                overwrite=True,
                timeout=cls.UPLOAD_TIMEOUT_SECS,
                chunk_size=cls.UPLOAD_CHUNK_SIZE,
            )
            # alternative method that is more verbose
            # file_client.create_file()
            # file_client.append_data(data, offset=0, length=len(data))
            # file_client.flush_data(len(data))
        logger.info("Successfully uploaded %s", local_file_name)

    @classmethod
    def read_bytes_from_directory(
        cls,
        directory_client: DataLakeDirectoryClient,
        file_name: str,
    ):
        file_client = directory_client.get_file_client(file_name)

        # Note: Using classmethod, so create temp logger for this operation
        import logging

        logger = logging.getLogger("adls_util")

        if cls.file_exists(file_client):
            data_bytes = file_client.download_file().readall()
            bytes_io = BytesIO(data_bytes)
            logger.info("Successfully downloaded %s and cached.", file_name)
            return bytes_io
        else:
            logger.warning(
                "Abort download since %s does not exist in azure directory.", file_name
            )

    @classmethod
    def rename_file(
        cls,
        directory_client: DataLakeDirectoryClient,
        old_file_name: str,
        new_file_name: str,
    ):
        file_client = directory_client.get_file_client(old_file_name)
        new_file_client = directory_client.get_file_client(new_file_name)
        nfc_fs_name = new_file_client.file_system_name
        nfc_path_name = new_file_client.path_name
        nfc_full_path = f"{nfc_fs_name}/{nfc_path_name}"
        # to rename, new file name must not already exist and old file name must exist
        if cls.file_exists(file_client) and not cls.file_exists(new_file_client):
            file_client.rename_file(nfc_full_path)
            # Create temporary logger for classmethod
            temp_logger = setup_logger(__name__)
            temp_logger.info(
                "Successfully renamed %s to %s", old_file_name, new_file_name
            )
        else:
            # Create temporary logger for classmethod
            temp_logger = setup_logger(__name__)
            temp_logger.warning(
                "Cannot rename %s to %s due to filename issues",
                old_file_name,
                new_file_name,
            )

    @classmethod
    def move_file_to_subdirectory(
        cls,
        source_directory_client: DataLakeDirectoryClient,
        file_name: str,
        target_subdirectory_path: str,
        new_file_name: str,
    ):
        """
        Move a file from one directory to a subdirectory with proper Azure Data Lake Storage handling.

        Args:
            source_directory_client: Directory client where the file currently exists
            file_name: Name of the file to move
            target_subdirectory_path: Full path to target subdirectory (e.g., "raw/proj_unnamed/db_test_cloud/.cloud_sync_conflict")
            new_file_name: New name for the file in the target directory

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the source file client
            source_file_client = source_directory_client.get_file_client(file_name)

            # Check if source file exists
            if not cls.file_exists(source_file_client):
                temp_logger = setup_logger(__name__)
                temp_logger.warning("Source file %s does not exist", file_name)
                return False

            # Construct the full target path for Azure rename operation
            # Azure rename_file expects: "filesystem/path/to/target/file"
            fs_name = source_file_client.file_system_name
            target_full_path = f"{fs_name}/{target_subdirectory_path}/{new_file_name}"

            # Perform the rename (move) operation
            source_file_client.rename_file(target_full_path)

            # Log success
            temp_logger = setup_logger(__name__)
            temp_logger.info(
                "Successfully moved file %s to %s/%s",
                file_name,
                target_subdirectory_path,
                new_file_name,
            )
            return True

        except Exception as e:
            temp_logger = setup_logger(__name__)
            temp_logger.error(
                "Failed to move file %s to %s/%s: %s",
                file_name,
                target_subdirectory_path,
                new_file_name,
                str(e),
            )
            return False

    @classmethod
    @retry_with_credential_refresh(max_retries=2)
    def get_fs_directory_object(
        cls, account_url: str, file_system_name: str, directory_name: str
    ):
        # get reference to Azure file system
        credential_manager = AzureCredentialManager.get_instance()
        az_fs_client = FileSystemClient(
            account_url=account_url,
            file_system_name=file_system_name,
            credential=credential_manager.get_credential(),
        )
        # get directory reference
        az_dir_client = DataLakeDirectoryClient(
            account_url=account_url,
            file_system_name=file_system_name,
            directory_name=directory_name,
            credential=credential_manager.get_credential(),
        )
        if not az_dir_client.exists():
            az_dir_client = cls.create_directory(
                file_system_client=az_fs_client, directory_name=directory_name
            )

        return az_fs_client, az_dir_client


class adls_tables:
    """Collection of tools to read and write data tables of specific formats in the Azure Data Lake Storage Gen2"""

    @staticmethod
    def get_cache_file_path(uri):
        cache_dir = os.environ.get("TLPT_ADLS_CACHE_DIR", "C:/Temp/tlpytools/adls")
        file_name = uri.split("/")[-1]
        cache_file = os.path.join(cache_dir, file_name)
        os.makedirs(cache_dir, exist_ok=True)
        return cache_file

    @classmethod
    def get_table_by_name(cls, uri):
        """returns byte io and cache location of table given uri

        Args:
            uri (str): uri starts with https for azure data lake store
        """
        # parse uri
        ADLS_URL = "/".join(uri.split("/")[0:3])
        ADLS_CONTAINER = uri.split("/")[3]
        ADLS_DIR = "/".join(uri.split("/")[4:-1])
        ADLS_FILE = "/".join(uri.split("/")[-1:])

        # get directory object from name
        az_fs, az_dir = adls_util.get_fs_directory_object(
            account_url=ADLS_URL,
            file_system_name=ADLS_CONTAINER,
            directory_name=ADLS_DIR,
        )
        return adls_util.read_bytes_from_directory(
            directory_client=az_dir, file_name=ADLS_FILE
        )

    @classmethod
    def write_table_by_name(cls, uri, local_path, file_name):
        # parse uri
        ADLS_URL = "/".join(uri.split("/")[0:3])
        ADLS_CONTAINER = uri.split("/")[3]
        ADLS_DIR = "/".join(uri.split("/")[4:-1])
        ADLS_FILE = "/".join(uri.split("/")[-1:])

        # get directory object from name
        az_fs, az_dir = adls_util.get_fs_directory_object(
            account_url=ADLS_URL,
            file_system_name=ADLS_CONTAINER,
            directory_name=ADLS_DIR,
        )
        adls_util.upload_file_to_directory(
            directory_client=az_dir,
            upload_file_name=ADLS_FILE,
            local_file_name=file_name,
            local_path=local_path,
        )
