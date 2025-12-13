import teradataml as tdml
import pandas as pd
from tdfs4ds.utils import execute_query, display_table, get_column_types, get_column_types_simple
from teradataml.context.context import _get_database_username
import inspect
import warnings
from tdfs4ds.process_store import register_process_view, run

warnings.filterwarnings("ignore")

data_domain             = None
schema                  = None
feature_catalog_name    = 'FS_FEATURE_CATALOG'
end_period              = 'UNTIL_CHANGED' #'9999-01-01 00:00:00'
date_in_the_past        = None
feature_version_default = 'dev.0.0'
display_logs            = True


def feature_store_catalog_creation(if_exists = 'replace',comment='this table is a feature catalog'):
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
    CREATE MULTISET TABLE {schema}.{feature_catalog_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                
                FEATURE_ID BIGINT,
                FEATURE_NAME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_TABLE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_DATABASE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_VIEW VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ENTITY_NAME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                DATA_DOMAIN VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (FEATURE_ID);
    """
    
    # SQL query to create a secondary index on the feature name
    query2 = f"CREATE INDEX (FEATURE_NAME) ON {schema}.{feature_catalog_name};"
    
    # SQL query to comment the table
    query3 = f"COMMENT ON TABLE {schema}.{feature_catalog_name} IS '{comment}'"
    
    try:
        # Attempt to execute the create table query
        execute_query(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        if display_logs: print(f'TABLE {schema}.{feature_catalog_name} has been created')
        execute_query(query3)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        if display_logs: print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            execute_query(f'DROP TABLE  {schema}.{feature_catalog_name}')
            print(f'TABLE {schema}.{feature_catalog_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                execute_query(query)
                if display_logs: print(f'TABLE {schema}.{feature_catalog_name} has been re-created')
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
        if display_logs: print(f'SECONDARY INDEX ON TABLE {schema}.{feature_catalog_name} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])
    
    return feature_catalog_name

def list_features():
    query = f"CURRENT VALIDTIME SEL * FROM {schema}.{feature_catalog_name}"

    return tdml.DataFrame.from_query(query)

def get_feature_store_table_name(entity_id, feature_type):
    """

    This function generates the table and view names for a feature store table based on the provided entity ID and feature type.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to construct the table and view names.
    - feature_type: The type of the feature.

    Returns:
    A tuple containing the generated table name and view name.

    """  

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Construct the table name by concatenating the elements 'FS', 'T', the keys of entity_id, and feature_type
    table_name = ['FS','T']+[data_domain]+list_entity_id+[feature_type]
    table_name = '_'.join(table_name)
    
    # Construct the view name by concatenating the elements 'FS', 'V', the keys of entity_id, and feature_type
    view_name  = ['FS','V']+[data_domain]+list_entity_id+[feature_type]
    view_name  = '_'.join(view_name)
    
    return table_name, view_name

def feature_store_table_creation(entity_id, feature_type, if_exists = 'fail'):

    """
    This function creates a feature store table and a corresponding view in a Teradata database schema based on the provided entity ID, feature type, and feature catalog.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to construct the table and view names.
    - feature_type: The type of the feature.
    - schema: The schema name in which the table and view will be created.
    - if_exists (optional): Specifies the behavior if the table already exists. The default is 'replace', which means the existing table will be replaced.
    - feature_catalog_name (optional): The name of the feature catalog table. The default is 'FS_FEATURE_CATALOG'.

    Returns:
    The name of the created or replaced feature store table.

    """
    
    table_name, view_name = get_feature_store_table_name(entity_id, feature_type)
    if tdml.db_list_tables(schema_name=schema, object_name=table_name+'%').shape[0] > 0:
        print(f'table {table_name} in the {schema} database already exists. No need to create it.')
        return
    else:
        print(f'table {table_name} in the {schema} database does not exists. Need to create it.')

    query_feature_value = {
        'FLOAT'   : 'FEATURE_VALUE FLOAT',
        'BIGINT'  : 'FEATURE_VALUE BIGINT',
        'VARCHAR' : 'FEATURE_VALUE VARCHAR(2048) CHARACTER SET LATIN'
    }

    # Construct the column definitions for the table based on the entity ID
    ENTITY_ID    = ', \n'.join([k+' '+v for k,v in entity_id.items()])
    ENTITY_ID_   = ', \n'.join(['B.'+k for k,v in entity_id.items()])
    ENTITY_ID__  = ','.join([k for k,v in entity_id.items()])
    
    # SQL query to create the feature store table
    query = f"""
    CREATE MULTISET TABLE {schema}.{table_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                
                {ENTITY_ID},
                FEATURE_ID BIGINT,
                {query_feature_value[feature_type]},
                FEATURE_VERSION VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX ({ENTITY_ID__},FEATURE_ID,FEATURE_VERSION);
    """
    
    # SQL query to create a secondary index on the feature ID
    query2 = f"CREATE INDEX (FEATURE_ID) ON {schema}.{table_name};"

    # SQL query to create the view
    query_view = f"""
    REPLACE VIEW {schema}.{view_name} AS
    CURRENT VALIDTIME
    SELECT
        A.FEATURE_NAME,
        {ENTITY_ID_},
        B.FEATURE_VALUE,
        B.FEATURE_VERSION
    FROM {schema}.{feature_catalog_name} A
    , {schema}.{table_name} B
    WHERE A.FEATURE_ID = B.FEATURE_ID
    """

    try:
        # Attempt to execute the create table query
        execute_query(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        if display_logs: print(f'TABLE {schema}.{table_name} has been created')
        execute_query(query2)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            execute_query(f'DROP TABLE  {schema}.{table_name}')
            if display_logs: print(f'TABLE {schema}.{table_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                execute_query(query)
                if display_logs: print(f'TABLE {schema}.{table_name} has been re-created')
                if tdml.display.print_sqlmr_query:
                    print(query)
            except Exception as e:
                print(str(e).split('\n')[0])
    
    try:
        # Attempt to create the view
        execute_query(query_view)
        if tdml.display.print_sqlmr_query:
            print(query)
        if display_logs: print(f'VIEW {schema}.{view_name} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])
    
    return table_name

def register_features(entity_id, feature_names_types):
    """

    This function registers features in the feature catalog table of a Teradata database. It creates or updates entries in the catalog based on the provided entity ID, feature names and types, and schema.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to identify the entity.
    - feature_names_types: A dictionary containing feature names and their corresponding types.
    - schema: The schema name in which the feature catalog table resides.
    - feature_catalog_name (optional): The name of the feature catalog table. The default is 'FS_FEATURE_CATALOG'.

    Returns:
    A DataFrame containing the registered features and their metadata.

    """

    if date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({date_in_the_past},{end_period})'"


    if len(list(feature_names_types.keys())) == 0:
        if display_logs: print('no new feature to register')
        return

    # Create a comma-separated string of entity IDs
    ENTITY_ID__  = ','.join([k for k,v in entity_id.items()])
    
    # Create a DataFrame from the feature_names_types dictionary
    if len(feature_names_types.keys())>1:
        df = pd.DataFrame(feature_names_types).transpose().reset_index()
        df.columns = ['FEATURE_NAME','TYPE','FEATURE_ID']
    else:
        df = pd.DataFrame(columns=['FEATURE_NAME','TYPE','FEATURE_ID'])
        k = list(feature_names_types.keys())[0]
        df['FEATURE_NAME'] = [k]
        df['TYPE'] = [feature_names_types[k]['type']]
        df['FEATURE_ID'] = [feature_names_types[k]['id']]
        
    # Generate the feature table and view names based on the entity ID and feature type
    df['FEATURE_TABLE'] = df.apply(lambda row:get_feature_store_table_name(entity_id, row.iloc[1])[0], axis=1)
    df['FEATURE_VIEW']  = df.apply(lambda row:get_feature_store_table_name(entity_id, row.iloc[1])[1], axis=1)
    
    # Add additional columns to the DataFrame
    df['ENTITY_NAME']     = ENTITY_ID__
    df['FEATURE_DATABASE'] = schema
    df['DATA_DOMAIN'] = data_domain
    
    # Copy the DataFrame to a temporary table in Teradata
    tdml.copy_to_sql(df,table_name = 'temp', schema_name = schema, if_exists = 'replace', primary_index = 'FEATURE_ID', types={'FEATURE_ID':tdml.BIGINT})
    
    # SQL query to update existing entries in the feature catalog
    query_update = f"""
    {validtime_statement} 
    UPDATE {schema}.{feature_catalog_name}
    FROM (
        CURRENT VALIDTIME
        SELECT
            NEW_FEATURES.FEATURE_ID
        ,   NEW_FEATURES.FEATURE_NAME
        ,   NEW_FEATURES.FEATURE_TABLE
        ,   NEW_FEATURES.FEATURE_DATABASE
        ,   NEW_FEATURES.FEATURE_VIEW
        ,   NEW_FEATURES.ENTITY_NAME
        ,   NEW_FEATURES.DATA_DOMAIN
        FROM {schema}.temp NEW_FEATURES
        LEFT JOIN {schema}.{feature_catalog_name} EXISTING_FEATURES
        ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
        AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
        WHERE EXISTING_FEATURES.FEATURE_NAME IS NOT NULL
    ) UPDATED_FEATURES
    SET
        FEATURE_NAME     = UPDATED_FEATURES.FEATURE_NAME,
        FEATURE_TABLE    = UPDATED_FEATURES.FEATURE_TABLE,
        FEATURE_DATABASE = UPDATED_FEATURES.FEATURE_DATABASE,
        FEATURE_VIEW     = UPDATED_FEATURES.FEATURE_VIEW,
        ENTITY_NAME      = UPDATED_FEATURES.ENTITY_NAME
    WHERE     {feature_catalog_name}.FEATURE_ID = UPDATED_FEATURES.FEATURE_ID
    AND {feature_catalog_name}.DATA_DOMAIN = UPDATED_FEATURES.DATA_DOMAIN;
    """
    
    # SQL query to insert new entries into the feature catalog
    if validtime_statement == 'CURRENT VALIDTIME':
        query_insert = f"""
        {validtime_statement} 
        INSERT INTO {schema}.{feature_catalog_name} (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE, FEATURE_VIEW, ENTITY_NAME,DATA_DOMAIN)
            SELECT
                NEW_FEATURES.FEATURE_ID
            ,   NEW_FEATURES.FEATURE_NAME
            ,   NEW_FEATURES.FEATURE_TABLE
            ,   NEW_FEATURES.FEATURE_DATABASE
            ,   NEW_FEATURES.FEATURE_VIEW
            ,   NEW_FEATURES.ENTITY_NAME
            ,   NEW_FEATURES.DATA_DOMAIN
            FROM {schema}.temp NEW_FEATURES
            LEFT JOIN {schema}.{feature_catalog_name} EXISTING_FEATURES
            ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
            WHERE EXISTING_FEATURES.FEATURE_NAME IS NULL;
        """
    elif date_in_the_past is not None:
        if end_period == 'UNTIL_CHANGED':
            end_period_ = '9999-01-01 00:00:00'
        else:
            end_period_ = end_period
        query_insert = f"""
        INSERT INTO {schema}.{feature_catalog_name} (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE, FEATURE_VIEW, ENTITY_NAME,DATA_DOMAIN,ValidStart,ValidEnd)
            SELECT
                NEW_FEATURES.FEATURE_ID
            ,   NEW_FEATURES.FEATURE_NAME
            ,   NEW_FEATURES.FEATURE_TABLE
            ,   NEW_FEATURES.FEATURE_DATABASE
            ,   NEW_FEATURES.FEATURE_VIEW
            ,   NEW_FEATURES.ENTITY_NAME
            ,   NEW_FEATURES.DATA_DOMAIN
            ,   TIMESTAMP '{date_in_the_past}'
            ,   TIMESTAMP '{end_period_}'
            FROM {schema}.temp NEW_FEATURES
            LEFT JOIN {schema}.{feature_catalog_name} EXISTING_FEATURES
            ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
            WHERE EXISTING_FEATURES.FEATURE_NAME IS NULL;
        """
    
    # Execute the update and insert queries
    execute_query(query_insert)
    execute_query(query_update)
    
    return df

def prepare_feature_ingestion(df, entity_id, feature_names, feature_versions = None, **kwargs):
    """
    
    This function prepares feature data for ingestion into the feature store. It transforms the input DataFrame by unpivoting the specified feature columns and adds additional columns for entity IDs, feature names, feature values, and feature versions.

    Parameters:
    - df: The input DataFrame containing the feature data.
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to identify the entity.
    - feature_names: A list of feature names to unpivot from the DataFrame.
    - feature_version_default (optional): The default feature version to assign if not specified in the feature_versions dictionary. Default is 'dev.0.0'.
    - feature_versions (optional): A dictionary specifying feature versions for specific feature names. The keys are feature names, and the values are feature versions.
    - **kwargs: Additional keyword arguments.

    Returns:
    A transformed tdml.DataFrame containing the prepared feature data.
    
    """    
    
    # Create the UNPIVOT clause for the specified feature columns
    unpivot_columns = ", \n".join(["("+x+") as '"+x+"'" for x in feature_names])

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Create the output column list including entity IDs, feature names, and feature values
    output_columns = ', \n'.join(list_entity_id+ ['FEATURE_NAME','FEATURE_VALUE'])
    primary_index = ','.join(list_entity_id)
    
    # Create a dictionary to store feature versions, using the default version if not specified
    versions = {f:feature_version_default for f in feature_names}
    if feature_versions is not None:
        for k,v in feature_versions.items():
            versions[k] = v

    # Create the CASE statement to assign feature versions based on feature names
    version_query = ["CASE"]+[f"WHEN FEATURE_NAME = '{k}' THEN '{v}' " for k,v in versions.items()]+["END AS FEATURE_VERSION"]
    version_query = '\n'.join(version_query)



    # Create a volatile table name based on the original table's name, ensuring it is unique.
    volatile_table_name = df._table_name.split('.')[1].replace('"', '')
    volatile_table_name = f'temp_{volatile_table_name}'

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # query casting in varchar everything
    nested_query = f"""
    CREATE VOLATILE TABLE {volatile_table_name} AS
    (
        SELECT 
        {','.join(list_entity_id)},
        {','.join([f'CAST({x} AS VARCHAR(2048)) AS {x}' for x in feature_names])}
        FROM {df._table_name}
    ) WITH DATA
    PRIMARY INDEX ({primary_index})
    ON COMMIT PRESERVE ROWS
    """


    # Execute the SQL query to create the volatile table.
    tdml.execute_sql(nested_query)




    # Construct the SQL query to create the volatile table with the transformed data.
    query = f"""
    SELECT 
    {output_columns},
    {version_query}
    FROM {tdml.in_schema(_get_database_username(), volatile_table_name)} 
    UNPIVOT ((FEATURE_VALUE )  FOR  FEATURE_NAME 
    IN ({unpivot_columns})) Tmp
    """



    # Optionally print the query if the display flag is set.
    if tdml.display.print_sqlmr_query:
        print(query)


    # Return the DataFrame representation of the volatile table and its name.
    return tdml.DataFrame.from_query(query), volatile_table_name

def store_feature(entity_id, prepared_features, **kwargs):
    """

    This function stores feature data in the corresponding feature tables in a Teradata database. It updates existing feature values and inserts new feature values based on the entity ID and prepared features.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to identify the entity.
    - prepared_features: A tdml.DataFrame containing the prepared feature data.
    - schema: The schema name in which the feature tables reside.
    - feature_catalog_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.
    - **kwargs: Additional keyword arguments.

    Returns:
    None

    """    

    feature_catalog = tdml.DataFrame(tdml.in_schema(schema, feature_catalog_name))
    
    if date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_statement2 = validtime_statement
    else:
        validtime_statement = f"VALIDTIME PERIOD '({date_in_the_past},{end_period})'"
        validtime_statement2 = f"VALIDTIME AS OF TIMESTAMP '{date_in_the_past}'"
    
    # SQL query to select feature data and corresponding feature metadata from the prepared features and feature catalog
    query = f"""
    {validtime_statement2}
    SELECT
        A.*
    ,   B.FEATURE_ID
    ,   B.FEATURE_TABLE
    ,   B.FEATURE_DATABASE
    FROM {prepared_features._table_name} A,
    {schema}.{feature_catalog_name} B
    WHERE A.FEATURE_NAME = B.FEATURE_NAME
    AND B.DATA_DOMAIN = '{data_domain}'
    """
    
    

    df = tdml.DataFrame.from_query(query)

    # Group the target tables by feature table and feature database and count the number of occurrences
    target_tables = df[['FEATURE_TABLE','FEATURE_DATABASE','FEATURE_ID']].groupby(['FEATURE_TABLE','FEATURE_DATABASE']).count().to_pandas()
    if display_logs:
        display_table(target_tables[['FEATURE_DATABASE','FEATURE_TABLE','count_FEATURE_ID']])
    
    
    ENTITY_ID            = ', \n'.join([k for k,v in entity_id.items()])
    ENTITY_ID_ON         = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k,v in entity_id.items()])
    ENTITY_ID_WHERE_INS  = ' OR '.join([f'EXISTING_FEATURES.{k} IS NOT NULL' for k,v in entity_id.items()])
    ENTITY_ID_WHERE_UP   = ' OR '.join([f'EXISTING_FEATURES.{k} IS NULL' for k,v in entity_id.items()])

    ENTITY_ID_SELECT = ', \n'.join(['NEW_FEATURES.'+k for k, v in entity_id.items()])
    # Iterate over target tables and perform update and insert operations
    for i,row in target_tables.iterrows():

        ENTITY_ID_WHERE_ = ' AND '.join([f'{row.iloc[0]}.{k}   = UPDATED_FEATURES.{k}' for k,v in entity_id.items()])
        # SQL query to update existing feature values
        query_update = f"""
        {validtime_statement} 
        UPDATE {row.iloc[1]}.{row.iloc[0]}
        FROM (
            {validtime_statement2} 
            SELECT
                {ENTITY_ID_SELECT},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION
            FROM {df._table_name} NEW_FEATURES
            LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            WHERE ({ENTITY_ID_WHERE_INS})
            AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
            AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
        ) UPDATED_FEATURES
        SET
            FEATURE_VALUE = UPDATED_FEATURES.FEATURE_VALUE
        WHERE     {ENTITY_ID_WHERE_}
        AND {row.iloc[0]}.FEATURE_ID          = UPDATED_FEATURES.FEATURE_ID
            AND {row.iloc[0]}.FEATURE_VERSION = UPDATED_FEATURES.FEATURE_VERSION;
        """
        
        # SQL query to insert new feature values
        if validtime_statement == 'CURRENT VALIDTIME':
            query_insert = f"""
            {validtime_statement} 
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION
                FROM {df._table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON {ENTITY_ID_ON}
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE ({ENTITY_ID_WHERE_UP})
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """
        elif date_in_the_past is not None:
            if end_period == 'UNTIL_CHANGED':
                end_period_ = '9999-01-01 00:00:00'
            else:
                end_period_ = end_period
            query_insert = f"""
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION, ValidStart, ValidEnd)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION,
                    TIMESTAMP '{date_in_the_past}',
                    TIMESTAMP '{end_period_}'
                FROM {df._table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON {ENTITY_ID_ON}
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE ({ENTITY_ID_WHERE_UP})
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """
        entity_id_str = ', \n'.join([k for k, v in entity_id.items()])
        if display_logs: print(f'insert feature values of new {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_insert)
        execute_query(query_insert)
        if display_logs: print(f'update feature values of existing {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_update)
        execute_query(query_update)
    
    
    return


def build_dataset(entity_id, selected_features, view_name,
                  comment='dataset', no_temporal=False, time_manager=None, query_only=False):
    """
    This function builds a dataset view in a Teradata database. It is designed to pivot and format data from the feature catalog and feature tables based on the specified parameters.

    Parameters:
    - entity_id (dict or list or other): A dictionary, list, or other format representing the entity ID. The keys of the dictionary are used to identify the entity. Lists and other formats are converted to a list of keys.
    - selected_features (dict): A dictionary specifying the selected features and their corresponding feature versions.
    - view_name (str): The name of the dataset view to be created.
    - comment (str, optional): A comment to associate with the dataset view. Defaults to 'dataset'.
    - no_temporal (bool, optional): Flag to determine if temporal aspects should be ignored. Defaults to False.
    - time_manager (object, optional): An object to manage time aspects. Defaults to None.
    - query_only (bool, optional): Flag to determine if we want only the generated query without the execution

    Returns:
    tdml.DataFrame: A DataFrame representing the dataset view.
    """

    # Retrieve feature data from the feature catalog table
    feature_catalog = tdml.DataFrame.from_query(f'CURRENT VALIDTIME SELECT * FROM {schema}.{feature_catalog_name}')

    # Determine the valid time statement based on the presence of a specific date in the past
    if date_in_the_past is None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{date_in_the_past}'"

    # Adjust valid time statement based on the presence of time_manager and no_temporal flag
    if no_temporal:
        validtime_statement = ''

    # Convert entity_id to a list format for processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Compose the entity names and retrieve the corresponding feature locations
    ENTITY_NAMES = ','.join([k for k in list_entity_id])
    ENTITY_ID = ', \n'.join([k for k in list_entity_id])
    if len(selected_features) > 1:
        ENTITY_ID_ = ','.join([','.join(['COALESCE('+','.join(['AA'+str(i+1)+'.'+k for i,c in enumerate(selected_features)])+') as '+k]) for k in list_entity_id])
    else:
        ENTITY_ID_ = ','.join([','.join(['' + ','.join(['AA' + str(i + 1) + '.' + k for i, c in enumerate(selected_features)]) + ' as ' + k]) for k in list_entity_id])


    feature_location = feature_catalog[(feature_catalog.FEATURE_NAME.isin(list(selected_features.keys()))) & \
                                        (feature_catalog.ENTITY_NAME == ENTITY_NAMES) & \
                                        (feature_catalog.DATA_DOMAIN == data_domain) \
                                       ].to_pandas()

    # manage the case sensitivity
    feature_location['FEATURE_NAME_UPPER'] = [x.upper() for x in feature_location['FEATURE_NAME']]
    feature_location['FEATURE_VERSION'] = feature_location['FEATURE_NAME_UPPER'].map({k.upper():v for k,v in selected_features.items()})


    # Build the query to retrieve the selected features from the feature tables
    query = []
    counter = 1
    feature_names = []
    for g,df in feature_location.groupby(['FEATURE_DATABASE','FEATURE_TABLE']):
        for i,row in df.iterrows():
            condition = ' \n '+f"(FEATURE_ID = {row['FEATURE_ID']} AND FEATURE_VERSION = '{row['FEATURE_VERSION']}')"
            if time_manager is not None:
                if 'date' in time_manager.data_type.lower():
                    print(f'Time Manager {time_manager.schema_name}.{time_manager.table_name} has a {time_manager.data_type} data type')
                    query_ = f"""
                    SELECT  A{counter}.* FROM (
                    SELECT * FROM {g[0]}.{g[1]}
                    WHERE  {condition} AND PERIOD(CAST(ValidStart AS DATE), CAST(ValidEnd AS DATE)) CONTAINS (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})
                    ) A{counter}
                    """
                else:
                    print(
                        f'Time Manager {time_manager.schema_name}.{time_manager.table_name} has a {time_manager.data_type} data type')
                    query_ = f"""
                    SELECT  A{counter}.* FROM (
                    SELECT * FROM {g[0]}.{g[1]}
                    WHERE  {condition} AND PERIOD(ValidStart, ValidEnd) CONTAINS (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})
                    ) A{counter}
                    """
            else:
                print(
                    f'no time manager used.')
                query_ = f"""
                SELECT  A{counter}.* FROM (
                {validtime_statement} SELECT * FROM {g[0]}.{g[1]}
                WHERE  {condition}
                ) A{counter}
                """
            query.append(query_)
            feature_names.append(row['FEATURE_NAME'])
            counter+=1



    query_select  = [f"SELECT {ENTITY_ID_}"]
    query_select  = query_select + ['AA'+str(i+1)+'.FEATURE_VALUE AS '+c for i,c in enumerate(feature_names)]
    if no_temporal:
        query_select = query_select + ['AA'+str(i+1)+'.ValidStart AS ValidStart_'+ c + ',AA'+str(i+1)+'.ValidEnd AS ValidEnd_'+ c for i,c in enumerate(feature_names)]
    query_select  = ', \n'.join(query_select)

    query_from    = [' FROM ('+query[0]+') AA1 ']
    query_from    = query_from + [' FULL OUTER JOIN ('+q+') AA'+str(i+1)+' \n ON '+' \n AND '.join([f'AA1.{c}=AA{i+1}.{c}' for c in list_entity_id]) for i,q in enumerate(query) if i>0]
    query_from    = '\n'.join(query_from)

    query_dataset = query_select + '\n' + query_from

    # Build the query to create the dataset view by pivoting the feature data
    query_create_view = f'REPLACE VIEW {schema}.{view_name} AS'
    query_pivot = f"""
    {query_dataset} 
    """

    if tdml.display.print_sqlmr_query:
        print(query_create_view+'\n'+query_pivot)
    if query_only:
        return query_pivot
    else:
        if view_name != None:
            execute_query(query_create_view+'\n'+query_pivot)
            execute_query(f"COMMENT ON VIEW {schema}.{view_name} IS '{comment}'")
            if display_logs: print(f'the dataset view {schema}.{view_name} has been created')

            return tdml.DataFrame(tdml.in_schema(schema, view_name))
        else:
            return tdml.DataFrame.from_query(query_pivot)
def GetTheLargestFeatureID():
    """
    This function retrieves the maximum feature ID from the feature catalog table in the Teradata database.

    Parameters:
    - schema: The schema name in which the feature catalog table resides.
    - table_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.

    Returns:
    The maximum feature ID. If no feature IDs are found (i.e., the table is empty), the function returns 0.

    """
    # Execute a SQL query to get the maximum feature ID from the feature catalog table.
    feature_id = execute_query(f'SEL MAX(FEATURE_ID) AS MAX_FEATURE_ID FROM {schema}.{feature_catalog_name}').fetchall()[0][0]

    # If the result of the query is None (which means the table is empty), return 0.
    if feature_id == None:
        return 0
    # If the result of the query is not None, return the maximum feature ID.
    else:
        return feature_id


def GetAlreadyExistingFeatureNames(feature_name, entity_id):
    """
    This function retrieves the list of already existing features in the feature catalog table in the Teradata database.

    Parameters:
    - feature_name: The name of the feature to check.
    - schema: The schema name in which the feature catalog table resides.
    - table_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.

    Returns:
    A list of existing features.

    """
    # Create a temporary DataFrame with the feature name.
    df = pd.DataFrame({'FEATURE_NAME': feature_name, 'DATA_DOMAIN': data_domain, 'ENTITY_NAME': ','.join([k for k,v in entity_id.items()])})

    # Define a temporary table name.
    tmp_name = 'tdfs__fgjnojnsmdoignmosnig'

    # Copy the temporary DataFrame to a temporary table in the Teradata database.
    tdml.copy_to_sql(df, schema_name=schema, table_name=tmp_name, if_exists='replace',
                     types={'FEATURE_NAME': tdml.VARCHAR(length=255, charset='LATIN')})

    # Execute a SQL query to get the feature names that exist in both the temporary table and the feature catalog table.
    existing_features = list(tdml.DataFrame.from_query(f"""
        SEL A.FEATURE_NAME
        FROM {schema}.{tmp_name} A
        INNER JOIN {schema}.{feature_catalog_name} B
        ON A.FEATURE_NAME = B.FEATURE_NAME
        AND A.ENTITY_NAME = B.ENTITY_NAME
        AND A.DATA_DOMAIN = B.DATA_DOMAIN
        """).to_pandas().FEATURE_NAME.values)

    # Return the list of existing features.
    return existing_features


def Gettdtypes(tddf, features_columns, entity_id):
    """
    This function retrieves the data types of the columns in the provided DataFrame (tddf) and checks their existence in the feature catalog table.
    It also assigns new feature IDs for those that do not already exist in the table.

    Parameters:
    - tddf: The input DataFrame.
    - features_columns: A list of feature column names.
    - schema: The schema name in which the feature catalog table resides.
    - table_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.

    Returns:
    A dictionary where keys are column names and values are dictionaries containing type and id of the feature.

    """
    # Get the data types of the columns in the DataFrame.
    types = get_column_types_simple(tddf, tddf.columns) #dict(tddf.to_pandas(num_rows=10).dtypes)

    # Get the names of the features that already exist in the feature catalog table.
    existing_features = GetAlreadyExistingFeatureNames(tddf.columns, entity_id)

    # Get the maximum feature ID from the feature catalog table.
    feature_id = GetTheLargestFeatureID()

    # Increment the maximum feature ID to create a new feature ID.
    feature_id = feature_id + 1

    # Initialize a dictionary to store the result.
    res = {}

    # Iterate over the data types of the columns in the DataFrame.
    for k, v in types.items():
        # If the column name does not exist in the feature catalog table and is in the list of feature column names...
        if k.upper() not in [n.upper() for n in existing_features] and k.upper() in [n.upper() for n in features_columns]:
            # If the data type of the column is integer...
            if 'int' in str(v):
                # Add an entry to the result dictionary for the column name with its data type and new feature ID.
                res[k] = {'type': 'BIGINT', 'id': feature_id}
            # If the data type of the column is float...
            elif 'float' in str(v):
                # Add an entry to the result dictionary for the column name with its data type and new feature ID.
                res[k] = {'type': 'FLOAT', 'id': feature_id}
            # If the data type of the column is neither integer nor float...
            else:
                res[k] = {'type': 'VARCHAR', 'id': feature_id}
                # Print a message that the data type is not yet managed.
                #if display_logs: print(f'{k} has a type that is not yet managed')

            # Increment the feature ID for the next iteration.
            feature_id += 1

    # Return the result dictionary.
    return res


def _upload_features(df, entity_id, feature_names,
                   feature_versions=feature_version_default):
    """
    This function uploads features from a Teradata DataFrame to the feature store.

    Parameters:
    - df: The input Teradata DataFrame.
    - entity_id: The ID of the entity that the features belong to.
    - feature_names: A list of feature names.
    - schema_name: The name of the schema where the feature store resides.
    - feature_catalog_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.
    - feature_versions (optional): The versions of the features. Can be a string or a list. If it's a string, it's used as the version for all features. If it's a list, it should have the same length as feature_names. Default is 'dev.0.0'.

    Returns:
    A DataFrame representing the dataset view created in the feature store.
    """


    register_entity(entity_id)

    # If feature_versions is a list, create a dictionary mapping each feature name to its corresponding version.
    # If feature_versions is a string, create a dictionary mapping each feature name to this string.
    if type(feature_versions) == list:
        selected_features = {k: v for k, v in zip(feature_names, feature_versions)}
    else:
        selected_features = {k: feature_versions for k in feature_names}

    # Get the Teradata types of the features in df.
    feature_names_types = Gettdtypes(
        df,
        features_columns=feature_names,
        entity_id=entity_id
    )

    # Register the features in the feature catalog.
    register_features(
        entity_id,
        feature_names_types
    )

    # Prepare the features for ingestion.
    prepared_features, volatile_table_name = prepare_feature_ingestion(
        df,
        entity_id,
        feature_names,
        feature_versions=selected_features
    )

    # Store the prepared features in the feature store.
    store_feature(
        entity_id,
        prepared_features
    )

    # Clean up by dropping the temporary volatile table.
    tdml.execute_sql(f'DROP TABLE {volatile_table_name}')

    # Build a dataset view in the feature store.
    dataset = build_dataset(
        entity_id,
        selected_features,
        view_name=None
    )

    # Return the dataset view.
    return dataset

def register_entity(entity_id):
    feature_store_table_name_float = feature_store_table_creation(entity_id, feature_type='FLOAT')
    feature_store_table_name_integer = feature_store_table_creation(entity_id, feature_type='BIGINT')
    feature_store_table_name_varchar = feature_store_table_creation(entity_id, feature_type='VARCHAR')

    return feature_store_table_name_float,feature_store_table_name_integer,feature_store_table_name_varchar


def get_available_features(entity_id, display_details=False):
    if date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF '{date_in_the_past}'"

    if type(entity_id) == dict:
        ENTITY_ID__ = ','.join([k.lower() for k, v in entity_id.items()])
    elif type(entity_id) == list:
        ENTITY_ID__ = ','.join([k.lower() for k in entity_id])
    else:
        ENTITY_ID__ = entity_id.lower()

    query = f"""
    {validtime_statement}
    SELECT 
          FEATURE_NAME
    FROM {schema}.{feature_catalog_name}
    WHERE LOWER(ENTITY_NAME) = '{ENTITY_ID__}'
    AND DATA_DOMAIN = '{data_domain}'
    """

    if display_details:
        print(tdml.DataFrame.from_query(f'{validtime_statement} SELECT * FROM {schema}.{feature_catalog_name}'))

    return list(tdml.DataFrame.from_query(query).to_pandas().FEATURE_NAME.values)


def tdstone2_entity_id(existing_model):
    """
    Generate a dictionary mapping entity IDs to their respective data types in a given model.

    This function iterates over the 'id_row' attribute of the 'mapper_scoring' object in the provided model.
    It then creates a dictionary where each key is an entity ID and its corresponding value is the data type of that entity ID,
    as defined in the 'types' attribute of the 'mapper_scoring' object.

    Args:
        existing_model (object): The model object that contains the 'mapper_scoring' attribute with necessary information.
                                 It is expected to have 'id_row' and 'types' attributes.

    Returns:
        dict: A dictionary where keys are entity IDs and values are their respective data types.

    Raises:
        TypeError: If the 'id_row' attribute in the model is not a list or a single value.

    Note:
        - If 'id_row' is a single value (not a list), it is converted into a list with that single value.
        - The function assumes 'mapper_scoring' and its attributes ('id_row' and 'types') are properly defined in the model.

    Example:
        entity_id = tdstone2_entity_id(model)
        # entity_id might look like {'ID': 'BIGINT'}
    """

    # Initialize an empty dictionary to store entity IDs and their data types.
    entity_id = {}

    # Retrieve the list of IDs from the 'id_row' attribute of 'mapper_scoring' in the model.
    if 'score' in [x[0] for x in inspect.getmembers(type(existing_model))]:
        ids = existing_model.mapper_scoring.id_row
        model_type = 'model scoring'
    elif existing_model.feature_engineering_type == 'feature engineering reducer':
        ids = existing_model.mapper.id_partition
        model_type = 'feature engineering'
    else:
        ids = existing_model.mapper.id_row
        model_type = 'feature engineering'

    # Ensure 'ids' is a list. If not, convert it into a list.
    if type(ids) != list:
        ids = [ids]

    # Iterate over each ID in 'ids' and map it to its corresponding data type in the dictionary.
    if model_type == 'model scoring':
        for k in ids:
            entity_id[k] = existing_model.mapper_scoring.types[k]
    else:
        for k in ids:
            entity_id[k] = existing_model.mapper.types[k]

    # Return the dictionary containing mappings of entity IDs to data types.
    return entity_id


def tdstone2_Gettdtypes(existing_model, entity_id, display_logs=False):
    """
    Generate a dictionary mapping feature names to their data types and unique feature IDs for a given model.

    This function processes a model to create a dictionary where each key is a feature name and its value
    is a dictionary containing the feature's data type and a unique ID. The function filters out features
    that already exist in a feature catalog and only includes new features with 'BIGINT' or 'FLOAT' data types.

    Args:
        existing_model (object): The model object containing necessary schema and scoring information.
        display_logs (bool): Flag to indicate whether to display logs. Defaults to False.

    Returns:
        dict: A dictionary with feature names as keys, and each value is a dictionary containing 'type' and 'id'.

    Raises:
        ValueError: If the data types encountered are neither integer nor float.

    Note:
        - The function assumes that 'tdstone.schema_name' and 'mapper_scoring.scores_repository' are properly defined.
        - The function auto-generates unique IDs for new features.

    Example:
        result = tdstone2_Gettdtypes(model)
        # result might look like {'count_AMOUNT': {'type': 'BIGINT', 'id': 1}, 'mean_AMOUNT': {'type': 'FLOAT', 'id': 3}, ...}
    """

    # Initialize an empty dictionary to store feature names and their types.
    types = {}

    # Create a DataFrame based on the model's schema and scores repository.
    if 'score' in [x[0] for x in inspect.getmembers(type(existing_model))]:
        df = existing_model.get_model_predictions()
    else:
        #if existing_model.feature_engineering_type == 'feature engineering reducer':
        df = existing_model.get_computed_features()

    # Group and count the DataFrame by feature name and type, converting it to a pandas DataFrame.
    df_ = df[['FEATURE_NAME', 'FEATURE_TYPE', 'FEATURE_VALUE']].groupby(['FEATURE_NAME', 'FEATURE_TYPE']).count()[
        ['FEATURE_NAME', 'FEATURE_TYPE']].to_pandas()

    # Iterate through the DataFrame to filter and assign types.
    for i, row in df_.iterrows():
        if 'float' in row['FEATURE_TYPE'] or 'int' in row['FEATURE_TYPE']:
            types[row['FEATURE_NAME']] = row['FEATURE_TYPE']

    # Retrieve existing feature names to filter out already cataloged features.
    existing_features = GetAlreadyExistingFeatureNames(types.keys(),entity_id)

    # Get the current maximum feature ID to ensure uniqueness for new features.
    feature_id = GetTheLargestFeatureID() + 1

    # Initialize a dictionary to store the result.
    res = {}

    # Process each feature type and assign a corresponding data type and unique ID.
    for k, v in types.items():
        if k not in existing_features and k in types.keys():
            if 'int' in str(v):
                res[k] = {'type': 'BIGINT', 'id': feature_id}
            elif 'float' in str(v):
                res[k] = {'type': 'FLOAT', 'id': feature_id}
            else:
                if display_logs:
                    print(f'{k} has a type that is not yet managed')
                continue  # Skip this iteration for unmanaged types.
            feature_id += 1

    # Return the dictionary containing feature names, types, and IDs.
    return res


def prepare_feature_ingestion_tdstone2(df, entity_id):
    """
    Prepare feature data for ingestion into the feature store by transforming a DataFrame.
    This function unpivots specified feature columns in the input DataFrame and adds additional columns
    for entity IDs, feature names, feature values, and feature versions. It creates a volatile table
    in the database to store the transformed data.

    Parameters:
    - df (tdml.DataFrame): The input DataFrame containing the feature data. This DataFrame should have a structure
      compatible with the requirements of the tdstone2 feature store.
    - entity_id (dict): A dictionary mapping column names to their respective entity ID types, used for identifying entities.

    Returns:
    - tdml.DataFrame: A transformed DataFrame containing the prepared feature data in a suitable format for feature store ingestion.
    - str: The name of the volatile table created for storing the transformed data.

    Note:
    - The function assumes the input DataFrame 'df' has a valid table name and is compatible with tdml operations.
    - The function automatically handles the creation and management of a volatile table for the transformed data.
    - 'ID_PROCESS' is used as the feature version identifier.

    Example usage:
        transformed_df, table_name = prepare_feature_ingestion_tdstone2(input_df, entity_id_dict)
    """

    # Ensure the internal table name of the DataFrame is set, necessary for further processing.
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Combine entity ID columns with feature name and value columns to form the output column list.
    output_columns = ', \n'.join(list_entity_id + ['FEATURE_NAME', 'FEATURE_VALUE'])
    primary_index = ','.join(list_entity_id)

    # Define a query segment to assign feature versions.
    version_query = "ID_PROCESS AS FEATURE_VERSION"

    # Create a volatile table name based on the original table's name, ensuring it is unique.
    volatile_table_name = df._table_name.split('.')[1].replace('"', '')
    volatile_table_name = f'temp_{volatile_table_name}'

    # Construct the SQL query to create the volatile table with the transformed data.
    query = f"""
    CREATE VOLATILE TABLE {volatile_table_name} AS
    (
    SELECT 
    {output_columns},
    {version_query}
    FROM {df._table_name}
    ) WITH DATA
    PRIMARY INDEX ({primary_index})
    ON COMMIT PRESERVE ROWS
    """
    # Execute the SQL query to create the volatile table.
    tdml.execute_sql(query)

    # Optionally print the query if the display flag is set.
    if tdml.display.print_sqlmr_query:
        print(query)

    # Return the DataFrame representation of the volatile table and its name.
    return tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name)), volatile_table_name


def upload_tdstone2_scores(model):
    """
    Uploads features from a model's predictions to the Teradata feature store. This function handles the entire
    workflow from extracting feature names and types, registering them in the feature catalog, preparing features for ingestion,
    storing them in the feature store, and finally creating a dataset view in the feature store.

    Parameters:
    - model: The model object whose predictions contain features to be uploaded. This model should have methods
      to extract predictions and feature information.

    Returns:
    - DataFrame: A DataFrame representing the dataset view created in the feature store, which includes
      features from the model's predictions.

    Note:
    - The function assumes that the model provides a method `get_model_predictions` which returns a Teradata DataFrame.
    - Entity ID for the model is extracted and registered in the data domain.
    - The function cleans up by dropping the volatile table created during the process.
    - The feature names and their types are extracted from the model's predictions and are registered in the feature catalog.
    """

    # Extract the entity ID from the existing model.
    entity_id = tdstone2_entity_id(model)

    # Register the entity ID in the data domain.
    register_entity(entity_id)

    # Get the Teradata types of the features from the model's predictions.
    feature_names_types = tdstone2_Gettdtypes(model,entity_id)

    # Register these features in the feature catalog.
    register_features(entity_id, feature_names_types)

    # Prepare the features for ingestion into the feature store.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_model_predictions(),
            entity_id
        )
    else:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_computed_features(),
            entity_id
        )

    # Store the prepared features in the feature store.
    store_feature(entity_id, prepared_features)

    # Clean up by dropping the temporary volatile table.
    tdml.execute_sql(f'DROP TABLE {volatile_table_name}')

    # Get the list of selected features for building the dataset view.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        selected_features = model.get_model_predictions().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']
    else:
        selected_features = model.get_computed_features().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']

    # Build and return the dataset view in the feature store.
    dataset = build_dataset(entity_id, selected_features, view_name=None)
    return dataset


def get_list_entity(domain=None):
    """
    Retrieve a list of unique entity names from a specified data domain.

    This function executes a database query to extract distinct entity names from
    a feature catalog, filtered by the provided data domain. If no domain is
    specified, it defaults to a predefined data domain.

    Parameters:
    domain (str, optional): The data domain to filter the entity names.
                            Defaults to None, in which case a predefined domain is used.

    Returns:
    DataFrame: A pandas-like DataFrame containing the unique entity names.
    """

    # Use the default data domain if none is specified
    if domain is None:
        domain = data_domain

    # Constructing the SQL query to fetch distinct entity names from the specified domain
    query = f"CURRENT VALIDTIME SEL DISTINCT ENTITY_NAME FROM {schema}.{feature_catalog_name} where DATA_DOMAIN = '{domain}'"

    # Executing the query and returning the result as a DataFrame
    return tdml.DataFrame.from_query(query)


def get_list_features(entity_name, domain=None):
    """
    Retrieve a list of feature names associated with a specific entity or entities
    from a given data domain.

    This function constructs and executes a database query to extract feature names
    for the specified entity or entities from a feature catalog, filtered by the
    provided data domain. If no domain is specified, it defaults to a predefined
    data domain.

    Parameters:
    entity_name (str or list): The name of the entity or a list of entity names
                               to fetch features for.
    domain (str, optional): The data domain to filter the feature names.
                            Defaults to None, where a predefined domain is used.

    Returns:
    DataFrame: A pandas-like DataFrame containing the feature names associated with the given entity or entities.
    """

    # Default to a predefined data domain if none is provided
    if domain is None:
        domain = data_domain

    # Convert the entity_name to a string if it is a list
    if type(entity_name) == list:
        entity_name = ','.join(entity_name)

    # Constructing the SQL query to fetch feature names for the specified entity or entities
    query = f"CURRENT VALIDTIME SEL FEATURE_NAME FROM {schema}.{feature_catalog_name} where entity_name = '{entity_name}' AND DATA_DOMAIN = '{domain}'"

    # Executing the query and returning the result as a DataFrame
    return tdml.DataFrame.from_query(query)


def get_feature_versions(entity_name, features, domain=None, latest_version_only=True, version_lag=0):
    """
    Retrieve feature versions for specified features associated with certain entities
    from a given data domain. This function allows fetching either all versions or
    just the latest versions of the features.

    Parameters:
    entity_name (str or list): The name of the entity or a list of entity names
                               for which feature versions are to be fetched.
    features (list): A list of features for which versions are required.
    domain (str, optional): The data domain to filter the feature versions.
                            Defaults to None, where a predefined domain is used.
    latest_version_only (bool, optional): Flag to fetch only the latest version
                                          of each feature. Defaults to True.
    version_lag (int, optional): The number of versions to lag behind the latest.
                                 Only effective if latest_version_only is True. Defaults to 0.

    Returns:
    dict: A dictionary with feature names as keys and their corresponding versions as values.
    """

    # Default to a predefined data domain if none is provided
    if domain is None:
        domain = data_domain

    # Convert the entity_name to a string if it is a list
    if type(entity_name) == list:
        entity_name = ','.join(entity_name)

    # Preparing the feature names for inclusion in the SQL query
    features = ["'" + f + "'" for f in features]

    # Constructing the SQL query to fetch basic feature data for the specified entities and features
    query = f"""CURRENT VALIDTIME 
    SEL FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE
    FROM {schema}.{feature_catalog_name} where entity_name = '{entity_name}' AND DATA_DOMAIN = '{domain}' 
    AND FEATURE_NAME in ({','.join(features)})"""

    # Executing the first query and converting the results to a pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Building the second query to fetch feature versions
    query = []
    for i, row in df.iterrows():
        query_ = f"""
        SEL DISTINCT A{i}.FEATURE_NAME, A{i}.FEATURE_VERSION
        FROM (
        CURRENT VALIDTIME
        SELECT CAST('{row['FEATURE_NAME']}' AS VARCHAR(255)) AS FEATURE_NAME, FEATURE_VERSION FROM {row['FEATURE_DATABASE']}.{row['FEATURE_TABLE']}
        WHERE FEATURE_ID = {row['FEATURE_ID']})
        A{i}
        """
        query.append(query_)

    # Combining the individual queries with UNION ALL
    query = '\n UNION ALL \n'.join(query)

    # Modifying the query to fetch only the latest versions, if specified
    if latest_version_only:
        query = 'SELECT * FROM (' + query + ') A \n' + f'QUALIFY ROW_NUMBER() OVER(PARTITION BY FEATURE_NAME ORDER BY FEATURE_VERSION DESC) = 1+{version_lag}'

    # Executing the final query and converting the results to a pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Returning the results as a dictionary with feature names as keys and their versions as values
    return {row['FEATURE_NAME']:row['FEATURE_VERSION'] for i,row in df.iterrows()}


def upload_features(df, entity_id, feature_names, metadata={}):
    """
    Uploads features from a dataframe to a specified entity, registering the process and returning the resulting dataset.

    Args:
        df (DataFrame): The dataframe containing the features to be uploaded.
        entity_id (dict or compatible type): The entity identifier. If not a dictionary, it will be converted using `get_column_types`.
        feature_names (list): The list of feature names to be uploaded.
        metadata (dict, optional): Additional metadata to associate with the upload. Defaults to an empty dictionary.

    Returns:
        DataFrame: The dataset resulting from the upload process.
    """

    # Convert entity_id to a dictionary if it's not already one
    if type(entity_id) != dict:
        entity_id = get_column_types(df, entity_id)
        print('entity_id has been converted to a proper dictionary : ', entity_id)

    # Register the process and retrieve the SQL query to insert the features, and the process ID
    query_insert, process_id = register_process_view.__wrapped__(
        view_name=df,
        entity_id=entity_id,
        feature_names=feature_names,
        metadata=metadata,
        with_process_id=True
    )

    # Execute the SQL query to insert the features into the database
    execute_query(query_insert)

    # Run the registered process and return the resulting dataset
    dataset = run(process_id=process_id, return_dataset=True)

    return dataset



def _build_time_series(entity_id, selected_feature, query_only=False):
    """
    Constructs a time series dataset for a given entity and feature.
    Optionally returns only the query used for dataset construction.

    This is a wrapper around the `build_dataset` function, tailored specifically for time series data by setting temporal parameters to null.

    Args:
        entity_id (dict): The identifier for the entity for which the dataset is being built.
        selected_feature (str or list): The feature(s) to be included in the dataset.
        query_only (bool, optional): If True, returns only the SQL query used for building the dataset, not the dataset itself. Defaults to False.

    Returns:
        DataFrame or str: The constructed time series dataset as a DataFrame, or the SQL query as a string if query_only is True.
    """

    # Call the build_dataset function with specific parameters set for time series dataset construction
    return build_dataset(
        entity_id=entity_id,  # The identifier for the entity
        selected_features=selected_feature,  # The feature(s) to be included in the dataset
        no_temporal=True,  # Indicates that the dataset should not have a temporal component
        query_only=query_only,  # Determines whether to return just the query or the constructed dataset
        time_manager=None,  # No time management for the dataset construction
        view_name=None  # No specific view name provided
    )


def build_dataset_time_series(df, time_column, entity_id, selected_features, query_only=False, time_manager=None):
    """
    Constructs a time series dataset based on the specified features and entity_id from the provided dataframe.

    Args:
        df (DataFrame): The source dataframe.
        time_column (str): The name of the column in df that represents time.
        entity_id (dict): A dictionary representing the entity identifier.
        selected_features (dict): A dictionary with keys as feature names and values as conditions or specifications for those features.
        query_only (bool, optional): If True, only the SQL query for the dataset is returned. Defaults to False.
        time_manager (TimeManager, optional): An instance of TimeManager to manage time-related operations. Defaults to None.

    Returns:
        DataFrame or str: The constructed time series dataset as a DataFrame, or the SQL query as a string if query_only is True.
    """

    # Convert column names to lowercase for case-insensitive matching
    col = [c.lower() for c in df.columns]

    # Check if the entity_id keys are present in the dataframe columns
    for e in entity_id:
        if e.lower() not in col:
            print(f' {e} is not present in your dataframe')
            print('Here are the columns of your dataframe:')
            print(str(col))
            return  # Exit if any entity_id key is not found

    # Check if the time_column is present in the dataframe columns
    if time_column.lower() not in col:
        print(f' {time_column} is not present in your dataframe')
        print('Here are the columns of your dataframe:')
        print(str(col))
        return  # Exit if the time_column is not found

    # Extract and check the data type of the time_column
    d_ = {x[0]: x[1] for x in df._td_column_names_and_types}
    time_column_data_type = d_[time_column]
    print('time column data type :', time_column_data_type)
    if 'date' not in time_column_data_type.lower() and 'time' not in time_column_data_type.lower():
        print('the time column of your data frame is neither a date nor a timestamp')
        return  # Exit if the time_column data type is not date or timestamp

    # Initialize the select query
    select_query = 'SELECT \n' + ', \n'.join(['A.' + c for c in col]) + '\n'

    # If a time_manager is provided, extract its details
    if time_manager is not None:
        tm_datatype = time_manager.data_type.lower()
        tm_schema = time_manager.schema_name
        tm_table = time_manager.table_name

    sub_queries_list = []
    # For each selected feature, build its part of the query
    for i, (k, v) in enumerate(selected_features.items()):
        select_query += ', BB' + str(i + 1) + '.' + k + '\n'

        nested_query = _build_time_series(entity_id, {k: v}, query_only=True)

        sub_queries = 'SELECT \n' + '\n ,'.join(entity_id) + '\n ,' + k + '\n'

        # Build the sub_queries based on the presence of a time_manager and the data types of time_column and time_manager
        if time_manager is None:
            # there is a time manager
            if 'date' in tm_datatype:
                # the data type of the time column is DATE
                sub_queries += f',	CAST(ValidStart_{k} AS DATE) AS ValidStart \n'
                sub_queries += f',	CAST(ValidEnd_{k} AS DATE) AS ValidEnd \n'
            else:
                # the data type of the time column is timestamp
                sub_queries += f',	CAST(ValidStart_{k} AS TIMESTAMP(0)) AS ValidStart \n'
                sub_queries += f',	CAST(ValidEnd_{k} AS TIMESTAMP(0)) AS ValidEnd \n'
        else:
            # there is a time manager
            if 'date' in time_column_data_type.lower():
                # the data type of the time column is DATE
                if 'date' in tm_datatype:
                    # the data type of the time manager is DATE
                    sub_queries += f',	CAST(ValidStart_{k} AS DATE) AS ValidStart \n'
                    sub_queries += f',	CASE WHEN CAST(ValidEnd_{k} AS DATE) > BUS_DATE.BUSINESS_DATE THEN BUS_DATE.BUSINESS_DATE ELSE CAST(ValidEnd_{k} AS DATE) END AS ValidEnd \n'
                else:
                    # the data type of the time manager is timestamp
                    sub_queries += f',	CAST(ValidStart_{k} AS DATE) AS ValidStart \n'
                    sub_queries += f',	CASE WHEN CAST(ValidEnd_{k} AS DATE) > BUS_DATE.BUSINESS_DATE THEN BUS_DATE.BUSINESS_DATE ELSE CAST(ValidEnd_{k} AS DATE) END AS ValidEnd \n'
            else:
                # the data type of the time column is TIMESTAMP
                if 'date' in tm_datatype:
                    sub_queries += f',	CAST(ValidStart_{k} AS TIMESTAMP(0)) AS ValidStart \n'
                    sub_queries += f',	CASE WHEN CAST(ValidEnd_{k} AS TIMESTAMP(0)) > CAST(BUS_DATE.BUSINESS_DATE AS TIMESTAMP(0)) THEN BUS_DATE.BUSINESS_DATE ELSE CAST(ValidEnd_{k} AS TIMESTAMP(0)) END AS ValidEnd \n'
                else:
                    sub_queries += f',	CAST(ValidStart_{k} AS TIMESTAMP(0)) AS ValidStart \n'
                    sub_queries += f',	CASE WHEN CAST(ValidEnd_{k} AS TIMESTAMP(0)) > CAST(BUS_DATE.BUSINESS_DATE AS TIMESTAMP(0)) THEN BUS_DATE.BUSINESS_DATE ELSE CAST(ValidEnd_{k} AS TIMESTAMP(0)) END AS ValidEnd \n'

        sub_queries += f'FROM ({nested_query}) tmp{i + 1} \n'
        if time_manager is not None:
            sub_queries += f',{tm_schema}.{tm_table} BUS_DATE \n'

        sub_queries += 'WHERE ValidStart < ValidEnd \n'

        sub_queries = 'LEFT JOIN ( \n' + sub_queries + ') BB' + str(i + 1) + '\n ON '

        sub_queries += '\n  AND '.join(['A.' + c + '=BB' + str(i + 1) + '.' + c for c in entity_id])

        sub_queries += f'\n AND PERIOD(BB{i + 1}.ValidStart, BB{i + 1}.ValidEnd) CONTAINS A.{time_column} \n'

        sub_queries_list.append(sub_queries)

    # Combine all parts of the query
    query = select_query + f'FROM ({df.show_query()}) A \n' + '\n --------------- \n'.join(sub_queries_list)

    # If only the query is requested, return it; otherwise, execute the query and return the resulting DataFrame
    if query_only:
        return query
    else:
        return tdml.DataFrame.from_query(query)
