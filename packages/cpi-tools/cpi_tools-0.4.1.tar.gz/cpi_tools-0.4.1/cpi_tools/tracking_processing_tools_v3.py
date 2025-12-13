import os
import pandas as pd
import numpy as np
import io
import unicodedata
from datetime import date
import uuid
from dotenv import load_dotenv, find_dotenv
import s3fs
import boto3
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from cpi_tools import sharepoint_tools, aws_tools

S3_STAGE = 'cpi-uk-us-datascience-stage'

"""
######################################################################################################
######################## File functions  ############################
######################################################################################################

"""

# ===============================================
# Internal helper functions
# ===============================================

def create_temp_dir(prefix: str) -> Path:
    """
    Create a temporary directory and return it as a Path.

    Parameters:
    - prefix : str
        Prefix for the temporary directory name.

    Returns:
    - Path
        Path to the newly created temporary directory.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix=prefix))
    print(f"Created temporary folder: {tmp_dir}")
    return tmp_dir


def cleanup_temp_dir(tmp_dir: Path) -> None:
    """
    Recursively delete a temporary directory, ignoring common errors.

    Parameters:
    - tmp_dir : Path
        Directory to be deleted.
    """
    try:
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
            print(f"✓ Cleaned up temp folder: {tmp_dir}")
    except Exception as e:
        print(f"⚠ Warning: failed to remove temp folder '{tmp_dir}': {e}")

 
# ===============================================
# Public file-level functions: SharePoint ↔ S3
# ===============================================

def export_sharepoint_file_to_s3(
    sharepoint_file_path: str,
    sharepoint_site: str,
    s3_bucket: str,
    s3_path: str,
    s3_file_name: str,
    overwrite: bool = False,
    sp_client: Optional["GraphSharePointClient"] = None,
) -> None:
    """
    Export a single file from SharePoint to an Amazon S3 bucket.

    Behavior
    --------
    - Normalizes the SharePoint path (handles optional '/sites/...').
    - Downloads the file into a dedicated temporary folder on local disk.
    - Checks if the S3 destination exists:
        * overwrite=False (default): raises FileExistsError if S3 object exists.
        * overwrite=True: allows replacement of the S3 object.
    - Uploads the downloaded file into S3, at key: `<s3_path>/<s3_file_name>`.
    - Cleans up the temporary folder afterward.

    Parameters:
    - sharepoint_file_path : str
        Path to the file in SharePoint. Can be:
            * 'Shared Documents/foo/bar.csv'
            * '/sites/program/Shared Documents/foo/bar.csv'
    sharepoint_site : str
        Site key for GraphSharePointClient (e.g., 'PROGRAM').
    s3_bucket : str
        Target S3 bucket name.
    s3_path : str
        Path/prefix in the S3 bucket (e.g., 'tracking/output/').
    s3_file_name : str
        File name to use in S3 (the tail of the key).
    overwrite : bool, default False
        Whether to overwrite an existing S3 object if it exists.
    sp_client : GraphSharePointClient or None, optional
        Optional pre-configured and authenticated SharePoint client.
        If None, a new client is created and authenticated.
    
    Raises:
    - FileNotFoundError
        If the SharePoint file does not exist.
    - FileExistsError
        If the S3 object exists and overwrite=False.
    - RuntimeError
        For problems with authentication, SharePoint download, or S3 upload.
    """
    client = sharepoint_tools.init_sharepoint_client(sharepoint_site, sp_client)
    sp_path = sharepoint_tools.normalize_sharepoint_path(sharepoint_file_path)
    s3_key = aws_tools.build_s3_key(s3_path, s3_file_name)

    # Check S3 destination if overwrite=False
    if not overwrite and aws_tools.check_s3_object_exists(s3_bucket, s3_key):
        raise FileExistsError(
            f"S3 object exists and overwrite=False: s3://{s3_bucket}/{s3_key}"
        )

    # Temporary folder & local file path
    tmp_dir = create_temp_dir("sharepoint_to_s3_file_")
    local_file_name = Path(sp_path).name
    local_path = tmp_dir / local_file_name

    try:
        # Download SharePoint → local (always overwrite temp files)
        client.download_file(sp_path, local_path.as_posix(), overwrite=True)
        print(f"✓ Downloaded SharePoint → {local_path}")

        # Upload local → S3
        s3 = aws_tools.get_s3_resource()
        s3.Bucket(s3_bucket).upload_file(local_path.as_posix(), Key=s3_key)
        print(f"✓ Uploaded to S3 → s3://{s3_bucket}/{s3_key}")

    finally:
        cleanup_temp_dir(tmp_dir)


def export_s3_file_to_sharepoint(
    s3_bucket: str,
    s3_path: str,
    s3_file_name: str,
    sharepoint_file_path: str,
    sharepoint_site: str,
    overwrite: bool = False,
    sp_client: Optional["GraphSharePointClient"] = None,
) -> None:
    """
    Export a single file from Amazon S3 to SharePoint.

    Behavior
    --------
    - Builds the S3 key from `s3_path` and `s3_file_name`.
    - Verifies the S3 object exists before proceeding.
    - Normalizes the SharePoint target path (handles optional '/sites/...').
    - Checks SharePoint for an existing file and honors overwrite rules:
        * overwrite=False (default): raises FileExistsError if the SP file exists.
        * overwrite=True: allows replacing the existing SP file.
    - Downloads from S3 into a temporary local folder.
    - Ensures the target SharePoint folder exists (if supported by the client).
    - Uploads the local file to SharePoint at the normalized path.
    - Cleans up the temporary folder afterward.

    Parameters:
    - s3_bucket : str
        Source S3 bucket name.
    - s3_path : str
        Path/prefix under which the file resides in S3.
    - s3_file_name : str
        File name in S3 (object name tail).
    - sharepoint_file_path : str
        Target file path in SharePoint. May be either:
            * 'Shared Documents/Workstreams/Tracking/example_file.csv'
            * '/sites/program/Shared Documents/Workstreams/Tracking/example_file.csv'
    - sharepoint_site : str
        Site key for GraphSharePointClient (e.g. 'PROGRAM').
    - overwrite : bool, default False
        Whether to overwrite the SharePoint file if it already exists.
    - sp_client : GraphSharePointClient or None, optional
        Optional pre-configured and authenticated SharePoint client.
        If None, a new client is created and authenticated.

    Raises:
    - FileNotFoundError
        If the S3 object does not exist.
    - FileExistsError
        If the SharePoint file exists and overwrite=False.
    RuntimeError
        For problems with authentication, S3 download, or SharePoint upload.
    """
    client = sharepoint_tools.init_sharepoint_client(sharepoint_site, sp_client)

    # Build S3 key + verify it exists
    s3_key = aws_tools.build_s3_key(s3_path, s3_file_name)
    if not aws_tools.check_s3_object_exists(s3_bucket, s3_key):
        raise FileNotFoundError(f"S3 object not found: s3://{s3_bucket}/{s3_key}")

    # Normalize SharePoint path
    sp_path = sharepoint_tools.normalize_sharepoint_path(sharepoint_file_path)

    # Check SharePoint existence + overwrite behavior
    if not overwrite and client.file_exists(sp_path):
        raise FileExistsError(
            f"SharePoint file already exists and overwrite=False: '{sp_path}'"
        )

    # Create a temp folder for S3 download
    tmp_dir = create_temp_dir("s3_to_sharepoint_file_")
    local_path = tmp_dir / s3_file_name

    try:
        # Download S3 → temp file
        s3 = aws_tools.get_s3_resource()
        s3.Object(s3_bucket, s3_key).download_file(local_path.as_posix())
        print(f"✓ Downloaded S3 → {local_path}")

        # Ensure SharePoint parent folder exists
        sp_folder = "/".join(sp_path.split("/")[:-1])
        client.ensure_sharepoint_folder(sp_folder)

        # Upload temp file → SharePoint (always overwrite temp → SharePoint)
        client.upload_file(local_path.as_posix(), sp_path, overwrite=True)
        print(f"✓ Uploaded to SharePoint → {sp_path}")

    finally:
        cleanup_temp_dir(tmp_dir)


# ===============================================
# Public folder-level functions: SharePoint ↔ S3
# ===============================================

def export_sharepoint_folder_to_s3(
    sharepoint_folder_path: str,
    sharepoint_site: str,
    s3_bucket: str,
    s3_prefix: str,
    overwrite: bool = False,
    recursive: bool = True,
    dry_run: bool = False,
    sp_client: Optional["GraphSharePointClient"] = None,
) -> None:
    """
    Export an entire SharePoint folder (optionally recursive) to an S3 prefix.

    Behavior
    --------
    - Normalizes the SharePoint folder path (handles optional '/sites/...').
    - Uses `client.describe_sharepoint_folder` to obtain a manifest of contents.
    - If `dry_run=True`, only prints what *would* be uploaded to S3 and returns.
    - If `dry_run=False`:
        * Downloads the SharePoint folder into a temporary local directory
          via `client.download_folder`.
        * Walks the local folder structure and uploads each file to S3 using
          key `<s3_prefix>/<relative_path>`.
        * The `overwrite` parameter controls whether existing S3 objects are replaced.
    - Cleans up the temporary folder at the end.

    Parameters:
    - sharepoint_folder_path : str
        Folder path in SharePoint. May be either:
            * 'Shared Documents/Workstreams/Tracking/'
            * '/sites/program/Shared Documents/Workstreams/Tracking/'
    - sharepoint_site : str
        Site key for GraphSharePointClient (e.g., 'PROGRAM').
    - s3_bucket : str
        Target S3 bucket name.
    - s3_prefix : str
        Destination prefix in S3 under which the folder contents will be uploaded.
    - overwrite : bool, default False
        Whether to overwrite existing S3 objects.
    - recursive : bool, default True
        Whether to include subfolders recursively.
    - dry_run : bool, default False
        If True, only prints actions (from the manifest) without downloading
        or uploading any files.
    - sp_client : GraphSharePointClient or None, optional
        Optional pre-configured and authenticated SharePoint client.
        If None, a new client is created and authenticated.

    Raises:
    - RuntimeError
        For problems describing or downloading the SharePoint folder, or
        for S3 upload issues.
    """
    client = sharepoint_tools.init_sharepoint_client(sharepoint_site, sp_client)
    sp_folder = sharepoint_tools.normalize_sharepoint_path(sharepoint_folder_path)

    # Get manifest from SharePoint
    manifest = client.describe_sharepoint_folder(sp_folder, recursive=recursive)

    files = [x for x in manifest if not x.get("is_folder")]
    folders = [x for x in manifest if x.get("is_folder")]

    total_files = len(files)
    total_bytes = sum(x.get("size", 0) for x in files)

    print("\n========= EXPORT SharePoint → S3 (FOLDER) =========")
    print(f"SharePoint source: {sp_folder}")
    print(f"S3 target bucket:  {s3_bucket}")
    print(f"S3 target prefix:  {s3_prefix}")
    print(f"Recursive:         {recursive}")
    print(f"Overwrite:         {overwrite}")
    print(f"Dry run:           {dry_run}")
    print(f"Folders:           {len(folders)}")
    print(f"Files:             {total_files}")
    print(f"Total size:        {total_bytes} bytes")
    print("===================================================\n")

    if total_files == 0:
        print("Nothing to export from SharePoint.")
        return

    # DRY RUN: print what would be uploaded
    if dry_run:
        print("🧪 DRY RUN — no files will be downloaded or uploaded.\n")
        for item in files:
            rel_path = item["relative_path"]
            s3_key = aws_tools.build_s3_key(s3_prefix, rel_path)
            print(f"[DRY RUN] Would upload SharePoint '{rel_path}' → s3://{s3_bucket}/{s3_key}")
        return

    # Non-dry run: download folder to temp, then upload to S3
    tmp_dir = create_temp_dir("sharepoint_folder_to_s3_")

    try:
        # Download entire SharePoint folder to temp (always overwrite temp files)
        client.download_folder(
            sp_folder_path=sp_folder,
            local_folder=tmp_dir.as_posix(),
            overwrite=True,
            recursive=recursive,
            dry_run=False,
        )

        # Walk temp folder and upload files to S3
        s3 = aws_tools.get_s3_resource()
        bucket = s3.Bucket(s3_bucket)

        for local_file in tmp_dir.rglob("*"):
            if local_file.is_dir():
                continue

            rel_path = local_file.relative_to(tmp_dir).as_posix()
            s3_key = aws_tools.build_s3_key(s3_prefix, rel_path)

            # Check if S3 object exists and skip if overwrite=False
            if not overwrite and aws_tools.check_s3_object_exists(s3_bucket, s3_key):
                print(f"⚠ Skipping upload; S3 object exists: s3://{s3_bucket}/{s3_key}")
                continue

            bucket.upload_file(local_file.as_posix(), Key=s3_key)
            print(f"✓ Uploaded {local_file.name} → s3://{s3_bucket}/{s3_key}")

    finally:
        cleanup_temp_dir(tmp_dir)

def export_s3_folder_to_sharepoint(
    s3_bucket: str,
    s3_prefix: str,
    sharepoint_folder_path: str,
    sharepoint_site: str,
    overwrite: bool = False,
    recursive: bool = True,
    dry_run: bool = False,
    sp_client: Optional["GraphSharePointClient"] = None,
) -> None:
    """
    Export an S3 prefix (folder-like) to a SharePoint folder.

    Behavior
    --------
    - Lists S3 objects under the given prefix.
    - If `recursive=True`, includes all nested keys.
      If `recursive=False`, only includes objects directly under the prefix
      (no further '/' in the relative path).
    - If `dry_run=True`, prints which S3 objects would be mapped and uploaded
      to which SharePoint paths, then returns.
    - If `dry_run=False`:
        * Downloads all selected S3 objects to a local temporary folder,
          preserving the relative folder structure.
        * Uses `client.upload_folder` to upload that local folder contents
          to the SharePoint folder.
    - Cleans up the temporary folder afterward.

    Notes
    -----
    This relies on the presence of an `upload_folder` method on your
    GraphSharePointClient, with a signature logically equivalent to:

        upload_folder(
            local_folder: str,
            sp_folder_path: str,
            overwrite: bool = False,
            recursive: bool = True,
            dry_run: bool = False,
        )

    Parameters:
    - s3_bucket : str
        Source S3 bucket name.
    - s3_prefix : str
        Folder-like prefix in S3 whose contents will be exported.
    - sharepoint_folder_path : str
        Target folder path in SharePoint. May be either:
            * 'Shared Documents/Workstreams/Tracking/'
            * '/sites/program/Shared Documents/Workstreams/Tracking/'
    - sharepoint_site : str
        Site key for GraphSharePointClient (e.g. 'PROGRAM').
    - overwrite : bool, default False
        Whether to overwrite files in SharePoint when uploading.
    - recursive : bool, default True
        If True, include nested prefixes/keys. If False, only include
        "top-level" keys under `s3_prefix`.
    - dry_run : bool, default False
        If True, do not download or upload anything; only print actions.
    - sp_client : GraphSharePointClient or None, optional
        Optional pre-configured and authenticated SharePoint client.
        If None, a new client is created and authenticated.

    Raises:
    - FileNotFoundError
        If no S3 objects are found under the given prefix.
    - RuntimeError
        For problems listing or downloading from S3, or for SharePoint uploads.
    """
    client = sharepoint_tools.init_sharepoint_client(sharepoint_site, sp_client)
    sp_folder = sharepoint_tools.normalize_sharepoint_path(sharepoint_folder_path)

    prefix = s3_prefix.strip("/")
    objects = aws_tools.list_s3_objects(s3_bucket, prefix)

    if not objects:
        raise FileNotFoundError(
            f"No S3 objects found under prefix 's3://{s3_bucket}/{prefix}'"
        )

    # Filter for non-recursive case
    def _rel_key(full_key: str) -> str:
        if prefix:
            return full_key[len(prefix):].lstrip("/")
        return full_key

    if not recursive:
        objects = [obj for obj in objects if "/" not in _rel_key(obj.key)]

    if not objects:
        print("No objects to export after applying recursion filter.")
        return

    # Summaries
    total_files = len(objects)
    total_bytes = sum(getattr(obj, "size", 0) for obj in objects)

    print("\n========= EXPORT S3 → SharePoint (FOLDER) =========")
    print(f"S3 source bucket:  {s3_bucket}")
    print(f"S3 source prefix:  {prefix}")
    print(f"SharePoint target: {sp_folder}")
    print(f"Recursive:         {recursive}")
    print(f"Overwrite:         {overwrite}")
    print(f"Dry run:           {dry_run}")
    print(f"Files:             {total_files}")
    print(f"Total size:        {total_bytes} bytes")
    print("===================================================\n")

    # DRY RUN: Print mapping only
    if dry_run:
        print("🧪 DRY RUN — no files will be downloaded or uploaded.\n")
        for obj in objects:
            rel = _rel_key(obj.key)
            target_path = "/".join(
                filter(None, [sp_folder.rstrip("/"), rel.replace("\\", "/")])
            )
            print(f"[DRY RUN] Would upload s3://{s3_bucket}/{obj.key} → SharePoint '{target_path}'")
        return

    # Non-dry run: download all S3 objects to temp, then call upload_folder
    tmp_dir = create_temp_dir("s3_folder_to_sharepoint_")

    try:
        s3 = aws_tools.get_s3_resource()
        bucket = s3.Bucket(s3_bucket)

        # Download all selected objects into temp dir preserving structure
        for obj in objects:
            rel = _rel_key(obj.key)
            local_path = tmp_dir / rel
            local_path.parent.mkdir(parents=True, exist_ok=True)

            bucket.download_file(obj.key, local_path.as_posix())
            print(f"✓ Downloaded s3://{s3_bucket}/{obj.key} → {local_path}")

        # Ensure target SharePoint folder exists
        client.ensure_sharepoint_folder(sp_folder)

        # Use upload_folder (assumes this method exists on the client)
        if not hasattr(client, "upload_folder"):
            raise RuntimeError(
                "GraphSharePointClient is missing 'upload_folder' method, "
                "required for folder-level export."
            )

        client.upload_folder(
            local_folder=tmp_dir.as_posix(),
            sp_folder_path=sp_folder,
            overwrite=overwrite,
            recursive=True,
            dry_run=False,
        )
        print(f"✓ Uploaded local folder {tmp_dir} → SharePoint folder '{sp_folder}'")

    finally:
        cleanup_temp_dir(tmp_dir)

"""
######################################################################################################
######################## Reference table functions ############################
######################################################################################################

