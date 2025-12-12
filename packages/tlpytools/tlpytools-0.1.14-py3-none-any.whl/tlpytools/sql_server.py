# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded, get_env_var

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    def get_env_var(key: str, default: str = None, required: bool = False) -> str:
        """Fallback function if env_config is not available"""
        import os

        value = os.environ.get(key, default)
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value


import os
import numpy as np
import pandas as pd
import logging

# Optional import for geopandas
try:
    import geopandas as gpd

    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False

    # Create a dummy class to prevent attribute errors
    class DummyGeoDataFrame:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "geopandas is required for spatial data operations. Install with: pip install geopandas"
            )

    # Create a mock geopandas module
    class MockGeopandas:
        GeoDataFrame = DummyGeoDataFrame

        def read_file(self, *args, **kwargs):
            raise ImportError(
                "geopandas is required for reading spatial files. Install with: pip install geopandas"
            )

    gpd = MockGeopandas()

import pyodbc as p
import sqlalchemy as sql
import openmatrix as omx
from cryptography.fernet import Fernet
import cryptpandas as crp
import getpass

# Import the unified logger
from .log import UnifiedLogger, setup_logger


class ms_sql_tables(UnifiedLogger):
    """Collection of tools to interact with MS SQL Servers online and offline. Some local set up may be required to use encrypted offline mode."""

    __cache_pswd = None
    __cache_fkey = None

    def __init__(self, logger: logging.Logger = None):
        """
        Initialize ms_sql_tables with unified logging.

        Args:
            logger (logging.Logger, optional): Logger instance. If not provided, creates new logger.
        """
        super().__init__(logger=logger, name="ms_sql_tables")

    @classmethod
    def __password_manager(cls, fromLocalEnv="ms_sql_secret", echoEncryptedPwd=True):
        """A simple local password manager that enables access to your encrypted data.
        Do not ever log print statements within password manager as saving encrypted string and
        salt will allow attackers to decrypt your password.

        Args:
            fromLocalEnv (str, optional): A local env stored encrypted password. Defaults to 'ms_sql_secret'.
            echoEncryptedPwd (bool, optional): print encrypted password to help with set up. Defaults to True.

        Returns:
            decryptedPassword: password that has been decrpyted
        """
        if cls.__cache_pswd == None:
            # get encrypted password from local env, cache, return decrypt
            if fromLocalEnv != None:
                secret_var = fromLocalEnv
                secret_salt_var = fromLocalEnv + "_salt"
                if os.getenv(secret_var) != None and os.getenv(secret_salt_var) != None:
                    # load and cache local env vars
                    cls.__cache_pswd = str.encode(os.getenv(secret_var), "utf-8")
                    cls.__cache_fkey = str.encode(os.getenv(secret_salt_var), "utf-8")
                    fernet = Fernet(cls.__cache_fkey)
                    pswd = fernet.decrypt(cls.__cache_pswd).decode()
                    print("\nPassword loaded and decrypted from local env var...")
                    return pswd
                else:
                    # local env vars not specified
                    print("\nLocal env vars for password not set up...")
            # get password from console, encrypt, then cache
            print("Enter password to read encrypted data.")
            pswd = getpass.getpass()
            cls.__cache_fkey = Fernet.generate_key()
            fernet = Fernet(cls.__cache_fkey)  # save hashed password to this session
            cls.__cache_pswd = fernet.encrypt(pswd.encode())
            print("Password saved to session.")
            if echoEncryptedPwd:
                print(
                    "\nSave pwd salt to your local env variable '{secret_salt_var}': {s}".format(
                        secret_salt_var=secret_salt_var, s=cls.__cache_fkey
                    )
                )
                print(
                    "Save encrypted pwd to your local env variable '{secret_var}': {s}\n".format(
                        secret_var=secret_var, s=cls.__cache_pswd
                    )
                )
            return pswd
        else:
            # get encrypted password from cache, then decrypt
            fernet = Fernet(cls.__cache_fkey)
            pswd = fernet.decrypt(cls.__cache_pswd).decode()
            return pswd

    @classmethod
    def write_tables(cls, table_spec, df_dict, con, method=None):
        """Write a dictionary of dataframes to a list of tables

        Args:
            table_spec (dict): specify schema and tables to load.
            df_dict (dict): dictionary of dataframes
            con (pyodbc Connection or SQLAlchemy Engine): connection to the database

        Raises:
            ValueError: wrong value or type provided
        """
        # push to sql server
        for tbl, filepath in table_spec.items():
            try:
                fsch = filepath.split(".")[0]
                ftbl = filepath.split(".")[1]
                # Note: Using classmethod, so create temp logger for this operation
                import logging

                logger = logging.getLogger("ms_sql_tables")
                logger.info("Starting table upload: %s into %s.%s", tbl, fsch, ftbl)
                df_dict[tbl].to_sql(
                    name=ftbl,
                    con=con,
                    schema=fsch,
                    if_exists="replace",
                    index=False,
                    chunksize=200,
                    method=method,
                )
                logger.info("Data upload complete for table: %s", tbl)
            except Exception as e:
                logger.error("Data upload failed for table %s: %s", tbl, str(e))

    @classmethod
    def read_tables(cls, schema="*", table="*", source="local", con=None):
        """
        usage for read ms_sql data
        - add salt of ms_sql data to environment variable 'ms_sql_salt'
        - add path of ms_sql data to environment variable 'ms_sql_path'
        - in addition to salt and path, you may also need to set up password encripted
          string and salt. Or you may forgo password set up and enter it every time
        "df_dict = read_ms_sql_tables()"
        then input your personal password when prompted

        Args:
            schema (str, optional): specify schema to load. Defaults to '*'.
            table (str, optional): specify table to load. Defaults to '*'.
            source (str, optional): sources may be local or server. Defaults to 'local'.
            con (pyodbc Connection or SQLAlchemy Engine): connection to the database. Mandatory if source is not 'local'

        Raises:
            ValueError: wrong value or type provided
        """
        df_dict = {}
        if source == "local":
            pswd = cls.__password_manager()
            # get ms_sql_salt
            if os.getenv("ms_sql_salt") == None:
                msg = """'ms_sql_salt' env var not found.
                If you lost your salt after previous data download, 
                you will need to download again and save your salt."""
                # raise Exception(msg)
                # Create temporary logger for classmethod
                temp_logger = setup_logger(__name__)
                temp_logger.warning(msg.replace("\n", " ").strip())
                plain_salt = input("Enter your ms_sql_salt: ")
                salt = str.encode(plain_salt, "utf-8")
            else:
                salt = str.encode(os.getenv("ms_sql_salt"), "utf-8")
            # get ms_sql_path
            if os.getenv("ms_sql_path") == None:
                folder = input("Enter your ms_sql_path: ")
            else:
                folder = os.getenv("ms_sql_path")
            # read crypt files
            filetype = "crypt"
            for root, dirs, files in os.walk(folder):
                for file in files:
                    # read data
                    file_list = file.split(".")
                    fsche = file_list[0]
                    ftbl = ".".join(file_list[1:-1])
                    ftyp = file_list[-1]
                    # check ignore criteria
                    if ftyp != filetype:
                        continue
                    if schema != "*" and schema != fsche:
                        continue
                    if table != "*" and table != ftbl:
                        continue

                    # Create temporary logger for classmethod
                    temp_logger = setup_logger(__name__)
                    temp_logger.info(
                        "Reading table from local %s", os.path.join(root, file)
                    )
                    # read data
                    sc = file.split(".")[0]
                    tb = ".".join(file.split(".")[1:-1])
                    table_name = "{}.{}".format(sc, tb)
                    df_dict[table_name] = crp.read_encrypted(
                        path=os.path.join(root, file), password=pswd, salt=salt
                    )
        elif source == "server":

            # build reference of db tables
            query = """
            (SELECT schema_id, SCHEMA_NAME(schema_id) AS schema_name, name FROM sys.tables)
            UNION
            (SELECT schema_id, SCHEMA_NAME(schema_id) AS schema_name, name FROM sys.views)
            """
            ref_tables = pd.read_sql_query(sql.text(query), con=con)
            ref_tables = ref_tables.sort_values(by=["schema_id", "schema_name", "name"])

            # filter selected schema and table
            if schema != "":
                ref_tables = ref_tables[ref_tables["schema_name"] == schema]
            if table != None:
                ref_tables = ref_tables[ref_tables["name"] == table]

            # query data into df dict
            for index, data in ref_tables.iterrows():
                db_table = "[{schema}].[{table}]".format(
                    schema=data["schema_name"], table=data["name"]
                )
                table_name = "{}.{}".format(data["schema_name"], data["name"])
                # Note: Using classmethod, so create temp logger for this operation
                import logging

                logger = logging.getLogger("ms_sql_tables")
                logger.info("Reading table from sql server: %s", db_table)
                query = "SELECT * FROM {db_tbl};".format(db_tbl=db_table)
                db_table_df = pd.read_sql_query(sql.text(query), con=con)
                df_dict[table_name] = db_table_df

        else:
            raise ValueError("source must be either local or server")
        logger.info("Table reading completed")
        return df_dict

    @classmethod
    def download_encrypted(cls, con, flag_csv="ms_sql.sys.tables_flag.csv"):
        """Download tables from ms_sql and encrypt it.

        Args:
            flag_csv (str, optional): A list of table with flag 'extract' to download. Defaults to "ms_sql.sys.tables_flag.csv".
            con (pyodbc Connection or SQLAlchemy Engine): connection to the database
        """

        # specify file extension type
        ext = "crypt"

        # get password
        pswd = cls.__password_manager()

        # read flagged_table csv
        try:
            flagged_tables = pd.read_csv(flag_csv)
            flagged_tables = flagged_tables[flagged_tables["extract"] == 1]
        except:
            # Note: Using classmethod, so create temp logger for this operation
            import logging

            logger = logging.getLogger("ms_sql_tables")
            logger.error("You need to build a flagged table of ms_sql.sys.tables")
            logger.error(
                "Specify tables to be extracted with 1 in the 'extract' column"
            )

        # save list of df into encrypted parquet

        # read salt
        plain_salt = os.getenv("ms_sql_salt")
        if plain_salt == None:
            salt = crp.make_salt()
            import logging

            logger = logging.getLogger("ms_sql_tables")
            logger.warning("Salt was not specified, post download set up is required!")
            logger.info(
                "Save salt to your environment variable 'ms_sql_salt': %s", salt
            )
            # encode decode to ensure double slash is handled properly for encryption
            plain_salt = input("Enter salt provided above: ")
            salt = str.encode(plain_salt, "utf-8")
        else:
            salt = str.encode(plain_salt, "utf-8")

        # read output folder
        folder = os.getenv("ms_sql_path")
        if folder == None:
            folder = os.path.join(os.getcwd(), "data_extract")
            logger.warning(
                "No ms_sql_path has been specified, using current directory instead."
            )
            logger.info("Specify ms_sql_path environment variable after download")
        logger.info("Data download completed: %s", folder)

        # folder = '..\ms_sql'

        for index, data in flagged_tables.iterrows():
            db_table = "[{schema}].[{table}]".format(
                schema=data["schema_name"], table=data["name"]
            )

            db_file = os.path.join(
                folder,
                "{schema}.{table}.{ext}".format(
                    schema=data["schema_name"], table=data["name"], ext=ext
                ),
            )

            if not os.path.isfile(db_file):
                query = "SELECT * FROM {db_tbl};".format(db_tbl=db_table)
                db_table_df = pd.read_sql_query(sql.text(query), con=con)
                # db_table_df.to_parquet(
                #     "{}.parquet".format(db_file), engine="pyarrow")
                crp.to_encrypted(db_table_df, password=pswd, path=db_file, salt=salt)
                del db_table_df
                logger.info("Table %s encrypted and saved.", db_table)
                pass

    @classmethod
    def export_tbl_list(cls, con, csv_file="ms_sql.sys.tables.csv"):
        query = "SELECT SCHEMA_NAME(schema_id) AS schema_name,* FROM sys.tables ;"
        all_tables = pd.read_sql_query(sql.text(query), con=con)
        all_tables = all_tables.sort_values(by=["schema_id", "schema_name", "name"])
        all_tables.insert(loc=0, column="extract", value=0)
        all_tables.to_csv(csv_file, index=False)


