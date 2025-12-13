import tdfs4ds.utils
import tdfs4ds.utils.info
import teradataml as tdml
import tdfs4ds
from tdfs4ds.utils.query_management import execute_query,execute_query_wrapper
from tdfs4ds.utils.info import get_column_types_simple
from tdfs4ds.feature_store.feature_query_retrieval import get_feature_store_table_name
import pandas as pd
import tqdm
import inspect
import re
from tdfs4ds import logger_safe, logger

@execute_query_wrapper
def feature_store_catalog_view_creation():
    """
    Constructs a SQL query to replace a view in the feature store catalog.

    The function generates a SQL query that replaces a view in the feature
    store catalog with the content of the feature catalog table. The query
    uses the `REPLACE VIEW` statement and locks rows for access during execution.

    Returns:
        str: A SQL query string that replaces the view with the current state
        of the feature catalog table.
    """
    query = f"""
    REPLACE VIEW {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} AS
    LOCK ROW FOR ACCESS
    SELECT *
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
    """

    return query

def feature_store_catalog_creation(if_exists='replace', comment='this table is a feature catalog'):
    """
    Creates or replaces a feature store catalog table in a Teradata database. The catalog table stores metadata about
    features such as their names, associated tables and databases, validity periods, and more.

    Parameters:
    - if_exists (str, optional): Specifies the action to be taken if the catalog table already exists.
                                 Options are 'replace' (default) and 'fail'. 'replace' drops the existing table and creates a new one,
                                 while 'fail' will raise an exception if the table already exists.
    - comment (str, optional): A comment to be associated with the catalog table, describing its purpose or other information.
                               The default comment is 'this table is a feature catalog'.

    Returns:
    str: The name of the created or replaced catalog table.

    Note:
    - The function uses default values for the schema and table name from the tdfs4ds module.
    - It creates the catalog table with a primary index on 'FEATURE_ID' and a secondary index on 'FEATURE_NAME'.
    - The function also handles the creation of the table's comment.
    - In case of an existing table and 'if_exists' set to 'replace', it will drop the existing table before creating the new one.
    - The function assumes access to the database and appropriate permissions to create or modify tables.

    Example Usage:
    >>> catalog_table_name = feature_store_catalog_creation()
    >>> print(f"Feature catalog table {catalog_table_name} created successfully.")
    """


    # SQL query to create the catalog table
    query = f"""
    CREATE MULTISET TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (

                FEATURE_ID BIGINT,
                FEATURE_NAME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_TYPE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
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
    query2 = f"CREATE INDEX (FEATURE_NAME) ON {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME};"

    # SQL query to comment the table
    query3 = f"COMMENT ON TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} IS '{comment}'"

    try:
        # Attempt to execute the create table query
        execute_query(query)
        if tdml.display.print_sqlmr_query:
            print(query)
        if tdfs4ds.DISPLAY_LOGS: print(f'TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} has been created')
        execute_query(query3)
    except Exception as e:
        # If the table already exists and if_exists is set to 'replace', drop the table and recreate it
        if tdfs4ds.DISPLAY_LOGS: print(str(e).split('\n')[0])
        if str(e).split('\n')[0].endswith('already exists.') and (if_exists == 'replace'):
            execute_query(f'DROP TABLE  {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}')
            print(f'TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                execute_query(query)
                if tdfs4ds.DISPLAY_LOGS: print(
                    f'TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} has been re-created')
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
        if tdfs4ds.DISPLAY_LOGS: print(
            f'SECONDARY INDEX ON TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} has been created')
    except Exception as e:
        print(str(e).split('\n')[0])

    return tdfs4ds.FEATURE_CATALOG_NAME


def feature_store_table_creation(entity_id, feature_type, if_exists='fail', primary_index=None, partitioning=''):
    """
    Creates a table and a corresponding view for feature storage in a Teradata database schema, based on specified entity ID and feature type.
    """
    table_name, view_name = get_feature_store_table_name(entity_id, feature_type, primary_index=primary_index, partitioning=partitioning)
    if len([t for t in tdml.db_list_tables(schema_name=tdfs4ds.SCHEMA).TableName if t.lower() == table_name.lower()]) > 0:
        logger_safe('info', f'table {table_name} in the {tdfs4ds.SCHEMA} database already exists. No need to create it.')
        return table_name
    else:
        logger_safe('info', f'table {table_name} in the {tdfs4ds.SCHEMA} database does not exists. Need to create it.')

    query_feature_value = {
        'FLOAT':            'FEATURE_VALUE FLOAT',
        'BIGINT':           'FEATURE_VALUE BIGINT',
        'VARCHAR_LATIN':    f'FEATURE_VALUE VARCHAR({tdfs4ds.VARCHAR_SIZE}) CHARACTER SET LATIN',
        'VARCHAR_UNICODE':  f'FEATURE_VALUE VARCHAR({tdfs4ds.VARCHAR_SIZE}) CHARACTER SET UNICODE',
        'TIMESTAMP0':       'FEATURE_VALUE TIMESTAMP(0)',
        'TIMESTAMP0TZ':     'FEATURE_VALUE TIMESTAMP(0) WITH TIME ZONE',
        'PERIODTS0':        'FEATURE_VALUE PERIOD(TIMESTAMP(0))',
        'PERIODTS0TZ':      'FEATURE_VALUE PERIOD(TIMESTAMP(0) WITH TIME ZONE)',
        'DECIMAL':          'FEATURE_VALUE DECIMAL(38,19)'
    }

    # Construct the column definitions for the table based on the entity ID
    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()

    ENTITY_ID   = ', \n'.join([k + ' ' + entity_id[k] for k in sorted_entity_id])
    ENTITY_ID_  = ', \n'.join(['B.' + k for k in sorted_entity_id])
    ENTITY_ID__ = ','.join([k for k in sorted_entity_id])

    if primary_index is None:
        primary_index = [k for k in entity_id.keys()]

    # SQL query to create the feature store table
    if feature_type.lower() == 'ref':
        partitioning = partitioning.replace('"', "'")
        partitioning = partitioning.replace(f'RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH}),', '')
        partitioning = partitioning.replace(
            f'RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH})',
            ''
        )
        substr = extract_partition_content(partitioning.upper())
        if len(substr) == 0:
            partitioning = ''
        query = f"""
        CREATE MULTISET TABLE {tdfs4ds.SCHEMA}.{table_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                {ENTITY_ID}
            )
            PRIMARY INDEX ({",".join(primary_index)})
            {partitioning};
    """
    else:
        partitioning = partitioning.replace('"', "'")
        query = f"""
        CREATE MULTISET TABLE {tdfs4ds.SCHEMA}.{table_name},
                FALLBACK,
                NO BEFORE JOURNAL,
                NO AFTER JOURNAL,
                CHECKSUM = DEFAULT,
                DEFAULT MERGEBLOCKRATIO,
                MAP = TD_MAP1
                (
    
                    {ENTITY_ID},
                    FEATURE_ID BIGINT,
                    FEATURE_VALUE {feature_type},
                    FEATURE_VERSION VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                    ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                    ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                    PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
                )
                PRIMARY INDEX ({",".join(primary_index)})
                {partitioning};
        """

    # SQL query to create a secondary index on the feature ID
    query2 = f"CREATE INDEX (FEATURE_ID) ON {tdfs4ds.SCHEMA}.{table_name};"

    # SQL query to comment the table indicating the entity id it is related to
    query3 = f"COMMENT ON TABLE {tdfs4ds.SCHEMA}.{table_name} IS 'Feature Store Table'"

    # SQL query to create the view
    query_view = f"""
    REPLACE VIEW {tdfs4ds.SCHEMA}.{view_name} AS
    LOCK ROW FOR ACCESS
    SEQUENCED VALIDTIME
    SELECT
        {ENTITY_ID_},
        A.FEATURE_NAME,
        B.FEATURE_ID,
        B.FEATURE_VALUE,
        B.FEATURE_VERSION,
        B.ValidStart,
        B.ValidEnd
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} A
    , {tdfs4ds.SCHEMA}.{table_name} B
    WHERE A.FEATURE_ID = B.FEATURE_ID
    """

    try:
        # Attempt to execute the create table query
        execute_query(query, raise_error=True)
        execute_query(query3, raise_error=True)
        if tdml.display.print_sqlmr_query:
            logger_safe('info', query)
            logger_safe('info', query3)
        logger_safe('info', f'TABLE {tdfs4ds.SCHEMA}.{table_name} has been created')
        # execute_query(query2)
    except Exception as e:
        msg = str(e).split('\n')[0]
        logger_safe('error', msg)
        if msg.endswith('already exists.') and (if_exists == 'replace'):
            execute_query(f'DROP TABLE  {tdfs4ds.SCHEMA}.{table_name}', raise_error=True)
            logger_safe('info', f'TABLE {tdfs4ds.SCHEMA}.{table_name} has been dropped')
            try:
                # Attempt to recreate the table after dropping it
                execute_query(query, raise_error=True)
                logger_safe('info', f'TABLE {tdfs4ds.SCHEMA}.{table_name} has been re-created')
                if tdml.display.print_sqlmr_query:
                    logger_safe('info', query)
            except Exception as e2:
                logger_safe('error', str(e2).split('\n')[0])

    try:
        # Attempt to create the view
        execute_query(query_view, raise_error=True)
        if tdml.display.print_sqlmr_query:
            logger_safe('info', query_view)
        logger_safe('info', f'VIEW {tdfs4ds.SCHEMA}.{view_name} has been created')
    except Exception as e:
        logger_safe('error', str(e).split('\n')[0])

    return table_name


def register_features(entity_id, feature_names_types, primary_index = None, partitioning = ''):
    """
    Orchestrates the registration or update of feature definitions in a Teradata database's feature catalog.
    This function selects between two methods for feature registration: update and insert, or merge, based
    on a configuration setting. It serves as an entry point for feature registration workflows, abstracting
    away the specifics of the underlying database operations.

    Parameters:
    - entity_id (dict): A dictionary specifying the entity's identifiers, where keys represent attribute names.
                        This parameter is crucial for defining the scope and granularity of feature data.
    - feature_names_types (dict): A dictionary mapping feature names to their properties, including data types
                                  and unique identifiers. Each value is a dictionary with keys 'type' and 'id'
                                  indicating the feature's data type and a unique identifier, respectively.
    - primary_index (list, optional): Specifies the primary index column(s) for the feature data. This parameter
                                      influences the organization and performance of database operations. If not
                                      specified, defaults are used based on the structure of entity_id.
    - partitioning (str, optional): A string that describes the partitioning strategy by listing column names used
                                    for partitioning. This parameter can affect data storage and retrieval performance.

    Returns:
    None: The function does not return a value but triggers feature registration or update processes within the
          database.

    Note:
    - The function relies on the `tdfs4ds.REGISTER_FEATURE` configuration to determine the registration strategy.
      The two supported strategies are 'UPDATE_INSERT' and 'MERGE', with the latter being the default if no
      specific configuration is provided.
    - It delegates the actual database operations to either `_register_features_update_insert` or
      `_register_features_merge`, depending on the selected strategy. These functions handle the specifics
      of the SQL operations required to register or update feature definitions in the database.

    Example Usage:
    >>> entity_id = {'customer_id': 'INTEGER'}
    >>> feature_names_types = {'age': {'type': 'BIGINT', 'id': 1}, 'gender': {'type': 'VARCHAR', 'id': 2}}
    >>> register_features(entity_id, feature_names_types, primary_index=['customer_id'], partitioning='monthly')

    This example demonstrates initiating the feature registration process for an entity with customer_id as the
    primary index and features such as age and gender, considering a partitioning strategy.
    """
    # Decision logic based on the tdfs4ds configuration for feature registration strategy
    if tdfs4ds.REGISTER_FEATURE == 'UPDATE_INSERT':
        # Use the update and insert method for registering features
        _register_features_update_insert(entity_id, feature_names_types, primary_index, partitioning)
    else:
        # Default to using the merge method for registering features
        _register_features_merge(entity_id, feature_names_types, primary_index, partitioning)

    return

def _register_features_merge(entity_id, feature_names_types, primary_index=None, partitioning=''):
    """
    Register or update feature definitions in the feature catalog, with temporal support.

    This function builds (or refreshes) entries in the Teradata feature catalog from a
    mapping of feature names to their metadata, computes the target feature store table
    and view names, stages the metadata to a temporary table, and executes a MERGE into
    the catalog (with optional VALIDTIME support based on `tdfs4ds.FEATURE_STORE_TIME`).

    Parameters
    ----------
    entity_id : dict[str, Any]
        Mapping of entity-key column names to types. Only the keys (column names) are
        required here; values are not used by this function.
    feature_names_types : dict[str, dict]
        Dict of feature name -> {"type": <SQL_TYPE>, "id": <int>} describing each
        feature’s storage type and identifier in the catalog.
    primary_index : list[str] | None, optional
        Primary index column(s) to use when deriving the feature store table/view names.
        If None, defaults are inferred by `get_feature_store_table_name`.
    partitioning : str, optional
        Partitioning expression or comma-separated column list used by
        `get_feature_store_table_name`.

    Returns
    -------
    pd.DataFrame
        A dataframe of the features that were (up)registered, including:
        FEATURE_NAME, FEATURE_TYPE, FEATURE_ID, FEATURE_TABLE, FEATURE_VIEW,
        ENTITY_NAME, FEATURE_DATABASE, DATA_DOMAIN.

    Notes
    -----
    - When `tdfs4ds.FEATURE_STORE_TIME is None`, uses CURRENT VALIDTIME (non-explicit start/end).
      Otherwise uses `VALIDTIME PERIOD ('<FEATURE_STORE_TIME>', '<END_PERIOD>')` and adds
      the valid-time start/end when inserting.
    - Respects `tdfs4ds.DISPLAY_LOGS` via `logger_safe`.
    """

    # --- VALIDTIME setup -----------------------------------------------------
    if tdfs4ds.FEATURE_STORE_TIME is None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_start = "CAST(CURRENT_TIME AS TIMESTAMP(0) WITH TIME ZONE)"
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"
        validtime_start = f"CAST('{tdfs4ds.FEATURE_STORE_TIME}' AS TIMESTAMP(0) WITH TIME ZONE)"

    if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
        end_period_ = '9999-01-01 00:00:00'
    else:
        end_period_ = tdfs4ds.END_PERIOD

    # --- Input checks & early exit ------------------------------------------
    if not feature_names_types:
        logger_safe("info", "register_features: no new features to register")
        return

    # --- Entity columns (ordered, stable) -----------------------------------
    entity_cols = sorted(list(entity_id.keys()))
    ENTITY_ID__ = ",".join(entity_cols)

    # --- Build dataframe safely (no transpose tricks) ------------------------
    rows = []
    for fname, meta in feature_names_types.items():
        try:
            rows.append({
                "FEATURE_NAME": fname,
                "FEATURE_TYPE": meta["type"],
                "FEATURE_ID":   meta["id"],
            })
        except KeyError as e:
            logger_safe("error", "register_features: missing key %s in feature '%s' meta=%s", str(e), fname, meta)
            raise

    df = pd.DataFrame(rows, columns=["FEATURE_NAME", "FEATURE_TYPE", "FEATURE_ID"])

    logger_safe(
        "debug",
        "register_features: features_count=%d | entity_cols=%s | primary_index=%s | partitioning=%s",
        len(df),
        entity_cols,
        primary_index,
        partitioning,
    )

    # --- Compute feature table & view names ---------------------------------
    # Use apply to preserve original order; get_feature_store_table_name returns (table, view)
    df["FEATURE_TABLE"] = df.apply(
        lambda row: get_feature_store_table_name(
            entity_id,
            row["FEATURE_TYPE"],
            primary_index=primary_index,
            partitioning=partitioning
        )[0],
        axis=1
    )
    df["FEATURE_VIEW"] = df.apply(
        lambda row: get_feature_store_table_name(
            entity_id,
            row["FEATURE_TYPE"],
            primary_index=primary_index,
            partitioning=partitioning
        )[1],
        axis=1
    )

    # --- Add catalog columns -------------------------------------------------
    df["ENTITY_NAME"] = ENTITY_ID__
    df["FEATURE_DATABASE"] = tdfs4ds.SCHEMA
    df["DATA_DOMAIN"] = tdfs4ds.DATA_DOMAIN

    # --- Stage to temp table -------------------------------------------------
    tdml.copy_to_sql(
        df,
        table_name="temp",
        schema_name=tdfs4ds.SCHEMA,
        if_exists="replace",
        primary_index="FEATURE_ID",
        types={"FEATURE_ID": tdml.BIGINT},
    )
    logger_safe("debug", "register_features: staged %d rows to %s.temp", len(df), tdfs4ds.SCHEMA)

    # --- Build MERGE statement ----------------------------------------------
    if tdfs4ds.FEATURE_STORE_TIME is None:
        # no explicit start/end in INSERT branch
        query_merge = f"""
         {validtime_statement}
         MERGE INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} EXISTING_FEATURES
         USING (
             SELECT
                   CASE WHEN B.FEATURE_ID IS NULL THEN A.FEATURE_ID ELSE B.FEATURE_ID END AS FEATURE_ID
                 , A.FEATURE_NAME
                 , A.FEATURE_TYPE
                 , A.FEATURE_TABLE
                 , A.FEATURE_DATABASE
                 , A.FEATURE_VIEW
                 , A.ENTITY_NAME
                 , A.DATA_DOMAIN
             FROM {tdfs4ds.SCHEMA}.temp A
             LEFT JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} B
               ON A.FEATURE_NAME = B.FEATURE_NAME
              AND A.ENTITY_NAME = B.ENTITY_NAME
              AND A.DATA_DOMAIN = B.DATA_DOMAIN
         ) UPDATED_FEATURES
           ON UPDATED_FEATURES.FEATURE_ID   = EXISTING_FEATURES.FEATURE_ID
          AND UPDATED_FEATURES.FEATURE_NAME = EXISTING_FEATURES.FEATURE_NAME
          AND UPDATED_FEATURES.DATA_DOMAIN  = EXISTING_FEATURES.DATA_DOMAIN
         WHEN MATCHED THEN UPDATE SET
               FEATURE_TABLE    = UPDATED_FEATURES.FEATURE_TABLE
             , FEATURE_TYPE     = UPDATED_FEATURES.FEATURE_TYPE
             , FEATURE_DATABASE = UPDATED_FEATURES.FEATURE_DATABASE
             , FEATURE_VIEW     = UPDATED_FEATURES.FEATURE_VIEW
         WHEN NOT MATCHED THEN INSERT
             (  UPDATED_FEATURES.FEATURE_ID
              , UPDATED_FEATURES.FEATURE_NAME
              , UPDATED_FEATURES.FEATURE_TYPE
              , UPDATED_FEATURES.FEATURE_TABLE
              , UPDATED_FEATURES.FEATURE_DATABASE
              , UPDATED_FEATURES.FEATURE_VIEW
              , UPDATED_FEATURES.ENTITY_NAME
              , UPDATED_FEATURES.DATA_DOMAIN
             );
        """
    else:
        # insert with explicit valid-time start/end
        query_merge = f"""
         {validtime_statement}
         MERGE INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} EXISTING_FEATURES
         USING (
             SELECT
                   CASE WHEN B.FEATURE_ID IS NULL THEN A.FEATURE_ID ELSE B.FEATURE_ID END AS FEATURE_ID
                 , A.FEATURE_NAME
                 , A.FEATURE_TYPE
                 , A.FEATURE_TABLE
                 , A.FEATURE_DATABASE
                 , A.FEATURE_VIEW
                 , A.ENTITY_NAME
                 , A.DATA_DOMAIN
             FROM {tdfs4ds.SCHEMA}.temp A
             LEFT JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} B
               ON A.FEATURE_NAME = B.FEATURE_NAME
              AND A.ENTITY_NAME = B.ENTITY_NAME
              AND A.DATA_DOMAIN = B.DATA_DOMAIN
         ) UPDATED_FEATURES
           ON UPDATED_FEATURES.FEATURE_ID   = EXISTING_FEATURES.FEATURE_ID
          AND UPDATED_FEATURES.FEATURE_NAME = EXISTING_FEATURES.FEATURE_NAME
          AND UPDATED_FEATURES.DATA_DOMAIN  = EXISTING_FEATURES.DATA_DOMAIN
         WHEN MATCHED THEN UPDATE SET
               FEATURE_TABLE    = UPDATED_FEATURES.FEATURE_TABLE
             , FEATURE_TYPE     = UPDATED_FEATURES.FEATURE_TYPE
             , FEATURE_DATABASE = UPDATED_FEATURES.FEATURE_DATABASE
             , FEATURE_VIEW     = UPDATED_FEATURES.FEATURE_VIEW
         WHEN NOT MATCHED THEN INSERT
             (  UPDATED_FEATURES.FEATURE_ID
              , UPDATED_FEATURES.FEATURE_NAME
              , UPDATED_FEATURES.FEATURE_TYPE
              , UPDATED_FEATURES.FEATURE_TABLE
              , UPDATED_FEATURES.FEATURE_DATABASE
              , UPDATED_FEATURES.FEATURE_VIEW
              , UPDATED_FEATURES.ENTITY_NAME
              , UPDATED_FEATURES.DATA_DOMAIN
              , {validtime_start}
              , '{end_period_}'
             );
        """

    logger_safe("debug", "register_features: merge_sql_preview=%s", " ".join(query_merge.split())[:400] + " ...")

    # --- Execute MERGE -------------------------------------------------------
    execute_query(query_merge)
    logger_safe(
        "info",
        "register_features: merged %d features into %s.%s",
        len(df),
        tdfs4ds.SCHEMA,
        tdfs4ds.FEATURE_CATALOG_NAME,
    )

    return df

def _register_features_update_insert(entity_id, feature_names_types, primary_index = None, partitioning = ''):
    """
    Registers or updates feature definitions in a Teradata database's feature catalog, associating entity identifiers
    with feature names, types, and other metadata. This function prepares and executes SQL operations to insert new
    feature definitions or update existing ones, considering partitioning strategies and primary index configurations.

    Parameters:
    - entity_id (dict): Specifies the entity's identifiers with keys representing attribute names. This dictionary
                        is crucial for defining the scope and granularity of feature data.
    - feature_names_types (dict): Maps feature names to their properties, including data types and unique identifiers.
                                  Each value is a dictionary with keys 'type' and 'id' indicating the feature's data
                                  type and a unique identifier, respectively.
    - primary_index (list, optional): Identifies the primary index column(s) for the feature data. This influences
                                      the organization and performance of database operations. If not specified,
                                      defaults are used based on the entity_id structure.
    - partitioning (str, optional): Describes the partitioning strategy through a string listing column names used
                                    for partitioning. This can impact data storage and retrieval performance.

    Returns:
    pd.DataFrame: Contains details of the registered features, including names, types, IDs, and references to the
                  respective feature store table and view names, alongside metadata about the entity and database schema.

    Note:
    - The function dynamically constructs SQL queries for inserting new features or updating existing ones in the
      feature catalog, adapting to the provided partitioning and primary index settings.
    - Assumes the existence of a Teradata feature catalog table in the specified schema and that the database connection
      is correctly configured.
    - Utilizes the tdfs4ds module for database schema configurations and valid-time temporal table considerations.

    Example Usage:
    >>> entity_id = {'customer_id': 'INTEGER'}
    >>> feature_names_types = {'age': {'type': 'BIGINT', 'id': 1}, 'gender': {'type': 'VARCHAR_LATIN', 'id': 2}}
    >>> registered_features = register_features(entity_id, feature_names_types)
    >>> print(registered_features)

    This example demonstrates registering features for an entity with attributes customer_id, age, and gender,
    where age and gender features have specified types and unique IDs.
    """

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"

    if len(list(feature_names_types.keys())) == 0:
        if tdfs4ds.DISPLAY_LOGS: print('no new feature to register')
        return

    # Create a comma-separated string of entity IDs
    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()
    ENTITY_ID__ = ','.join([k for k in sorted_entity_id])

    # Create a DataFrame from the feature_names_types dictionary
    if len(feature_names_types.keys()) > 1:
        df = pd.DataFrame(feature_names_types).transpose().reset_index()
        df.columns = ['FEATURE_NAME', 'TYPE', 'FEATURE_ID']
    else:
        df = pd.DataFrame(columns=['FEATURE_NAME', 'TYPE', 'FEATURE_ID'])
        k = list(feature_names_types.keys())[0]
        df['FEATURE_NAME'] = [k]
        df['TYPE'] = [feature_names_types[k]['type']]
        df['FEATURE_ID'] = [feature_names_types[k]['id']]

    if tdfs4ds.DEBUG_MODE:
        print('register_features','primary_index', primary_index)
        print('register_features','partitioning', partitioning)
    # Generate the feature table and view names based on the entity ID and feature type
    df['FEATURE_TABLE'] = df.apply(lambda row: get_feature_store_table_name(entity_id, row.iloc[1], primary_index = primary_index, partitioning = partitioning)[0], axis=1)
    df['FEATURE_VIEW'] = df.apply(lambda row: get_feature_store_table_name(entity_id, row.iloc[1], primary_index = primary_index, partitioning = partitioning)[1], axis=1)

    # Add additional columns to the DataFrame
    df['ENTITY_NAME'] = ENTITY_ID__
    df['FEATURE_DATABASE'] = tdfs4ds.SCHEMA
    df['DATA_DOMAIN'] = tdfs4ds.DATA_DOMAIN

    # Copy the DataFrame to a temporary table in Teradata
    tdml.copy_to_sql(df, table_name='temp', schema_name=tdfs4ds.SCHEMA, if_exists='replace', primary_index='FEATURE_ID',
                     types={'FEATURE_ID': tdml.BIGINT})

    # SQL query to update existing entries in the feature catalog
    query_update = f"""
    {validtime_statement} 
    UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
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
        FROM {tdfs4ds.SCHEMA}.temp NEW_FEATURES
        LEFT JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} EXISTING_FEATURES
        ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
        AND NEW_FEATURES.ENTITY_NAME = EXISTING_FEATURES.ENTITY_NAME -- modified
        AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
        WHERE EXISTING_FEATURES.FEATURE_NAME IS NOT NULL
    ) UPDATED_FEATURES
    SET
        FEATURE_NAME     = UPDATED_FEATURES.FEATURE_NAME,
        FEATURE_TABLE    = UPDATED_FEATURES.FEATURE_TABLE,
        FEATURE_DATABASE = UPDATED_FEATURES.FEATURE_DATABASE,
        FEATURE_VIEW     = UPDATED_FEATURES.FEATURE_VIEW
        --,ENTITY_NAME      = UPDATED_FEATURES.ENTITY_NAME -- modified
    WHERE     {tdfs4ds.FEATURE_CATALOG_NAME_VIEW}.FEATURE_ID = UPDATED_FEATURES.FEATURE_ID
    AND {tdfs4ds.FEATURE_CATALOG_NAME_VIEW}.DATA_DOMAIN = UPDATED_FEATURES.DATA_DOMAIN;
    """

    # SQL query to insert new entries into the feature catalog
    if validtime_statement == 'CURRENT VALIDTIME':
        query_insert = f"""
        {validtime_statement} 
        INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE, FEATURE_VIEW, ENTITY_NAME,DATA_DOMAIN)
            SELECT
                NEW_FEATURES.FEATURE_ID
            ,   NEW_FEATURES.FEATURE_NAME
            ,   NEW_FEATURES.FEATURE_TABLE
            ,   NEW_FEATURES.FEATURE_DATABASE
            ,   NEW_FEATURES.FEATURE_VIEW
            ,   NEW_FEATURES.ENTITY_NAME
            ,   NEW_FEATURES.DATA_DOMAIN
            FROM {tdfs4ds.SCHEMA}.temp NEW_FEATURES
            LEFT JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} EXISTING_FEATURES
            ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.ENTITY_NAME = EXISTING_FEATURES.ENTITY_NAME -- modified
            AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
            WHERE EXISTING_FEATURES.FEATURE_NAME IS NULL;
        """
    elif tdfs4ds.FEATURE_STORE_TIME is not None:
        if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
            end_period_ = '9999-01-01 00:00:00'
        else:
            end_period_ = tdfs4ds.END_PERIOD
        query_insert = f"""
        INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE, FEATURE_VIEW, ENTITY_NAME,DATA_DOMAIN,ValidStart,ValidEnd)
            SELECT
                NEW_FEATURES.FEATURE_ID
            ,   NEW_FEATURES.FEATURE_NAME
            ,   NEW_FEATURES.FEATURE_TABLE
            ,   NEW_FEATURES.FEATURE_DATABASE
            ,   NEW_FEATURES.FEATURE_VIEW
            ,   NEW_FEATURES.ENTITY_NAME
            ,   NEW_FEATURES.DATA_DOMAIN
            ,   TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'
            ,   TIMESTAMP '{end_period_}'
            FROM {tdfs4ds.SCHEMA}.temp NEW_FEATURES
            LEFT JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} EXISTING_FEATURES
            ON NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.ENTITY_NAME = EXISTING_FEATURES.ENTITY_NAME -- modified
            AND NEW_FEATURES.DATA_DOMAIN = EXISTING_FEATURES.DATA_DOMAIN
            WHERE EXISTING_FEATURES.FEATURE_NAME IS NULL;
        """

    # Execute the update and insert queries
    execute_query(query_insert)
    execute_query(query_update)

    return df

def GetTheLargestFeatureID():
    """
    Retrieves the highest feature ID currently in use from the feature catalog table of a Teradata database.

    This function queries the feature catalog table to find the maximum value of the FEATURE_ID column. It is useful for
    identifying the next available feature ID in scenarios where a new feature needs to be added to the catalog.

    Parameters:
    - schema (str): The schema name where the feature catalog table is located.
    - table_name (str, optional): The name of the feature catalog table. Defaults to 'FS_FEATURE_CATALOG'.

    Returns:
    int: The maximum feature ID found in the feature catalog table. If the table is empty, returns 0.

    Note:
    - The function assumes that the feature catalog table exists and is accessible in the specified schema.
    - If the feature catalog table has no entries, the function returns 0, indicating no feature IDs are currently in use.
    - The function is designed for use with Teradata databases and assumes appropriate database access.

    Example Usage:
    >>> max_feature_id = GetTheLargestFeatureID()
    >>> print(f"The largest feature ID is: {max_feature_id}")
    """
    # Execute a SQL query to get the maximum feature ID from the feature catalog table.
    feature_id = execute_query(f'SEL MAX(FEATURE_ID) AS MAX_FEATURE_ID FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}').fetchall()[0][0]

    # If the result of the query is None (which means the table is empty), return 0.
    if feature_id == None:
        return 0
    # If the result of the query is not None, return the maximum feature ID.
    else:
        return feature_id


import pandas as pd
import uuid

def GetAlreadyExistingFeatureNames(feature_name, entity_id):
    """
    Retrieves a list of already existing feature names from the feature catalog table in a Teradata database.
    The function checks against a specific feature name and entity ID to determine if similar features already exist in the catalog.

    Parameters:
    - feature_name (str/list): The name(s) of the feature(s) to check. Can be a single feature name or a list of names.
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.

    Returns:
    list: A list of feature names that already exist in the feature catalog table and match the given feature name and entity ID.

    Note:
    - The function creates a temporary table in the database to facilitate the comparison.
    - It assumes that the feature catalog table exists and is accessible in the specified schema.
    - The function is designed for use with Teradata databases and assumes appropriate database access.
    """

    # Ensure feature_name is a list
    if isinstance(feature_name, str):
        feature_name = [feature_name]

    # Create a temporary DataFrame with the feature name(s)
    list_entity = sorted(entity_id.keys())
    df = pd.DataFrame({
        'FEATURE_NAME': feature_name,
        'DATA_DOMAIN': tdfs4ds.DATA_DOMAIN,
        'ENTITY_NAME': ','.join(list_entity)
    })

    # Generate a unique temporary table name
    tmp_name = f"tdfs_tmp_{uuid.uuid4().hex[:12]}"

    try:
        # Copy the temporary DataFrame to a temporary table in the Teradata database
        tdml.copy_to_sql(
            df,
            schema_name=tdfs4ds.SCHEMA,
            table_name=tmp_name,
            if_exists='replace',
            types={'FEATURE_NAME': tdml.VARCHAR(length=255, charset='LATIN')}
        )

        # Execute a SQL query to get the feature names that exist in both the temporary table and the feature catalog table
        query = f"""
            SEL A.FEATURE_NAME
            FROM {tdfs4ds.SCHEMA}.{tmp_name} A
            INNER JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} B
            ON A.FEATURE_NAME = B.FEATURE_NAME
            AND A.ENTITY_NAME = B.ENTITY_NAME
            AND A.DATA_DOMAIN = B.DATA_DOMAIN
        """
        existing_features = list(
            tdml.DataFrame.from_query(query).to_pandas().FEATURE_NAME.values
        )

    finally:
        # Clean up: drop the temporary table
        try:
            tdml.execute(f"DROP TABLE {tdfs4ds.SCHEMA}.{tmp_name};")
        except Exception as e:
            # Ignore if already dropped or not found
            pass

    return existing_features


def Gettdtypes(tddf, features_columns, entity_id):
    """
    Retrieves the data types of columns in the provided DataFrame and assigns new feature IDs for columns that are not
    already registered in the feature catalog table of a Teradata database. This function is useful for preparing a
    DataFrame for feature ingestion by ensuring each feature has a unique ID and a recognized data type.

    Parameters:
    - tddf (tdml.DataFrame): The input DataFrame containing the features.
    - features_columns (list): A list of column names in the DataFrame to be considered as features.
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - schema (str): The schema name where the feature catalog table is located.
    - table_name (str, optional): The name of the feature catalog table. Defaults to 'FS_FEATURE_CATALOG'.

    Returns:
    dict: A dictionary where keys are column names from the input DataFrame and values are dictionaries containing
          the type and ID of the feature. The type is determined based on the column's data type in the DataFrame,
          and the ID is either retrieved from the feature catalog (for existing features) or newly assigned.

    Note:
    - The function checks each column in the DataFrame against the feature catalog table to determine if it already exists.
    - New feature IDs are sequentially assigned starting from the highest existing feature ID in the catalog.
    - Currently managed data types include integers (mapped to 'BIGINT') and floats (mapped to 'FLOAT').
      Other data types are mapped to 'VARCHAR'.
    - The function assumes that the feature catalog table exists and is accessible in the specified schema.

    Example Usage:
    >>> input_df = tdml.DataFrame(...)
    >>> feature_columns = ['age', 'income', 'gender']
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> feature_types = Gettdtypes(input_df, feature_columns, entity_id_dict)
    >>> print(feature_types)
    """
    # Get the data types of the columns in the DataFrame.
    #types = get_column_types_simple(tddf, tddf.columns) #dict(tddf.to_pandas(num_rows=10).dtypes)
    types = tdfs4ds.utils.info.get_feature_types_sql_format(tddf, tddf.columns)

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
            res[k] = {'type' : v.upper(), 'id' : feature_id}
            # Increment the feature ID for the next iteration.
            feature_id += 1

    # Return the result dictionary.
    return res

def tdstone2_Gettdtypes(existing_model, entity_id, display_logs=False):
    """
    Generates a dictionary mapping feature names to their data types and unique feature IDs for a given tdstone2 model.
    The function filters out features that already exist in the feature catalog and includes new features with 'BIGINT'
    or 'FLOAT' data types.

    Args:
        existing_model (object): The tdstone2 model object containing necessary schema and scoring information.
        entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
        display_logs (bool, optional): Flag to indicate whether to display logs. Defaults to False.

    Returns:
        dict: A dictionary with feature names as keys. Each key's value is a dictionary containing 'type' (either 'BIGINT' or 'FLOAT') and 'id' (unique feature ID).

    Raises:
        ValueError: If the data types encountered in the model are neither integer ('int') nor float ('float').

    Note:
        - This function is specifically designed for tdstone2 model objects.
        - It assumes that the feature catalog already exists and is accessible.
        - Unique IDs for new features are automatically generated, starting from the largest existing feature ID in the catalog.
        - Existing features in the catalog are not included in the output dictionary.

    Example Usage:
        model = <instance of tdstone2 model>
        entity_id_dict = {'customer_id': 'INTEGER'}
        feature_types = tdstone2_Gettdtypes(model, entity_id_dict)
        # feature_types might look like {'feature1': {'type': 'BIGINT', 'id': 101}, 'feature2': {'type': 'FLOAT', 'id': 102}}
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
                if tdfs4ds.DISPLAY_LOGS:
                    print(f'{k} has a type that is not yet managed')
                continue  # Skip this iteration for unmanaged types.
            feature_id += 1

    # Return the dictionary containing feature names, types, and IDs.
    return res