"""

def process_reference_data(base_data, file_name=None, sql_field_name=None, col_name_row=0, start_row=3, project_type=False): 
    '''
    This function takes an unprocessed reference dataframe taken from the master reference table excel and converts it
    into a format useable within processing code
    
    If a filename is provided, it then writes this processed data to an s3 bucket 
    
    Parameters:
    - base_data: Pandas Dataframe
    - file_name: String
    - sql_field_name: String - If the reference table has a SQL Field name column, this is dropped
    - col_name_row: Int - selects the row that is used as the column names for the processed data
    - start_row: Int - Selects the row to start from, drops the rows prior to this one
    - project_type: Boolean - If project_type reference data, apply additional processing steps
    
    Returns:
    - df: Pandas Dataframe - processed reference data
    '''
    
    df = base_data.copy()

    #Set the column names to the correct rows
    df.columns = df.iloc[col_name_row]
    
    #If the ref table has a sql field, drop it
    if sql_field_name:

        df.drop(columns = sql_field_name, inplace=True)
    
    #Select the row to start from
    df = df.iloc[start_row:]
    
    #Drop columns called nan
    df = df.loc[:, df.columns.notna()]
    
    #If ref_project_type reference data, create a use column
    if project_type:
            df['use'] = df.apply(lambda x: generate_project_type_use(x['MI'], x['AD']), axis=1)
        
    
    #Drop rows where all values are nan
    df.dropna(axis = 0, how = 'all', inplace = True)

    #Remove whitespace from strings and column names
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    #Enforce unicode conversion
    df = df.map(lambda x: unicodedata.normalize("NFKD",x) if isinstance(x, str) else x)
    
    #Write to S3 if filename is provided
    if file_name:
        aws_tools.write_to_s3(df, S3_STAGE, 'auxiliary-data/reference-data/cpi-reference-tables', file_name)
        
def generate_project_type_use(mi, ad):
    '''
    This function generates a Use column in the project type reference data using the MI and AD columns
    
    Parameters:
    - mi: Boolean Column
    - ad: Boolean Column
    
    Returns:
    - use: String Column
    
    '''

    if ((mi == 1) & (ad == 1)):
        use = 'Multiple Objectives'
    elif mi == 1:
        use = 'Mitigation'
    elif ad == 1:
        use = 'Adaptation'
    else:
        use = np.nan

    return use

def extract_reference_sheets():
    """
    This function extracts multiple reference sheets from an Excel file stored in an Amazon S3 bucket.
    It then processes each sheet using the 'process_reference_data' function.

    Parameters:
    - None

    Returns:
    - None

    !!
    FLAG: 
    There's an odd excel macro issue that enforces pd.read_csv to process the max columns in the institution_cpi sheet after our Sharepoint migration. 
    We've manually set usecols to avoid timing out as a temporary fix, but if you add columns past Column Z (set with a ~8 column buffer) to institution_list_cpi, 
    please reset the usecols parameter for that sheet or you will lose the new columns. 
    !!

    """
    # Define the path to the file in the S3 bucket
    s3_file_path = 'auxiliary-data/reference-data/cpi-reference-tables'
    # Define the name of the file
    file_name = 'master_ref.xlsm'
    
    # For each sheet in the Excel file, read the data into a pandas DataFrame
    # and then process that data using the 'process_reference_data' function.
    # The arguments passed to 'process_reference_data' vary depending on the specific sheet being processed.

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='coeff'),
                           'ref_coef', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='double_counting'),
                           'ref_double_counting', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='fx'),
                           'ref_fx', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='gearing'),
                           'ref_gearing')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='gender'),
                           'ref_gender', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='geog_list_all'),
                           'ref_geog_list_all', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='geog_list_cpi'),
                           'ref_geog_list_cpi', 'SQL Field Name', 1,4)

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='institution_list_all'),
                           'ref_institution_list_all', 'SQL Field Name')

    ### FLAG: manually set use_cols as a temporary fix to the max_cols processing issue.
    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='institution_list_cpi', usecols='A:Z'),
                           'ref_institution_list_cpi','SQL Field Name', start_row=4)

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='instr'),
                           'ref_instr', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='multiplier'),
                           'ref_multiplier')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='recipient'),
                           'ref_recipient')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='project_type'),
                           'ref_project_type', 'SQL Field Name', project_type=True)
        
    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='ownership'),
                           'ref_ownership')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='sector'),
                           'ref_sector', 'SQL Field Name')

    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='soe'),
                           'ref_soe', 'SQL Field Name')
    
    process_reference_data(pd.read_excel(f's3://{S3_STAGE}/{s3_file_path}/{file_name}', sheet_name='data_source'),
                           'ref_data_source')

    return None

def update_ref_tables():
    """
    This function updates reference tables by reading a master reference table from Sharepoint,
    exporting it to an Amazon S3 bucket, and then extracting reference data from the table.

    Parameters:
    - None

    Returns:
    - None
    """

    # Output status update
    print('Reading Master Reference Table from Sharepoint...')

    # Define the path to the file in Sharepoint
    reference_metadata_sharepoint_path = 'Workstreams/Tracking/GLCF/GLCF MASTER/3. Reference Tables Excel/Reference Tables_v1_MASTER_2022.xlsm'
    # Define the site the file in Sharepoint is hosted in (since differ from path depending on structure)
    reference_metadata_sharepoint_site = 'PROGRAM'

    # Export the file from Sharepoint to an S3 bucket
    export_sharepoint_file_to_s3(reference_metadata_sharepoint_path, reference_metadata_sharepoint_site, 
                                 s3_bucket='cpi-uk-us-datascience-stage',
                              s3_path='auxiliary-data/reference-data/cpi-reference-tables', s3_file_name='master_ref.xlsm', overwrite=True)
    
    # Output status update
    print('Extracting reference data')

    # Extract reference data from the master reference table
    extract_reference_sheets()

    print("✓ Reference Tables Successfully Updated in S3")

    return None

def get_reference_tables(update=False):
    """
    This function retrieves various reference tables stored in an Amazon S3 bucket as pandas DataFrames.
    If the 'update' parameter is set to True, it will first update the reference tables
    by calling the 'update_ref_tables' function.

    Parameters:
    - update (bool): If True, the reference tables are updated before being retrieved.

    Returns:
    - tuple: A tuple of pandas DataFrames, each one representing a reference table.
    """
    
    # If the 'update' parameter is set to True, update the reference tables
    if update:
        update_ref_tables()

    # Define the path to the folder in the S3 bucket where the reference tables are stored
    cpi_reference_folder = 'auxiliary-data/reference-data/cpi-reference-tables'

    # Retrieve each reference table from the S3 bucket and read it into a pandas DataFrame.
    # Note that each file is read with 'utf-8' encoding.
    # Each DataFrame is stored in a separate variable.

    # Data Source Geography Names
    ref_geog_list_all = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_geog_list_all.csv', encoding='utf-8')
    
    # Coefficient table
    ref_coeff =  pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_coef.csv', encoding='utf-8')
    
    # Foreign exchange rates
    ref_fx =  pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_fx.csv', encoding='utf-8')
    
    # Gender table
    ref_gender =  pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_gender.csv', encoding='utf-8')
    
    # CPI Geography Names
    ref_geog_list_cpi =  pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_geog_list_cpi.csv', encoding='utf-8')
    
    # Data Source Institution names
    ref_institution_list_all = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_institution_list_all.csv', encoding='utf-8')
    
    # CPI Institution names
    ref_institution_list_cpi = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_institution_list_cpi.csv', encoding='utf-8')

    # Ownership table
    ref_ownership = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_ownership.csv', encoding='utf-8')
    
    # Project type table
    ref_project_type = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_project_type.csv')
    
    # Sector table
    ref_sector = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_sector.csv', encoding='utf-8')
    
    # Instrument table
    ref_instr = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_instr.csv', encoding='utf-8')
    
    # Recipient table
    ref_recipient = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_recipient.csv', encoding='utf-8')
    
    # Data source
    ref_data_source = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_data_source.csv', encoding='utf-8')

    ref_gearing = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_gearing.csv', encoding='utf-8')

    ref_multiplier = pd.read_csv(f's3://{S3_STAGE}/{cpi_reference_folder}/ref_multiplier.csv', encoding='utf-8')

    # Return all the DataFrames as a tuple
    return ref_geog_list_all, ref_coeff, ref_fx, ref_gender, ref_gearing, ref_geog_list_all, ref_geog_list_cpi, ref_institution_list_all, \
    ref_institution_list_cpi, ref_ownership, ref_project_type, ref_sector, ref_instr, ref_multiplier, \
    ref_recipient, ref_data_source

################################### Ref Table Helper Functions ###################################

def forward_fill_ref_ownership(ref_ownership: pd.DataFrame) -> pd.DataFrame:

    '''
    As not all ownership values are up to date - if a year is missing, fill with the closest available previous year

    Parameters:
    - ref_ownership table (pd.DataFrame): Ownership Reference Table 

    Returns:
    - ref_ownership table (pd.DataFrame): Ownership Reference Table with forward filled values
    '''
    max_year = date.today().year
    ref_ownership_grouped = ref_ownership.groupby(['institution_cpi', 'year', 'country']).agg({'proportion of ownership': 'sum'}).reset_index()
    #For each institution, if a year is missing, create a duplicate df of the closest available year and concatenate
    for institute in ref_ownership_grouped.institution_cpi.unique():
        df = ref_ownership_grouped[ref_ownership_grouped.institution_cpi == institute]
        # Fill forward to current year
        year = df.year.min()
        while (year < max_year):
            if ((year + 1) not in df.year.unique()):
                dff = ref_ownership_grouped[(ref_ownership_grouped.institution_cpi == institute) & (ref_ownership_grouped.year == year)].copy()
                dff['year'] = (year+1)
                ref_ownership_grouped = pd.concat([ref_ownership_grouped, dff])
            year = year+1
    return ref_ownership_grouped

def normalize_strings(value):
    
    """
    Normalises any string values. This ensures smoother joining between strings, especially for non-latin characters
    
    Parameters:
    - value: Value in a DataFrame columns
        
    Returns:
    - value: normalised value (if string)
    """
    if isinstance(value, str):
        #normalized_text = unicodedata.normalize('NFC', value).encode('ascii', 'ignore').decode('utf-8')
        
        normalized_text = unicodedata.normalize('NFKD', value)
        # Encode to ASCII, replacing non-ASCII characters with a space
        encoded_text = normalized_text.encode('ascii', 'replace').decode('ascii')
        # Replace any question marks (resulting from 'replace') with a space
        cleaned_text = encoded_text.replace('?', ' ')
        return normalized_text
    return value

################################### Read Ref tables ###################################

def read_reference_tables(sector_data_source_filters: list[str] = None, update: bool = False):
    """
    Fetches reference tables and filters reference sectors based on specific criteria.
    
    Parameters:
    - sector_data_source_filters list[string]: List of data sources to filter on in ref sectors
    - update (bool): If True, updates ref tables based on dropbox value and stores in S3. Otherwise will read direct from S3

    Returns:
    - dict: A dictionary containing filtered reference tables.
    """
    (
        ref_geog_list_all, 
        ref_coeff, 
        ref_fx, 
        ref_gender, 
        ref_gearing, 
        ref_geog_list_all,
        ref_geog_list_cpi, 
        ref_institution_list_all,
        ref_institution_list_cpi, 
        ref_ownership, 
        ref_project_type, 
        ref_sector, 
        ref_instr, 
        ref_multiplier,
        ref_recipient, 
        ref_data_source
    ) = get_reference_tables(update=update)
    
    # Normalise ref tables where it is necessary for joins (should really be done in tracking_processing_tools.get_reference_tables
    # function. Same with forward filling)
    ref_institution_list_cpi = ref_institution_list_cpi.map(normalize_strings)
    ref_institution_list_all = ref_institution_list_all.map(normalize_strings)
    ref_geog_list_all = ref_geog_list_all.map(normalize_strings)
    ref_geog_list_cpi = ref_geog_list_cpi.map(normalize_strings)
    
    # Forward fill ownership
    ref_ownership = forward_fill_ref_ownership(ref_ownership)

    # Filter on the reference data used 
    if sector_data_source_filters is not None:
        ref_sector = ref_sector[ref_sector['reference_data'].isin(sector_data_source_filters)]

    # Return reference tables as a dictionary for better structure and future use
    reference_tables = {
        "ref_geog_list_all": ref_geog_list_all,
        "ref_coeff": ref_coeff,
        "ref_fx": ref_fx,
        "ref_gender": ref_gender,
        "ref_gearing": ref_gearing,
        "ref_geog_list_cpi": ref_geog_list_cpi,
        "ref_institution_list_all": ref_institution_list_all,
        "ref_institution_list_cpi": ref_institution_list_cpi,
        "ref_ownership": ref_ownership,
        "ref_project_type": ref_project_type,
        "ref_sector": ref_sector,
        "ref_instr": ref_instr,
        "ref_multiplier": ref_multiplier,
        "ref_recipient": ref_recipient,
        "ref_data_source": ref_data_source
    }

    print("Reference tables successfully read")
    return reference_tables
