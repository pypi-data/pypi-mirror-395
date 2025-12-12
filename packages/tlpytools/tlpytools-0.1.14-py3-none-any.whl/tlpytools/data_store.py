# Load environment variables from .env file automatically
try:
    from .env_config import ensure_env_loaded

    ensure_env_loaded()
except ImportError:
    # Fallback if env_config is not available
    pass

import os
import warnings
import pandas as pd
import json
import logging
from datetime import datetime
from pathlib import Path

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

import shelve

# Optional import for data_tables to avoid circular dependencies
try:
    from tlpytools.data import data_tables

    HAS_DATA_TABLES = True
except ImportError:
    HAS_DATA_TABLES = False
    data_tables = None

# Import the unified logger
from .log import UnifiedLogger


class DataStore(UnifiedLogger):
    """Enhanced data store for managing datasets with metadata and versioning."""

    def __init__(
        self, base_path=None, project_name="default", logger: logging.Logger = None
    ):
        """
        Initialize DataStore.

        Args:
            base_path (str, optional): Base directory for data storage
            project_name (str): Name of the project
            logger (logging.Logger, optional): Logger instance. If not provided, creates new logger.
        """
        # Initialize unified logging first
        super().__init__(logger=logger, name=f"DataStore_{project_name}")

        if base_path is None:
            base_path = os.path.join(os.getcwd(), "data_store")

        self.base_path = Path(base_path)
        self.project_name = project_name
        self.project_path = self.base_path / project_name

        # Create directories
        self.project_path.mkdir(parents=True, exist_ok=True)
        (self.project_path / "data").mkdir(exist_ok=True)
        (self.project_path / "metadata").mkdir(exist_ok=True)

        # Legacy attributes for backwards compatibility
        self.vars_filename = str(self.project_path / "tmp" / "data_store_vars")
        self.dfs_filename_pattern = str(
            self.project_path / "tmp" / "data_store_dfs_{df_name}.fea"
        )
        self.gdfs_filename = str(self.project_path / "tmp" / "data_store_gdfs.gpkg")
        self.data_store_write_mode = True

        # Create tmp directory for legacy support
        tmp_dir = self.project_path / "tmp"
        tmp_dir.mkdir(exist_ok=True)

        # Suppress performance warning for pytables
        warnings.filterwarnings("ignore", category=pd.io.pytables.PerformanceWarning)

        self.log.info(f"DataStore initialized for project: {project_name}")
        self.log.info(f"Base path: {self.base_path}")
        self.log.info(f"Project path: {self.project_path}")

    def save_data(self, data, name, metadata=None, format="parquet", compression=None):
        """
        Save data with metadata.

        Args:
            data (pd.DataFrame): Data to save
            name (str): Dataset name
            metadata (dict, optional): Additional metadata
            format (str): File format ('csv', 'parquet', 'feather')
            compression (str, optional): Compression method

        Returns:
            bool: True if successful
        """
        try:
            # Prepare file paths
            if format == "csv":
                file_path = self.project_path / "data" / f"{name}.csv"
                data.to_csv(file_path, index=False, compression=compression)
            elif format == "parquet":
                file_path = self.project_path / "data" / f"{name}.parquet"
                data.to_parquet(file_path, compression=compression)
            elif format == "feather":
                file_path = self.project_path / "data" / f"{name}.feather"
                data.to_feather(file_path, compression=compression)
            else:
                raise ValueError(f"Unsupported format: {format}")

            # Save metadata
            meta_data = {
                "name": name,
                "format": format,
                "compression": compression,
                "shape": data.shape,
                "columns": list(data.columns),
                "dtypes": {col: str(dtype) for col, dtype in data.dtypes.items()},
                "created_at": datetime.now().isoformat(),
                "file_path": str(file_path.relative_to(self.project_path)),
            }

            if metadata:
                meta_data.update(metadata)

            meta_file = self.project_path / "metadata" / f"{name}.json"
            with open(meta_file, "w") as f:
                json.dump(meta_data, f, indent=2)

            return True

        except Exception as e:
            self.log.error("Error saving data %s: %s", name, e)
            return False

    def load_data(self, name):
        """
        Load data by name.

        Args:
            name (str): Dataset name

        Returns:
            pd.DataFrame or None: Loaded data
        """
        try:
            # Load metadata
            meta_file = self.project_path / "metadata" / f"{name}.json"
            if not meta_file.exists():
                return None

            with open(meta_file, "r") as f:
                metadata = json.load(f)

            # Load data based on format
            file_path = self.project_path / metadata["file_path"]

            if metadata["format"] == "csv":
                return pd.read_csv(file_path)
            elif metadata["format"] == "parquet":
                return pd.read_parquet(file_path)
            elif metadata["format"] == "feather":
                return pd.read_feather(file_path)
            else:
                raise ValueError(f"Unsupported format: {metadata['format']}")

        except Exception as e:
            self.log.error("Error loading data %s: %s", name, e)
            return None

    def dataset_exists(self, name):
        """
        Check if dataset exists.

        Args:
            name (str): Dataset name

        Returns:
            bool: True if exists
        """
        meta_file = self.project_path / "metadata" / f"{name}.json"
        return meta_file.exists()

    def list_datasets(self):
        """
        List all available datasets.

        Returns:
            list: List of dataset names
        """
        metadata_dir = self.project_path / "metadata"
        if not metadata_dir.exists():
            return []

        datasets = []
        for meta_file in metadata_dir.glob("*.json"):
            datasets.append(meta_file.stem)

        return sorted(datasets)

    def get_metadata(self, name):
        """
        Get metadata for a dataset.

        Args:
            name (str): Dataset name

        Returns:
            dict or None: Metadata
        """
        try:
            meta_file = self.project_path / "metadata" / f"{name}.json"
            if not meta_file.exists():
                return None

            with open(meta_file, "r") as f:
                return json.load(f)

        except Exception as e:
            self.log.error("Error loading metadata for %s: %s", name, str(e))
            return None

    def delete_dataset(self, name):
        """
        Delete a dataset and its metadata.

        Args:
            name (str): Dataset name

        Returns:
            bool: True if successful
        """
        try:
            # Load metadata to get file path
            metadata = self.get_metadata(name)
            if not metadata:
                return False

            # Delete data file
            file_path = self.project_path / metadata["file_path"]
            if file_path.exists():
                file_path.unlink()

            # Delete metadata file
            meta_file = self.project_path / "metadata" / f"{name}.json"
            if meta_file.exists():
                meta_file.unlink()

            return True

        except Exception as e:
            self.log.error("Error deleting dataset %s: %s", name, str(e))
            return False

    def list_versions(self, name):
        """
        List versions of a dataset (placeholder for versioning feature).

        Args:
            name (str): Dataset name

        Returns:
            list: List of versions
        """
        # This is a placeholder for future versioning implementation
        if self.dataset_exists(name):
            return [1]
        return []

    def enable_versioning(self):
        """
        Enable versioning for this data store (placeholder).
        """
        # Placeholder for future versioning implementation
        pass

    def load_existing_data(self, spec: dict):
        # initialize objects
        vars_obj = {}
        dfs_obj = {}
        gdfs_obj = {}
        if os.path.exists(self.vars_filename + ".dat"):
            vars_store = shelve.open(self.vars_filename)
        else:
            # no files available, return nothing
            self.log.warning("DATA WARNING - data store files are not available.")
            return None, None, None

        # build metadata
        metadata_obj = vars_store["metadata"]
        saved_spec = metadata_obj["spec"]
        current_step = spec["RESUME_AFTER"]
        completed_step = metadata_obj["completed_step"]
        saved_completed_steps = spec["STEPS"][: spec["STEPS"].index(completed_step) + 1]
        current_completed_steps = saved_spec["STEPS"][
            : saved_spec["STEPS"].index(completed_step) + 1
        ]
        if completed_step != current_step:
            # steps do not match, return nothing
            self.log.warning(
                "CONFIG WARNING - data file has step %s but config wants to resume from step %s.",
                completed_step,
                current_step,
            )
            return None, None, None
        if saved_completed_steps != current_completed_steps:
            # steps do not match, return nothing
            self.log.warning(
                "CONFIG WARNING - data file has previous steps %s do not match config %s.",
                saved_completed_steps,
                current_completed_steps,
            )
            return None, None, None

        # build data objects
        for var_name in metadata_obj["var_list"]:
            vars_obj[var_name] = vars_store[var_name]
        for df_name in metadata_obj["dfs_list"]:
            input_df_filename = self.dfs_filename_pattern.format(df_name=df_name)
            dfs_obj[df_name] = pd.read_parquet(input_df_filename, engine="pyarrow")
        for gdf_name in metadata_obj["gdf_list"]:
            gdfs_obj[gdf_name] = gpd.read_file(
                self.gdfs_filename, layer=gdf_name, driver="GPKG"
            )
        # check and read additional tables added to spec
        missing_spatials = set(spec["FILES"]["SPATIALS"].keys()).difference(
            set(metadata_obj["gdf_list"])
        )
        query_spec = spec.copy()
        missing_tbls = set(spec["FILES"]["INPUTS"].keys()).difference(
            set(metadata_obj["dfs_list"])
        )
        if len(missing_tbls) > 0:
            query_spec["FILES"]["INPUTS"] = {
                key: query_spec["FILES"]["INPUTS"][key] for key in list(missing_tbls)
            }
            missing_dfs = data_tables.read_tbl_data(s=query_spec)
            for tbl_name in missing_dfs.keys():
                dfs_obj[tbl_name] = missing_dfs[tbl_name].copy()
        if len(missing_spatials) > 0:
            query_spec["FILES"]["SPATIALS"] = {
                key: query_spec["FILES"]["SPATIALS"][key]
                for key in list(missing_spatials)
            }
            missing_gdfs = data_tables.read_spatial_data(s=query_spec)
            for tbl_name in missing_gdfs.keys():
                gdfs_obj[tbl_name] = missing_gdfs[tbl_name].copy()

        # check and load vars object
        for stored_var_name, stored_var_value in spec["VARS"].items():
            if stored_var_name not in list(vars_obj.keys()):
                # warn that new variable values will be inserted
                self.log.warning(
                    "CONFIG WARNING - Variables %s is new, so it will be added.",
                    stored_var_name,
                )
                vars_obj[stored_var_name] = stored_var_value
            if stored_var_value != vars_obj[stored_var_name]:
                # warn if variable values has changed
                self.log.warning(
                    "CONFIG WARNING - Variables %s have changed, using saved value %s instead of %s.",
                )

        # close data stores
        vars_store.close()

        # since we have successful resume after data loaded, write mode is now disabled
        self.data_store_write_mode = False

        # return data
        return vars_obj, dfs_obj, gdfs_obj

    def save_all_data(self, vars_obj, dfs_obj, gdfs_obj, current_step: str, spec: dict):
        # skip write if step matches resume after or write mode is False
        if self.data_store_write_mode == False or current_step != spec["RESUME_AFTER"]:
            return False

        # build metadata
        metadata_obj = {
            "var_list": list(vars_obj.keys()),
            "dfs_list": list(dfs_obj.keys()),
            "gdf_list": list(gdfs_obj.keys()),
            "spec": spec,
            "completed_step": current_step,
        }

        # clean up old files
        for file in [
            self.vars_filename + ".bak",
            self.vars_filename + ".dat",
            self.vars_filename + ".dir",
            self.dfs_filename_pattern,
            self.gdfs_filename,
        ]:
            if os.path.exists(file):
                os.remove(file)

        # establish data stores
        vars_store = shelve.open(self.vars_filename)

        # assign data into data stores
        vars_store["metadata"] = metadata_obj
        for var_name in metadata_obj["var_list"]:
            vars_store[var_name] = vars_obj[var_name]
        for df_name in metadata_obj["dfs_list"]:
            export_df_filename = self.dfs_filename_pattern.format(df_name=df_name)
            if os.path.exists(export_df_filename):
                os.remove(export_df_filename)
            # fix data types
            for var_name, inferred_type in (
                (dfs_obj[df_name].apply(pd.api.types.infer_dtype, axis=0))
                .to_dict()
                .items()
            ):
                if "mixed" in inferred_type:
                    data_type = "str"
                elif inferred_type == "decimal":
                    data_type = "float64"
                elif inferred_type == "string":
                    data_type = "str"
                elif inferred_type == "integer":
                    # use float for int in case there are na values
                    data_type = "float64"
                elif inferred_type == "floating":
                    data_type = "float64"
                elif inferred_type == "date":
                    data_type = "datetime64"
                else:
                    data_type = "str"
                dfs_obj[df_name][var_name] = dfs_obj[df_name][var_name].astype(
                    data_type
                )
                # fix non string column names
                if type(var_name) != str:
                    dfs_obj[df_name][str(var_name)] = dfs_obj[df_name][var_name].copy()
                    dfs_obj[df_name] = dfs_obj[df_name].drop(columns=[var_name])

            # export to parquet
            dfs_obj[df_name].to_parquet(export_df_filename, engine="pyarrow")
        for gdf_name in metadata_obj["gdf_list"]:
            gdfs_obj[gdf_name].to_file(
                self.gdfs_filename, layer=gdf_name, driver="GPKG"
            )

        # close and save data stores
        vars_store.close()

        return True
