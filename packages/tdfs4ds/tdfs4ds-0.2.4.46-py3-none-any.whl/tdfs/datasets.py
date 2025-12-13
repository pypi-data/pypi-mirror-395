import pandas as pd
import teradataml as tdml
import os

outstanding_amounts_dataset_filename = 'curves.csv'
package_dir, _ = os.path.split(__file__)

def outstanding_amounts_dataset():
    return pd.read_csv(os.path.join(package_dir, "data", outstanding_amounts_dataset_filename),parse_dates =  ['OUTSTANDING_DATE'])

def upload_outstanding_amounts_dataset(table_name='outstanding_amount_dataset', **kwargs):
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