import re

import tdfs4ds
import teradataml as tdml
from tdfs4ds import logger
import numpy as np

def get_column_types(df, columns):
    """
    Retrieve the column types for specified columns from a TeradataML DataFrame.

    This function retrieves the data types of specified columns in a TeradataML DataFrame. It is tailored to work with
    DataFrames that have specific attributes like `_td_column_names_and_types` and `_td_column_names_and_sqlalchemy_types`,
    which are not standard in typical pandas DataFrames.

    Parameters:
    - df (DataFrame): The TeradataML DataFrame from which to get the column types.
    - columns (list or str): A list of column names or a single column name whose types are to be retrieved.

    Returns:
    dict: A dictionary where keys are column names and values are their types, including character set for VARCHAR columns.

    Notes:
    - This function is designed to work with TeradataML DataFrames, which may have extended column type information.
    - For VARCHAR columns, it retrieves the detailed type information, including the character set.

    Dependencies:
    - TeradataML DataFrame containing attributes '_td_column_names_and_types' and '_td_column_names_and_sqlalchemy_types'.
    """

    # Convert columns to a list if it's not already a list
    if type(columns) != list:
        columns = [columns]

    # Build a dictionary of column types for the specified columns
    col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}
    types_ = {x.split()[0]: ''.join(x.split()[1::]) for x in str(df.tdtypes).split('\n')}
    col_type_ = {k: v for k,v in types_.items() if k in columns}

    # Iterate over the column types
    for k, v in col_type.items():
        # Special handling for columns of type VARCHAR
        if 'VARCHAR' in v.upper():
            # Retrieve detailed type information, including character set
            temp = df._td_column_names_and_sqlalchemy_types[k.lower()]
            col_type[k] = f"{temp.compile()} CHARACTER SET {temp.charset}"

    return col_type



def get_column_types_simple(df, columns = None):
    """
    Retrieve simplified column types for specified columns from a DataFrame.

    This function simplifies the data types of the specified columns in a DataFrame, translating database-specific data types
    (such as INTEGER, BYTEINT, etc.) into more generalized Python data types (e.g., int, float). It assumes the DataFrame has
    a specific attribute '_td_column_names_and_types' that stores column names and their types.

    Parameters:
    - df (DataFrame): The DataFrame from which to get the column types.
    - columns (list or str): A list of column names or a single column name whose types are to be retrieved.

    Returns:
    dict: A dictionary where keys are column names and values are simplified Python data types.

    Notes:
    - This function is designed to work with DataFrames that have a specific attribute '_td_column_names_and_types'.
    - It uses a mapping from specific database column types to simplified Python data types for simplification.

    Dependencies:
    - DataFrame containing the '_td_column_names_and_types' attribute.
    """

    # Ensure that the columns parameter is in list format
    if columns is None:
        columns = df.columns

    if type(columns) != list:
        columns = [columns]

    # Extract the column types for the specified columns
    #col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}
    types_ = {x.split()[0]: ''.join(x.split()[1::]) for x in str(df.tdtypes).split('\n')}
    col_type = {k: v for k,v in types_.items() if k in columns}

    # Define a mapping from specific database column types to simplified Python data types
    mapping = {'INTEGER': 'int',
               'BYTEINT': 'int',
               'BIGINT': 'int',
               'FLOAT': 'float'
               }

    # Update the column types in the dictionary using the mapping
    for k, v in col_type.items():
        if v in mapping:
            col_type[k] = mapping[v]

    return col_type

