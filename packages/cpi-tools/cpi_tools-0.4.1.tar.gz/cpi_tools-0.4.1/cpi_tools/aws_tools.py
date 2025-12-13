
import pandas as pd
import boto3
from botocore.exceptions import ClientError

import s3fs  # required so pandas can read/write s3:// URLs
from io import StringIO
from typing import Optional, List

def build_s3_key(s3_path: str, file_or_relative_path: str) -> str:
    """
    Build a clean S3 object key from a base path/prefix and a file or relative path.

    Parameters:
    - s3_path (str): Base path or prefix in the S3 bucket (e.g., "foo/bar" or "/foo/bar/").
    - file_or_relative_path (str): File name or relative path under the prefix.

    Returns:
    - str: Normalized S3 key with no leading slash.

    Examples:
    - build_s3_key("foo/bar", "file.csv") -> "foo/bar/file.csv"
    - build_s3_key("/foo/bar/", "nested/file.csv") -> "foo/bar/nested/file.csv"
    """
    base = s3_path.strip("/")
    rel = file_or_relative_path.lstrip("/")
    if base:
        return f"{base}/{rel}"
    return rel


def get_s3_resource():
    """
    Get a boto3 S3 resource.

    Parameters:
    - (none)

    Returns:
    - boto3.resources.base.ServiceResource: Boto3 S3 resource for S3.
    """
    return boto3.resource("s3")


def check_s3_object_exists(bucket: str, key: str) -> bool:
    """
    Check if an S3 object exists.

    Parameters:
    - bucket (str): S3 bucket name.
    - key (str): Object key within the bucket.

    Returns:
    - bool: True if the object exists, False otherwise.

    Raises:
    - RuntimeError: If there is an unexpected error checking the object.

    Examples:
    - check_s3_object_exists("my-bucket", "path/to/file.csv")
    """
    s3 = get_s3_resource()
    try:
        s3.Object(bucket, key).load()
        return True
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "404":
            return False
        raise RuntimeError(
            f"Error checking S3 object existence: s3://{bucket}/{key}"
        ) from e


def list_s3_objects(
    bucket: str, prefix: str
) -> List["boto3.resources.factory.s3.ObjectSummary"]:
    """
    List S3 objects under a given prefix.

    Parameters:
    - bucket (str): S3 bucket name.
    - prefix (str): Prefix (folder-like path) to filter objects.

    Returns:
    - list[boto3.resources.factory.s3.ObjectSummary]: List of object summaries
      under the prefix.

    Examples:
    - list_s3_objects("my-bucket", "path/to/folder/")
    """
    s3 = get_s3_resource()
    return list(s3.Bucket(bucket).objects.filter(Prefix=prefix))

def read_from_s3(
    s3_bucket: str,
    s3_file_path: str,
    file_name: str,
    file_type: str = "csv",
    sheet_name: Optional[str] = None,
    skip_rows: int = 0,
) -> pd.DataFrame:
    """
    Read a CSV, Excel, or Parquet file from S3 into a pandas DataFrame.

    Parameters:
    - s3_bucket (str): Name of the S3 bucket where the file is located.
    - s3_file_path (str): Folder/prefix within the S3 bucket.
    - file_name (str): Base file name (without extension) to be read.
    - file_type (str): File type to read ("csv", "xlsx", "parquet").
                      Defaults to "csv".
    - sheet_name (str | None): Excel sheet name to read (only for xlsx).
    - skip_rows (int): Number of rows to skip when reading CSV/Excel.

    Returns:
    - pd.DataFrame: Data read from the S3 object.

    Examples:
    - read_from_s3("my-bucket", "data", "table")
    - read_from_s3("my-bucket", "data", "table", file_type="xlsx")
    - read_from_s3("my-bucket", "data", "table", file_type="parquet")
    """

    # ---- Build key based on file type ----
    if file_type == "csv":
        key = build_s3_key(s3_file_path, f"{file_name}.csv")
    elif file_type == "xlsx":
        key = build_s3_key(s3_file_path, f"{file_name}.xlsx")
    elif file_type == "parquet":
        key = build_s3_key(s3_file_path, f"{file_name}.parquet")
    else:
        raise ValueError(
            f"Unsupported file_type '{file_type}'. "
            "Supported: 'csv', 'xlsx', 'parquet'."
        )

    # ---- Existence check ----
    if not check_s3_object_exists(s3_bucket, key):
        raise FileNotFoundError(f"S3 object does not exist: s3://{s3_bucket}/{key}")

    s3_url = f"s3://{s3_bucket}/{key}"

    # ---- Read based on type ----
    if file_type == "csv":
        return pd.read_csv(s3_url, skiprows=skip_rows, encoding="utf-8")

    elif file_type == "xlsx":
        read_kwargs = {"skiprows": skip_rows}
        if sheet_name is not None:
            read_kwargs["sheet_name"] = sheet_name
        return pd.read_excel(s3_url, **read_kwargs)

    elif file_type == "parquet":
        return pd.read_parquet(s3_url)



def write_to_s3(
    df: pd.DataFrame,
    s3_bucket: str,
    s3_file_path: str,
    file_name: str,
) -> None:
    """
    Write a pandas DataFrame to S3 as a CSV file.

    Parameters:
    - df (pd.DataFrame): DataFrame to be written to S3.
    - s3_bucket (str): Name of the S3 bucket where the file will be saved.
    - s3_file_path (str): Folder/prefix within the S3 bucket.
    - file_name (str): Base file name (without extension) to be saved.

    Returns:
    - None

    Examples:
    - write_to_s3(df, "my-bucket", "data/processed", "output_table")
      # writes s3://my-bucket/data/processed/output_table.csv
    """
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")

    key = build_s3_key(s3_file_path, f"{file_name}.csv")
    s3_resource = get_s3_resource()
    s3_resource.Object(s3_bucket, key).put(Body=csv_buffer.getvalue())


def write_to_s3_parquet(
    df: pd.DataFrame,
    numeric_cols: List[str],
    s3_bucket: str,
    s3_file_path: str,
    file_name: str,
) -> None:
    """
    Write a pandas DataFrame to S3 in Parquet format, with specified columns
    cast to nullable Float64 (useful for Athena).

    Parameters:
    - df (pd.DataFrame): DataFrame to be written to S3.
    - numeric_cols (list[str]): List of column names in df that should be
      stored as numeric (Float64) in the Parquet file.
    - s3_bucket (str): Name of the S3 bucket where the file will be saved.
    - s3_file_path (str): Folder/prefix within the S3 bucket.
    - file_name (str): Base file name (without extension) to be saved.

    Returns:
    - None

    Examples:
    - write_to_s3_parquet(df, ["amount", "year"], "my-bucket", "data", "table_parquet")
      # writes s3://my-bucket/data/table_parquet.parquet
    """
    # Store everything as string by default, then cast selected columns to Float64
    df = df.astype("string")
    for col in numeric_cols:
        df[col] = df[col].astype("Float64")

    key = build_s3_key(s3_file_path, f"{file_name}.parquet")
    s3_url = f"s3://{s3_bucket}/{key}"

    df.to_parquet(s3_url, index=False)

    print("Data written to S3")
    print("Copy below when adding bulk schema in Athena")
    for col in df.columns:
        col_type = df[col].dtype
        if col_type == "Float64":
            col_type = "double"
        print(f"{col} {col_type}, ")
