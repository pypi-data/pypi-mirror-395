import teradataml as tdml
import tdfs4ds
from tdfs4ds.utils.query_management import execute_query_wrapper
import uuid
import json
from tdfs4ds import logger,logger_safe

@execute_query_wrapper
def register_process_view(view_name, entity_id, feature_names, metadata={}, entity_null_substitute = {}, **kwargs):
    """
    Registers a process view in the feature store or updates an existing one, based on global configuration and
    specified parameters. This function serves as a wrapper that dynamically chooses the registration method
    (either update-insert or merge) according to the global `tdfs4ds.REGISTER_PROCESS` setting. It supports
    registering views with an option to return the process ID for tracking and further operations.

    Parameters:
    - view_name (str | DataFrame): The name of the view as a string or a DataFrame object. If a DataFrame is provided,
                                   it is expected that the table name will be used as the view name.
    - entity_id (str): The identifier of the entity associated with this view.
    - feature_names (List[str]): A list of the names of features to be included in the view.
    - metadata (dict, optional): Additional metadata related to the view. Defaults to an empty dictionary.
    - **kwargs: Arbitrary keyword arguments. This includes 'with_process_id', which dictates whether the process ID
                should be returned along with the query.

    Returns:
    - If 'with_process_id' is specified and True, the function returns a tuple containing the main SQL query string,
      the process ID, the distribution query, and the filter manager query (if applicable). Otherwise, it returns the
      main SQL query string, the distribution query, and the filter manager query, omitting the process ID.

    Note:
    - The function determines the registration method (update-insert or merge) based on the global configuration.
    - It delegates the actual registration logic to `_register_process_view_update_insert` or `_register_process_view_merge`,
      depending on the chosen method.
    """
    # Determine the process registration method based on global settings and delegate accordingly
    if kwargs.get('with_process_id'):
        # Choose the registration function based on global configuration and unpack the returned values
        if tdfs4ds.REGISTER_PROCESS == 'UPDATE_INSERT':
            query_upsert, process_id, query_upsert_dist, query_upsert_filtermanager = _register_process_view_update_insert.__wrapped__(view_name, entity_id, feature_names, metadata=metadata, entity_null_substitute = entity_null_substitute, **kwargs)
        else:
            query_upsert, process_id, query_upsert_dist, query_upsert_filtermanager = _register_process_view_merge.__wrapped__(view_name, entity_id, feature_names, metadata=metadata, entity_null_substitute = entity_null_substitute,  **kwargs)
        return query_upsert, process_id, query_upsert_dist, query_upsert_filtermanager
    else:
        # Repeat the process without returning the process ID
        if tdfs4ds.REGISTER_PROCESS == 'UPDATE_INSERT':
            query_upsert, query_upsert_dist, query_upsert_filtermanager = _register_process_view_update_insert.__wrapped__(view_name, entity_id, feature_names, metadata=metadata, entity_null_substitute = entity_null_substitute, **kwargs)[:3]
        else:
            query_upsert, query_upsert_dist, query_upsert_filtermanager = _register_process_view_merge.__wrapped__(view_name, entity_id, feature_names, metadata=metadata, entity_null_substitute = entity_null_substitute, **kwargs)[:3]
        return query_upsert, query_upsert_dist, query_upsert_filtermanager