def seconds_to_dhms(seconds):
    """
    Converts a duration in seconds to a formatted string representing days, hours, minutes, and seconds with three decimal places.

    Args:
        seconds (float): The duration in seconds.

    Returns:
        str: A formatted string representing the duration in days, hours, minutes, and seconds with three decimal places.
    """
    minutes = int(seconds // 60) % 60
    hours = int(seconds // (60 * 60)) % 24
    days = int(seconds // (60 * 60 * 24))
    seconds = seconds % 60

    # Construct a list of time parts to include in the formatted string
    time_parts = []
    if days > 0:
        time_parts.append(f"{days}d")
    if hours > 0:
        time_parts.append(f"{hours}h")
    if minutes > 0:
        time_parts.append(f"{minutes}m")
    time_parts.append(f"{seconds:.3f}s")

    # Join the time parts into a single string
    formatted_time = " ".join(time_parts)
    return formatted_time

def extract_partition_content(partitioning):
    """
    Extracts the content within the parentheses after 'PARTITION BY' in the given partitioning string.

    Parameters:
        partitioning (str): The input string containing 'PARTITION BY'.

    Returns:
        str: The content within the parentheses after 'PARTITION BY', or None if no match is found.
    """
    pattern = r'PARTITION\s+BY\s*\((.*)\)'  # Matches content within outer parentheses after PARTITION BY
    match = re.search(pattern, partitioning, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return None

def generate_partitioning_clause(partitioning):
    """
    Generates a partitioning clause by ensuring the presence of 'FEATURE_ID' partitioning.

    Parameters:
        partitioning (str or list): The input partitioning string or list of partitioning clauses.

    Returns:
        str: A partitioning clause string with 'FEATURE_ID' partitioning included.
    """

    # Check if the input is a string
    if isinstance(partitioning, str):
        # Check if the string contains 'partition by'
        if 'partition by' in partitioning.lower():
            # Check if 'feature_id' is already in the partitioning clause
            if 'feature_id' in partitioning.lower():
                return partitioning
            else:
                # Extract existing partition content and add 'FEATURE_ID' partitioning
                substr = extract_partition_content(partitioning.upper())
                if len(substr) > 0:
                    return f"""PARTITION BY (
    RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH}),
    {substr}
)"""
                else:
                    return f"""PARTITION BY (
    RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH})
)"""
        else:
            partitioning = f"""PARTITION BY (
{partitioning}
)"""
            return generate_partitioning_clause(partitioning)
    # Check if the input is a list
    elif isinstance(partitioning, list):
        # Check if 'feature_id' is not in any of the partitioning clauses
        if 'feature_id' not in ','.join(partitioning).lower():
            partitioning = [f'RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH})'] + partitioning
            partitioning = ',\n'.join(partitioning)
        return f"""PARTITION BY (
{partitioning}
)"""

def get_feature_types_sql_format(tddf, columns = None):
    """
    Retrieve the SQL data types of specified columns from a Teradata dataframe.

    This function executes a query to fetch the SQL data types of the given columns
    and returns them in a dictionary format.

    Parameters:
    tddf (tdml.DataFrame): A Teradata dataframe.
    columns (list): List of column names to retrieve their data types.

    Returns:
    dict: A dictionary where keys are column names and values are their corresponding SQL data types.

    Example:
    >>> tdml.load_example_data("GLM", ["admissions_train"])
    >>> df = tdml.DataFrame("admissions_train")
    >>> get_feature_types_sql_format(df, columns=df.columns)
    {'id': 'INTEGER',
     'masters': 'VARCHAR(5)',
     'gpa': 'FLOAT',
     'stats': 'VARCHAR(30)',
     'programming': 'VARCHAR(30)',
     'admitted': 'INTEGER'}

    >>> df.to_sql(table_name='test_admission_train', types={'stats': tdml.VARCHAR(length=40, charset='UNICODE')}, if_exists='replace')
    >>> df = tdml.DataFrame("test_admission_train")
    >>> get_feature_types_sql_format(df, columns=df.columns)
    {'id': 'INTEGER',
     'masters': 'VARCHAR(5)',
     'gpa': 'FLOAT',
     'stats': 'VARCHAR(40) CHARACTER SET UNICODE',
     'programming': 'VARCHAR(30)',
     'admitted': 'INTEGER'}
    """

    if columns is None:
        columns = tddf.columns
        
    # Validate inputs
    if not isinstance(tddf, tdml.DataFrame):
        raise TypeError("tddf must be an instance of tdml.DataFrame")
    if not isinstance(columns, list) or not all(isinstance(col, str) for col in columns):
        raise TypeError("columns must be a list of strings")

    # Assign a table name to the Teradata dataframe internally
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)
    view_name = tddf._table_name  # Get the assigned table name

    sqlalchemy_types = tddf._td_column_names_and_sqlalchemy_types
    sqlalchemy_types = {c:sqlalchemy_types[c.lower()] for c in columns}
    args = {k:tddf[k].cast(v) for k,v in sqlalchemy_types.items()}
    args['drop_columns'] = True
    sql_types = tddf.assign(**args).show_query()
    if tdfs4ds.DEBUG_MODE:
        print('sql_types', sql_types)
        print('-------')
        print('sql_types.replace', sql_types.replace(',',',\n'))
    res =  [')'.join(x.split(')')[0:-1]).replace('"','') for x in sql_types.split('select ')[1].split('from ')[0].split('CAST(') if len(x)>0]
    return  {x.split(' AS ')[0] : x.split(' AS ')[1] for x in res}

def update_varchar_length(feature_types: dict, new_varchar_length: int) -> dict:
    """
    Updates the length of all VARCHAR fields in the feature_types dictionary based on an increment.
    The new length is calculated as ceil(previous_length / new_varchar_length) * new_varchar_length,
    ensuring that when new_varchar_length is equal to the current length, no change occurs.
    
    Args:
        feature_types (dict): A dictionary where keys are feature names and values are dictionaries with 'type' and 'id'.
        new_varchar_length (int): The increment value for adjusting VARCHAR lengths.
    
    Returns:
        dict: A dictionary with updated VARCHAR lengths.
    
    Issues a warning if the new length is smaller than the original length.
    """
    updated_feature_types = {}
    varchar_pattern = re.compile(r'VARCHAR\((\d+)\)', re.IGNORECASE)
    
    for key, value in feature_types.items():
        type_value = value['type']
        match = varchar_pattern.search(type_value)
        if match:
            original_length = int(match.group(1))
            modified_length = int(np.ceil(original_length / new_varchar_length) * new_varchar_length)
            
            if modified_length < original_length:
                logger.warning(f"Reducing VARCHAR length for {key} from {original_length} to {modified_length}")
            
            # Replace only the VARCHAR length
            updated_value = varchar_pattern.sub(f'VARCHAR({modified_length})', type_value)
            updated_feature_types[key] = {'type': updated_value, 'id': value['id']}
        else:
            updated_feature_types[key] = value
    
    return updated_feature_types