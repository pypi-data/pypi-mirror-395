# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

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

import sqlalchemy as sql
import openmatrix as omx
from cryptography.fernet import Fernet
import cryptpandas as crp
import getpass
import shutil

# Optional imports for other tlpytools modules to avoid circular dependencies
try:
    from tlpytools.sql_server import azure_td_tables, savona_tables

    HAS_SQL_SERVER = True
except ImportError:
    HAS_SQL_SERVER = False
    azure_td_tables = None
    savona_tables = None

try:
    from tlpytools.adls_server import adls_tables

    HAS_ADLS_SERVER = True
except ImportError:
    HAS_ADLS_SERVER = False
    adls_tables = None


def validate_dataframe(df, required_columns):
    """
    Validate that a dataframe contains all required columns and is not empty.

    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names

    Returns:
        bool: True if valid, False otherwise
    """
    if df is None or df.empty:
        return False

    missing_columns = set(required_columns) - set(df.columns)
    return len(missing_columns) == 0


def standardize_zone_data(df):
    """
    Standardize zone data by ensuring consistent column names and data types.

    Args:
        df (pd.DataFrame): DataFrame with zone data

    Returns:
        pd.DataFrame: Standardized DataFrame
    """
    df_copy = df.copy()

    # Ensure zone_id is integer if it exists
    if "zone_id" in df_copy.columns:
        df_copy["zone_id"] = pd.to_numeric(df_copy["zone_id"], errors="coerce")

    # Ensure numeric columns are properly typed
    numeric_columns = ["households", "population", "employment", "area"]
    for col in numeric_columns:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")

    return df_copy


def aggregate_to_districts(df, district_mapping, zone_col="zone_id", sum_cols=None):
    """
    Aggregate zone-level data to district level.

    Args:
        df (pd.DataFrame): DataFrame with zone data
        district_mapping (dict): Mapping from zone_id to district
        zone_col (str): Name of zone ID column
        sum_cols (list): Columns to sum during aggregation

    Returns:
        pd.DataFrame: District-level aggregated data
    """
    if sum_cols is None:
        sum_cols = ["households", "population", "employment"]

    df_copy = df.copy()

    # Add district column
    df_copy["district"] = df_copy[zone_col].map(district_mapping)

    # Filter out zones without district mapping
    df_copy = df_copy[df_copy["district"].notna()]

    # Aggregate
    agg_dict = {col: "sum" for col in sum_cols if col in df_copy.columns}

    if not agg_dict:
        return pd.DataFrame()

    result = df_copy.groupby("district").agg(agg_dict).reset_index()

    return result


def calculate_density(
    df, area_data, pop_col="population", area_col="area_km2", join_col="zone_id"
):
    """
    Calculate population density by joining with area data.

    Args:
        df (pd.DataFrame): DataFrame with population data
        area_data (pd.DataFrame): DataFrame with area data
        pop_col (str): Name of population column
        area_col (str): Name of area column
        join_col (str): Column to join on

    Returns:
        pd.DataFrame: DataFrame with density calculations
    """
    # Join dataframes
    merged = df.merge(area_data, on=join_col, how="left")

    # Calculate density
    density_col = f"{pop_col}_density"
    merged[density_col] = merged[pop_col] / merged[area_col]

    # Handle division by zero
    merged[density_col] = merged[density_col].replace([np.inf, -np.inf], np.nan)

    return merged


def read_spatial_data(file_path):
    """
    Read spatial data files using GeoPandas.

    Args:
        file_path (str): Path to spatial data file

    Returns:
        geopandas.GeoDataFrame: Spatial data

    Raises:
        ImportError: If geopandas is not available
    """
    if not HAS_GEOPANDAS:
        raise ImportError(
            "geopandas is required for spatial data operations. "
            "Install with: pip install geopandas"
        )

    return gpd.read_file(file_path)


