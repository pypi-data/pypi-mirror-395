import pandas as pd
import teradataml as tdml
import os

outstanding_amounts_dataset_filename = 'curves.csv'
package_dir, _ = os.path.split(__file__)

def outstanding_amounts_dataset():
    """
    Load and return a dataset of outstanding amounts from a CSV file.

    This function reads a CSV file named by the variable `outstanding_amounts_dataset_filename` located in the
    "data" subdirectory of the directory specified by `package_dir`. It parses the 'OUTSTANDING_DATE' column in the
    dataset as dates.

    Returns:
        pandas.DataFrame: A DataFrame containing the dataset of outstanding amounts. The 'OUTSTANDING_DATE' column
        is parsed as datetime objects.

    Note:
        - This function requires the `pandas` library to be imported as `pd`.
        - The variables `package_dir` and `outstanding_amounts_dataset_filename` must be defined in the scope where
          this function is called.
        - The CSV file must have a column named 'OUTSTANDING_DATE' for the date parsing to work correctly.
    """
    return pd.read_csv(os.path.join(package_dir, "data", outstanding_amounts_dataset_filename),parse_dates =  ['OUTSTANDING_DATE'])

def upload_outstanding_amounts_dataset(table_name='outstanding_amount_dataset', **kwargs):
    """
    Uploads the outstanding amounts dataset to a database table and returns the table as a DataFrame.

    This function uploads the dataset returned by `outstanding_amounts_dataset()` to a specified table in a database.
    If a 'schema_name' is provided via keyword arguments, it uploads the data to that schema; otherwise, it uses the
    default schema. It prints to the console where the dataset is uploaded. After uploading, it retrieves the newly
    uploaded table into a DataFrame and returns it.

    Parameters:
        table_name (str, optional): The name of the database table where the dataset will be uploaded. Defaults to
                                    'outstanding_amount_dataset'.
        **kwargs: Arbitrary keyword arguments. Can be used to specify 'schema_name' and other parameters that
                  `tdml.copy_to_sql()` might accept, such as connection details.

    Returns:
        tdml.DataFrame: A DataFrame representing the database table into which the dataset was uploaded. This DataFrame
                        is created either in the specified schema (if 'schema_name' is provided) or the default schema.

    Note:
        - This function requires the `tdml` library to be available and correctly configured to interact with the
          target database.
        - The `outstanding_amounts_dataset()` function is called within this function to obtain the dataset to upload.
        - If 'schema_name' is provided in `kwargs`, it is used for both uploading the dataset and retrieving it into
          a DataFrame. If not provided, a notice is printed, and the default schema is used.
    """
    if 'schema_name' in kwargs.keys():
        print('dataset uploaded in '+ kwargs['schema_name'] + '.' + table_name)
    else:
        print('schema_name not specified. default used')
        print('dataset uploaded in '+table_name)

    tdml.copy_to_sql(df=outstanding_amounts_dataset(),
                     table_name=table_name,
                     **kwargs)

    if 'schema_name' in kwargs.keys():
        df = tdml.DataFrame(tdml.in_schema(kwargs['schema_name'], table_name))
    else:
        df = tdml.DataFrame(table_name)

    return df