@execute_query_wrapper
def _register_process_view_merge(view_name, entity_id, feature_names, metadata={}, entity_null_substitute= {}, **kwargs):
    """
    This function registers a new process view or updates an existing one in the feature store. It is versatile,
    accepting either a view name as a string or a DataFrame, and can handle different time parameters for data validity.
    The primary operations include generating a unique process ID, constructing SQL queries for inserting or updating
    view details, and optionally returning the process ID for further use. It leverages global configurations and
    specific modules for its operations.

    Parameters:
    - view_name (str | DataFrame): The name of the view as a string, or a DataFrame object. If a DataFrame is provided,
                                   its table name is extracted and used as the view name.
    - entity_id (str): The identifier of the entity to which the view is associated.
    - feature_names (List[str]): The names of features included in the view.
    - metadata (dict, optional): A dictionary of additional metadata related to the view. Defaults to {}.
    - **kwargs: Arbitrary keyword arguments. Includes options like 'with_process_id' to return the process ID,
                'filtermanager' for applying a filter manager, 'primary_index', and 'partitioning' for data distribution.

    Returns:
    - If 'with_process_id' is True, returns a tuple containing the main SQL query string, process ID, distribution query,
      and filter manager query (if applicable). Otherwise, returns the main SQL query string, distribution query, and
      filter manager query without the process ID.

    Note:
    - Assumes certain global variables and configurations (e.g., `tdfs4ds.END_PERIOD`, `tdfs4ds.FEATURE_STORE_TIME`) are set.
    - Requires 'tdml' module for DataFrame operations and 'uuid' for generating unique identifiers.
    """

    # Handle teradataml DataFrame input
    if isinstance(view_name, tdml.dataframe.dataframe.DataFrame):
        try:
            view_name = view_name._table_name
        except Exception:
            logger_safe(
                "error",
                "Invalid DataFrame for view registration. Use: tdml.DataFrame(<table/view>). Crystallize if needed."
            )
            raise

    # Prevent using temporary teradataml views
    if view_name.split('.')[1].startswith('ml__'):
        logger_safe(
            "error",
            "Invalid view name '%s': starts with 'ml__'. Please crystallize your view first.",
            view_name
        )
        raise ValueError("Invalid process view name: temporary teradataml views are not allowed.")

    # Get optional arguments
    filtermanager = kwargs.get('filtermanager', None)
    query_upsert_filtermanager = None
    primary_index = kwargs.get('primary_index', list(entity_id.keys()))
    partitioning = kwargs.get('partitioning', '').replace("'", '"')

    if primary_index is None:
        primary_index = list(entity_id.keys())

    feature_names = ','.join(feature_names)

    # Validtime period
    end_period_ = '9999-01-01 00:00:00' if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED' else tdfs4ds.END_PERIOD
    validtime_statement = (
        'CURRENT VALIDTIME'
        if tdfs4ds.FEATURE_STORE_TIME is None
        else f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{end_period_})'"
    )

    logger_safe("info", "Registering process view: %s", view_name)

    # Check if view already exists in catalog
    query_process_id = f"""
        SEL PROCESS_ID FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW}
        WHERE view_name = '{view_name}'
    """
    process_id_result = tdml.execute_sql(query_process_id).fetchall()

    if process_id_result:
        process_id = process_id_result[0][0]
        logger_safe("info", "Updating existing process_id=%s", process_id)

        query_feature_version = f"""
            SEL PROCESS_VERSION FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW}
            WHERE view_name = '{view_name}'
        """
        feature_version = tdml.execute_sql(query_feature_version).fetchall()[0][0]

        query_primary_index = f"""
            SEL FOR_PRIMARY_INDEX, FOR_DATA_PARTITIONING
            FROM {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
            WHERE process_id = '{process_id}'
        """
        dist_res = tdml.execute_sql(query_primary_index).fetchall()
        if dist_res:
            FOR_PRIMARY_INDEX, FOR_DATA_PARTITIONING = dist_res[0]
        else:
            logger_safe(
                "error",
                "Missing data distribution info for existing process %s. Check distribution table.",
                process_id
            )
            raise ValueError("Missing distribution info.")
    else:
        process_id = str(uuid.uuid4())
        feature_version = 1
        FOR_PRIMARY_INDEX = ",".join(primary_index)
        FOR_DATA_PARTITIONING = partitioning
        logger_safe("info", "Generated new process_id=%s", process_id)

    # Build entity_id string
    ENTITY_ID__ = ','.join(sorted(entity_id.keys()))
    logger_safe("debug", "Entity IDs: %s", ENTITY_ID__)
    logger_safe("debug", "Feature names: %s", feature_names)

    if tdfs4ds.FEATURE_STORE_TIME == None:



        query_upsert = f"""
        {validtime_statement}
        MERGE INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} EXISTING_PROCESS
        USING (
            SEL 
                '{process_id}' AS PROCESS_ID
            ,   'denormalized view' AS PROCESS_TYPE
            ,   '{view_name}' AS VIEW_NAME
            ,   '{ENTITY_ID__}' AS ENTITY_ID
            ,   '{json.dumps(entity_null_substitute).replace("'", '"')}' AS ENTITY_NULL_SUBSTITUTE
            ,   '{feature_names}' AS FEATURE_NAMES
            ,   '{feature_version}' AS FEATURE_VERSION
            ,   '{tdfs4ds.DATA_DOMAIN}' AS DATA_DOMAIN
            ,   '{json.dumps(metadata).replace("'", '"')}' AS METADATA
        ) UPDATED_PROCESS
        ON EXISTING_PROCESS.PROCESS_ID = UPDATED_PROCESS.PROCESS_ID
        AND EXISTING_PROCESS.VIEW_NAME = UPDATED_PROCESS.VIEW_NAME
        WHEN MATCHED THEN
            UPDATE
            SET
                PROCESS_TYPE    = UPDATED_PROCESS.PROCESS_TYPE
            ,   ENTITY_ID       = UPDATED_PROCESS.ENTITY_ID 
            ,   ENTITY_NULL_SUBSTITUTE       = UPDATED_PROCESS.ENTITY_NULL_SUBSTITUTE 
            ,   FEATURE_NAMES   = UPDATED_PROCESS.FEATURE_NAMES
            ,   FEATURE_VERSION = UPDATED_PROCESS.FEATURE_VERSION
            ,   METADATA        = UPDATED_PROCESS.METADATA
            ,   DATA_DOMAIN     = UPDATED_PROCESS.DATA_DOMAIN
        WHEN NOT MATCHED THEN
        INSERT (
            UPDATED_PROCESS.PROCESS_ID,
            UPDATED_PROCESS.PROCESS_TYPE,
            UPDATED_PROCESS.VIEW_NAME,
            UPDATED_PROCESS.ENTITY_ID,
            UPDATED_PROCESS.ENTITY_NULL_SUBSTITUTE,
            UPDATED_PROCESS.FEATURE_NAMES,
            UPDATED_PROCESS.FEATURE_VERSION,
            UPDATED_PROCESS.DATA_DOMAIN,
            UPDATED_PROCESS.METADATA
            )   
        """
        if tdfs4ds.DATA_DISTRIBUTION_TEMPORAL:
            query_upsert_dist = f"""
            {validtime_statement}
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
            SET
                    FOR_PRIMARY_INDEX     = '{FOR_PRIMARY_INDEX}'
                ,   FOR_DATA_PARTITIONING = '{FOR_DATA_PARTITIONING}'         
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} 
                    (
                        '{process_id}'
                    ,   '{",".join(primary_index)}'
                    ,   '{partitioning}' 
            
                    )
            """
        else:
            query_upsert_dist = f"""
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
            SET
                    FOR_PRIMARY_INDEX     = '{FOR_PRIMARY_INDEX}'
                ,   FOR_DATA_PARTITIONING = '{FOR_DATA_PARTITIONING}'         
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} 
                    (
                        '{process_id}'
                    ,   '{",".join(primary_index)}'
                    ,   '{partitioning}'
                    )
            """

        if filtermanager is not None:

            query_upsert_filtermanager = f"""
            {validtime_statement}
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME}
            SET
                DATABASE_NAME = '{filtermanager.schema_name}',
                VIEW_NAME     = '{filtermanager.view_name}',
                TABLE_NAME    = '{filtermanager.table_name}'
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME} 
                (
                    '{process_id}'
                ,   '{filtermanager.schema_name}'
                ,   '{filtermanager.view_name}'
                ,   '{filtermanager.table_name}'
                )
            """
    else:
        query_upsert = f"""
        {validtime_statement}
        UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME}
        SET
                PROCESS_TYPE    = 'denormalized view'
            ,   ENTITY_ID       = '{ENTITY_ID__}'
            ,   ENTITY_NULL_SUBSTITUTE = '{json.dumps(entity_null_substitute).replace("'", '"')}'
            ,   FEATURE_NAMES   = '{feature_names}'
            ,   FEATURE_VERSION = {int(feature_version) + 1}
            ,   METADATA        = '{json.dumps(metadata).replace("'", '"')}'
            ,   DATA_DOMAIN     = '{tdfs4ds.DATA_DOMAIN}'           
        WHERE view_name = '{view_name}'
        ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} 
                (
                '{process_id}',
                'denormalized view',
                '{view_name}',
                '{ENTITY_ID__}',
                '{feature_names}',
                '1',
                '{json.dumps(metadata).replace("'", '"')}',
                '{tdfs4ds.DATA_DOMAIN}',
                TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                TIMESTAMP '{end_period_}'
                )
        """

        query_upsert = f"""
        {validtime_statement}
        MERGE INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} EXISTING_PROCESS
        USING (
            SEL
            PROCESS_ID
            FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW}
            WHERE VIEW_NAME = '{view_name}'
        ) UPDATED_PROCESS
        ON EXISTING_PROCESS.PROCESS_ID = UPDATED_PROCESS.PROCESS_ID
        WHEN MATCHED THEN
            UPDATE
            SET
                PROCESS_TYPE    = 'denormalized view'
            ,   ENTITY_ID       = '{ENTITY_ID__}'
            ,   ENTITY_NULL_SUBSTITUTE = '{json.dumps(entity_null_substitute).replace("'", '"')}'
            ,   FEATURE_NAMES   = '{feature_names}'
            ,   FEATURE_VERSION = {int(feature_version)+1}
            ,   METADATA        = '{json.dumps(metadata).replace("'", '"')}'
            ,   DATA_DOMAIN     = '{tdfs4ds.DATA_DOMAIN}'           
            WHERE view_name = '{view_name}'
        WHEN NOT MATCHED THEN
            INSERT INTO  {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} (PROCESS_ID, PROCESS_TYPE, VIEW_NAME, ENTITY_ID, ENTITY_NULL_SUBSTITUTE, FEATURE_NAMES, FEATURE_VERSION, METADATA, DATA_DOMAIN, ValidStart, ValidEnd)
            VALUES (
                '{process_id}',
                'denormalized view',
                '{view_name}',
                '{ENTITY_ID__}',
                '{json.dumps(entity_null_substitute).replace("'", '"')}',
                '{feature_names}',
                '1',
                '{json.dumps(metadata).replace("'", '"')}',
                '{tdfs4ds.DATA_DOMAIN}',
                TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                TIMESTAMP '{end_period_}'
                )            
        """

        query_upsert = f"""
        {validtime_statement}
        MERGE INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} EXISTING_PROCESS
        USING (
            SEL 
                '{process_id}' AS PROCESS_ID
            ,   'denormalized view' AS PROCESS_TYPE
            ,   '{view_name}' AS VIEW_NAME
            ,   '{ENTITY_ID__}' AS ENTITY_ID
            ,   '{json.dumps(entity_null_substitute).replace("'", '"')}' AS ENTITY_NULL_SUBSTITUTE
            ,   '{feature_names}' AS FEATURE_NAMES
            ,   '{feature_version}' AS FEATURE_VERSION
            ,   '{tdfs4ds.DATA_DOMAIN}' AS DATA_DOMAIN
            ,   '{json.dumps(metadata).replace("'", '"')}' AS METADATA
        ) UPDATED_PROCESS
        ON EXISTING_PROCESS.PROCESS_ID = UPDATED_PROCESS.PROCESS_ID
        AND EXISTING_PROCESS.VIEW_NAME = UPDATED_PROCESS.VIEW_NAME
        WHEN MATCHED THEN
            UPDATE
            SET
                PROCESS_TYPE    = UPDATED_PROCESS.PROCESS_TYPE
            ,   ENTITY_ID       = UPDATED_PROCESS.ENTITY_ID 
            ,   ENTITY_NULL_SUBSTITUTE       = UPDATED_PROCESS.ENTITY_NULL_SUBSTITUTE 
            ,   FEATURE_NAMES   = UPDATED_PROCESS.FEATURE_NAMES
            ,   FEATURE_VERSION = UPDATED_PROCESS.FEATURE_VERSION
            ,   METADATA        = UPDATED_PROCESS.METADATA
            ,   DATA_DOMAIN     = UPDATED_PROCESS.DATA_DOMAIN
        WHEN NOT MATCHED THEN
        INSERT (
            UPDATED_PROCESS.PROCESS_ID,
            UPDATED_PROCESS.PROCESS_TYPE,
            UPDATED_PROCESS.VIEW_NAME,
            UPDATED_PROCESS.ENTITY_ID,
            UPDATED_PROCESS.ENTITY_NULL_SUBSTITUTE,
            UPDATED_PROCESS.FEATURE_NAMES,
            UPDATED_PROCESS.FEATURE_VERSION,
            UPDATED_PROCESS.DATA_DOMAIN,
            UPDATED_PROCESS.METADATA,
            TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
            TIMESTAMP '{end_period_}'
            )    
        """
        if tdfs4ds.DATA_DISTRIBUTION_TEMPORAL:
            query_upsert_dist = f"""
            {validtime_statement}
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
            SET
                    FOR_PRIMARY_INDEX     = '{FOR_PRIMARY_INDEX}'
                ,   FOR_DATA_PARTITIONING = '{FOR_DATA_PARTITIONING}'         
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} 
                    (
                        '{process_id}'
                    ,   '{",".join(primary_index)}'
                    ,   '{partitioning}' 
                    ,   TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'
                    ,   TIMESTAMP '{end_period_}'                
                    )
            """
        else:
            query_upsert_dist = f"""
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
            SET
                    FOR_PRIMARY_INDEX     = '{FOR_PRIMARY_INDEX}'
                ,   FOR_DATA_PARTITIONING = '{FOR_DATA_PARTITIONING}'         
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} 
                    (
                        '{process_id}'
                    ,   '{",".join(primary_index)}'
                    ,   '{partitioning}'
                    )
            """

        if filtermanager is not None:
            query_upsert_filtermanager = f"""
            {validtime_statement}
            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME}
            SET
                DATABASE_NAME = '{filtermanager.schema_name}',
                VIEW_NAME     = '{filtermanager.view_name}',
                TABLE_NAME    = '{filtermanager.table_name}'
            WHERE PROCESS_ID = '{process_id}'
            ELSE INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME} 
                (
                    '{process_id}'
                ,   '{filtermanager.schema_name}'
                ,   '{filtermanager.view_name}'
                ,   '{filtermanager.table_name}'
                ,   TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'
                ,   TIMESTAMP '{end_period_}'
                )
            """


    logger_safe("info", "Process registered: process_id=%s", process_id)
    logger_safe("info", "To rerun: run(process_id='%s')", process_id)
    logger_safe("info", "To build dataset: dataset = run(process_id='%s', return_dataset=True)", process_id)

    # Return queries
    if kwargs.get('with_process_id'):
        return query_upsert, process_id, query_upsert_dist, query_upsert_filtermanager
    else:
        return query_upsert, query_upsert_dist, query_upsert_filtermanager
    