class data_tables:
    """Collection of tools to handle table data."""

    @staticmethod
    def read_tbl_data(s):
        """Read table data according to spec. Typically ran as part of run_yaml.load_yaml_data.
        Use get_sample_spec() to see example.

        Args:
            s (dict): dictionary object containing spec

        Returns:
            dfs: a dictionary of DataFrame objects
        """
        # read input data
        dfs = {}
        for tbl in s["FILES"]["INPUTS"].keys():
            file_identifier = s["FILES"]["INPUTS"][tbl]
            file_protocol = file_identifier.split("://")[0]
            file_type = file_identifier.split(".")[-1]
            # check for INPUT_COLUMNS select
            col_select = False
            if "INPUT_COLUMNS" in s["FILES"]:
                if tbl in s["FILES"]["INPUT_COLUMNS"]:
                    col_select = True
            if file_protocol == "https":
                # protocol is set - use azure cloud source to handle different file types
                bytes_io = adls_tables.get_table_by_name(uri=file_identifier)
                # override value of file_path to use cache_file path
                file_path = adls_tables.get_cache_file_path(uri=file_identifier)
                # save cache file
                with open(file_path, "wb") as file:
                    file.write(bytes_io.getbuffer())
            else:
                file_path = file_identifier
            # read file, file types supported:
            # .csv will use pd.read_csv, a file is required
            # .xlsx will use pd.read_excel, a file is required
            # .crypt requires a file and password prior set up needed
            # .sqlsvr requires valid db connection and credential
            # .azuresql requires valid db connection and credential
            # .omx will use openmatrix, a file is required
            # .fea will use pd.read_feather, a file is required
            if file_type == "csv":
                dfs[tbl] = pd.read_csv(file_path)
            elif file_type == "xlsx":
                dfs[tbl] = pd.read_excel(file_path)
            elif file_type == "azuresql":
                fsch = file_path.split(".")[0]
                ftbl = file_path.split(".")[1]
                tkey = "{}.{}".format(fsch, ftbl)
                dfs[tbl] = azure_td_tables.read_tables(
                    schema=fsch, table=ftbl, source="server"
                )[tkey]
            elif file_type == "crypt":
                fsch = file_path.split(".")[0]
                ftbl = file_path.split(".")[1]
                tkey = "{}.{}".format(fsch, ftbl)
                dfs[tbl] = savona_tables.read_tables(
                    schema=fsch, table=ftbl, source="local"
                )[tkey]
            elif file_type == "sqlsvr":
                fsch = file_path.split(".")[0]
                ftbl = file_path.split(".")[1]
                tkey = "{}.{}".format(fsch, ftbl)
                dfs[tbl] = savona_tables.read_tables(
                    schema=fsch, table=ftbl, source="server"
                )[tkey]
            elif file_type == "fea":
                if col_select:
                    cols = s["FILES"]["INPUT_COLUMNS"][tbl]
                    dfs[tbl] = pd.read_feather(file_path, columns=cols)
                else:
                    dfs[tbl] = pd.read_feather(file_path)
            elif file_type == "parquet":
                dfs[tbl] = pd.read_parquet(file_path)
            elif file_type == "omx":
                omxfile = omx.open_file(file_path)
                if col_select:
                    mat_list = s["FILES"]["INPUT_COLUMNS"][tbl]
                else:
                    mat_list = omxfile.list_matrices()
                df = pd.DataFrame()
                for matrix in mat_list:
                    mat = np.array(omxfile[matrix])
                    df[matrix] = mat.flatten()
                dfs[tbl] = df
                omxfile.close()
            else:
                raise (ValueError("File type {} not supported.".format(file_type)))
            # post process col select
            if col_select:
                cols = s["FILES"]["INPUT_COLUMNS"][tbl]
                dfs[tbl] = dfs[tbl][cols]

        return dfs

    @staticmethod
    def read_spatial_data(s):
        """Read spatial files using GeoPandas according to spec

        Args:
            s (dict): dictionary object containing spec

        Returns:
            dict: dictionary of GeoDataFrame objects
        """
        if not HAS_GEOPANDAS:
            raise ImportError(
                "geopandas is required for spatial data operations. "
                "Install with: pip install geopandas"
            )

        if not HAS_ADLS_SERVER:
            raise ImportError(
                "adls_server module is required for cloud data operations. "
                "Check that all dependencies are installed."
            )

        # read in spatial files
        gdfs = {}
        for tbl in s["FILES"]["SPATIALS"].keys():
            file_identifier = s["FILES"]["SPATIALS"][tbl]
            file_protocol = file_identifier.split("://")[0]
            file_type = file_identifier.split(".")[-1]
            # check for INPUT_COLUMNS select
            col_select = False
            if "INPUT_COLUMNS" in s["FILES"]:
                if tbl in s["FILES"]["INPUT_COLUMNS"]:
                    col_select = True
            if file_protocol == "https":
                # protocol is set - use azure cloud source to handle different file types
                bytes_io = adls_tables.get_table_by_name(uri=file_identifier)
                # override value of file_path to use cache_file path
                file_path = adls_tables.get_cache_file_path(uri=file_identifier)
                # save cache file
                with open(file_path, "wb") as file:
                    file.write(bytes_io.getbuffer())
            else:
                file_path = file_identifier
            # read file, file types supported:
            # .shp will use gpd.read_file
            # .geojson will use gpd.read_file
            if file_type == "shp":
                if file_protocol == "https":
                    raise (ValueError(f"{file_type} not supported for https."))
                else:
                    gdfs[tbl] = gpd.read_file(file_path)
            elif file_type == "geojson":
                gdfs[tbl] = gpd.read_file(file_path)
            elif file_type == "parquet":
                gdfs[tbl] = gpd.read_parquet(file_path)
            else:
                raise (ValueError("File type {} not supported.".format(file_type)))
            # post process col select
            if col_select:
                cols = s["FILES"]["INPUT_COLUMNS"][tbl]
                gdfs[tbl] = gdfs[tbl][cols]

        return gdfs

    @staticmethod
    def export_data(dict_df, ofiles, omx_size=None, omx_mode="a"):
        """Export dictionary of dataframes into data files. Typically ran as part of a step within run_yaml.run_steps.
        Unlike export_csv, this method supports many file types: csv, omx, fea, and sqlsvr.
        Note omx matices will always be exported as 1-d flattened if omx_size is None.
        For other omx sizes, input duples such as (NoTAZ, NoTAZ)

        Args:
            dict_df (dict): dictionary of dataframes
            files (dict): dictionary of table names with file extension in file paths
            omx_size (duple): omx mat sizes, Default None
            omx_mode (str): omx file read write mode, 'a' for append, 'w' for write, Default is 'a'
        """
        # export data
        for otbl in ofiles.keys():
            try:
                file_path = ofiles[otbl]
                file_protocol = file_path.split("://")[0]
                file_type = file_path.split(".")[-1]
                # for https protocol for ADLS, update the file path to cache path
                if file_protocol == "https":
                    uri_path = ofiles[otbl]
                    # protocol is set - use azure cloud source to handle different file types
                    local_file_name = f"{otbl}.{file_type}"
                    # save as cache file
                    cache_dir = os.environ.get(
                        "TLPT_ADLS_CACHE_DIR", "C:/Temp/tlpytools/adls"
                    )
                    cache_file = os.path.join(cache_dir, local_file_name)
                    os.makedirs(cache_dir, exist_ok=True)
                    # override value of file_path to use cache_file path
                    file_path = cache_file
                else:
                    # create local directory if doesn't exist
                    if file_type not in ["azuresql", "sqlsvr"]:
                        filedir = os.path.dirname(file_path)
                        os.makedirs(filedir, exist_ok=True)
                # export data of a particular type
                if file_type == "csv":
                    dict_df[otbl].to_csv(file_path, index=False)
                elif file_type == "azuresql":
                    table_spec = {otbl: file_path}
                    azure_td_tables.write_tables(table_spec, df_dict=dict_df)
                elif file_type == "sqlsvr":
                    table_spec = {otbl: file_path}
                    savona_tables.write_tables(table_spec, df_dict=dict_df)
                elif file_type == "fea":
                    dict_df[otbl].to_feather(file_path)
                elif file_type == "parquet":
                    dict_df[otbl].to_parquet(file_path)
                elif file_type == "omx":
                    # by default use append mode 'a'
                    # overwrite 'w' mode is not used here
                    omxfile = omx.open_file(file_path, omx_mode)
                    omx_mat_list = omxfile.list_matrices()
                    mat_list = list(dict_df[otbl].columns)
                    for mat_name in mat_list:
                        if mat_name in omx_mat_list:
                            # delete existing mapping
                            omxfile.delete_mapping(mat_name)
                        colseries = dict_df[otbl][mat_name]
                        if omx_size == None:
                            slength = len(colseries)
                            root = np.sqrt(slength)
                            if int(root) ** 2 == slength:
                                mat_size = (root, root)
                            else:
                                mat_size = (1, slength)
                        else:
                            mat_size = omx_size
                        omxfile[mat_name] = colseries.to_numpy().reshape(mat_size)
                    omxfile.close()
                elif file_type == "shp":
                    if file_protocol == "https":
                        raise (ValueError(f"{file_type} not supported for https."))
                    else:
                        # spatial data types - shp
                        dict_df[otbl].to_file(file_path)
                elif file_type == "geojson":
                    # spatial data types - geojson
                    dict_df[otbl].to_file(file_path, driver="GeoJSON")
                # elif file_type == "parquet":
                #     # recommended file format is shp or geojson, don't use parquet for spatial
                #     # spatial data types - parquet
                #     # even if the dataframe does not contain geometry, we will cast it to enable GeoDataFrame support
                #     gpd.GeoDataFrame(dict_df[otbl].copy()).to_parquet(file_path)
                # for https protocol for ADLS, upload the output file at the end
                if file_protocol == "https":
                    # finally, write saved table to ADLS
                    adls_tables.write_table_by_name(
                        uri=uri_path, local_path=cache_dir, file_name=local_file_name
                    )
            except Exception as e:
                logging.error("Export table %s failed: %s", otbl, e)
        # clean up cache data folder
        cache_keep = os.environ.get("TLPT_ADLS_CACHE_KEEP", "0")
        cache_dir = os.environ.get("TLPT_ADLS_CACHE_DIR", "C:/Temp/tlpytools/adls")
        if int(cache_keep) == 0:
            shutil.rmtree(cache_dir, ignore_errors=True)

    @staticmethod
    def export_csv(dict_df, ofiles):
        """Export dictionary of dataframes into csv files. Typically ran as part of a step within run_yaml.run_steps.

        Args:
            dict_df (dict): dictionary of dataframes
            files (dict): dictionary of table names and csv file paths
        """
        # export data
        for otbl in ofiles.keys():
            try:
                # create directory if doesn't exist
                filepath = ofiles[otbl]
                filedir = os.path.dirname(filepath)
                if not os.path.exists(filedir):
                    os.makedirs(filedir)
                dict_df[otbl].to_csv(filepath, index=False)
            except Exception as e:
                logging.error("Export table %s failed: %s", otbl, e)