def delete_feature(feature_name, entity_id, data_domain=None):
    """
    Delete the values of a specific feature for given entities from the feature table 
    within a specified data domain.

    This function constructs and executes two SQL queries against a Teradata database
    to remove a feature specified by its name and entity identifiers. The first query 
    retrieves the table name where the feature resides, based on the feature name, 
    entity, and data domain. The second query deletes the feature values from the 
    identified table.

    Parameters:
    - feature_name (str): The name of the feature to be removed.
    - entity_id (str or list of str): Entity identifier(s). If a string is provided, 
      it will be converted to a single-element list. The list is always sorted 
      alphabetically before use.
    - data_domain (str, optional): The data domain where the feature is located. 
      If not specified, the function uses the default data domain defined in 
      `tdfs4ds.DATA_DOMAIN`.

    Behavior:
    - The function checks if the `DEBUG_MODE` flag in the `tdfs4ds` module is set to True. 
      If so, it prints the generated SQL queries and the resolved table name for debugging.
    - If the feature table cannot be resolved, the function returns without executing 
      a delete query.

    Returns:
    - None

    Note:
    - The function assumes the presence of a module `tdfs4ds` with predefined constants
      such as `DATA_DOMAIN`, `SCHEMA`, `FEATURE_CATALOG_NAME_VIEW`, and a flag `DEBUG_MODE`.
    - It also assumes a `tdml` module or object with an `execute_sql` method capable of
      executing SQL queries against a Teradata database and fetching the results.

    Raises:
    - Exceptions related to SQL execution or connection issues may be raised but are not 
      explicitly handled, except for printing the error message.
    """

    if isinstance(entity_id, str):
        entity_id = [entity_id]
    entity_id = sorted(entity_id)

    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN

    query0 = f"""
    SEL FEATURE_DATABASE||'.'||FEATURE_TABLE AS TABLE_NAME
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}
    WHERE FEATURE_NAME = '{feature_name}'
    AND DATA_DOMAIN = '{data_domain}'
    AND ENTITY_NAME = '{','.join([e.upper() for e in entity_id])}'"""
    if tdfs4ds.DEBUG_MODE:
        print(query0)

    table_name = tdml.execute_sql(query0).fetchall()
    if len(table_name) > 0:
        table_name = table_name[0][0]
    else:
        return
    if tdfs4ds.DEBUG_MODE:
        print('table name : ', table_name)

    query = f"""
    NONSEQUENCED VALIDTIME DELETE {table_name}
    WHERE FEATURE_ID = (
        SEL FEATURE_ID FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}
        WHERE FEATURE_NAME = '{feature_name}'
        AND DATA_DOMAIN = '{data_domain}'
    )"""
    if tdfs4ds.DEBUG_MODE:
        print(query)

    try:
        tdml.execute_sql(query)
    except Exception as e:
        print(str(e).split('\n')[0])

    return


