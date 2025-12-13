import teradataml as tdml
import pandas as pd


def feature_store_catalog_creation(schema,if_exists = 'replace',table_name='FS_FEATURE_CATALOG',comment='this table is a feature catalog'):
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
    CREATE MULTISET TABLE {schema}.{table_name},
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
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (FEATURE_ID);
    """
    
    # SQL query to create a secondary index on the feature name
    query2 = f"CREATE INDEX (FEATURE_NAME) ON {schema}.{table_name};"
    
    # SQL query to comment the table
    query3 = f"COMMENT ON TABLE {schema}.{table_name} IS '{comment}'"
    
    try:
        # Attempt to execute the create table query
        tdml.get_context().execute(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        print(f'TABLE {schema}.{table_name} has been created')
        tdml.get_context().execute(query3)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            tdml.get_context().execute(f'DROP TABLE  {schema}.{table_name}')
            print(f'TABLE {schema}.{table_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                tdml.get_context().execute(query)
                print(f'TABLE {schema}.{table_name} has been re-created')
                if tdml.display.print_sqlmr_query:
                    print(query)
                tdml.get_context().execute(query3)
            except Exception as e:
                print(str(e).split('\n')[0])
    
    try:
        # Attempt to create the secondary index
        tdml.get_context().execute(query2)
        if tdml.display.print_sqlmr_query:
            print(query)
        print(f'SECONDARY INDEX ON TABLE {schema}.{table_name} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])
    
    return table_name


def get_feature_store_table_name(entity_id, feature_type):
    """

    This function generates the table and view names for a feature store table based on the provided entity ID and feature type.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to construct the table and view names.
    - feature_type: The type of the feature.

    Returns:
    A tuple containing the generated table name and view name.

    """  
    
    # Construct the table name by concatenating the elements 'FS', 'T', the keys of entity_id, and feature_type
    table_name = ['FS','T']+list(entity_id.keys())+[feature_type]
    table_name = '_'.join(table_name)
    
    # Construct the view name by concatenating the elements 'FS', 'V', the keys of entity_id, and feature_type
    view_name  = ['FS','V']+list(entity_id.keys())+[feature_type]
    view_name  = '_'.join(view_name)
    
    return table_name, view_name

def feature_store_table_creation(entity_id, feature_type, schema, if_exists = 'replace',feature_catalog_name='FS_FEATURE_CATALOG'):

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
                FEATURE_VALUE FLOAT,
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
        tdml.get_context().execute(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        print(f'TABLE {schema}.{table_name} has been created')
        tdml.get_context().execute(query2)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            tdml.get_context().execute(f'DROP TABLE  {schema}.{table_name}')
            print(f'TABLE {schema}.{table_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                tdml.get_context().execute(query)
                print(f'TABLE {schema}.{table_name} has been re-created')
                if tdml.display.print_sqlmr_query:
                    print(query)
            except Exception as e:
                print(str(e).split('\n')[0])
    
    try:
        # Attempt to create the view
        tdml.get_context().execute(query_view)
        if tdml.display.print_sqlmr_query:
            print(query)
        print(f'VIEW {schema}.{view_name} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])
    
    return table_name

def register_features(entity_id, feature_names_types, schema, feature_catalog_name='FS_FEATURE_CATALOG'):
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

    if len(list(feature_names_types.keys())) == 0:
        print('no new feature to register')
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
    df['FEATURE_TABLE'] = df.apply(lambda row:get_feature_store_table_name(entity_id, row[1])[0], axis=1)
    df['FEATURE_VIEW']  = df.apply(lambda row:get_feature_store_table_name(entity_id, row[1])[1], axis=1)
    
    # Add additional columns to the DataFrame
    df['ENTITY_NAME']     = ENTITY_ID__
    df['FEATURE_DATABASE'] = schema
    
    # Copy the DataFrame to a temporary table in Teradata
    tdml.copy_to_sql(df,table_name = 'temp', schema_name = schema, if_exists = 'replace', primary_index = 'FEATURE_ID', types={'FEATURE_ID':tdml.BIGINT})
    
    # SQL query to update existing entries in the feature catalog
    query_update = f"""
    CURRENT VALIDTIME 
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
        FROM {schema}.temp NEW_FEATURES
        LEFT JOIN {schema}.{feature_catalog_name} EXISTING_FEATURES
        ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
        WHERE EXISTING_FEATURES.FEATURE_NAME IS NOT NULL
    ) UPDATED_FEATURES
    SET
        FEATURE_NAME     = UPDATED_FEATURES.FEATURE_NAME,
        FEATURE_TABLE    = UPDATED_FEATURES.FEATURE_TABLE,
        FEATURE_DATABASE = UPDATED_FEATURES.FEATURE_DATABASE,
        FEATURE_VIEW     = UPDATED_FEATURES.FEATURE_VIEW,
        ENTITY_NAME        = UPDATED_FEATURES.ENTITY_NAME
    WHERE     {feature_catalog_name}.FEATURE_ID       = UPDATED_FEATURES.FEATURE_ID;
    """
    
    # SQL query to insert new entries into the feature catalog
    query_insert = f"""
    CURRENT VALIDTIME 
    INSERT INTO {schema}.{feature_catalog_name} (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE, FEATURE_VIEW, ENTITY_NAME)
        SELECT
            NEW_FEATURES.FEATURE_ID
        ,   NEW_FEATURES.FEATURE_NAME
        ,   NEW_FEATURES.FEATURE_TABLE
        ,   NEW_FEATURES.FEATURE_DATABASE
        ,   NEW_FEATURES.FEATURE_VIEW
        ,   NEW_FEATURES.ENTITY_NAME
        FROM {schema}.temp NEW_FEATURES
        LEFT JOIN {schema}.{feature_catalog_name} EXISTING_FEATURES
        ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
        WHERE EXISTING_FEATURES.FEATURE_NAME IS NULL;
    """    
    
    # Execute the update and insert queries
    tdml.get_context().execute(query_insert)
    tdml.get_context().execute(query_update)
    
    return df

def prepare_feature_ingestion(df, entity_id, feature_names, feature_version_default = 'dev.0.0', feature_versions = None, **kwargs):
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
    
    # Create the output column list including entity IDs, feature names, and feature values
    output_columns = ', \n'.join(list(entity_id.keys()) + ['FEATURE_NAME','FEATURE_VALUE'])
    
    # Create a dictionary to store feature versions, using the default version if not specified
    versions = {f:feature_version_default for f in feature_names}
    if feature_versions is not None:
        for k,v in feature_versions.items():
            versions[k] = v

    # Create the CASE statement to assign feature versions based on feature names
    version_query = ["CASE"]+[f"WHEN FEATURE_NAME = '{k}' THEN '{v}' " for k,v in versions.items()]+["END AS FEATURE_VERSION"]
    version_query = '\n'.join(version_query)
    
    # Create the UNPIVOT query to transform the DataFrame
    query_unpivot = f"""
    SELECT 
    {output_columns},
    {version_query}
    FROM {df._table_name} UNPIVOT ((FEATURE_VALUE)  FOR  FEATURE_NAME 
                              IN ({unpivot_columns})) Tmp;
    """
    if tdml.display.print_sqlmr_query:
        print(query_unpivot)
            
    return tdml.DataFrame.from_query(query_unpivot)

def store_feature(entity_id, prepared_features, schema, feature_catalog_name='FS_FEATURE_CATALOG', date_in_the_past = None, **kwargs):
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
    else:
        validtime_statement = f"VALIDTIME AS OF DATE '{date_in_the_past}'"
    
    # SQL query to select feature data and corresponding feature metadata from the prepared features and feature catalog
    query = f"""
    {validtime_statement}
    SELECT
        A.*
    ,   B.FEATURE_ID
    ,   B.FEATURE_TABLE
    ,   B.FEATURE_DATABASE
    FROM {prepared_features._table_name} A,
    {schema}.{feature_catalog_name} B
    WHERE A.FEATURE_NAME = B.FEATURE_NAME
    """
    
    

    df = tdml.DataFrame.from_query(query)

    # Group the target tables by feature table and feature database and count the number of occurrences
    target_tables = df[['FEATURE_TABLE','FEATURE_DATABASE','FEATURE_ID']].groupby(['FEATURE_TABLE','FEATURE_DATABASE']).count().to_pandas()
    print(target_tables)
    
    
    ENTITY_ID            = ', \n'.join([k for k,v in entity_id.items()])
    ENTITY_ID_ON         = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k,v in entity_id.items()])
    ENTITY_ID_WHERE_INS  = ' OR '.join([f'EXISTING_FEATURES.{k} IS NOT NULL' for k,v in entity_id.items()])
    ENTITY_ID_WHERE_UP   = ' OR '.join([f'EXISTING_FEATURES.{k} IS NULL' for k,v in entity_id.items()])
    
    
    # Iterate over target tables and perform update and insert operations
    for i,row in target_tables.iterrows():
        
        # SQL query to update existing feature values
        query_update = f"""
        {validtime_statement} 
        UPDATE {row[1]}.{row[0]}
        FROM (
            CURRENT VALIDTIME
            SELECT
                NEW_FEATURES.{ENTITY_ID},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION
            FROM {df._table_name} NEW_FEATURES
            LEFT JOIN {row[1]}.{row[0]} EXISTING_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            WHERE ({ENTITY_ID_WHERE_INS})
            AND NEW_FEATURES.FEATURE_DATABASE = '{row[1]}'
            AND NEW_FEATURES.FEATURE_TABLE = '{row[0]}'
        ) UPDATED_FEATURES
        SET
            FEATURE_VALUE = UPDATED_FEATURES.FEATURE_VALUE
        WHERE     {row[0]}.{ENTITY_ID}   = UPDATED_FEATURES.{ENTITY_ID}
        AND {row[0]}.FEATURE_ID          = UPDATED_FEATURES.FEATURE_ID
            AND {row[0]}.FEATURE_VERSION = UPDATED_FEATURES.FEATURE_VERSION;
        """
        
        # SQL query to insert new feature values
        query_insert = f"""
        {validtime_statement} 
        INSERT INTO {row[1]}.{row[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION)
            SELECT
                NEW_FEATURES.{ENTITY_ID},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION
            FROM {df._table_name} NEW_FEATURES
            LEFT JOIN {row[1]}.{row[0]} EXISTING_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            WHERE ({ENTITY_ID_WHERE_UP})
            AND NEW_FEATURES.FEATURE_DATABASE = '{row[1]}'
            AND NEW_FEATURES.FEATURE_TABLE = '{row[0]}'

        """    
        
        print(f'insert feature values of new {ENTITY_ID} combinations in {row[1]}.{row[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_insert)
        tdml.get_context().execute(query_insert)
        print(f'update feature values of existing {ENTITY_ID} combinations in {row[1]}.{row[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_update)
        tdml.get_context().execute(query_update)
    
    
    return

def build_dataset(entity_id, selected_features, schema, view_name, feature_catalog_name='FS_FEATURE_CATALOG', comment = 'dataset', date_in_the_past = None, **kwargs):
    """
    
    This function builds a dataset view in a Teradata database based on the selected features and entity ID. It retrieves the necessary feature data from the feature catalog and feature tables, and creates a view that pivots the data to the desired format.

    Parameters:
    - entity_id: A dictionary representing the entity ID. The keys of the dictionary are used to identify the entity.
    - selected_features: A dictionary specifying the selected features and their corresponding feature versions.
    - schema: The schema name in which the dataset view will be created.
    - view_name: The name of the dataset view.
    - feature_catalog_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.
    - comment (optional): A comment to associate with the dataset view.
    - **kwargs: Additional keyword arguments.

    Returns:
    A tdml.DataFrame representing the dataset view.

    """
    
    feature_catalog = tdml.DataFrame.from_query(f'CURRENT VALIDTIME SELECT * FROM {schema}.{feature_catalog_name}')
    
    if date_in_the_past == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF DATE '{date_in_the_past}'"

    # Compose the entity names and retrieve the corresponding feature locations
    ENTITY_NAMES = ','.join([k for k in entity_id.keys()])
    feature_location = feature_catalog[(feature_catalog.FEATURE_NAME.isin(list(selected_features.keys()))) & (feature_catalog.ENTITY_NAME == ENTITY_NAMES)].to_pandas()
    feature_location['FEATURE_VERSION'] = feature_location['FEATURE_NAME'].map(selected_features)
    
    # Build the query to retrieve the selected features from the feature tables
    query = []
    for g,df in feature_location.groupby(['FEATURE_DATABASE','FEATURE_TABLE']):
        condition = ' \n OR '.join([f"(FEATURE_ID = {row['FEATURE_ID']} AND FEATURE_VERSION = '{row['FEATURE_VERSION']}')" for i,row in df.iterrows()])
        query_ = f"""
        SELECT * FROM {g[0]}.{g[1]}
        WHERE  {condition}
        """
        query.append(query_)
    query = 'UNION ALL '.join(query)
    
    ENTITY_ID   = ', \n'.join([k for k in entity_id.keys()])
    ENTITY_ID_   = ', \n'.join(['B.'+k for k in entity_id.keys()])

    # Build the query to construct the dataset view by joining the feature catalog and feature data
    query_dataset = f"""
    {validtime_statement}
    SELECT
        A.FEATURE_NAME,
        {ENTITY_ID_},
        B.FEATURE_VALUE
    FROM {schema}.{feature_catalog_name} A
    , ({query}) B
    WHERE A.FEATURE_ID = B.FEATURE_ID
    """

    # Define the output column names for the pivoted view
    output_name  = ',\n'.join([f"'{k}' as {k}" for k in selected_features.keys()])
    output_name_ = ',\n'.join([f'CASE WHEN {k}_cnt=1 THEN {k} END AS {k}' for k in selected_features.keys()])


    # Build the query to create the dataset view by pivoting the feature data
    query_create_view = f'REPLACE VIEW {schema}.{view_name} AS'
    query_pivot = f"""
    SELECT
      {ENTITY_ID}
    , {output_name_}
    FROM ({query_dataset}) AA PIVOT (
          AVG(FEATURE_VALUE),
          COUNT(FEATURE_VALUE) as cnt 
          FOR FEATURE_NAME IN (
            {output_name}
            )
    )Tmp;
    """
    if tdml.display.print_sqlmr_query:
        print(query_create_view+'\n'+query_pivot)
        
    if view_name != None:
        tdml.get_context().execute(query_create_view+'\n'+query_pivot)
        tdml.get_context().execute(f"COMMENT ON VIEW {schema}.{view_name} IS '{comment}'")
        print(f'the dataset view {schema}.{view_name} has been created')

        return tdml.DataFrame(tdml.in_schema(schema, view_name))
    else:
        return tdml.DataFrame.from_query(query_pivot)
def GetTheLargestFeatureID(schema,table_name='FS_FEATURE_CATALOG'):
    """
    This function retrieves the maximum feature ID from the feature catalog table in the Teradata database.

    Parameters:
    - schema: The schema name in which the feature catalog table resides.
    - table_name (optional): The name of the feature catalog table. Default is 'FS_FEATURE_CATALOG'.

    Returns:
    The maximum feature ID. If no feature IDs are found (i.e., the table is empty), the function returns 0.

    """
    # Execute a SQL query to get the maximum feature ID from the feature catalog table.
    feature_id = tdml.get_context().execute(f'SEL MAX(FEATURE_ID) AS MAX_FEATURE_ID FROM {schema}.{table_name}').fetchall()[0][0]

    # If the result of the query is None (which means the table is empty), return 0.
    if feature_id == None:
        return 0
    # If the result of the query is not None, return the maximum feature ID.
    else:
        return feature_id


def GetAlreadyExistingFeatureNames(feature_name, schema, table_name='FS_FEATURE_CATALOG'):
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
    df = pd.DataFrame({'FEATURE_NAME': feature_name})

    # Define a temporary table name.
    tmp_name = 'tdfs__fgjnojnsmdoignmosnig'

    # Copy the temporary DataFrame to a temporary table in the Teradata database.
    tdml.copy_to_sql(df, schema_name=schema, table_name=tmp_name, if_exists='replace',
                     types={'FEATURE_NAME': tdml.VARCHAR(length=255, charset='LATIN')})

    # Execute a SQL query to get the feature names that exist in both the temporary table and the feature catalog table.
    existing_features = list(tdml.DataFrame.from_query(f"""
        SEL A.FEATURE_NAME
        FROM {schema}.{tmp_name} A
        INNER JOIN {schema}.{table_name} B
        ON A.FEATURE_NAME = B.FEATURE_NAME
        """).to_pandas().FEATURE_NAME.values)

    # Return the list of existing features.
    return existing_features


def Gettdtypes(tddf, features_columns, schema, table_name='FS_FEATURE_CATALOG'):
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
    types = dict(tddf.to_pandas(num_rows=10).dtypes)

    # Get the names of the features that already exist in the feature catalog table.
    existing_features = GetAlreadyExistingFeatureNames(tddf.columns, schema, table_name=table_name)

    # Get the maximum feature ID from the feature catalog table.
    feature_id = GetTheLargestFeatureID(schema, table_name=table_name)

    # Increment the maximum feature ID to create a new feature ID.
    feature_id = feature_id + 1

    # Initialize a dictionary to store the result.
    res = {}

    # Iterate over the data types of the columns in the DataFrame.
    for k, v in types.items():
        # If the column name does not exist in the feature catalog table and is in the list of feature column names...
        if k not in existing_features and k in features_columns:
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
                # Print a message that the data type is not yet managed.
                print(f'{k} has a type that is not yet managed')

            # Increment the feature ID for the next iteration.
            feature_id += 1

    # Return the result dictionary.
    return res


def upload_feature(df, entity_id, feature_names, schema_name, feature_catalog_name='FS_FEATURE_CATALOG',
                   feature_versions='dev.0.0'):
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
    # If feature_versions is a list, create a dictionary mapping each feature name to its corresponding version.
    # If feature_versions is a string, create a dictionary mapping each feature name to this string.
    if type(feature_versions) == list:
        selected_features = {k: v for k, v in zip(feature_names, feature_versions)}
    else:
        selected_features = {k: feature_versions for k in feature_names}

    # Get the Teradata types of the features in df.
    feature_names_types = feature_store.Gettdtypes(
        df,
        features_columns=feature_names,
        schema=schema_name
    )

    # Register the features in the feature catalog.
    feature_store.register_features(
        entity_id,
        feature_names_types,
        schema=schema_name,
        feature_catalog_name=feature_catalog_name
    )

    # Prepare the features for ingestion.
    prepared_features = feature_store.prepare_feature_ingestion(
        df,
        entity_id,
        feature_names,
        feature_versions=selected_features
    )

    # Store the prepared features in the feature store.
    feature_store.store_feature(
        entity_id,
        prepared_features,
        schema=Param['database'],
        feature_catalog_name=feature_catalog_name
    )

    # Build a dataset view in the feature store.
    dataset = feature_store.build_dataset(
        entity_id,
        selected_features,
        schema=schema_name,
        view_name=None
    )

    # Return the dataset view.
    return dataset
