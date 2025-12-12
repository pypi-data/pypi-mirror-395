import os
import pandas as pd
from tlpytools.adls_server import adls_tables
from tlpytools.sql_server import azure_td_tables


def main():
    df_dict = dict()
    example_file = "src/examples/data_files/example.csv"
    df_dict["tbl_example"] = pd.read_csv(example_file)

    # test writing to and reading from azure sql server
    out_files = {"tbl_example": "td_2023.example.azuresql"}
    print("writing to azure sql...")
    azure_td_tables.write_tables(out_files, df_dict)
    fsch = out_files["tbl_example"].split(".")[0]
    ftbl = out_files["tbl_example"].split(".")[1]
    print("reading from azure sql...")
    azure_td_tables.read_tables(schema=fsch, table=ftbl)

    # test writing to and reading from azure data lake
    adls_base = os.getenv("ORCA_ADLS_URL", "yourstorageaccount.dfs.core.windows.net")
    adls_base_url = f"https://{adls_base}" if adls_base else None

    if adls_base_url:
        out_files = {"tbl_example": f"{adls_base_url}/dev/temp_tables/example.csv"}
        print("writing to azure adls...")
        adls_tables.write_table_by_name(
            uri=out_files["tbl_example"],
            local_path=os.path.dirname(example_file),
            file_name=os.path.basename(example_file),
        )
        print("reading from azure adls...")
        bytes_io = adls_tables.get_table_by_name(uri=out_files["tbl_example"])
        tbl = "tbl_example"
        file_type = "csv"
        file_name = f"{tbl}.{file_type}"
        cache_dir = os.environ.get("TLPT_ADLS_CACHE_DIR", "C:/Temp/tlpytools/adls")
        cache_file = os.path.join(cache_dir, file_name)
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_file, "wb") as file:
            file.write(bytes_io.getbuffer())
        df = pd.read_csv(cache_file)
    else:
        print("⚠️  ORCA_ADLS_URL not configured, skipping ADLS tests")


if __name__ == "__main__":
    main()
