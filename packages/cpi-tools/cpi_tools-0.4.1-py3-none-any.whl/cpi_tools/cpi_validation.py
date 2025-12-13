from operator import ge
from webbrowser import get
import pandas as pd
import pandera as pa
from cpi_tools import aws_tools
import boto3
import s3fs

def get_valid_ref_values(ref_file, ref_column) -> list[str]:
    """ Retrieve valid GLCF column values from ref table"""
    ref_bucket = 'cpi-reference-data'
    ref_file_path = 'cpi/processed'
    ref_table = aws_tools.read_from_s3(ref_bucket, ref_file_path, ref_file)
    return list(ref_table[ref_column].unique())


def validate_glcf_data(df: pd.DataFrame, min_date: int = 2019, max_date:int = 2020) -> None:

    '''
    Input:

    df: pandas DataFrame containing GLCF data to be validated
    min_date (optional): integer representing the minimum year for valid data (default value is 2019)
    max_date (optional): integer representing the maximum year for valid data (default value is 2020)

    Returns: None

    This function validates a pandas DataFrame containing GLCF data, ensuring that it conforms to a specified schema. 
    The schema includes checks for valid values in various columns, such as sector, sub_sector, country, region, and institution type. 
    The function uses the validate method from the pandas_schema library to validate the DataFrame against the schema, 
    and raises an exception if the validation fails. If the validation is successful, the function prints a message 
    indicating that the DataFrame is GLCF compatible.
        
    '''

    # Get or define valid column values

    valid_data_source_values = get_valid_ref_values('ref_data_source', 'data_source')
    valid_sector_values = get_valid_ref_values('ref_project_type', 'sector')
    valid_sub_sector_values = get_valid_ref_values('ref_project_type', 'sub_sector')
    valid_solution_values = get_valid_ref_values('ref_project_type', 'solution')
    valid_country_values = get_valid_ref_values('ref_geog_list_cpi', 'country_cpi')
    valid_region_values = get_valid_ref_values('ref_geog_list_cpi', 'region_cpi')
    valid_oecd_values = get_valid_ref_values('ref_geog_list_cpi', 'oecd_membership')
    valid_r3_ipcc_values = get_valid_ref_values('ref_geog_list_cpi', 'r3_ipcc')
    valid_instrument_values = get_valid_ref_values('ref_instr', 'instrument_type')
    
    valid_institution_type_layer2_values =  ["Bilateral DFI", "Commercial FI", 'Corporation', 'Export Credit Agency (ECA)',
                            'Funds','Government', 'Household/Individual', 'Institutional Investors', 
                            'Multilateral Climate Funds','Multilateral DFI','National DFI', 'Public Fund',
                            'SOE', 'State-owned FI', 'Unknown']
    
    valid_institution_type_layer1_values = ['Public', 'Private', 'Unknown']
    valid_domestic_international_values = ['Domestic', 'International']
    valid_use_values = ['Mitigation', 'Adaptation', 'Multiple Objectives']
    valid_exclusion_values = ['Include', 'Exclude']


    # Define GLCF Schema
    schema = pa.DataFrameSchema({
        "id_glcf": pa.Column(str),
        "id_original": pa.Column(str, required=False),
        "data_source": pa.Column(str),
        "year": pa.Column(int, checks=pa.Check.in_range(min_date, max_date)),
        "project_name": pa.Column(str),
        "project_description": pa.Column(str, nullable=True),
        "country_origin_cpi": pa.Column(str, pa.Check.isin(valid_country_values)),
        "region_origin_cpi": pa.Column(str, pa.Check.isin(valid_region_values)),
        "oecd_origin_cpi": pa.Column(str, pa.Check.isin(valid_oecd_values)),
        "r3_ipcc_origin_cpi": pa.Column(str, pa.Check.isin(valid_r3_ipcc_values)),
        "country_destination_cpi": pa.Column(str, pa.Check.isin(valid_country_values)),
        "region_destination_cpi": pa.Column(str, pa.Check.isin(valid_region_values)),
        "oecd_destination_cpi": pa.Column(str, pa.Check.isin(valid_oecd_values)),
        "r3_ipcc_destination_cpi": pa.Column(str, pa.Check.isin(valid_r3_ipcc_values)),
        "institution_cpi": pa.Column(str),
        "institution_type_layer1": pa.Column(str, pa.Check.isin(valid_institution_type_layer1_values)),
        "institution_type_layer2": pa.Column(str, pa.Check.isin(valid_institution_type_layer2_values)),
        "recipient_type_layer1": pa.Column(str),
        "domestic_international": pa.Column(str, pa.Check.isin(valid_domestic_international_values)),
        "value_USDm": pa.Column(float, pa.Check.ge(0)), #Greater than or equal to 0
        "instrument_cpi": pa.Column(str, pa.Check.isin(valid_instrument_values)),
        "sector_original": pa.Column(str),
        "sector_key_cpi": pa.Column(str),
        "sector_cpi": pa.Column(str, checks=pa.Check.isin(valid_sector_values)),
        "sub_sector_cpi": pa.Column(str, pa.Check.isin(valid_sub_sector_values)),
        "solution_cpi": pa.Column(str, pa.Check.isin(valid_solution_values)),
        "use_cpi": pa.Column(str, pa.Check.isin(valid_use_values)),
        "gender_cpi": pa.Column(str),
        "exclude_include": pa.Column(str, pa.Check.isin(valid_exclusion_values))
    })

    # Attempt Validation
    try:
        schema.validate(df, lazy=True)
        print('Dataframe GLCF Compatible')
    except pa.errors.SchemaErrors as e:
        #Display Errors upon validation failure
        display(e.failure_cases)



    
    
    
    
    
    