import yaml
import os
import re

# Optional imports to avoid circular dependencies
try:
    from tlpytools.log import logger

    HAS_LOGGER = True
except ImportError:
    HAS_LOGGER = False
    logger = None

try:
    from tlpytools.data import data_tables

    HAS_DATA_TABLES = True
except ImportError:
    HAS_DATA_TABLES = False
    data_tables = None

try:
    from tlpytools.data_store import DataStore

    HAS_DATA_STORE = True
except ImportError:
    HAS_DATA_STORE = False
    DataStore = None


def load_config(config_file):
    """
    Load configuration from YAML file.

    Args:
        config_file (str): Path to YAML configuration file

    Returns:
        dict: Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config


def load_config_with_env(config_file):
    """
    Load configuration from YAML file with environment variable substitution.

    Supports ${VAR_NAME} syntax for environment variable substitution.

    Args:
        config_file (str): Path to YAML configuration file

    Returns:
        dict: Configuration dictionary with environment variables substituted
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, "r") as f:
        content = f.read()

    # Substitute environment variables
    def env_var_replacer(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    content = re.sub(r"\$\{([^}]+)\}", env_var_replacer, content)

    config = yaml.safe_load(content)
    return config


def get_config_value(config, key_path, default=None):
    """
    Get configuration value using dot notation.

    Args:
        config (dict): Configuration dictionary
        key_path (str): Dot-separated path to configuration value (e.g., 'database.host')
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    keys = key_path.split(".")
    value = config

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def validate_config(config, required_keys=None):
    """
    Validate configuration against required keys.

    Args:
        config (dict): Configuration dictionary
        required_keys (list): List of required key paths (dot notation)

    Returns:
        bool: True if all required keys are present
    """
    if required_keys is None:
        return True

    for key_path in required_keys:
        if get_config_value(config, key_path) is None:
            return False

    return True


def merge_configs(*configs):
    """
    Merge multiple configuration dictionaries.

    Later configurations override earlier ones.

    Args:
        *configs: Configuration dictionaries to merge

    Returns:
        dict: Merged configuration
    """
    merged = {}

    for config in configs:
        merged = _deep_merge(merged, config)

    return merged


def _deep_merge(dict1, dict2):
    """
    Deep merge two dictionaries.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary (takes precedence)

    Returns:
        dict: Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value

    return result


class run_yaml:
    """usage: run in order
    - load_yaml
    - load_yaml_data
    - load_yaml_spatials (optional)
    - run_steps
    """

    def load_yaml(self, filename=None):
        """
        read yaml, initialize data objects, and returns yaml file
        """
        if filename == None:
            filename = "{}.yaml".format(type(self).__name__)
        with open(filename) as f:
            s = yaml.load(f, Loader=yaml.SafeLoader)
        if "FILES" in s:
            self.load_yaml_data(s)

        self.s = s
        return self.s

    def load_yaml_data(self, s):
        """load yaml global variables and dataframe, and return them.

        Args:
            s (setting from load_yaml): setting from load_yaml

        Returns:
            s, dfs: setting and dataframe dictionary
        """

        self.data_store = DataStore()

        if "RESUME_AFTER" not in s:
            s["RESUME_AFTER"] = ""

        # if RESUME_AFTER has been set, read from existing files
        if s["RESUME_AFTER"] in list(s["STEPS"]):
            vars_obj, dfs_obj, gdfs_obj = self.data_store.load_existing_data(spec=s)
            if vars_obj != None:
                self.resume_after = s["RESUME_AFTER"]
                for var_name in list(vars_obj.keys()):
                    setattr(self, var_name, vars_obj[var_name])
                self.dfs = dfs_obj
                self.gdfs = gdfs_obj
                return self.dfs, self.gdfs
            else:
                self.resume_after = ""
                if hasattr(self, "log") and self.log:
                    self.log.warning(
                        "CONFIG WARNING - RESUME_AFTER is ignored since there's no valid data files available."
                    )
                elif HAS_LOGGER and logger:
                    print(
                        "CONFIG WARNING - RESUME_AFTER is ignored since there's no valid data files available."
                    )
                else:
                    print(
                        "CONFIG WARNING - RESUME_AFTER is ignored since there's no valid data files available."
                    )

        # otherwise, create new data stores
        if "VARS" in s:
            self.resume_after = ""
            for var in s["VARS"].keys():
                setattr(self, var, s["VARS"][var])
        # read table data
        if "FILES" in s:
            self.dfs = {}
            self.gdfs = {}
            if "INPUTS" in s["FILES"]:
                if s["FILES"]["INPUTS"] is not None:
                    self.dfs = data_tables.read_tbl_data(s)
            # read spatial table data
            if "SPATIALS" in s["FILES"]:
                if s["FILES"]["SPATIALS"] is not None:
                    self.gdfs = data_tables.read_spatial_data(s)
        return self.dfs, self.gdfs

    def run_steps(self, s, log=None):
        """run steps specified in setting s

        Args:
            s (dict): specification from yaml
            log (object): logger object
        """
        # handle no logger
        if log == None:
            log = logger()
            log.init_logger()

        # exclude skipped steps
        if (
            s["RESUME_AFTER"] in list(s["STEPS"])
            and self.resume_after == s["RESUME_AFTER"]
        ):
            skip_step_index = s["STEPS"].index(s["RESUME_AFTER"])
            run_step_list = s["STEPS"][skip_step_index + 1 :]
        else:
            run_step_list = s["STEPS"]

        # perform steps
        for step in run_step_list:
            log.info("===={}====".format(step))
            if step not in s:
                s[step] = None
            # run current step
            eval("self.{}".format(step))(spec=s[step], files=s["FILES"])
            # save data at the end of current step
            vars_obj = {}
            for var_name in list(s["VARS"].keys()):
                vars_obj[var_name] = getattr(self, var_name)
            store_save_status = self.data_store.save_all_data(
                vars_obj=vars_obj,
                dfs_obj=self.dfs,
                gdfs_obj=self.gdfs,
                current_step=step,
                spec=s,
            )
            if store_save_status == True:
                log.info("data store for resume after step {} saved.".format(step))
            log.info("step {} completed.".format(step))

    def export_data_csv(self, spec, files):
        """wrapper function for exporting file outputs as csv;
        self.dfs must contain DataFrame tables for export.

        Args:
            spec (dict): large specification containing the imputation settings, see yaml file under 'impute_hh_income'
            files (dict):  a list of input and output file names
        """
        if "OUTPUTS" in files:
            data_tables.export_csv(dict_df=self.dfs, ofiles=files["OUTPUTS"])
        else:
            raise ValueError("data export called when no export files are specified.")

    def export_data(self, spec, files):
        """wrapper function for exporting file outputs as csv;
        self.dfs must contain DataFrame tables for export.

        Args:
            spec (dict): large specification containing the imputation settings, see yaml file under 'impute_hh_income'
            files (dict):  a list of input and output file names
        """
        if "OUTPUTS" in files:
            # append all data frames into a big dictionary
            dfs_combined = {}
            for key, value in self.dfs.items():
                dfs_combined[key] = value
            if self.gdfs is not None:
                for key, value in self.gdfs.items():
                    dfs_combined[key] = value
            # call data export
            data_tables.export_data(dict_df=dfs_combined, ofiles=files["OUTPUTS"])
        else:
            raise ValueError("data export called when no export files are specified.")

    @staticmethod
    def get_sample_spec():
        """returns a sample data specificationf or config"""
        example_spec = {
            "__COMMENT__": "THIS IS AN AUTOGENERATED YAML FILE example.",
            "FILES": {
                "INPUTS": {
                    "tbl1": "td_2017.tbl1.crypt",
                    "tbl2": "td_2017.tbl2.sqlsvr",
                    "tbl3": "data_files/tbl3.csv",
                },
                "SPATIALS": {
                    "region_taz": "Inputs/ShpFiles/TAZ1700_GY_v7.shp",
                    "external_crossings": "Inputs/ShpFiles/external_crossings.json",
                },
                "INPUT_COLUMNS": {"tbl_blended_skim": ["col1", "col2", "col3"]},
                "OUTPUTS": {
                    "tblOut1": "tblOut1.csv",
                },
            },
            "VARS": {
                "colTAZ": "TAZ",
                "colSubSeed": "SubSeedGeo",
                "colSeed": "SeedGeo",
                "tblCTName": "tblCTMV",
                "tblGeoName": "tblGeo",
                "tblHHWgtName": "tblHHWeights",
                "geoStructure": "A1_9_44",
                "clearMem": True,
            },
            "STEPS": ["example_step1", "export_data_csv"],
            "example_step1": {"test": "test_val"},
        }

        return example_spec