def remove_feature(feature_name, entity_id, data_domain=None):
    """
    Attempts to remove a specific feature from the feature catalog and any associated data,
    within a given data domain in the tdfs4ds package.

    This function performs two main operations to remove a feature:
    1. Attempts to delete the feature's data using a helper function `delete_feature`, which handles
       the specific logic for removing feature data from its storage location. If this operation
       encounters any exceptions, the function catches these, logs the first word of the exception message,
       and exits.
    2. If the `delete_feature` operation succeeds, the function constructs and executes a SQL query to
       remove the feature's metadata entry from the feature catalog, cleaning up the catalog by removing
       the reference to the now-deleted feature.

    Parameters:
    - feature_name (str): The name of the feature to be removed.
    - entity_id (str or list of str): Entity identifier(s). If a string is provided, 
      it will be converted to a single-element list. The list is always sorted 
      alphabetically before use.
    - data_domain (str, optional): The data domain where the feature is located. If not provided,
      the function uses the default data domain from the `tdfs4ds.DATA_DOMAIN` setting.

    This function utilizes a DEBUG_MODE flag from the `tdfs4ds` module to control the logging of SQL
    queries for debugging purposes. If DEBUG_MODE is set to True, the deletion query is printed to the console.

    Returns:
    - None. The function's primary goal is to modify the database state by removing entries,
      and it does not return any value.

    Note:
    - The function is part of the tdfs4ds package and relies on external modules `tdfs4ds` for configuration
      constants and `tdml` for database interaction. It also assumes the existence of a `delete_feature`
      function responsible for the initial attempt to delete the feature's data.
    - Exception handling within this function is limited to logging the first word of any exception message
      encountered during the `delete_feature` call. Further error handling, especially for the SQL deletion
      operation, may be necessary depending on application requirements.

    Raises:
    - Exceptions from the `delete_feature` function are caught and logged, but not re-raised.
    - SQL execution or connection exceptions might occur but are not explicitly handled by this function.
    """

    if isinstance(entity_id, str):
        entity_id = [entity_id]
    entity_id = sorted(entity_id)

    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN

    try:
        delete_feature(feature_name, entity_id, data_domain)
    except Exception as e:
        print(str(e).split('\n')[0])
        return

    query = f"""
    NONSEQUENCED VALIDTIME DELETE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
    WHERE FEATURE_NAME = '{feature_name}'
        AND DATA_DOMAIN = '{data_domain}'
        AND ENTITY_NAME = '{','.join([e.upper() for e in entity_id])}'
    """
    if tdfs4ds.DEBUG_MODE:
        print(query)

    tdml.execute_sql(query)
    return