class savona_tables(ms_sql_tables):
    engine = sql.create_engine(
        "mssql+pyodbc:///?odbc_connect="
        "Driver={SQL Server Native Client 11.0};"
        "Server=SAVONA;"
        "Database=TL_RESEARCH_ANALYTICS_DEV;"
        "Trusted_Connection=yes;"
    )

    @classmethod
    def write_tables(cls, table_spec, df_dict):
        return super().write_tables(table_spec, df_dict, cls.engine, method="multi")

    @classmethod
    def read_tables(cls, schema="*", table="*", source="server"):
        return super().read_tables(schema, table, source, cls.engine.connect())

    @classmethod
    def download_encrypted(cls, flag_csv="savona.sys.tables_flag.csv"):
        return super().download_encrypted(cls.engine.connect(), flag_csv)

    @classmethod
    def export_tbl_list(cls, csv_file="savona.sys.tables.csv"):
        return super().export_tbl_list(cls.engine.connect(), csv_file)


class azure_td_tables(ms_sql_tables):
    # get azure server url from environment variable
    azure_sql_svr_uri = get_env_var("TLPT_AZURE_SQL_URI", required=True)

    # create engine
    engine = sql.create_engine(
        "mssql+pyodbc:///?odbc_connect="
        "Driver={ODBC Driver 17 for SQL Server};"
        + f"Server={azure_sql_svr_uri};"
        + "Database=forecasting;"
        + "Authentication=ActiveDirectoryInteractive;"
        + "Encrypt=yes;"
        + "TrustServerCertificate=no;"
        + "Connection Timeout=30"
    )

    @classmethod
    def write_tables(cls, table_spec, df_dict):
        return super().write_tables(table_spec, df_dict, cls.engine)

    @classmethod
    def read_tables(cls, schema="*", table="*", source="server"):
        return super().read_tables(schema, table, source, cls.engine.connect())

    @classmethod
    def download_encrypted(cls, flag_csv="azure_td.sys.tables_flag.csv"):
        return super().download_encrypted(cls.engine.connect(), flag_csv)

    @classmethod
    def export_tbl_list(cls, csv_file="azure_td.sys.tables.csv"):
        return super().export_tbl_list(cls.engine.connect(), csv_file)