@execute_query_wrapper
def _register_process_view_update_insert(view_name, entity_id, feature_names, metadata={}, entity_null_substitute={}, **kwargs):
    """
    Registers or updates a process view in the feature store. This function supports both the creation of new views
    and the modification of existing ones. It handles the process based on the type of view name provided (str or DataFrame)
    and the specified time parameters (current or past).

    The function generates a unique process identifier and constructs a SQL query to insert or update the view details
    in the feature store. Additionally, it handles logging of the process registration.

    Parameters:
    view_name (str or DataFrame): The name of the view (string) or a DataFrame object representing the view. If a DataFrame is provided,
                                  its table name is used as the view name.
    entity_id (str): The identifier of the entity associated with the view.
    feature_names (list of str): A list of feature names included in the view.
    metadata (dict, optional): Additional metadata related to the view. Defaults to an empty dictionary.
    kwargs: Additional keyword arguments. If 'with_process_id' is provided and set to True, the function also returns the process ID.

    Returns:
    tuple or str: If 'with_process_id' is True, returns a tuple containing the SQL query string and the process ID.
                  Otherwise, returns only the SQL query string. The query is for inserting or updating the view details
                  in the feature store.

    Note:
    - The function assumes specific global variables and configurations (like `tdfs4ds.END_PERIOD`, `tdfs4ds.FEATURE_STORE_TIME`, etc.)
      are already set in the environment.
    - It requires the 'tdml' module for DataFrame operations and 'uuid' for generating unique identifiers.
    """

    # Handling the case where the view name is provided as a DataFrame
    if type(view_name) == tdml.dataframe.dataframe.DataFrame:
        try:
            view_name = view_name._table_name
        except:
            print('create your teradata dataframe using tdml.DataFrame(<view name>). Crystallize your view if needed')
            return []

    # Get filter manager:
    filtermanager = kwargs.get('filtermanager',None)
    if filtermanager is None:
        query_insert_filtermanager = None

    # Get data distribution related inputs:
    primary_index = kwargs.get('primary_index', [e for e in entity_id.keys()])
    partitioning  = kwargs.get('partitioning','').replace("'",'"')

    if primary_index is None:
        primary_index = [e for e in entity_id.keys()]

    # Generating a unique process identifier
    process_id = str(uuid.uuid4())

    # Joining the feature names into a comma-separated string
    feature_names = ','.join(feature_names)

    # Setting the end period for the view
    if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
        end_period_ = '9999-01-01 00:00:00'
    else:
        end_period_ = tdfs4ds.END_PERIOD

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{end_period_})'"

    # Create a comma-separated string of entity IDs
    entity_id_list = list(entity_id.keys())
    entity_id_list.sort()
    ENTITY_ID__ = ','.join([k for k in entity_id_list])

    # Handling cases based on whether the date is in the past or not
    if tdfs4ds.FEATURE_STORE_TIME == None:

        # Checking if the view already exists in the feature store
        query_ = f"CURRENT VALIDTIME SEL * FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} WHERE view_name = '{view_name}'"
        df = tdml.DataFrame.from_query(query_)

        # Constructing the query for new views
        if df.shape[0] == 0:
            query_insert = f"""
                CURRENT VALIDTIME INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} (PROCESS_ID, PROCESS_TYPE, VIEW_NAME, ENTITY_ID, ENTITY_NULL_SUBSTITUTE, FEATURE_NAMES, FEATURE_VERSION, METADATA, DATA_DOMAIN)
                    VALUES ('{process_id}',
                    'denormalized view',
                    '{view_name}',
                    '{ENTITY_ID__}',
                    '{json.dumps(entity_null_substitute).replace("'", '"')}',
                    '{feature_names}',
                    '1',
                    '{json.dumps(metadata).replace("'", '"')}',
                    '{tdfs4ds.DATA_DOMAIN}'
                    )
                """

            query_insert_dist = f"""
                CURRENT VALIDTIME INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} (PROCESS_ID, FOR_PRIMARY_INDEX, FOR_DATA_PARTITIONING)
                    VALUES ('{process_id}',
                    '{",".join(primary_index)}',
                    '{partitioning}'
                    )
                """

            if filtermanager is not None:
                query_insert_filtermanager = f"""
                CURRENT VALIDTIME INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME} (PROCESS_ID, DATABASE_NAME, VIEW_NAME, TABLE_NAME)
                    VALUES ('{process_id}',
                    '{filtermanager.schema_name}',
                    '{filtermanager.view_name}',
                    '{filtermanager.table_name}'
                    )
                """
        # Constructing the query for updating existing views
        else:
            query_insert = f"""
                            CURRENT VALIDTIME UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} 
                            SET 
                                PROCESS_TYPE = 'denormalized view'
                            ,   ENTITY_ID = '{ENTITY_ID__}'
                            ,   ENTITY_NULL_SUBSTITUTE = '{json.dumps(entity_null_substitute).replace("'", '"')}'
                            ,   FEATURE_NAMES = '{feature_names}'
                            ,   FEATURE_VERSION = CAST((CAST(FEATURE_VERSION AS INTEGER) +1) AS VARCHAR(4))
                            ,   METADATA = '{json.dumps(metadata).replace("'", '"')}'
                            ,   DATA_DOMAIN = '{tdfs4ds.DATA_DOMAIN}'
                            WHERE VIEW_NAME = '{view_name}'
                            """
            process_id = tdml.DataFrame.from_query(f"CURRENT VALIDTIME SEL PROCESS_ID FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} WHERE VIEW_NAME = '{view_name}'").to_pandas().PROCESS_ID.values[0]

            query_insert_dist = f"""
                CURRENT VALIDTIME UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
                SET 
                    FOR_PRIMARY_INDEX = '{",".join(primary_index)}',
                    FOR_DATA_PARTITIONING = '{partitioning}' 
                WHERE PROCESS_ID = '{process_id}'
                """

            if filtermanager is not None:
                query_insert_filtermanager = f"""
                CURRENT VALIDTIME UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME}
                SET 
                    DATABASE_NAME = '{filtermanager.schema_name}',
                    VIEW_NAME     = '{filtermanager.view_name}',
                    TABLE_NAME    = '{filtermanager.table_name}'
                WHERE PROCESS_ID = '{process_id}'
                """
    else:
        # Handling the case when the date is in the past
        df = tdml.DataFrame.from_query(f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}' SEL * FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} WHERE view_name = '{view_name}'")



        # Constructing the query for new views with a past date
        if df.shape[0] == 0:
            query_insert = f"""
            INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} (PROCESS_ID, PROCESS_TYPE, VIEW_NAME,  ENTITY_ID, ENTITY_NULL_SUBSTITUTE, FEATURE_NAMES, FEATURE_VERSION, METADATA, DATA_DOMAIN,ValidStart, ValidEnd)
                VALUES ('{process_id}',
                'denormalized view',
                '{view_name}',
                '{ENTITY_ID__}',
                '{json.dumps(entity_null_substitute).replace("'", '"')}'
                ,'{feature_names}',
                '1',
                '{json.dumps(metadata).replace("'", '"')}',
                '{tdfs4ds.DATA_DOMAIN}',
                TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                TIMESTAMP '{end_period_}'
                )
            """

            query_insert_dist = f"""
                INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME} (PROCESS_ID, FOR_PRIMARY_INDEX, FOR_DATA_PARTITIONING,ValidStart, ValidEnd)
                    VALUES ('{process_id}',
                    '{",".join(primary_index)}',
                    '{partitioning}',
                    TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                    TIMESTAMP '{end_period_}' 
                """

            if filtermanager is not None:
                query_insert_filtermanager = f"""
                INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME} (PROCESS_ID, DATABASE_NAME, VIEW_NAME, TABLE_NAME,ValidStart, ValidEnd)
                    VALUES ('{process_id}',
                    '{filtermanager.schema_name}',
                    '{filtermanager.view_name}',
                    '{filtermanager.table_name}',
                    TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                    TIMESTAMP '{end_period_}' 
                    )
                """
        # Constructing the query for updating existing views with a past date
        else:
            query_insert = f"""{validtime_statement}
                            UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} 
                            SET 
                                PROCESS_TYPE = 'denormalized view'
                            ,   ENTITY_ID = '{ENTITY_ID__}'
                            ,   ENTITY_ID = '{json.dumps(entity_null_substitute).replace("'", '"')}'
                            ,   FEATURE_NAMES = '{feature_names}'
                            ,   FEATURE_VERSION = CAST((CAST(FEATURE_VERSION AS INTEGER) +1) AS VARCHAR(4))
                            ,   METADATA = '{json.dumps(metadata).replace("'", '"')}'
                            ,   DATA_DOMAIN = '{tdfs4ds.DATA_DOMAIN}'
                            WHERE VIEW_NAME = '{view_name}'
                            """
            process_id = tdml.DataFrame.from_query(
                f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}' SEL PROCESS_ID FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} WHERE VIEW_NAME = '{view_name}'").to_pandas().PROCESS_ID.values[
                0]

            query_insert_dist = f"""{validtime_statement}
                UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.DATA_DISTRIBUTION_NAME}
                SET 
                    FOR_PRIMARY_INDEX = '{",".join(primary_index)}',
                    FOR_DATA_PARTITIONING = '{partitioning}' 
                WHERE PROCESS_ID = '{process_id}'
                """

            if filtermanager is not None:
                query_insert_filtermanager = f"""{validtime_statement}
                UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FILTER_MANAGER_NAME}
                SET 
                    DATABASE_NAME = '{filtermanager.schema_name}',
                    VIEW_NAME     = '{filtermanager.view_name}',
                    TABLE_NAME    = '{filtermanager.table_name}'
                WHERE PROCESS_ID = '{process_id}'
                """

    # Logging the process registration
    print(f'register process with id : {process_id}')
    print(f'to run the process again just type : run(process_id={process_id})')
    print(f'to update your dataset : dataset = run(process_id={process_id},return_dataset=True)')

    if kwargs.get('with_process_id'):
        return query_insert, process_id, query_insert_dist, query_insert_filtermanager
    else:
        return query_insert, query_insert_dist, query_insert_filtermanager

