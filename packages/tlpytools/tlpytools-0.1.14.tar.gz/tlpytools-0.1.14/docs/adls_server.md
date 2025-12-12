# Working with the Azure DataLake Server (ADLS)

# Important settings

## URL for Azure SQL

`TLPT_AZURE_SQL_URI` environment variable should be set to your Azure SQL Server URI (e.g., `yourserver.database.windows.net`)

For url of adls, that is set using the file identifier as part of the https path.

## Cache Directory

Because ADLS Gen2 requires the data file (like csv, parquet, etc) to be either downloaded or uploaded from local direction, a temporary cache directory needed to be specified to work.

Specify your own custom directory with [`TLPT_ADLS_CACHE_DIR`, `C:/Temp/tlpytools/adls`] in your operating system. Check out [this guide for setting environment variable for Windows](https://www.thesagenext.com/support/set-environment-variables-in-windows). The default if nothing is set will be `C:/Temp/tlpytools/adls`.

Clean up of the entire folder will occur after a successful run of the function data_tables -> export_csv.

There is also a `TLPT_ADLS_CACHE_KEEP` environment variable with default of "0". Set it to "1" to keep all of the cached content. This is not recommended since it can lead to sensitive data being kept on disk, so do remember to clear the cache file location manually and often if you decide to keep the cache.

# Usage for ADLS Gen2 

## In yaml config with tlpytools.config

```python
# import libraries
from tlpytools.log import logger
from tlpytools.config import run_yaml
import yaml

# define main class
class mydataproject(logger, run_yaml):
    # ...
```

Simply add input or output path to file name that resides in ADLS Gen2, where `example_adls_domain` is the resource name of the data lake, `.dfs.core.windows.net` is the domain of the service provider Azure, `dev` is the container / top directory name, the rest is the subdirectory and file path.

```json
"FILES": {
    "INPUTS": {
        "example_csv": "https://example_adls_domain.dfs.core.windows.net/dev/temp_tables/example.parquet",
    },
    "INPUT_COLUMNS": {
        "example_csv": ["ID", "Example_Data", "Example_Data2"]
    },
    "OUTPUTS": {
        "example_csv": "https://example_adls_domain.dfs.core.windows.net/dev/temp_tables/example.parquet",
    },
},
```

## Directly in Python script

```python
import os
import pandas as pd
from tlpytools.adls_server import adls_tables


def main():
    df_dict = dict()
    example_file = "src/examples/data_files/example.csv"
    df_dict["tbl_example"] = pd.read_csv(example_file)

    # test writing to and reading from azure data lake
    out_files = {
        "tbl_example": "https://example_adls_domain.dfs.core.windows.net/dev/temp_tables/example.csv"
    }
    print("writing to azure adls...")
    adls_tables.write_table_by_name(
        uri=out_files["tbl_example"],
        local_path=os.path.dirname(example_file),
        file_name=os.path.basename(example_file),
    )
    print("reading from azure adls...")
    test_bytes = adls_tables.get_table_by_name(uri=out_files["tbl_example"])
    print(pd.read_csv(test_bytes))


if __name__ == "__main__":
    main()
```