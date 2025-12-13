import teradataml as tdml
from tdfs4ds import feature_store
from tdfs4ds.utils import execute_query_wrapper,execute_query


import uuid
import json

process_catalog_name    = 'FS_PROCESS_CATALOG'

def process_store_catalog_creation(if_exists='replace', comment='this table is a process catalog'):
    """
    This function creates a feature store catalog table in Teradata database.
    The catalog table stores information about features such as their names, associated tables, databases, validity periods, etc.

    Parameters:
    - schema: The schema name in which the catalog table will be created.
    - if_exists (optional): Specifies the behavior if the catalog table already exists. The default is 'replace', which means the existing table will be replaced.
    - table_name (optional): The name of the catalog table. The default is 'FS_FEATURE_CATALOG'.

    Returns:
    The name of the created or replaced catalog table.

    """

    # SQL query to create the catalog table
    query = f"""
    CREATE MULTISET TABLE {feature_store.schema}.{process_catalog_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (

                PROCESS_ID VARCHAR(36) NOT NULL,
                PROCESS_TYPE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                VIEW_NAME   VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC,
                ENTITY_ID JSON(32000),
                FEATURE_NAMES VARCHAR(1024) CHARACTER SET LATIN NOT CASESPECIFIC,
                FEATURE_VERSION VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC,
                DATA_DOMAIN VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                METADATA JSON(32000),
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (PROCESS_ID);
    """

    # SQL query to create a secondary index on the feature name
    query2 = f"CREATE INDEX (PROCESS_TYPE) ON {feature_store.schema}.{process_catalog_name};"

    # SQL query to comment the table
    query3 = f"COMMENT ON TABLE {feature_store.schema}.{process_catalog_name} IS '{comment}'"

    try:
        # Attempt to execute the create table query
        execute_query(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        if feature_store.display_logs: print(f'TABLE {feature_store.schema}.{process_catalog_name} has been created')
        execute_query(query3)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        if feature_store.display_logs: print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            execute_query(f'DROP TABLE  {feature_store.schema}.{process_catalog_name}')
            print(f'TABLE {feature_store.schema}.{process_catalog_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                execute_query(query)
                if feature_store.display_logs: print(f'TABLE {feature_store.schema}.{process_catalog_name} has been re-created')
                if tdml.display.print_sqlmr_query:
                    print(query)
                execute_query(query3)
            except Exception as e:
                print(str(e).split('\n')[0])

    try:
        # Attempt to create the secondary index
        execute_query(query2)
        if tdml.display.print_sqlmr_query:
            print(query)
        if feature_store.display_logs: print(f'SECONDARY INDEX ON TABLE {feature_store.schema}.{process_catalog_name} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])

    return process_catalog_name

@execute_query_wrapper
def register_process_view(view_name, entity_id, feature_names, metadata={}, **kwargs):
    """
    Registers a process view with the specified details in the feature store. The function
    handles both the creation of new views and the updating of existing views.

    Parameters:
    view_name (str or DataFrame): The name of the view or a DataFrame object representing the view.
    entity_id (str): The identifier of the entity associated with the view.
    feature_names (list): A list of feature names included in the view.
    metadata (dict, optional): Additional metadata related to the view. Defaults to an empty dictionary.

    Returns:
    str: A query string to insert or update the view details in the feature store.
    """

    # Handling the case where the view name is provided as a DataFrame
    if type(view_name) == tdml.dataframe.dataframe.DataFrame:
        try:
            view_name = view_name._table_name
        except:
            print('create your teradata dataframe using tdml.DataFrame(<view name>). Crystallize your view if needed')
            return []

    # Generating a unique process identifier
    process_id = str(uuid.uuid4())

    # Joining the feature names into a comma-separated string
    feature_names = ','.join(feature_names)

    # Setting the end period for the view
    if feature_store.end_period == 'UNTIL_CHANGED':
        end_period_ = '9999-01-01 00:00:00'
    else:
        end_period_ = feature_store.end_period

    if feature_store.date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({feature_store.date_in_the_past},{end_period_})'"

    # Handling cases based on whether the date is in the past or not
    if feature_store.date_in_the_past == None:

        # Checking if the view already exists in the feature store
        query_ = f"CURRENT VALIDTIME SEL * FROM {feature_store.schema}.{process_catalog_name} WHERE view_name = '{view_name}'"
        df = tdml.DataFrame.from_query(query_)

        # Constructing the query for new views
        if df.shape[0] == 0:
            query_insert = f"""
                CURRENT VALIDTIME INSERT INTO {feature_store.schema}.{process_catalog_name} (PROCESS_ID, PROCESS_TYPE, VIEW_NAME, ENTITY_ID, FEATURE_NAMES, FEATURE_VERSION, METADATA, DATA_DOMAIN)
                    VALUES ('{process_id}',
                    'denormalized view',
                    '{view_name}',
                    '{json.dumps(entity_id).replace("'", '"')}',
                    '{feature_names}',
                    '1',
                    '{json.dumps(metadata).replace("'", '"')}',
                    '{feature_store.data_domain}'
                    )
                """
        # Constructing the query for updating existing views
        else:
            query_insert = f"""
                            CURRENT VALIDTIME UPDATE {feature_store.schema}.{process_catalog_name} 
                            SET 
                                PROCESS_TYPE = 'denormalized view'
                            ,   ENTITY_ID = '{json.dumps(entity_id).replace("'", '"')}'
                            ,   FEATURE_NAMES = '{feature_names}'
                            ,   FEATURE_VERSION = CAST((CAST(FEATURE_VERSION AS INTEGER) +1) AS VARCHAR(4))
                            ,   METADATA = '{json.dumps(metadata).replace("'", '"')}'
                            ,   DATA_DOMAIN = '{feature_store.data_domain}'
                            WHERE VIEW_NAME = '{view_name}'
                            """
            process_id = tdml.DataFrame.from_query(f"CURRENT VALIDTIME SEL PROCESS_ID FROM {feature_store.schema}.{process_catalog_name} WHERE VIEW_NAME = '{view_name}'").to_pandas().PROCESS_ID.values[0]

    else:
        # Handling the case when the date is in the past
        df = tdml.DataFrame.from_query(f"VALIDTIME AS OF TIMESTAMP '{feature_store.date_in_the_past}' SEL * FROM {feature_store.schema}.{process_catalog_name} WHERE view_name = '{view_name}'")



        # Constructing the query for new views with a past date
        if df.shape[0] == 0:
            query_insert = f"""
            INSERT INTO {feature_store.schema}.{process_catalog_name} (PROCESS_ID, PROCESS_TYPE, VIEW_NAME,  ENTITY_ID, FEATURE_NAMES, FEATURE_VERSION, METADATA, DATA_DOMAIN,ValidStart, ValidEnd)
                VALUES ('{process_id}',
                'denormalized view',
                '{view_name}',
                '{json.dumps(entity_id).replace("'", '"')}'
                ,'{feature_names}',
                '1',
                '{json.dumps(metadata).replace("'", '"')}',
                '{feature_store.data_domain}',
                TIMESTAMP '{feature_store.date_in_the_past}',
                TIMESTAMP '{end_period_}'
                )
            """
        # Constructing the query for updating existing views with a past date
        else:
            query_insert = f"""{validtime_statement}
                            UPDATE {feature_store.schema}.{process_catalog_name} 
                            SET 
                                PROCESS_TYPE = 'denormalized view'
                            ,   ENTITY_ID = '{json.dumps(entity_id).replace("'", '"')}'
                            ,   FEATURE_NAMES = '{feature_names}'
                            ,   FEATURE_VERSION = CAST((CAST(FEATURE_VERSION AS INTEGER) +1) AS VARCHAR(4))
                            ,   METADATA = '{json.dumps(metadata).replace("'", '"')}'
                            ,   DATA_DOMAIN = '{feature_store.data_domain}'
                            WHERE VIEW_NAME = '{view_name}'
                            """
            process_id = tdml.DataFrame.from_query(
                f"VALIDTIME AS OF TIMESTAMP '{feature_store.date_in_the_past}' SEL PROCESS_ID FROM {feature_store.schema}.{process_catalog_name} WHERE VIEW_NAME = '{view_name}'").to_pandas().PROCESS_ID.values[
                0]
    # Logging the process registration
    print(f'register process with id : {process_id}')
    print(f'to run the process again just type : run(process_id={process_id})')
    print(f'to update your dataset : dataset = run(process_id={process_id},return_dataset=True)')

    if kwargs.get('with_process_id'):
        return query_insert, process_id
    else:
        return query_insert

@execute_query_wrapper
def register_process_tdstone(model, metadata={}):
    """
    Registers a 'tdstone2 view' process in the feature store with specified model details and metadata.
    It handles both the scenarios where the feature store date is current or in the past.

    Parameters:
    model (Model Object): The model object containing necessary details for the registration.
    metadata (dict, optional): Additional metadata related to the process. Defaults to an empty dictionary.

    Returns:
    str: A query string to insert the process details into the feature store.
    """

    # Generating a unique process identifier
    process_id = str(uuid.uuid4())

    # Handling the current date scenario
    if feature_store.date_in_the_past is None:
        # Constructing the query for insertion with current valid time
        query_insert = f"""
            CURRENT VALIDTIME INSERT INTO {feature_store.schema}.{process_catalog_name} (PROCESS_ID, PROCESS_TYPE, ENTITY_ID, FEATURE_VERSION, METADATA, DATA_DOMAIN)
                VALUES ('{process_id}',
                'tdstone2 view',
                '{model.mapper_scoring.id_row}',
                '{model.id}',
                '{json.dumps(metadata).replace("'", '"')}',
                '{feature_store.data_domain}'
                )
            """
    else:
        # Determining the end period based on feature store configuration
        end_period_ = '9999-01-01 00:00:00' if feature_store.end_period == 'UNTIL_CHANGED' else feature_store.end_period

        # Constructing the query for insertion with a specified past date
        query_insert = f"""
        INSERT INTO {feature_store.schema}.{process_catalog_name} (PROCESS_ID, PROCESS_TYPE, ENTITY_ID, FEATURE_VERSION, METADATA, DATA_DOMAIN, ValidStart, ValidEnd)
            VALUES ('{process_id}',
            'tdstone2 view',
            '{model.mapper_scoring.id_row}',
            '{model.id}',
            '{json.dumps(metadata).replace("'", '"')}',
            '{feature_store.data_domain}',
            TIMESTAMP '{feature_store.date_in_the_past}',
            TIMESTAMP '{end_period_}')
        """

    # Logging the process registration
    print(f'register process with id : {process_id}')

    return query_insert


def list_processes():
    """
    Retrieves and returns a list of all processes from the feature store.
    The function fetches details like process ID, type, view name, entity ID,
    feature names, feature version, and metadata.

    Returns:
    DataFrame: A DataFrame containing the details of all processes in the feature store.
    """

    # Constructing the SQL query to fetch process details
    query = f"""
    CURRENT VALIDTIME
    SELECT 
        PROCESS_ID ,
        PROCESS_TYPE ,
        VIEW_NAME ,
        ENTITY_ID ,
        FEATURE_NAMES ,
        FEATURE_VERSION AS PROCESS_VERSION,
        DATA_DOMAIN,
        METADATA
    FROM {feature_store.schema}.{process_catalog_name}
    """

    # Optionally printing the query if configured to do so
    if tdml.display.print_sqlmr_query:
        print(query)

    # Executing the query and returning the result as a DataFrame
    try:
        return tdml.DataFrame.from_query(query)
    except Exception as e:
        print(str(e))
        print(query)


def run(process_id, return_dataset = False):
    """
    Executes a specific process from the feature store identified by the process ID.
    The function handles different process types and performs appropriate actions.

    Args:
    process_id (str): The unique identifier of the process to run.
    as_date_of (str, optional): Date parameter for the process execution. Defaults to None.

    Returns:
    None: The function returns None, but performs operations based on process type.
    """

    if feature_store.date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{feature_store.date_in_the_past}'"

    # Construct SQL query to retrieve process details by process ID
    query = f"""
    {validtime_statement}
    SEL * FROM {feature_store.schema}.{process_catalog_name}
    WHERE PROCESS_ID = '{process_id}'
    """

    # Executing the query and converting the result to Pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Check if exactly one record is returned, else print an error
    if df.shape[0] != 1:
        print('error - there is ', df.shape[0], f' records. Check table {feature_store.schema}.{process_catalog_name}')
        return

    # Fetching the process type from the query result
    process_type = df['PROCESS_TYPE'].values[0]

    # Fetching the data domain from the query result
    feature_store.data_domain = df['DATA_DOMAIN'].values[0]

    # Handling 'denormalized view' process type
    if process_type == 'denormalized view':
        # Extracting necessary details for this process type
        view_name = df['VIEW_NAME'].values[0]
        entity_id = eval(df['ENTITY_ID'].values[0])
        feature_names = df['FEATURE_NAMES'].values[0].split(',')

        # Fetching data and uploading features to the feature store
        df_data = tdml.DataFrame(tdml.in_schema(view_name.split('.')[0], view_name.split('.')[1]))

        dataset = feature_store._upload_features(
            df_data,
            entity_id,
            feature_names,
            feature_versions = process_id)

    # Handling 'tdstone2 view' process type
    elif process_type == 'tdstone2 view':
        print('not implemented yet')

    if return_dataset:
        return dataset
    else:
        return

@execute_query_wrapper
def remove_process(process_id):
    """
    Deletes a process from the feature store's process catalog based on the given process ID.

    Args:
    process_id (str): The unique identifier of the process to be removed.

    Returns:
    str: SQL query string that deletes the specified process from the process catalog.
    """

    # Constructing SQL query to delete a process by its ID
    query = f"DELETE FROM {feature_store.schema}.{process_catalog_name} WHERE process_id = '{process_id}'"

    # Returning the SQL query string
    return query