@execute_query_wrapper
def register_process_tdstone(model, metadata={}):
    """
    Registers a 'tdstone2 view' process in the feature store with specified model details and metadata.
    This function is designed for registering hyper-segmented models created using the 'tdstone2' Python package.
    It handles both scenarios where the feature store date is current or in the past.

    Parameters:
    model (Model Object): An instance of the 'tdstone2' model containing necessary details for the registration.
    metadata (dict, optional): Additional metadata related to the process. Defaults to an empty dictionary.

    Returns:
    str: A SQL query string to insert the process details into the feature store.

    Notes:
    - The 'model' parameter should be an object of the 'tdstone2' model class.
    - This function generates a unique process identifier for each registration.
    - It constructs SQL queries for both current valid time and past date scenarios based on 'tdfs4ds' global variables.
    - The function logs the process registration by printing the process ID.

    Dependencies:
    - 'tdfs4ds' global variables and configurations must be set in the environment.
    - The 'uuid' and 'json' modules are used for generating unique identifiers and handling metadata, respectively.
    - This function requires the 'tdstone2' Python package for working with 'tdstone2' models.
    """

    # Generating a unique process identifier
    process_id = str(uuid.uuid4())

    # Handling the current date scenario
    if tdfs4ds.FEATURE_STORE_TIME is None:
        # Constructing the query for insertion with current valid time
        query_insert = f"""
            CURRENT VALIDTIME INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} (PROCESS_ID, PROCESS_TYPE, ENTITY_ID, FEATURE_VERSION, METADATA, DATA_DOMAIN)
                VALUES ('{process_id}',
                'tdstone2 view',
                '{model.mapper_scoring.id_row}',
                '{model.id}',
                '{json.dumps(metadata).replace("'", '"')}',
                '{tdfs4ds.DATA_DOMAIN}'
                )
            """
    else:
        # Determining the end period based on feature store configuration
        end_period_ = '9999-01-01 00:00:00' if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED' else tdfs4ds.END_PERIOD

        # Constructing the query for insertion with a specified past date
        query_insert = f"""
        INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME} (PROCESS_ID, PROCESS_TYPE, ENTITY_ID, FEATURE_VERSION, METADATA, DATA_DOMAIN, ValidStart, ValidEnd)
            VALUES ('{process_id}',
            'tdstone2 view',
            '{model.mapper_scoring.id_row}',
            '{model.id}',
            '{json.dumps(metadata).replace("'", '"')}',
            '{tdfs4ds.DATA_DOMAIN}',
            TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
            TIMESTAMP '{end_period_}')
        """

    # Logging the process registration
    print(f'register process with id : {process_id}')

    return query_insert